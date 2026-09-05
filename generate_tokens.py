#!/usr/bin/env python3
"""Standalone, gate-controlled generator for Dakk's Ultimate Tokens.

Dependencies: the official ``openai`` Python SDK and Pillow. The queue is read
only from ``upload/ASSETS-universal.csv``; this script never opens or writes the
Excel workbook.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import inspect
from io import BytesIO
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
import time
from typing import Any, Mapping, Sequence

from PIL import Image, UnidentifiedImageError


MODEL = "gpt-image-2"
MAX_RETRY_DELAY_SECONDS = 90.0
MODERATION_FALLBACK_NOTE = (
    "moderation=low unsupported by edits endpoint; retried without moderation"
)
REFERENCE_SHA256 = "2b0c44d077d651709fcacc8845c25417815d2df882af4aeeb2fda092cf3554b9"
REFERENCE_DECLARATION = f"generic-sheet-01.png#{REFERENCE_SHA256}"
HANDSHAKE = "Black Dragon · black-dragon.webp · 1200 · bfe60d6a8251"
GATE_1_FIXED = ("JOB-0001", "JOB-0007", "JOB-0012", "JOB-0431")
RESULT_FIELDS = (
    "job_id",
    "build_filename",
    "art_dir",
    "status",
    "model",
    "created_at",
    "sent_prompt_sha256",
    "master_path",
    "master_sha256",
    "export_path",
    "export_sha256",
    "export_px",
    "note",
    "error",
)
REQUIRED_HEADERS = frozenset(
    {
        "job_id",
        "asset_id",
        "display_name",
        "batch_id",
        "status",
        "lock_state",
        "layout_profile",
        "art_dir",
        "build_filename",
        "filename_stem",
        "master_px",
        "export_px",
        "reference_file",
        "resolved_prompt",
        "prompt_sha256",
    }
)
REFUSAL_CODES = frozenset(
    {
        "content_policy_violation",
        "moderation_blocked",
        "policy_violation",
        "safety_violation",
    }
)
FATAL_CODES = frozenset(
    {
        "billing_hard_limit_reached",
        "insufficient_quota",
        "invalid_api_key",
        "invalid_request_error",
        "invalid_value",
        "model_not_found",
        "permission_denied",
    }
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JOB_ID_RE = re.compile(r"^JOB-(\d+)$")
HEX_64_RE = re.compile(r"^[0-9a-f]{64}$")
WINDOWS_RESERVED_NAMES = frozenset(
    {
        "con",
        "prn",
        "aux",
        "nul",
        *(f"com{number}" for number in range(1, 10)),
        *(f"lpt{number}" for number in range(1, 10)),
    }
)


class GeneratorError(RuntimeError):
    """A deterministic local or source validation failure."""


class SourceChangedError(GeneratorError):
    """The queue or reference changed after the gate was prepared."""


@dataclass(frozen=True)
class PreparedRow:
    source: dict[str, str]
    job_id: str
    display_name: str
    prompt: str
    prompt_sha256: str
    art_dir: str
    build_filename: str
    export_px: int
    master_px: int
    master_path: Path
    export_path: Path
    master_rel: str
    export_rel: str
    note: str


@dataclass(frozen=True)
class ImageResponse:
    png_bytes: bytes
    request_id: str
    attempts: int
    revised_prompt: str
    moderation_note: str


@dataclass(frozen=True)
class ImageObservation:
    job_id: str
    has_alpha_channel: bool
    transparent_background: bool
    alpha_extrema: tuple[int, int]
    transparent_fraction: float
    corner_alphas: tuple[int, int, int, int]
    checkerboard_baked: bool


class APIRequestFailure(RuntimeError):
    def __init__(
        self,
        error_text: str,
        *,
        refused: bool,
        fatal: bool,
        attempts: int,
        moderation_note: str,
    ) -> None:
        super().__init__(error_text)
        self.error_text = error_text
        self.refused = refused
        self.fatal = fatal
        self.attempts = attempts
        self.moderation_note = moderation_note


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def local_date() -> str:
    return datetime.now().astimezone().date().isoformat()


def read_queue(path: Path) -> tuple[list[dict[str, str]], str]:
    if not path.is_file():
        raise GeneratorError(f"queue does not exist: {path}")
    source_hash = sha256_file(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise GeneratorError("queue has no CSV header")
        headers = [str(header) for header in reader.fieldnames]
        if len(headers) != len(set(headers)):
            raise GeneratorError("queue contains duplicate header names")
        missing = sorted(REQUIRED_HEADERS - set(headers))
        if missing:
            raise GeneratorError("queue is missing required headers: " + ", ".join(missing))

        rows: list[dict[str, str]] = []
        for record_number, raw in enumerate(reader, start=2):
            if None in raw:
                raise GeneratorError(f"queue record {record_number} has more fields than headers")
            row = {header: (raw.get(header) if raw.get(header) is not None else "") for header in headers}
            rows.append(row)
    if not rows:
        raise GeneratorError("queue has no data rows")
    return rows, source_hash


def is_superseded_row(row: Mapping[str, str]) -> bool:
    if "PILOT" in row.get("batch_id", "").upper():
        return True
    for field in ("status", "source_scope"):
        if row.get(field, "").strip().casefold() in {"pilot", "sample", "example"}:
            return True
    for field in ("job_id", "asset_id", "catalog_id"):
        value = row.get(field, "").strip().upper()
        if value.startswith(("PILOT-", "SAMPLE-", "EXAMPLE-")):
            return True
    return False


def job_number(row: Mapping[str, str]) -> int:
    job_id = row.get("job_id", "").strip()
    match = JOB_ID_RE.fullmatch(job_id)
    if match is None:
        raise GeneratorError(f"invalid job_id in queue: {job_id!r}")
    return int(match.group(1))


def production_index(rows: Sequence[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        if is_superseded_row(row):
            continue
        job_id = row.get("job_id", "").strip()
        if JOB_ID_RE.fullmatch(job_id) is None:
            raise GeneratorError(f"invalid production job_id: {job_id!r}")
        if job_id in result:
            raise GeneratorError(f"duplicate production job_id: {job_id}")
        result[job_id] = row
    return result


def first_profile_rows(
    rows: Sequence[dict[str, str]], profile: str, count: int
) -> list[dict[str, str]]:
    matches = sorted(
        (
            row
            for row in rows
            if not is_superseded_row(row)
            and row.get("layout_profile", "").strip().casefold() == profile.casefold()
        ),
        key=job_number,
    )
    if len(matches) < count:
        raise GeneratorError(f"queue has fewer than {count} production rows for {profile!r}")
    return matches[:count]


def select_gate(rows: Sequence[dict[str, str]], gate: int) -> list[dict[str, str]]:
    index = production_index(rows)

    def require(job_id: str) -> dict[str, str]:
        try:
            return index[job_id]
        except KeyError as exc:
            raise GeneratorError(f"requested row is not in ASSETS queue: {job_id}") from exc

    if gate == 0:
        return [require("JOB-0001")]
    if gate == 1:
        selected = [require(job_id) for job_id in GATE_1_FIXED]
        selected.extend(first_profile_rows(rows, "armor-icon", 1))
        selected.extend(first_profile_rows(rows, "item-icon", 1))
        selected.extend(first_profile_rows(rows, "emblem", 2))
        ids = [row["job_id"].strip() for row in selected]
        if len(ids) != 8 or len(set(ids)) != 8:
            raise GeneratorError(f"Gate 1 did not resolve to eight unique rows: {ids}")
        return selected

    bounds = {2: (1, 23), 3: (24, 102), 4: (103, 1408)}
    if gate not in bounds:
        raise GeneratorError(f"unsupported gate: {gate}")
    start, end = bounds[gate]
    selected = [require(f"JOB-{number:04d}") for number in range(start, end + 1)]
    ordinary = [row for row in selected if parse_positive_int(row, "master_px") != 1536]
    large = [row for row in selected if parse_positive_int(row, "master_px") == 1536]
    return ordinary + large


def parse_positive_int(row: Mapping[str, str], field: str) -> int:
    raw = row.get(field, "").strip()
    if not raw.isdigit() or int(raw) <= 0:
        raise GeneratorError(f"{row.get('job_id', '?')} has invalid {field}: {raw!r}")
    return int(raw)


def safe_path_component(value: str, *, field: str, job_id: str) -> str:
    if (
        not value
        or value in {".", ".."}
        or value[-1] in {" ", "."}
        or any(character in '<>:"/\\|?*' or ord(character) < 32 for character in value)
        or value.split(".", 1)[0].casefold() in WINDOWS_RESERVED_NAMES
    ):
        raise GeneratorError(f"{job_id} has unsafe {field}: {value!r}")
    return value


def safe_directory(value: str, *, field: str, job_id: str) -> PurePosixPath:
    if not value or value != value.strip() or value.startswith("/") or value.endswith("/"):
        raise GeneratorError(f"{job_id} has unsafe {field}: {value!r}")
    parts = value.split("/")
    if any(not part for part in parts):
        raise GeneratorError(f"{job_id} has unsafe {field}: {value!r}")
    for part in parts:
        safe_path_component(part, field=field, job_id=job_id)
    return PurePosixPath(*parts)


def safe_filename(value: str, *, field: str, job_id: str) -> str:
    if value != value.strip():
        raise GeneratorError(f"{job_id} has unsafe {field}: {value!r}")
    return safe_path_component(value, field=field, job_id=job_id)


def ensure_under_root(root: Path, candidate: Path) -> Path:
    root_resolved = root.resolve()
    candidate_resolved = candidate.resolve(strict=False)
    try:
        candidate_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise GeneratorError(f"output path escapes repository root: {candidate}") from exc
    return candidate_resolved


def prepare_rows(root: Path, selected: Sequence[dict[str, str]]) -> list[PreparedRow]:
    prepared: list[PreparedRow] = []
    seen_paths: dict[str, str] = {}
    for row in selected:
        job_id = row["job_id"].strip()
        if row.get("status", "") != "prompt_ready":
            raise GeneratorError(f"{job_id} is not prompt_ready")
        if row.get("lock_state", "") != "unlocked":
            raise GeneratorError(f"{job_id} is not unlocked")
        if row.get("reference_file", "") != REFERENCE_DECLARATION:
            raise GeneratorError(f"{job_id} does not declare the verified reference sheet")

        prompt = row.get("resolved_prompt", "")
        stored_hash = row.get("prompt_sha256", "").strip()
        actual_hash = sha256_bytes(prompt.encode("utf-8"))
        if HEX_64_RE.fullmatch(stored_hash) is None or actual_hash != stored_hash:
            raise GeneratorError(
                f"{job_id} prompt hash mismatch: stored={stored_hash!r}, actual={actual_hash}"
            )

        art_dir_text = row.get("art_dir", "")
        art_dir = safe_directory(art_dir_text, field="art_dir", job_id=job_id)
        stem = safe_filename(row.get("filename_stem", ""), field="filename_stem", job_id=job_id)
        build_filename = safe_filename(
            row.get("build_filename", ""), field="build_filename", job_id=job_id
        )
        if not build_filename.casefold().endswith(".webp"):
            raise GeneratorError(f"{job_id} build_filename is not WebP: {build_filename!r}")

        master_path = ensure_under_root(root, root / "masters" / Path(*art_dir.parts) / f"{stem}.png")
        export_path = ensure_under_root(root, root / "art" / Path(*art_dir.parts) / build_filename)
        for path in (master_path, export_path):
            key = os.path.normcase(str(path))
            previous = seen_paths.get(key)
            if previous is not None:
                raise GeneratorError(f"output collision: {previous} and {job_id} both map to {path}")
            seen_paths[key] = job_id

        export_px = parse_positive_int(row, "export_px")
        master_px = parse_positive_int(row, "master_px")
        prepared.append(
            PreparedRow(
                source=row,
                job_id=job_id,
                display_name=row.get("display_name", "").strip(),
                prompt=prompt,
                prompt_sha256=actual_hash,
                art_dir=art_dir.as_posix(),
                build_filename=build_filename,
                export_px=export_px,
                master_px=master_px,
                master_path=master_path,
                export_path=export_path,
                master_rel=master_path.relative_to(root.resolve()).as_posix(),
                export_rel=export_path.relative_to(root.resolve()).as_posix(),
                note="master below spec: 1024" if master_px == 1536 else "",
            )
        )
    return prepared


def verify_handshake(row: Mapping[str, str]) -> str:
    prompt_hash = row.get("prompt_sha256", "").strip()
    actual_prompt_hash = sha256_bytes(row.get("resolved_prompt", "").encode("utf-8"))
    if actual_prompt_hash != prompt_hash:
        raise GeneratorError("JOB-0001 prompt re-hash failed")
    output = " · ".join(
        (
            row.get("display_name", "").strip(),
            row.get("build_filename", "").strip(),
            row.get("export_px", "").strip(),
            prompt_hash[:12],
        )
    )
    if output != HANDSHAKE:
        raise GeneratorError(f"Gate 0 handshake mismatch: {output}")
    return output


def verify_sources(queue_path: Path, queue_hash: str, reference_path: Path) -> None:
    current_queue_hash = sha256_file(queue_path)
    if current_queue_hash != queue_hash:
        raise SourceChangedError("ASSETS-universal.csv changed during this gate")
    current_reference_hash = sha256_file(reference_path)
    if current_reference_hash != REFERENCE_SHA256:
        raise SourceChangedError(
            f"reference SHA-256 changed or mismatched: {current_reference_hash}"
        )


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return str(value)


def api_error_details(exc: Exception) -> dict[str, Any]:
    body = getattr(exc, "body", None)
    error = body.get("error", body) if isinstance(body, Mapping) else {}
    code = str(error.get("code") or getattr(exc, "code", "") or "")
    error_type = str(error.get("type") or getattr(exc, "type", "") or "")
    param = str(error.get("param") or getattr(exc, "param", "") or "")
    message = str(error.get("message") or str(exc))
    status = getattr(exc, "status_code", None)
    request_id = str(getattr(exc, "request_id", "") or "")
    return {
        "message": message,
        "code": code,
        "type": error_type,
        "param": param,
        "status_code": status if isinstance(status, int) else None,
        "request_id": request_id,
        "body": json_safe(body),
    }


def is_transient_api_error(exc: Exception) -> bool:
    details = api_error_details(exc)
    status = details["status_code"]
    code = str(details["code"]).casefold()
    return (status == 429 and code != "insufficient_quota") or (
        isinstance(status, int) and status >= 500
    )


def is_unknown_moderation_parameter(exc: Exception) -> bool:
    details = api_error_details(exc)
    if details["status_code"] != 400:
        return False
    param = str(details["param"]).casefold()
    message = str(details["message"]).casefold()
    code = str(details["code"]).casefold()
    error_type = str(details["type"]).casefold()
    if param == "moderation" and (
        code in {"unknown_parameter", "unrecognized_parameter"}
        or error_type in {"unknown_parameter", "unrecognized_parameter"}
    ):
        return True
    unknown_markers = (
        "unknown parameter",
        "unrecognized parameter",
        "unrecognised parameter",
        "unrecognized request argument",
        "unsupported parameter",
        "unexpected parameter",
    )
    return "moderation" in message and any(marker in message for marker in unknown_markers)


def retry_after_seconds(exc: Exception) -> float | None:
    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", None) or getattr(exc, "headers", None)
    if headers is None or not hasattr(headers, "get"):
        return None
    raw = headers.get("retry-after")
    if raw is None:
        raw = headers.get("Retry-After")
    if raw is None:
        return None
    text = str(raw).strip()
    try:
        return max(0.0, float(text))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(text)
        except (TypeError, ValueError, OverflowError):
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return max(0.0, (parsed - datetime.now(timezone.utc)).total_seconds())


def retry_delay_seconds(exc: Exception, transient_retry_number: int) -> float:
    exponent = min(7, max(0, transient_retry_number - 1))
    backoff = float(2**exponent)
    status = api_error_details(exc)["status_code"]
    retry_after = retry_after_seconds(exc) if status == 429 else None
    requested = max(backoff, retry_after or 0.0)
    return min(MAX_RETRY_DELAY_SECONDS, requested)


def sleep_in_chunks(delay: float) -> None:
    remaining = max(0.0, delay)
    while remaining > 0:
        chunk = min(30.0, remaining)
        time.sleep(chunk)
        remaining -= chunk


def is_refusal(exc: Exception) -> bool:
    details = api_error_details(exc)
    code = str(details["code"]).casefold()
    error_type = str(details["type"]).casefold()
    message = str(details["message"]).casefold()
    if code in REFUSAL_CODES:
        return True
    if error_type in {"content_policy_violation", "moderation_blocked"}:
        return True
    policy_markers = (
        "content policy",
        "moderation blocked",
        "policy violation",
        "safety policy",
        "safety system",
    )
    if any(marker in message for marker in policy_markers):
        return True
    artist_named = any(name in message for name in ("brom", "parkinson", "easley"))
    refusal_worded = any(
        marker in message for marker in ("cannot", "can't", "not allowed", "refus", "unsupported")
    )
    return artist_named and refusal_worded


def is_fatal_api_error(exc: Exception, *, refused: bool) -> bool:
    if refused:
        return False
    details = api_error_details(exc)
    status = details["status_code"]
    code = str(details["code"]).casefold()
    message = str(details["message"]).casefold()
    # An exhausted balance is fatal whatever shape it arrives in: the API has returned it
    # as 429 insufficient_quota, as 402, and as a bare "no credits remaining" message.
    # Treating it per-row once spent eight requests learning the same fact.
    if "no credits" in message or "add credits" in message or code in {"insufficient_quota", "billing_not_active"}:
        return True
    if status == 429:
        return code == "insufficient_quota"
    if status in {400, 402}:
        return True
    if status in {401, 403, 404}:
        return True
    return code in FATAL_CODES


class OpenAIImageEditor:
    def __init__(self, api_key: str, *, max_attempts: int = 4) -> None:
        if max_attempts < 1:
            raise GeneratorError("max_attempts must be at least one")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise GeneratorError(
                "official openai SDK is missing; install requirements.txt"
            ) from exc
        self.client = OpenAI(api_key=api_key, max_retries=0, timeout=300.0)
        self.max_attempts = max_attempts
        try:
            parameters = inspect.signature(self.client.images.edit).parameters
        except (TypeError, ValueError) as exc:
            raise GeneratorError(f"cannot inspect official Images.edit SDK method: {exc}") from exc
        required = {"model", "image", "prompt", "n", "size", "quality", "background", "output_format"}
        missing = sorted(required - set(parameters))
        if missing:
            raise GeneratorError("official Images.edit method lacks: " + ", ".join(missing))
        if "moderation" in parameters:
            self.moderation_kwargs: dict[str, Any] = {"moderation": "low"}
        elif "extra_body" in parameters:
            self.moderation_kwargs = {"extra_body": {"moderation": "low"}}
        else:
            raise GeneratorError("official Images.edit method cannot send moderation=low")
        self.moderation_unsupported = False

    @property
    def moderation_note(self) -> str:
        return MODERATION_FALLBACK_NOTE if self.moderation_unsupported else ""

    def edit_one(self, *, reference_path: Path, prompt: str) -> ImageResponse:
        actual_attempts = 0
        transient_retries = 0
        use_moderation = not self.moderation_unsupported
        while True:
            actual_attempts += 1
            try:
                with reference_path.open("rb") as reference:
                    request: dict[str, Any] = {
                        "model": MODEL,
                        "image": reference,
                        "prompt": prompt,
                        "n": 1,
                        "size": "1024x1024",
                        "quality": "high",
                        "background": "transparent",
                        "output_format": "png",
                    }
                    if use_moderation:
                        request.update(self.moderation_kwargs)
                    raw = self.client.images.with_raw_response.edit(**request)
                response = raw.parse()
                data = getattr(response, "data", None) or []
                encoded = getattr(data[0], "b64_json", None) if data else None
                if not encoded:
                    raise GeneratorError("Image API returned no base64 PNG")
                try:
                    png_bytes = base64.b64decode(encoded, validate=True)
                except (ValueError, TypeError) as exc:
                    raise GeneratorError(f"Image API returned invalid base64: {exc}") from exc
                request_id = str(raw.headers.get("x-request-id", "") or "")
                revised = str(getattr(data[0], "revised_prompt", "") or "")
                return ImageResponse(
                    png_bytes,
                    request_id,
                    actual_attempts,
                    revised,
                    self.moderation_note,
                )
            except GeneratorError:
                raise
            except Exception as exc:
                if use_moderation and is_unknown_moderation_parameter(exc):
                    use_moderation = False
                    self.moderation_unsupported = True
                    print(
                        "NOTICE: edits endpoint rejected moderation=low as an unknown "
                        "parameter; retrying once without moderation",
                        file=sys.stderr,
                        flush=True,
                    )
                    continue
                if (
                    is_transient_api_error(exc)
                    and transient_retries < self.max_attempts - 1
                ):
                    transient_retries += 1
                    delay = retry_delay_seconds(exc, transient_retries)
                    status = api_error_details(exc)["status_code"]
                    print(
                        f"Transient API failure HTTP {status or 'unknown'}; retry wire call "
                        f"{actual_attempts + 1} in {delay:.0f}s",
                        file=sys.stderr,
                        flush=True,
                    )
                    sleep_in_chunks(delay)
                    continue
                refused = is_refusal(exc)
                raise APIRequestFailure(
                    str(api_error_details(exc)["message"]),
                    refused=refused,
                    fatal=is_fatal_api_error(exc, refused=refused),
                    attempts=actual_attempts,
                    moderation_note=self.moderation_note,
                ) from exc


def background_metrics(image: Image.Image) -> dict[str, float | bool]:
    with image.convert("RGBA") as rgba:
        width, height = rgba.size
        pixels = rgba.load()
        step_x = max(1, math.ceil(width / 128))
        step_y = max(1, math.ceil(height / 128))
        sampled = [
            (x, y, pixels[x, y])
            for y in range(0, height, step_y)
            for x in range(0, width, step_x)
        ]
        sample_count = max(1, len(sampled))
        opaque_count = sum(pixel[3] >= 250 for _, _, pixel in sampled)
        light_neutral: Counter[tuple[int, int, int]] = Counter()
        quadrants: dict[tuple[int, int, int], set[int]] = {}
        for x, y, pixel in sampled:
            red, green, blue, alpha = pixel
            if alpha < 250 or max(red, green, blue) - min(red, green, blue) > 18:
                continue
            if (red + green + blue) / 3 < 160:
                continue
            bucket = (red // 16, green // 16, blue // 16)
            light_neutral[bucket] += 1
            quadrant = (1 if x >= width / 2 else 0) + (2 if y >= height / 2 else 0)
            quadrants.setdefault(bucket, set()).add(quadrant)

        checkerboard = False
        top = light_neutral.most_common(2)
        if len(top) == 2:
            (first, first_count), (second, second_count) = top
            coverage = (first_count + second_count) / sample_count
            first_luma = sum(first) / 3
            second_luma = sum(second) / 3
            checkerboard = (
                opaque_count / sample_count >= 0.75
                and coverage >= 0.60
                and first_count / sample_count >= 0.12
                and second_count / sample_count >= 0.12
                and abs(first_luma - second_luma) >= 1.0
                and len(quadrants.get(first, ())) >= 3
                and len(quadrants.get(second, ())) >= 3
            )
        return {
            "checkerboard_baked": checkerboard,
            "opaque_sample_fraction": opaque_count / sample_count,
        }


def inspect_png_bytes(job_id: str, png_bytes: bytes) -> ImageObservation:
    if not png_bytes.startswith(PNG_SIGNATURE):
        raise GeneratorError(f"{job_id} response is not a PNG")
    try:
        with Image.open(BytesIO(png_bytes)) as opened:
            opened.load()
            if opened.format != "PNG":
                raise GeneratorError(f"{job_id} response format is {opened.format!r}, not PNG")
            if getattr(opened, "n_frames", 1) != 1:
                raise GeneratorError(f"{job_id} response is an animated or multi-frame PNG")
            if opened.size != (1024, 1024):
                raise GeneratorError(f"{job_id} response size is {opened.size}, not 1024x1024")
            has_alpha = "A" in opened.getbands()
            with opened.convert("RGBA") as rgba:
                with rgba.getchannel("A") as alpha:
                    extrema = alpha.getextrema()
                    histogram = alpha.histogram()
                    transparent_count = sum(histogram[:6])
                    transparent_fraction = transparent_count / (1024 * 1024)
                    corner_alphas = (
                        alpha.getpixel((0, 0)),
                        alpha.getpixel((1023, 0)),
                        alpha.getpixel((0, 1023)),
                        alpha.getpixel((1023, 1023)),
                    )
                checkerboard = bool(background_metrics(rgba)["checkerboard_baked"])
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        raise GeneratorError(f"{job_id} response cannot be decoded as PNG") from exc
    return ImageObservation(
        job_id=job_id,
        has_alpha_channel=has_alpha,
        transparent_background=(
            has_alpha
            and transparent_fraction >= 0.01
            and all(value <= 5 for value in corner_alphas)
        ),
        alpha_extrema=extrema,
        transparent_fraction=transparent_fraction,
        corner_alphas=corner_alphas,
        checkerboard_baked=checkerboard,
    )


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w+b", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as temporary:
            temporary_name = temporary.name
            temporary.write(data)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, path)
        temporary_name = None
    finally:
        if temporary_name is not None:
            try:
                Path(temporary_name).unlink()
            except FileNotFoundError:
                pass


def export_webp_premultiplied(master_path: Path, export_path: Path, export_px: int) -> None:
    resized: Image.Image | None = None
    with Image.open(master_path) as opened:
        opened.load()
        with opened.convert("RGBA") as rgba:
            with rgba.getchannel("A") as source_alpha:
                source_alpha_min = source_alpha.getextrema()[0]
            with rgba.convert("RGBa") as premultiplied:
                with premultiplied.resize(
                    (export_px, export_px), resample=Image.Resampling.LANCZOS
                ) as resized_pm:
                    resized = resized_pm.convert("RGBA")

    export_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w+b",
            dir=export_path.parent,
            prefix=f".{export_path.name}.",
            suffix=".tmp.webp",
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            resized.save(
                temporary,
                format="WEBP",
                lossless=False,
                quality=90,
                method=6,
                exact=True,
            )
            temporary.flush()
            os.fsync(temporary.fileno())
        with Image.open(temporary_name) as verification:
            verification.load()
            if verification.format != "WEBP" or verification.size != (export_px, export_px):
                raise GeneratorError(f"invalid WebP derivative: {export_path}")
            if source_alpha_min < 255 and "A" not in verification.getbands():
                raise GeneratorError(f"WebP derivative lost its alpha channel: {export_path}")
            with verification.convert("RGBA") as verification_rgba:
                with verification_rgba.getchannel("A") as export_alpha:
                    export_alpha_min = export_alpha.getextrema()[0]
            if source_alpha_min < 255 and export_alpha_min >= 255:
                raise GeneratorError(f"WebP derivative lost transparency: {export_path}")
        if export_path.exists():
            raise GeneratorError(f"refusing to overwrite build file created during request: {export_path}")
        os.replace(temporary_name, export_path)
        temporary_name = None
    finally:
        if resized is not None:
            resized.close()
        if temporary_name is not None:
            try:
                Path(temporary_name).unlink()
            except FileNotFoundError:
                pass


def merge_notes(*values: str) -> str:
    return "; ".join(value for value in values if value)


def result_note(
    row: PreparedRow,
    observation: ImageObservation | None,
    *,
    extra_note: str = "",
) -> str:
    if observation is None:
        transparent = "unknown"
        checkerboard = "unknown"
    else:
        transparent = "yes" if observation.transparent_background else "no"
        checkerboard = "yes" if observation.checkerboard_baked else "no"
    return merge_notes(
        row.note,
        extra_note,
        f"transparent_background={transparent}",
        f"checkerboard_baked={checkerboard}",
    )


def transparency_failure_reason(observation: ImageObservation) -> str:
    reasons: list[str] = []
    if not observation.has_alpha_channel:
        reasons.append("PNG has no alpha channel")
    if observation.transparent_fraction < 0.01:
        reasons.append(
            f"fully transparent fraction {observation.transparent_fraction:.6f} is below 0.010000"
        )
    if any(value > 5 for value in observation.corner_alphas):
        reasons.append(f"corner alpha values are {observation.corner_alphas}")
    detail = ", ".join(reasons) or "alpha-channel background checks did not pass"
    return f"transparent background validation failed: {detail}; master kept; export not written"


def model_result_json(result: Any) -> str:
    if hasattr(result, "model_dump"):
        value = result.model_dump(mode="json")
    elif isinstance(result, Mapping):
        value = dict(result)
    else:
        value = {"id": getattr(result, "id", ""), "result": str(result)}
    return json.dumps(json_safe(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def result_record(
    row: PreparedRow,
    *,
    status: str,
    model_id: str = MODEL,
    master_sha256: str = "",
    export_sha256: str = "",
    observation: ImageObservation | None = None,
    extra_note: str = "",
    error: str = "",
) -> dict[str, Any]:
    if status not in {"generated", "refused", "error"}:
        raise GeneratorError(f"invalid result status: {status}")
    record: dict[str, Any] = {
        "job_id": row.job_id,
        "build_filename": row.build_filename,
        "art_dir": row.art_dir,
        "status": status,
        "model": model_id,
        "created_at": now_utc(),
        "sent_prompt_sha256": row.prompt_sha256,
        "master_path": row.master_rel,
        "master_sha256": master_sha256,
        "export_path": row.export_rel,
        "export_sha256": export_sha256,
        "export_px": row.export_px,
        "note": result_note(row, observation, extra_note=extra_note),
        "error": error,
    }
    if tuple(record) != RESULT_FIELDS:
        raise AssertionError("result schema changed")
    return record


def append_result(path: Path, record: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(
        dict(record), ensure_ascii=False, allow_nan=False, separators=(",", ":")
    ) + "\n"
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())


def print_gate_plan(gate: int, rows: Sequence[PreparedRow]) -> None:
    print(f"MODEL {MODEL}")
    print(f"Gate {gate}: {len(rows)} row(s)")
    for row in rows:
        disposition = "SKIP existing build" if row.export_path.exists() else "READY"
        print(
            f"{row.job_id} · {row.display_name} · {row.source['layout_profile']} · "
            f"{row.build_filename} · {row.export_px} · {row.prompt_sha256[:12]} · {disposition}"
        )


def execute_gate(
    *,
    root: Path,
    gate: int,
    rows: Sequence[PreparedRow],
    queue_path: Path,
    queue_hash: str,
    reference_path: Path,
    max_attempts: int,
) -> int:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise GeneratorError(
            "OPENAI_API_KEY is not set in this process environment; no image calls were made"
        )
    editor = OpenAIImageEditor(api_key, max_attempts=max_attempts)
    for model_attempt in range(1, max_attempts + 1):
        try:
            model_result = editor.client.models.retrieve(MODEL)
            break
        except Exception as exc:
            if is_transient_api_error(exc) and model_attempt < max_attempts:
                delay = retry_delay_seconds(exc, model_attempt)
                print(
                    f"Transient model preflight failure; retry {model_attempt + 1}/"
                    f"{max_attempts} in {delay:.0f}s",
                    file=sys.stderr,
                    flush=True,
                )
                sleep_in_chunks(delay)
                continue
            message = str(api_error_details(exc)["message"])
            raise GeneratorError(f"model preflight failed for {MODEL}: {message}") from exc
    else:
        raise AssertionError("unreachable model retry boundary")
    print(f"MODEL_RETRIEVE {model_result_json(model_result)}", flush=True)
    resolved_model_id = getattr(model_result, "id", None)
    if not isinstance(resolved_model_id, str) or not resolved_model_id:
        raise GeneratorError("model preflight returned no model id; no image calls were made")
    if resolved_model_id != MODEL and not resolved_model_id.startswith(f"{MODEL}-"):
        raise GeneratorError(
            f"model preflight returned unexpected id {resolved_model_id!r}; no image calls were made"
        )
    results_path = root / f"results-{local_date()}.jsonl"
    observations: list[ImageObservation] = []
    refusal_seen = False
    attempted = 0
    generated = 0
    skipped = 0
    errors = 0

    for row in rows:
        if row.export_path.exists():
            skipped += 1
            print(f"SKIP {row.job_id}: {row.export_rel} already exists", flush=True)
            continue
        verify_sources(queue_path, queue_hash, reference_path)
        if sha256_bytes(row.prompt.encode("utf-8")) != row.prompt_sha256:
            raise SourceChangedError(f"{row.job_id} in-memory prompt changed before request")
        attempted += 1
        print(f"EDIT {row.job_id}: {row.display_name}", flush=True)
        observation: ImageObservation | None = None
        master_hash = ""
        export_hash = ""
        request_note = editor.moderation_note
        try:
            response = editor.edit_one(reference_path=reference_path, prompt=row.prompt)
            request_note = response.moderation_note
            verify_sources(queue_path, queue_hash, reference_path)
            observation = inspect_png_bytes(row.job_id, response.png_bytes)
            response_hash = sha256_bytes(response.png_bytes)
            atomic_write_bytes(row.master_path, response.png_bytes)
            master_hash = sha256_file(row.master_path)
            if master_hash != response_hash:
                raise GeneratorError(f"{row.job_id} master differs from the API response bytes")
            observations.append(observation)
            if not observation.transparent_background:
                reason = transparency_failure_reason(observation)
                append_result(
                    results_path,
                    result_record(
                        row,
                        status="error",
                        model_id=resolved_model_id,
                        master_sha256=master_hash,
                        observation=observation,
                        extra_note=merge_notes(request_note, reason),
                        error=reason,
                    ),
                )
                errors += 1
                print(f"ERROR {row.job_id}: {reason}", file=sys.stderr, flush=True)
                continue
            export_webp_premultiplied(row.master_path, row.export_path, row.export_px)
            export_hash = sha256_file(row.export_path)
            append_result(
                results_path,
                result_record(
                    row,
                    status="generated",
                    model_id=resolved_model_id,
                    master_sha256=master_hash,
                    export_sha256=export_hash,
                    observation=observation,
                    extra_note=request_note,
                ),
            )
            generated += 1
            print(
                f"OK {row.job_id}: alpha={'yes' if observation.transparent_background else 'no'} "
                f"checkerboard={'yes' if observation.checkerboard_baked else 'no'} "
                f"request_id={response.request_id or '-'} attempts={response.attempts}",
                flush=True,
            )
            if response.revised_prompt:
                print(
                    f"NOTICE {row.job_id}: API returned revised_prompt metadata; sent hash remains "
                    f"{row.prompt_sha256}",
                    flush=True,
                )
        except APIRequestFailure as exc:
            status = "refused" if exc.refused else "error"
            append_result(
                results_path,
                result_record(
                    row,
                    status=status,
                    model_id=resolved_model_id,
                    extra_note=exc.moderation_note,
                    error=exc.error_text,
                ),
            )
            refusal_seen = refusal_seen or exc.refused
            errors += 1
            print(f"{status.upper()} {row.job_id}: {exc.error_text}", file=sys.stderr, flush=True)
            if exc.fatal:
                print("Fatal API configuration/account error; stopping this gate.", file=sys.stderr)
                break
        except Exception as exc:
            request_note = editor.moderation_note or request_note
            master_hash = sha256_file(row.master_path) if row.master_path.is_file() else master_hash
            export_hash = sha256_file(row.export_path) if row.export_path.is_file() else export_hash
            append_result(
                results_path,
                result_record(
                    row,
                    status="error",
                    model_id=resolved_model_id,
                    master_sha256=master_hash,
                    export_sha256=export_hash,
                    observation=observation,
                    extra_note=request_note,
                    error=str(exc),
                ),
            )
            errors += 1
            print(f"ERROR {row.job_id}: {exc}", file=sys.stderr, flush=True)
            if isinstance(exc, SourceChangedError):
                break

    print(f"RESULTS {results_path}")
    print(
        f"SUMMARY gate={gate} attempted={attempted} generated={generated} "
        f"refusal={'yes' if refusal_seen else 'no'} errors={errors} skipped={skipped}"
    )
    if observations:
        print(
            "TRANSPARENT_BACKGROUND "
            + ("yes" if all(item.transparent_background for item in observations) else "no")
        )
        print(
            "BAKED_CHECKERBOARD "
            + ("yes" if any(item.checkerboard_baked for item in observations) else "no")
        )
    print(f"STOP Gate {gate} complete; no later gate was selected.")
    return 0 if errors == 0 else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", type=int, choices=range(0, 5), required=True)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="make live API calls; without this flag the script only validates and lists the gate",
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--max-attempts", type=int, default=4)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = args.root.resolve()
        queue_path = (args.queue or root / "upload" / "ASSETS-universal.csv").resolve()
        reference_path = (args.reference or root / "upload" / "generic-sheet-01.png").resolve()
        if not reference_path.is_file():
            raise GeneratorError(f"reference does not exist: {reference_path}")
        reference_hash = sha256_file(reference_path)
        if reference_hash != REFERENCE_SHA256:
            raise GeneratorError(f"reference SHA-256 mismatch: {reference_hash}")

        rows, queue_hash = read_queue(queue_path)
        gate_zero = select_gate(rows, 0)[0]
        print(verify_handshake(gate_zero))
        all_prepared = prepare_rows(
            root,
            sorted(production_index(rows).values(), key=job_number),
        )
        prepared_by_id = {row.job_id: row for row in all_prepared}
        selected = select_gate(rows, args.gate)
        prepared = [prepared_by_id[row["job_id"].strip()] for row in selected]
        print_gate_plan(args.gate, prepared)
        if args.gate == 0:
            print("STOP Gate 0 complete; no image calls were made.")
            return 0
        if not args.execute:
            print("DRY RUN: no image calls or output files were created.")
            return 0
        return execute_gate(
            root=root,
            gate=args.gate,
            rows=prepared,
            queue_path=queue_path,
            queue_hash=queue_hash,
            reference_path=reference_path,
            max_attempts=args.max_attempts,
        )
    except GeneratorError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
