"""Classify every revised row by the magnitude of its change and write the change log.

    .venv\\Scripts\\python.exe changelog.py                     # CHANGELOG-2.0.md + changelog-2.0.json
    .venv\\Scripts\\python.exe changelog.py --release 2.0.0 --mad 12 --scale 0.05

A row is revised when art/versions.json records a version of 2 or more. Its latest
"generated" ledger line says how: ``revise:<reason>`` is a fresh generation on a corrected
brief and is always a REDESIGN; ``polish v<N>`` is image-to-image and is measured against
the retired predecessor under _superseded/: a mean absolute greyscale difference at 200 px
(0..255) of at least --mad, or a subject-scale drift of at least --scale, makes it a CHANGE;
anything smaller is POLISH. The thresholds were set from polish pass 1 (2026-09-05), where
every faithful revision scored below 12 and design departures scored above it.

The JSON is what prune_superseded.py reads; the Markdown is the release note.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import generate_tokens as approved  # noqa: E402
import import_builtin_image as builtin  # noqa: E402

GREY = (128, 128, 128, 255)


def on_grey(im: Image.Image, size: int) -> Image.Image:
    im = im.convert("RGBA").resize((size, size), Image.LANCZOS)
    return Image.alpha_composite(Image.new("RGBA", im.size, GREY), im)


def bbox_area(im: Image.Image) -> float:
    b = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if not b:
        return 0.0
    w, h = im.size
    return ((b[2] - b[0]) / w) * ((b[3] - b[1]) / h)


def measure(old_p: Path, new_p: Path) -> tuple[float, float]:
    """(mean absolute greyscale difference at 200 px, subject scale ratio new/old)."""
    old = Image.open(old_p).convert("RGBA")
    new = Image.open(new_p).convert("RGBA")
    mad = ImageStat.Stat(ImageChops.difference(on_grey(old, 200).convert("L"), on_grey(new, 200).convert("L"))).mean[0]
    ao, an = bbox_area(old), bbox_area(new)
    scale = math.sqrt(an / ao) if ao and an else 1.0
    return round(mad, 2), round(scale, 3)


def classify(kind: str, mad: float | None, scale: float | None, mad_max: float, scale_max: float) -> str:
    if kind == "redesign":
        return "redesign"
    if mad is None or scale is None:
        return "change"          # no predecessor to measure against: never call it minor
    if mad >= mad_max or abs(scale - 1.0) >= scale_max:
        return "change"
    return "polish"


def ledger_lines(root: Path) -> list[dict]:
    lines: list[dict] = []
    for path in sorted(root.glob("results-*.jsonl")):
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.strip():
                lines.append(json.loads(raw))
    return lines


def latest_revision_line(lines: list[dict], job_id: str, version: int) -> dict | None:
    """The generated line that produced version `version` of this row."""
    tag_polish = f"polish v{version}"
    tag_revise = f" v{version}"
    for rec in reversed(lines):
        if rec.get("job_id") != job_id or rec.get("status") != "generated":
            continue
        note = rec.get("note", "")
        if tag_polish in note or ("revise:" in note and tag_revise in note):
            return rec
    return None


def build(root: Path, release: str, mad_max: float, scale_max: float) -> tuple[list[dict], dict]:
    rows, _ = approved.read_queue(root / "upload" / "ASSETS-universal.csv")
    ordered = sorted(approved.production_index(rows).values(), key=approved.job_number)
    prepared = {builtin.version_key(r): r for r in approved.prepare_rows(root, ordered)}
    versions = builtin.load_versions(root)
    lines = ledger_lines(root)
    out: list[dict] = []
    for key, version in sorted(versions.items(), key=lambda kv: approved.job_number(prepared[kv[0]].source) if kv[0] in prepared else 0):
        row = prepared.get(key)
        if row is None:
            out.append({"key": key, "version": version, "class": "unknown", "reason": "no queue row"})
            continue
        rec = latest_revision_line(lines, row.job_id, version)
        note = rec.get("note", "") if rec else ""
        kind = "redesign" if "revise:" in note else "polish"
        reason = ""
        if kind == "redesign":
            reason = note.split("revise:", 1)[1].split(" ", 1)[0]
        previous = builtin.retired_set(root, row, version - 1)
        mad = scale = None
        if "master" in previous and row.master_path.exists():
            mad, scale = measure(previous["master"], row.master_path)
        klass = classify(kind, mad, scale, mad_max, scale_max)
        out.append({
            "job_id": row.job_id, "name": row.display_name, "key": key, "version": version,
            "kind": kind, "reason": reason, "class": klass, "mad": mad, "scale": scale,
            "model": rec.get("model", "") if rec else "",
            "predecessors": [p.relative_to(root).as_posix() for p in previous.values()],
            "ledger_created_at": rec.get("created_at", "") if rec else "",
        })
    summary = {
        "release": release, "rows_revised": len(out),
        "redesign": sum(1 for o in out if o["class"] == "redesign"),
        "change": sum(1 for o in out if o["class"] == "change"),
        "polish": sum(1 for o in out if o["class"] == "polish"),
        "unknown": sum(1 for o in out if o["class"] == "unknown"),
        "thresholds": {"mad": mad_max, "scale": scale_max},
    }
    return out, summary


def write_markdown(path: Path, entries: list[dict], summary: dict) -> None:
    lines = [f"# Dakk's Ultimate Tokens {summary['release']}: change log", ""]
    lines.append(f"{summary['rows_revised']} of 1408 rows revised: {summary['redesign']} redesigned, "
                 f"{summary['change']} changed noticeably, {summary['polish']} polished. "
                 f"Filenames are unchanged; the version number lives in the workbook and art/versions.json.")
    lines.append("")
    for klass, title, blurb in (
        ("redesign", "Redesigned", "Fresh paintings on corrected briefs: the previous image had the wrong body plan, identity or object."),
        ("change", "Changed noticeably", "Image-to-image revisions whose measured difference from the previous painting is large; reviewed by eye."),
        ("polish", "Polished", "Image-to-image revisions with the same design: sharper detail, cleaner edges, richer material."),
    ):
        group = [e for e in entries if e["class"] == klass]
        lines.append(f"## {title} ({len(group)})")
        lines.append("")
        lines.append(blurb)
        lines.append("")
        for e in group:
            extra = f" ({e['reason']})" if e.get("reason") else ""
            metric = "" if e.get("mad") is None else f" diff {e['mad']}, scale x{e['scale']}"
            lines.append(f"- {e['name']} ({e['job_id']}) v{e['version']}{extra}{metric}")
        lines.append("")
    unknown = [e for e in entries if e["class"] == "unknown"]
    if unknown:
        lines.append(f"## Unresolved ({len(unknown)})")
        lines.extend(f"- {e['key']}: {e['reason']}" for e in unknown)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--release", default="2.0.0")
    ap.add_argument("--mad", type=float, default=12.0, help="mean abs greyscale difference (0-255) at or above which a polish is a CHANGE")
    ap.add_argument("--scale", type=float, default=0.05, help="subject scale drift at or above which a polish is a CHANGE")
    ap.add_argument("--out", default=None, help="basename for the outputs (default CHANGELOG-<release>)")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    entries, summary = build(root, args.release, args.mad, args.scale)
    base = args.out or f"CHANGELOG-{args.release.rsplit('.', 1)[0]}"
    md = root / f"{base}.md"
    js = root / f"{base.lower()}.json"
    write_markdown(md, entries, summary)
    js.write_text(json.dumps({"summary": summary, "rows": entries}, indent=1), encoding="utf-8")
    print(json.dumps(summary))
    print(f"wrote {md} and {js}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
