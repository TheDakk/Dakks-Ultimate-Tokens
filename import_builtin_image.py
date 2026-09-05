#!/usr/bin/env python3
"""Bridge Codex built-in image outputs into the approved token pipeline.

This companion never calls the OpenAI API and never writes ``upload/`` or the
workbook.  ``prompt-json`` emits one production queue prompt without alteration;
``import`` validates one built-in PNG, keeps the untouched capture, keys the magenta
out into the RGBA master, creates the premultiplied-alpha WebP derivative (and every
shared-file copy the queue asks for), and appends a result record.

``--polish`` is the versioned revision route: ``prompt-json --polish`` emits the fixed
polish preamble (POLISH-PREAMBLE.txt) plus the row prompt and its hash, and names the
preserved capture to attach as the image to refine; ``import --polish`` accepts only
that hash, retires the approved capture, master and export to ``_superseded/`` as
``<stem>-<date>-polish-v<N>``, writes the new files under the unchanged names, and
records version N+1 in ``art/versions.json`` for the queue generator. Filenames never
carry a version. ``sync-copies`` writes any shared-file copy that is missing or stale.
"""

from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass, replace
from io import BytesIO
import json
from pathlib import Path
import re
from typing import Any, Sequence

from PIL import Image, UnidentifiedImageError

import generate_tokens as approved
import chroma_key


BUILTIN_MODEL_ID = "gpt-image-2 (Codex built-in)"
POLISH_MODEL_ID = "unreported (Codex built-in)"
POLISH_PREAMBLE_FILE = "POLISH-PREAMBLE.txt"
VERSIONS_FILE = "versions.json"
PASS_MANIFEST_FILE = "pass-manifest.json"


def load_pass_manifest(root: Path) -> dict[str, Any] | None:
    path = root / PASS_MANIFEST_FILE
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("revise"), dict) or not isinstance(data.get("baseline_versions"), dict):
        raise approved.GeneratorError(f"{PASS_MANIFEST_FILE} is malformed: needs 'revise' and 'baseline_versions'")
    return data
# The queue generator names every other directory a file serves in the row's notes.
COPY_NOTE_RE = re.compile(
    r"also drop a copy at \S+?/art/([a-z][a-z-]*)/([A-Za-z0-9][A-Za-z0-9._-]*\.webp)"
)


def polish_preamble(root: Path) -> str:
    """The fixed polish preamble: one trimmed line, hashed together with the row prompt."""
    path = root / POLISH_PREAMBLE_FILE
    if not path.is_file():
        raise approved.GeneratorError(f"polish preamble does not exist: {path}")
    text = path.read_bytes().decode("utf-8")
    if not text or text != text.strip() or "\r" in text or "\n" in text:
        raise approved.GeneratorError(f"polish preamble must be one trimmed line: {path}")
    return text


def polish_prompt(root: Path, row: approved.PreparedRow) -> tuple[str, str, str]:
    """Return (full polish prompt, its SHA-256, the preamble's SHA-256)."""
    preamble = polish_preamble(root)
    full = preamble + "\n\n" + row.prompt
    return (
        full,
        approved.sha256_bytes(full.encode("utf-8")),
        approved.sha256_bytes(preamble.encode("utf-8")),
    )


def versions_path(root: Path) -> Path:
    return root / "art" / VERSIONS_FILE


def load_versions(root: Path) -> dict[str, int]:
    """art/versions.json: "<art_dir>/<stem>" -> accepted revision (absent means 1)."""
    path = versions_path(root)
    if not path.is_file():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    versions: dict[str, int] = {}
    for key, value in raw.items():
        if key.startswith("_"):
            continue
        if isinstance(value, bool) or not isinstance(value, int) or value < 2:
            raise approved.GeneratorError(
                f"art/{VERSIONS_FILE}: {key!r} must be an integer version of 2 or more"
            )
        versions[key] = value
    return versions


def save_versions(root: Path, versions: dict[str, int]) -> None:
    body: dict[str, Any] = {
        "_format": (
            '"<art_dir>/<stem>": accepted revision number of art/<art_dir>/<stem>.webp; '
            "absent means version 1. Written only by import_builtin_image.py when it "
            "supersedes an approved file (the previous files go to _superseded/), read by "
            "the queue generator for the ASSETS version column. Filenames never carry the version."
        )
    }
    body.update({key: versions[key] for key in sorted(versions)})
    approved.atomic_write_bytes(
        versions_path(root),
        (json.dumps(body, indent=2, ensure_ascii=False) + "\n").encode("utf-8"),
    )


def version_key(row: approved.PreparedRow) -> str:
    return f"{row.art_dir}/{row.master_path.stem}"


def capture_path_for(root: Path, row: approved.PreparedRow) -> Path:
    return (
        root / "masters" / "_captures"
        / Path(*row.art_dir.split("/")) / f"{row.master_path.stem}.png"
    )


