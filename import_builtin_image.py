#!/usr/bin/env python3
"""Bridge Codex built-in image outputs into the approved token pipeline.

This companion never calls the OpenAI API and never writes ``upload/`` or the
workbook.  ``prompt-json`` emits one production queue prompt without alteration;
``import`` validates one built-in PNG, preserves its bytes as the master,
creates the premultiplied-alpha WebP derivative, and appends a result record.
"""

from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass, replace
from io import BytesIO
import json
from pathlib import Path
from typing import Any, Sequence

from PIL import Image, UnidentifiedImageError

import generate_tokens as approved
import chroma_key


BUILTIN_MODEL_ID = "gpt-image-2 (Codex built-in)"


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


def prompt_object(context: GateContext) -> dict[str, Any]:
    row = context.row
    prompt_hash = approved.sha256_bytes(row.prompt.encode("utf-8"))
    if prompt_hash != row.prompt_sha256:
        raise approved.SourceChangedError(f"{row.job_id} in-memory prompt changed before emission")
    return {
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
) -> int:
    row = context.row
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
    results_path = context.root / f"results-{approved.local_date()}.jsonl"

    # Built-in generation returns opaque RGB. The prompt therefore puts the subject on a
    # flat magenta key, and the transparent master is produced here by keying it out —
    # the contract's own remedy for an opaque result. The untouched capture is kept under
    # masters/_captures as evidence; only the keyed image becomes the master.
    capture_path = (
        context.root / "masters" / "_captures"
        / Path(*row.art_dir.split("/")) / f"{row.master_path.stem}.png"
    )
    if not capture_path.exists():
        approved.atomic_write_bytes(capture_path, capture_bytes)
    try:
        png_bytes, key_note = chroma_key.key_png_if_needed(capture_bytes)
    except chroma_key.KeyingError as exc:
        append_import_error(
            context,
            results_path,
            error=str(exc),
            extra_note="source=builtin_imagegen; capture kept under masters/_captures",
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
            extra_note="source=builtin_imagegen; actual_properties=unavailable",
        )
        print(f"ERROR {row.job_id}: {exc}")
        print(f"RESULTS {results_path}")
        return 1

    actual_row = row_with_actual_master_note(row, image)
    observation = image.observation
    properties_note = approved.merge_notes(actual_properties_note(image), key_note)
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

    failure = ""
    if image.width != image.height:
        failure = (
            f"square output validation failed: source dimensions are "
            f"{image.width}x{image.height}; master kept; export not written"
        )
    elif not observation.transparent_background:
        failure = approved.transparency_failure_reason(observation)
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

    approved.append_result(
        results_path,
        approved.result_record(
            actual_row,
            status="generated",
            model_id=BUILTIN_MODEL_ID,
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
    print(f"RESULTS {results_path}")
    return 0


def record_refusal(
    context: GateContext,
    sent_prompt_sha256: str,
    error_base64: str,
) -> int:
    row = context.row
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
            model_id=BUILTIN_MODEL_ID,
            extra_note="source=builtin_imagegen; no image returned",
            error=error,
        ),
    )
    print(f"REFUSED {row.job_id}: {error}")
    print(f"RESULTS {results_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    common.add_argument("--job", required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "prompt-json",
        parents=[common],
        help="emit an exact production prompt and orchestration metadata as one JSON object",
    )
    importer = subparsers.add_parser(
        "import",
        parents=[common],
        help="validate and import one PNG returned by Codex built-in image generation",
    )
    importer.add_argument("--input", type=Path, required=True)
    importer.add_argument("--sent-prompt-sha256", required=True)
    refusal = subparsers.add_parser(
        "record-refusal",
        parents=[common],
        help="append one exact built-in image-generation refusal to the results ledger",
    )
    refusal.add_argument("--sent-prompt-sha256", required=True)
    refusal.add_argument("--error-base64", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        context = load_gate_context(args.root, args.job)
        if args.command == "prompt-json":
            print(
                json.dumps(
                    prompt_object(context),
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
            return import_png(context, args.input, args.sent_prompt_sha256)
        if args.command == "record-refusal":
            return record_refusal(
                context, args.sent_prompt_sha256, args.error_base64
            )
        raise AssertionError(f"unknown command: {args.command}")
    except approved.GeneratorError as exc:
        print(f"BLOCKED: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
