#!/usr/bin/env python3
"""Lay every generated master out in labelled contact sheets, in job order, for review.

    .venv\\Scripts\\python.exe review_sheets.py                 all masters -> review\\sheet-NN.png
    .venv\\Scripts\\python.exe review_sheets.py --since JOB-0212 only rows at or after that job
    .venv\\Scripts\\python.exe review_sheets.py --jobs JOB-0022 JOB-0088 ...

Twelve per sheet (4 x 3), each master downscaled onto a mid-grey ground that stands in for a
map, labelled with job_id and display name. The reviewer looks at every sheet: the automated
gates catch technical defects, and a wrong subject or a missing head only shows up to an eye.
"""

from __future__ import annotations

import argparse
import csv
import io
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
TILE, COLS, ROWS = 480, 4, 3


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", help="first job_id to include")
    ap.add_argument("--jobs", nargs="*", help="explicit job ids")
    ap.add_argument("--out", type=Path, default=ROOT / "review")
    args = ap.parse_args()

    rows = list(csv.DictReader(io.StringIO((ROOT / "upload" / "ASSETS-universal.csv").read_text(encoding="utf-8-sig"))))
    have = []
    for r in rows:
        if args.jobs and r["job_id"] not in args.jobs:
            continue
        if args.since and r["job_id"] < args.since:
            continue
        p = ROOT / "masters" / r["art_dir"] / f"{r['filename_stem']}.png"
        if p.is_file():
            have.append((r["job_id"], r["display_name"], p))
    have.sort()
    args.out.mkdir(parents=True, exist_ok=True)
    for old in args.out.glob("sheet-*.png"):
        old.unlink()
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
    per = COLS * ROWS
    for i in range(0, len(have), per):
        batch = have[i:i + per]
        sheet = Image.new("RGB", (COLS * TILE, ROWS * (TILE + 34)), (96, 92, 84))
        d = ImageDraw.Draw(sheet)
        for k, (job, name, p) in enumerate(batch):
            x, y = (k % COLS) * TILE, (k // COLS) * (TILE + 34)
            with Image.open(p) as im:
                im = im.convert("RGBA"); im.thumbnail((TILE - 8, TILE - 8), Image.Resampling.LANCZOS)
                tile = Image.new("RGBA", (TILE, TILE), (96, 92, 84, 255))
                tile.alpha_composite(im, ((TILE - im.width) // 2, (TILE - im.height) // 2))
                sheet.paste(tile.convert("RGB"), (x, y))
            d.text((x + 8, y + TILE + 6), f"{job}  {name[:26]}", fill=(240, 236, 226), font=font)
        n = i // per + 1
        sheet.save(args.out / f"sheet-{n:02d}.png", optimize=True)
    print(f"{len(have)} masters -> {(len(have) + per - 1) // per} sheets in {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