def extra_export_paths(root: Path, row: approved.PreparedRow) -> list[Path]:
    """Every other art directory the queue says this one file serves."""
    paths: list[Path] = []
    for match in COPY_NOTE_RE.finditer(row.source.get("notes", "")):
        directory = approved.safe_directory(
            match.group(1), field="notes copy dir", job_id=row.job_id
        )
        filename = approved.safe_filename(
            match.group(2), field="notes copy file", job_id=row.job_id
        )
        path = approved.ensure_under_root(
            root, root / "art" / Path(*directory.parts) / filename
        )
        if path != row.export_path and path not in paths:
            paths.append(path)
    return paths


def write_export_copies(root: Path, row: approved.PreparedRow) -> list[Path]:
    """Copy the approved export to every directory it serves; return what was written."""
    data = row.export_path.read_bytes()
    written: list[Path] = []
    for path in extra_export_paths(root, row):
        if not path.exists() or path.read_bytes() != data:
            approved.atomic_write_bytes(path, data)
            written.append(path)
    return written


def retire(root: Path, row: approved.PreparedRow, path: Path, suffix: str) -> Path | None:
    """Move an approved file to _superseded/<dir>/<stem>-<date>-<suffix><ext>; never overwrite."""
    if not path.exists():
        return None
    folder = root / "_superseded" / Path(*row.art_dir.split("/"))
    folder.mkdir(parents=True, exist_ok=True)
    base = f"{path.stem}-{approved.local_date()}-{suffix}"
    target = folder / f"{base}{path.suffix}"
    counter = 2
    while target.exists():
        target = folder / f"{base}-{counter}{path.suffix}"
        counter += 1
    path.replace(target)
    return target


@dataclass(frozen=True)
class BuiltinPng:
    width: int
    height: int
    mode: str
    observation: approved.ImageObservation


@dataclass(frozen=True)
class GateContext:
    root: Path
    queue_path: Path
    queue_hash: str
    reference_path: Path
    row: approved.PreparedRow


def _edge_checker_periodicity(
    pixels: Sequence[tuple[int, int, int, int]],
) -> tuple[int, float] | None:
    """Return the strongest checker half-period on one bright neutral edge.

    Built-in image output can render the transparency preview into an opaque
    PNG.  Those previews are not always clean enough for a global two-colour
    histogram, but their unobstructed outer edges retain the alternating
    light/dark square-wave.  A checker edge repeats after two square widths and
    inverts after one, which distinguishes it from a plain matte or gradient.
    """
    length = len(pixels)
    if length < 96:
        return None

    lumas: list[float] = []
    usable: list[bool] = []
    for red, green, blue, alpha in pixels:
        luma = (299 * red + 587 * green + 114 * blue) / 1000
        lumas.append(luma)
        usable.append(
            alpha >= 250
            and max(red, green, blue) - min(red, green, blue) <= 24
            and luma >= 200
        )

    usable_lumas = sorted(
        luma for luma, is_usable in zip(lumas, usable) if is_usable
    )
    if len(usable_lumas) < length * 0.75:
        return None

    low = usable_lumas[len(usable_lumas) // 10]
    high = usable_lumas[(len(usable_lumas) * 9) // 10]
    if high - low < 4.0:
        return None

    midpoint = (low + high) / 2
    states = [luma >= midpoint for luma in lumas]
    high_fraction = sum(
        state for state, is_usable in zip(states, usable) if is_usable
    ) / len(usable_lumas)
    if not 0.20 <= high_fraction <= 0.80:
        return None

    candidates: list[tuple[int, float]] = []
    best_score = 0.0
    maximum_period = min(96, length // 6)
    for period in range(4, maximum_period + 1):
        opposite_pairs = [
            index
            for index in range(length - period)
            if usable[index] and usable[index + period]
        ]
        repeated_pairs = [
            index
            for index in range(length - 2 * period)
            if usable[index] and usable[index + 2 * period]
        ]
        if (
            len(opposite_pairs) < length * 0.55
            or len(repeated_pairs) < length * 0.50
        ):
            continue

        opposite_score = sum(
            states[index] != states[index + period]
            for index in opposite_pairs
        ) / len(opposite_pairs)
        repeated_score = sum(
            states[index] == states[index + 2 * period]
            for index in repeated_pairs
        ) / len(repeated_pairs)
        score = min(opposite_score, repeated_score)
        candidates.append((period, score))
        if score > best_score:
            best_score = score

    if best_score < 0.65:
        return None
    # Odd multiples of a square width also invert/repeat, and can score a few
    # points higher because generated tile boundaries wobble.  Select the
    # shortest strong peak so both axes resolve to the fundamental scale.
    minimum_strong_score = max(0.65, best_score - 0.20)
    return next(
        (period, score)
        for period, score in candidates
        if score >= minimum_strong_score
    )


def _border_checkerboard_baked(image: Image.Image) -> bool:
    """Detect an opaque checker preview from matching edge periodicity."""
    with image.convert("RGBA") as rgba:
        width, height = rgba.size
        if width < 96 or height < 96:
            return False
        pixels = rgba.load()
        horizontal = [
            _edge_checker_periodicity(
                [pixels[x, y] for x in range(width)]
            )
            for y in (0, height - 1)
        ]
        vertical = [
            _edge_checker_periodicity(
                [pixels[x, y] for y in range(height)]
            )
            for x in (0, width - 1)
        ]

    horizontal = [result for result in horizontal if result is not None]
    vertical = [result for result in vertical if result is not None]
    if not horizontal or not vertical:
        return False
    horizontal_period, _ = max(horizontal, key=lambda result: result[1])
    vertical_period, _ = max(vertical, key=lambda result: result[1])
    tolerance = max(4, round(max(horizontal_period, vertical_period) * 0.30))
    return abs(horizontal_period - vertical_period) <= tolerance


def load_gate_context(root: Path, job_id: str) -> GateContext:
    root = root.resolve()
    queue_path = (root / "upload" / "ASSETS-universal.csv").resolve()
    reference_path = (root / "upload" / "generic-sheet-01.png").resolve()

    if not reference_path.is_file():
        raise approved.GeneratorError(f"reference does not exist: {reference_path}")
    reference_hash = approved.sha256_file(reference_path)
    if reference_hash != approved.REFERENCE_SHA256:
        raise approved.GeneratorError(f"reference SHA-256 mismatch: {reference_hash}")

    rows, queue_hash = approved.read_queue(queue_path)
    index = approved.production_index(rows)
    try:
        gate_zero = index["JOB-0001"]
    except KeyError as exc:
        raise approved.GeneratorError("requested row is not in ASSETS queue: JOB-0001") from exc
    approved.verify_handshake(gate_zero)

    # Preserve the calibration selection for its eight rows, then resolve every
    # other production job through its contractual gate.  Preparing the whole
    # selected gate retains the approved collision and row-state validation.
    calibration = approved.select_gate(rows, 1)
    calibration_ids = {item["job_id"].strip() for item in calibration}
    if job_id in calibration_ids:
        selected = calibration
    else:
        try:
            number = approved.job_number(index[job_id])
        except KeyError as exc:
            raise approved.GeneratorError(
                f"requested row is not in ASSETS queue: {job_id}"
            ) from exc
        if 1 <= number <= 23:
            selected = approved.select_gate(rows, 2)
        elif 24 <= number <= 102:
            selected = approved.select_gate(rows, 3)
        elif 103 <= number <= 1408:
            selected = approved.select_gate(rows, 4)
        else:
            raise approved.GeneratorError(
                f"{job_id} is outside the production gate range JOB-0001..JOB-1408"
            )
    prepared = approved.prepare_rows(root, selected)
    by_id = {row.job_id: row for row in prepared}
    try:
        row = by_id[job_id]
    except KeyError as exc:
        raise approved.GeneratorError(
            f"requested row is not in the selected production gate: {job_id}"
        ) from exc

    approved.verify_sources(queue_path, queue_hash, reference_path)
    return GateContext(root, queue_path, queue_hash, reference_path, row)


def prompt_object(context: GateContext, *, polish: bool = False) -> dict[str, Any]:
    row = context.row
    prompt_hash = approved.sha256_bytes(row.prompt.encode("utf-8"))
    if prompt_hash != row.prompt_sha256:
        raise approved.SourceChangedError(f"{row.job_id} in-memory prompt changed before emission")
    # A pass manifest decides the route for every row so the generator's agent never looks a
    # row up in a table: revise:<reason> (fresh generation, corrected brief) or polish.
    manifest = load_pass_manifest(context.root)
    route: dict[str, Any] = {}
    if manifest is not None:
        if manifest.get("queue_sha256") and manifest["queue_sha256"] != context.queue_hash:
            raise approved.GeneratorError(
                f"{PASS_MANIFEST_FILE} was written for queue {manifest['queue_sha256'][:12]}, "
                f"current queue is {context.queue_hash[:12]}; the reviewer must reissue the manifest"
            )
        current = load_versions(context.root).get(version_key(row), 1)
        baseline = int(manifest["baseline_versions"].get(version_key(row), 1))
        reason = manifest["revise"].get(row.job_id)
        # done when revised since the pass began, or when a polish row already stood at
        # version 2+ at pass start (pass 1 put it on the new model; no second polish)
        route = {
            "pass": manifest.get("pass", ""),
            "route": "revise" if reason else "polish",
            "revise_reason": reason or "",
            "done_in_pass": current > baseline or (not reason and baseline >= 2),
        }
        if not reason:
            polish = True
    payload: dict[str, Any] = {
        "job_id": row.job_id,
        "display_name": row.display_name,
        "resolved_prompt": row.prompt,
        "prompt_sha256": prompt_hash,
        "reference_path": str(context.reference_path),
        "reference_sha256": approved.REFERENCE_SHA256,
        "master_path": str(row.master_path),
        "export_path": str(row.export_path),
        "export_px": row.export_px,
        "expected_master_px": row.master_px,
        "master_exists": row.master_path.exists(),
        "export_exists": row.export_path.exists(),
    }
    payload.update(route)
    if polish:
        full, polish_hash, preamble_hash = polish_prompt(context.root, row)
        capture = capture_path_for(context.root, row)
        if not capture.is_file():
            raise approved.GeneratorError(
                f"{row.job_id} has no preserved capture to polish: {capture}"
            )
        current = load_versions(context.root).get(version_key(row), 1)
        payload.update(
            {
                "polish_prompt": full,
                "polish_sha256": polish_hash,
                "preamble_sha256": preamble_hash,
                "input_capture": str(capture),
                "version": current,
                "next_version": current + 1,
            }
        )
    return payload


def inspect_builtin_png(job_id: str, png_bytes: bytes) -> BuiltinPng:
    """Apply the approved alpha/checkerboard checks without assuming output size."""
    if not png_bytes.startswith(approved.PNG_SIGNATURE):
        raise approved.GeneratorError(f"{job_id} built-in output is not a PNG")
    try:
        with Image.open(BytesIO(png_bytes)) as opened:
            opened.load()
            if opened.format != "PNG":
                raise approved.GeneratorError(
                    f"{job_id} built-in output format is {opened.format!r}, not PNG"
                )
            if getattr(opened, "n_frames", 1) != 1:
                raise approved.GeneratorError(
                    f"{job_id} built-in output is an animated or multi-frame PNG"
                )
            width, height = opened.size
            if width < 1 or height < 1:
                raise approved.GeneratorError(
                    f"{job_id} built-in output has invalid dimensions {opened.size}"
                )
            mode = opened.mode
            has_alpha = "A" in opened.getbands()
            with opened.convert("RGBA") as rgba:
                with rgba.getchannel("A") as alpha:
                    extrema = alpha.getextrema()
                    histogram = alpha.histogram()
                    transparent_count = sum(histogram[:6])
                    transparent_fraction = transparent_count / (width * height)
                    corner_alphas = (
                        alpha.getpixel((0, 0)),
                        alpha.getpixel((width - 1, 0)),
                        alpha.getpixel((0, height - 1)),
                        alpha.getpixel((width - 1, height - 1)),
                    )
                checkerboard = bool(
                    approved.background_metrics(rgba)["checkerboard_baked"]
                    or _border_checkerboard_baked(rgba)
                )
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        raise approved.GeneratorError(
            f"{job_id} built-in output cannot be decoded as PNG"
        ) from exc

    observation = approved.ImageObservation(
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
    return BuiltinPng(width, height, mode, observation)


def actual_properties_note(image: BuiltinPng) -> str:
    observation = image.observation
    return approved.merge_notes(
        "source=builtin_imagegen",
        "source_format=PNG",
        f"source_dimensions={image.width}x{image.height}",
        f"source_mode={image.mode}",
        f"has_alpha_channel={'yes' if observation.has_alpha_channel else 'no'}",
        f"alpha_extrema={observation.alpha_extrema[0]},{observation.alpha_extrema[1]}",
        f"transparent_fraction={observation.transparent_fraction:.6f}",
        "corner_alphas=" + ",".join(str(value) for value in observation.corner_alphas),
        "artists_assessment=not_automatically_verifiable",
    )


def row_with_actual_master_note(
    row: approved.PreparedRow, image: BuiltinPng
) -> approved.PreparedRow:
    shortest_edge = min(image.width, image.height)
    note = f"master below spec: {shortest_edge}" if shortest_edge < row.master_px else ""
    return replace(row, note=note)


def append_import_error(
    context: GateContext,
    results_path: Path,
    *,
    error: str,
    row: approved.PreparedRow | None = None,
    observation: approved.ImageObservation | None = None,
    master_sha256: str = "",
    extra_note: str = "",
) -> None:
    approved.append_result(
        results_path,
        approved.result_record(
            row or context.row,
            status="error",
            model_id=BUILTIN_MODEL_ID,
            master_sha256=master_sha256,
            observation=observation,
            extra_note=extra_note,
            error=error,
        ),
    )


def import_png(
    context: GateContext,
    input_path: Path,
    sent_prompt_sha256: str,
    *,
    polish: bool = False,
    revise: str | None = None,
    model_id: str = BUILTIN_MODEL_ID,
) -> int:
    """Import one capture. Plain: a first image for an empty row. ``polish``: an image-to-image
    revision. ``revise=<reason>``: a fresh generation replacing an accepted image (a corrected
    brief). Both revisions retire the current files and record version N+1."""
    row = context.row
    root = context.root
    capture_path = capture_path_for(root, row)
    polish_note = ""
    current_version = 1
    if polish and revise:
        raise approved.GeneratorError(f"{row.job_id}: --polish and --revise are mutually exclusive")
    if revise is not None:
        revise = approved.safe_filename(revise, field="revise", job_id=row.job_id)
        expected_prompt_hash = approved.sha256_bytes(row.prompt.encode("utf-8"))
        if sent_prompt_sha256 != expected_prompt_hash or sent_prompt_sha256 != row.prompt_sha256:
            raise approved.GeneratorError(
                f"{row.job_id} sent prompt hash mismatch: "
                f"sent={sent_prompt_sha256!r}, expected={row.prompt_sha256}"
            )
        current_version = load_versions(root).get(version_key(row), 1)
        polish_note = approved.merge_notes(
            f"revise:{revise} v{current_version + 1}",
            "fresh generation on a corrected brief" if row.export_path.exists()
            else "fresh generation for a row emptied by review",
        )
    elif polish:
        _, polish_hash, preamble_hash = polish_prompt(root, row)
        if sent_prompt_sha256 != polish_hash:
            raise approved.GeneratorError(
                f"{row.job_id} sent polish prompt hash mismatch: "
                f"sent={sent_prompt_sha256!r}, expected={polish_hash}"
            )
        missing = [
            path for path in (row.master_path, row.export_path, capture_path)
            if not path.exists()
        ]
        if missing:
            raise approved.GeneratorError(
                f"{row.job_id} polish needs an approved master, export and capture; missing: "
                + ", ".join(str(path) for path in missing)
            )
        current_version = load_versions(root).get(version_key(row), 1)
        polish_note = approved.merge_notes(
            f"polish v{current_version + 1}",
            f"sent_polish_sha256={sent_prompt_sha256}",
            f"preamble_sha256={preamble_hash}",
        )
    else:
        expected_prompt_hash = approved.sha256_bytes(row.prompt.encode("utf-8"))
        if sent_prompt_sha256 != expected_prompt_hash or sent_prompt_sha256 != row.prompt_sha256:
            raise approved.GeneratorError(
                f"{row.job_id} sent prompt hash mismatch: "
                f"sent={sent_prompt_sha256!r}, expected={row.prompt_sha256}"
            )
        if row.export_path.exists():
            print(f"SKIP {row.job_id}: {row.export_rel} already exists")
            return 0
        if row.master_path.exists():
            raise approved.GeneratorError(
                f"refusing to overwrite existing master: {row.master_path}"
            )

    input_path = input_path.resolve()
    if not input_path.is_file():
        raise approved.GeneratorError(f"built-in output does not exist: {input_path}")
    approved.verify_sources(context.queue_path, context.queue_hash, context.reference_path)
    capture_bytes = input_path.read_bytes()
    results_path = root / f"results-{approved.local_date()}.jsonl"

    # Built-in generation returns opaque RGB. The prompt therefore puts the subject on a
    # flat magenta key, and the transparent master is produced here by keying it out —
    # the contract's own remedy for an opaque result. The untouched capture is kept under
    # masters/_captures as evidence; only the keyed image becomes the master. A polish
    # leaves the library untouched until the new image has passed every check.
    if not revising and not capture_path.exists():
        approved.atomic_write_bytes(capture_path, capture_bytes)
    try:
        png_bytes, key_note = chroma_key.key_png_if_needed(capture_bytes)
    except chroma_key.KeyingError as exc:
        append_import_error(
            context,
            results_path,
            error=str(exc),
            extra_note=approved.merge_notes(
                "source=builtin_imagegen",
                "revision rejected; library untouched" if revising else "capture kept under masters/_captures",
                polish_note,
            ),
        )
        print(f"ERROR {row.job_id}: {exc}")
        print(f"RESULTS {results_path}")
        return 1

    try:
        image = inspect_builtin_png(row.job_id, png_bytes)
    except approved.GeneratorError as exc:
        append_import_error(
            context,
            results_path,
            error=str(exc),
            extra_note=approved.merge_notes(
                "source=builtin_imagegen; actual_properties=unavailable", polish_note
            ),
        )
        print(f"ERROR {row.job_id}: {exc}")
        print(f"RESULTS {results_path}")
        return 1

    actual_row = row_with_actual_master_note(row, image)
    observation = image.observation
    failure = ""
    if image.width != image.height:
        failure = (
            f"square output validation failed: source dimensions are "
            f"{image.width}x{image.height}; master kept; export not written"
        )
    elif not observation.transparent_background:
        failure = approved.transparency_failure_reason(observation)

    if revising and failure:
        append_import_error(
            context,
            results_path,
            row=actual_row,
            error=failure,
            observation=observation,
            extra_note=approved.merge_notes(
                actual_properties_note(image), key_note, polish_note,
                failure, "polish rejected; library untouched",
            ),
        )
        print(f"ERROR {row.job_id}: {failure}")
        print(f"RESULTS {results_path}")
        return 1

    retired: list[Path] = []
    revising = polish or revise is not None
    if revising and not row.export_path.exists():
        # a row emptied by review (its files already under _superseded/): nothing to retire
        approved.atomic_write_bytes(capture_path, capture_bytes)
    elif revising:
        previous = (
            f"supersedes master_sha256={approved.sha256_file(row.master_path)} "
            f"export_sha256={approved.sha256_file(row.export_path)}"
        )
        suffix = f"polish-v{current_version}" if polish else f"{revise}-v{current_version}"
        for path, tag in ((capture_path, "-capture"), (row.master_path, ""), (row.export_path, "")):
            moved = retire(root, row, path, suffix + tag)
            if moved is not None:
                retired.append(moved)
        approved.atomic_write_bytes(capture_path, capture_bytes)
        polish_note = approved.merge_notes(
            polish_note,
            previous,
            "previous files retired as "
            + ", ".join(path.relative_to(root).as_posix() for path in retired),
        )
    properties_note = approved.merge_notes(actual_properties_note(image), key_note, polish_note)

    approved.verify_sources(context.queue_path, context.queue_hash, context.reference_path)
    approved.atomic_write_bytes(row.master_path, png_bytes)
    input_hash = approved.sha256_bytes(png_bytes)
    master_hash = approved.sha256_file(row.master_path)
    if master_hash != input_hash:
        error = f"{row.job_id} master differs from the built-in output bytes"
        append_import_error(
            context,
            results_path,
            row=actual_row,
            error=error,
            observation=observation,
            master_sha256=master_hash,
            extra_note=properties_note,
        )
        print(f"ERROR {row.job_id}: {error}")
        print(f"RESULTS {results_path}")
        return 1

    if failure:
        append_import_error(
            context,
            results_path,
            row=actual_row,
            error=failure,
            observation=observation,
            master_sha256=master_hash,
            extra_note=approved.merge_notes(properties_note, failure),
        )
        print(f"ERROR {row.job_id}: {failure}")
        print(f"RESULTS {results_path}")
        return 1

    try:
        approved.export_webp_premultiplied(
            row.master_path, row.export_path, row.export_px
        )
        export_hash = approved.sha256_file(row.export_path)
        copies = write_export_copies(root, row)
    except Exception as exc:
        error = str(exc)
        append_import_error(
            context,
            results_path,
            row=actual_row,
            error=error,
            observation=observation,
            master_sha256=master_hash,
            extra_note=properties_note,
        )
        print(f"ERROR {row.job_id}: {error}")
        print(f"RESULTS {results_path}")
        return 1

    if revising:
        versions = load_versions(root)
        versions[version_key(row)] = current_version + 1
        save_versions(root, versions)
    if copies:
        properties_note = approved.merge_notes(
            properties_note,
            "shared-file copies written: "
            + ", ".join(path.relative_to(root).as_posix() for path in copies),
        )

    approved.append_result(
        results_path,
        approved.result_record(
            actual_row,
            status="generated",
            model_id=model_id,
            master_sha256=master_hash,
            export_sha256=export_hash,
            observation=observation,
            extra_note=properties_note,
        ),
    )
    print(
        f"OK {row.job_id}: source={image.width}x{image.height} mode={image.mode} "
        f"alpha={'yes' if observation.transparent_background else 'no'} "
        f"checkerboard={'yes' if observation.checkerboard_baked else 'no'}"
    )
    print(f"MASTER {row.master_path} sha256={master_hash}")
    print(f"EXPORT {row.export_path} sha256={export_hash}")
    for path in copies:
        print(f"COPY {path}")
    if revising:
        print(
            f"VERSION {version_key(row)} v{current_version + 1}; previous retired: "
            + (", ".join(path.relative_to(root).as_posix() for path in retired) or "none (row was empty)")
        )
    print(f"RESULTS {results_path}")
    return 0


def record_refusal(
    context: GateContext,
    sent_prompt_sha256: str,
    error_base64: str,
    *,
    polish: bool = False,
    model_id: str = BUILTIN_MODEL_ID,
) -> int:
    row = context.row
    if polish:
        _, expected_prompt_hash, _ = polish_prompt(context.root, row)
        if sent_prompt_sha256 != expected_prompt_hash:
            raise approved.GeneratorError(
                f"{row.job_id} sent polish prompt hash mismatch: "
                f"sent={sent_prompt_sha256!r}, expected={expected_prompt_hash}"
            )
    else:
        expected_prompt_hash = approved.sha256_bytes(row.prompt.encode("utf-8"))
        if sent_prompt_sha256 != expected_prompt_hash or sent_prompt_sha256 != row.prompt_sha256:
            raise approved.GeneratorError(
                f"{row.job_id} sent prompt hash mismatch: "
                f"sent={sent_prompt_sha256!r}, expected={row.prompt_sha256}"
            )
    try:
        error = base64.b64decode(error_base64, validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise approved.GeneratorError(f"invalid refusal error payload: {exc}") from exc
    approved.verify_sources(context.queue_path, context.queue_hash, context.reference_path)
    results_path = context.root / f"results-{approved.local_date()}.jsonl"
    approved.append_result(
        results_path,
        approved.result_record(
            row,
            status="refused",
            model_id=model_id,
            extra_note=approved.merge_notes(
                "source=builtin_imagegen; no image returned",
                f"polish attempt; sent_polish_sha256={sent_prompt_sha256}" if polish else "",
            ),
            error=error,
        ),
    )
    print(f"REFUSED {row.job_id}: {error}")
    print(f"RESULTS {results_path}")
    return 0


def retired_set(root: Path, row: approved.PreparedRow, version: int) -> dict[str, Path]:
    """The capture, master and export retired when version `version` was superseded
    (by a polish or a revise; the suffix is <reason>-v<version>)."""
    folder = root / "_superseded" / Path(*row.art_dir.split("/"))
    stem = row.master_path.stem
    found: dict[str, list[Path]] = {"capture": [], "master": [], "export": []}
    # <stem>-<date>-<reason>-v<N>[-capture][-<n>].<ext>; the keyer's own -key-v* retirements
    # from the first run and -rejected files are not revision predecessors
    pattern = re.compile(r"^-(\d{4}-\d{2}-\d{2})-(?P<reason>[a-z0-9]+(?:-[a-z0-9]+)*?)-v(?P<v>\d+)(?P<cap>-capture)?(?:-\d+)?\.(?:png|webp)$", re.I)
    for path in sorted(folder.glob(f"{stem}-*-v{version}*")):
        name = path.name[len(stem):]
        m = pattern.match(name)
        if not m or int(m.group("v")) != version:
            continue
        reason = m.group("reason").lower()
        if reason == "key" or "rejected" in reason:
            continue
        if path.suffix.lower() == ".webp":
            found["export"].append(path)
        elif m.group("cap"):
            found["capture"].append(path)
        elif path.suffix.lower() == ".png":
            # legacy naming from the first polish pass: tell capture (RGB) from master (RGBA)
            with Image.open(path) as opened:
                found["capture" if "A" not in opened.getbands() else "master"].append(path)
    out: dict[str, Path] = {}
    for role, paths in found.items():
        if len(paths) > 1:
            raise approved.GeneratorError(
                f"{row.job_id} has more than one retired {role} for v{version}: "
                + ", ".join(str(x) for x in paths)
            )
        if paths:
            out[role] = paths[0]
    return out


def revert_polish(context: GateContext, reason: str, *, restore: bool = True) -> int:
    """Reject the current polish revision: retire it as rejected and restore the previous one."""
    row = context.row
    root = context.root
    reason = approved.safe_filename(reason, field="reason", job_id=row.job_id)
    versions = load_versions(root)
    current = versions.get(version_key(row), 1)
    if current < 2:
        raise approved.GeneratorError(f"{row.job_id} is at version 1; there is no polish to revert")
    previous = retired_set(root, row, current - 1) if restore else {}
    if restore and ("master" not in previous or "export" not in previous):
        raise approved.GeneratorError(
            f"{row.job_id} cannot restore v{current - 1}: retired master/export not found under _superseded/"
        )
    capture_path = capture_path_for(root, row)
    approved.verify_sources(context.queue_path, context.queue_hash, context.reference_path)
    results_path = root / f"results-{approved.local_date()}.jsonl"

    rejected: list[Path] = []
    suffix = f"polish-v{current}-rejected-{reason}"
    for path, tag in ((capture_path, "-capture"), (row.master_path, ""), (row.export_path, "")):
        moved = retire(root, row, path, suffix + tag)
        if moved is not None:
            rejected.append(moved)
    restored: list[Path] = []
    if restore:
        for role, target in (("capture", capture_path), ("master", row.master_path), ("export", row.export_path)):
            source = previous.get(role)
            if source is not None:
                target.parent.mkdir(parents=True, exist_ok=True)
                source.replace(target)
                restored.append(target)
        write_export_copies(root, row)
    if current - 1 >= 2:
        versions[version_key(row)] = current - 1
    else:
        versions.pop(version_key(row), None)
    save_versions(root, versions)

    note = approved.merge_notes(
        f"polish v{current} rejected by review: {reason}",
        "rejected files retired as " + ", ".join(x.relative_to(root).as_posix() for x in rejected),
        ("restored v%d: " % (current - 1)) + ", ".join(x.relative_to(root).as_posix() for x in restored)
        if restore else "row left empty for a re-roll (plain import)",
    )
    if restore:
        approved.append_result(
            results_path,
            approved.result_record(
                row,
                status="generated",
                model_id=POLISH_MODEL_ID,
                master_sha256=approved.sha256_file(row.master_path),
                export_sha256=approved.sha256_file(row.export_path),
                extra_note=note,
            ),
        )
    else:
        approved.append_result(
            results_path,
            approved.result_record(
                row, status="error", model_id=POLISH_MODEL_ID, extra_note=note,
                error=f"polish v{current} rejected by review: {reason}; row emptied for re-roll",
            ),
        )
    print(f"REVERTED {row.job_id}: v{current} -> v{current - 1 if restore else 'none'}; {note}")
    print(f"RESULTS {results_path}")
    return 0


def sync_copies(root: Path) -> int:
    """Write every shared-file copy the queue asks for that is missing or stale."""
    root = root.resolve()
    rows, _ = approved.read_queue(root / "upload" / "ASSETS-universal.csv")
    ordered = sorted(approved.production_index(rows).values(), key=approved.job_number)
    prepared = approved.prepare_rows(root, ordered)
    results_path = root / f"results-{approved.local_date()}.jsonl"
    written = 0
    pending = 0
    for row in prepared:
        if not extra_export_paths(root, row):
            continue
        if not row.export_path.exists():
            pending += 1
            print(f"PENDING {row.job_id}: {row.export_rel} not generated yet")
            continue
        for path in write_export_copies(root, row):
            written += 1
            relative = path.relative_to(root).as_posix()
            approved.append_result(
                results_path,
                approved.result_record(
                    row,
                    status="generated",
                    model_id=BUILTIN_MODEL_ID,
                    master_sha256=approved.sha256_file(row.master_path),
                    export_sha256=approved.sha256_file(row.export_path),
                    extra_note=f"shared-file copy written: {relative}; master and primary export unchanged",
                ),
            )
            print(f"COPY {row.job_id}: {relative}")
    print(f"copies written: {written}; rows pending generation: {pending}; ledger {results_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    common.add_argument("--job", required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    polish_help = (
        "the versioned polish route: the preamble in POLISH-PREAMBLE.txt plus the row prompt, "
        "image-to-image from the preserved capture; the approved files are retired to _superseded/"
    )
    prompt = subparsers.add_parser(
        "prompt-json",
        parents=[common],
        help="emit an exact production prompt and orchestration metadata as one JSON object",
    )
    prompt.add_argument("--polish", action="store_true", help=polish_help)
    importer = subparsers.add_parser(
        "import",
        parents=[common],
        help="validate and import one PNG returned by Codex built-in image generation",
    )
    importer.add_argument("--input", type=Path, required=True)
    importer.add_argument("--sent-prompt-sha256", required=True)
    importer.add_argument("--polish", action="store_true", help=polish_help)
    importer.add_argument(
        "--revise",
        default=None,
        metavar="REASON",
        help="versioned re-roll: a fresh generation replacing an accepted image on a corrected brief; "
             "the current files are retired to _superseded/ as <stem>-<date>-<REASON>-v<N> and version N+1 is recorded",
    )
    importer.add_argument(
        "--model",
        default=None,
        help="model id the image tool reports, recorded on the ledger line (default: the route's constant)",
    )
    refusal = subparsers.add_parser(
        "record-refusal",
        parents=[common],
        help="append one exact built-in image-generation refusal to the results ledger",
    )
    refusal.add_argument("--sent-prompt-sha256", required=True)
    refusal.add_argument("--error-base64", required=True)
    refusal.add_argument("--polish", action="store_true", help=polish_help)
    refusal.add_argument("--model", default=None)
    revert = subparsers.add_parser(
        "revert-polish",
        parents=[common],
        help="reject the current polish revision: retire it as rejected and restore the previous files",
    )
    revert.add_argument("--reason", required=True, help="short slug recorded in the retired filename and the ledger")
    revert.add_argument("--no-restore", action="store_true", help="leave the row empty for a fresh re-roll instead of restoring the previous version")
    sync = subparsers.add_parser(
        "sync-copies",
        help='write every shared-file copy the queue asks for ("also drop a copy at ...") that is missing or stale',
    )
    sync.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "sync-copies":
            return sync_copies(args.root)
        context = load_gate_context(args.root, args.job)
        polish = bool(getattr(args, "polish", False))
        model_id = getattr(args, "model", None) or (POLISH_MODEL_ID if polish else BUILTIN_MODEL_ID)
        if args.command == "prompt-json":
            print(
                json.dumps(
                    prompt_object(context, polish=polish),
                    # Keep the shell bridge byte-safe on Windows consoles. JSON
                    # parsing restores these escapes to the original code points
                    # before the prompt is passed to built-in image generation.
                    ensure_ascii=True,
                    allow_nan=False,
                    separators=(",", ":"),
                )
            )
            return 0
        if args.command == "import":
            return import_png(
                context, args.input, args.sent_prompt_sha256, polish=polish,
                revise=getattr(args, "revise", None), model_id=model_id,
            )
        if args.command == "revert-polish":
            return revert_polish(context, args.reason, restore=not args.no_restore)
        if args.command == "record-refusal":
            return record_refusal(
                context, args.sent_prompt_sha256, args.error_base64, polish=polish, model_id=model_id
            )
        raise AssertionError(f"unknown command: {args.command}")
    except approved.GeneratorError as exc:
        print(f"BLOCKED: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
