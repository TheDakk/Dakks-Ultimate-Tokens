#!/usr/bin/env python3
"""Verify a block of generated rows and answer GO or STOP. Run after every block.

    .venv\\Scripts\\python.exe verify_gate.py            check everything imported since the last GO
    .venv\\Scripts\\python.exe verify_gate.py --all      check every master in the library
    .venv\\Scripts\\python.exe verify_gate.py --reset    forget the cursor (next run checks everything)

What it checks, in the order failures actually happen:
  1. the suite's intake gate, npm run art-check: filenames match rows, real alpha, no white
     halo, square, right export size, nothing clipped;
  2. the ledger, results-*.jsonl, last line per job_id: refusal and error rates for the block;
  3. every master written since the last GO, by pixel: corners fully transparent, no hot
     magenta anywhere, no green rim, rose cast (by hue) below the level the keyer leaves on
     a clean subject, and a sane transparent fraction.

Stop rules: art-check fails; any master fails the pixel checks; refusals or errors above
--max-fail-rate of the block's attempts; a block of zero attempts is a GO with a note.

It never modifies masters, exports, the queue or the workbook. It writes verify-<stamp>.json
and, on GO, advances a cursor file (.verify-cursor) so the next run checks only new rows.
Exit code 0 = GO, 1 = STOP, 2 = could not run.
"""

from __future__ import annotations

import argparse
import colorsys
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
DND2E = Path("C:/Projects/FoundryVTT/DnD2E")
CURSOR = ROOT / ".verify-cursor"

# pixel thresholds, calibrated on the Gate 1-3 masters after keyer v3.9
CORNER_ALPHA_MAX = 5
HOT_MAGENTA_MAX = 60          # pixels with min(R,B)-G > 100 anywhere visible (sampled every 2nd px)
GREEN_RIM_MAX = 400           # green pixels ON THE RIM (sampled); a subject's own green lives inside the body and is not counted
GREEN_FRINGE_RATIO = 3.0      # a keying fringe is green on the rim ONLY: rim share must exceed 3x the interior share (+2 pts) to count
ROSE_SHARE_MAX = 0.06         # low-saturation rose (315-360) on the rim or partial pixels, as a share of visible pixels
CLEAR_MIN, CLEAR_MAX = 0.20, 0.995   # a lance or a chain is a thin line in an empty frame; emptiness is judged by MIN_VISIBLE below, not by this ceiling
MIN_VISIBLE = 1500            # sampled visible pixels (every 2nd px); below this the frame is effectively empty


def ledger_lines() -> list[dict]:
    out = []
    for p in sorted(ROOT.glob("results-*.jsonl")):
        for line in p.open("r", encoding="utf-8"):
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    out.append({"job_id": "?", "status": "error", "error": f"unparseable line in {p.name}"})
    return out


def read_cursor() -> int:
    try:
        return int(CURSOR.read_text().strip())
    except (FileNotFoundError, ValueError):
        return 0


def art_check(log: list[str]) -> bool:
    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        log.append("STOP npm not on PATH; cannot run art-check"); return False
    proc = subprocess.run([npm, "run", "art-check"], cwd=str(DND2E), capture_output=True, text=True, encoding="utf-8", errors="replace")
    tail = [l for l in proc.stdout.splitlines() if l.strip()][-6:]
    log.extend("  art-check | " + l for l in tail)
    return proc.returncode == 0


def pixel_check(path: Path) -> tuple[bool, dict]:
    with Image.open(path) as im:
        im.load()
        rgb = im.convert("RGB"); a = im.getchannel("A"); px = rgb.load(); pa = a.load(); w, h = im.size
        corners = [a.getpixel(q) for q in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
        hist = a.histogram(); clear = hist[0] / (w * h)
        # the rim: within 3px of a fully transparent pixel. A keying fringe lives here;
        # a subject's own green glow or violet smoke lives inside the body.
        from PIL import ImageFilter
        clear_mask = a.point(lambda v: 255 if v <= 5 else 0)
        rim = clear_mask.filter(ImageFilter.MaxFilter(7)).load()
        visible = hot = green = rose = 0
        rim_n = green_in = 0
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                if not pa[x, y]:
                    continue
                visible += 1
                r, g, b = px[x, y]
                if min(r, b) - g > 100: hot += 1
                is_green = g > max(r, b) + 40
                if rim[x, y]:
                    rim_n += 1
                    if is_green: green += 1
                elif is_green:
                    green_in += 1
                # keying rose is LOW saturation (the keyer pulls it toward grey); painted
                # rose or mauve smoke is saturated and is the subject's own colour
                hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                if 0.12 < ss <= 0.30 and vv > 0.45 and 315 <= hh * 360 <= 360 and (rim[x, y] or pa[x, y] < 255): rose += 1
    rim_share = green / max(rim_n, 1)
    in_share = green_in / max(visible - rim_n, 1)
    # painted green (a rainbow, a green glow) is green inside the body as well; a keying
    # fringe is green on the rim only (measured 2026-09-03: fringe = rim 6%+ vs interior 0%)
    green_flag = green > GREEN_RIM_MAX and rim_share > GREEN_FRINGE_RATIO * in_share + 0.02
    stats = {"corners": corners, "clear": round(clear, 3), "hot_magenta": hot, "green": green,
             "rose_share": round(rose / max(visible, 1), 3), "visible": visible,
             "green_rim_share": round(rim_share, 3), "green_in_share": round(in_share, 3)}
    ok = (max(corners) <= CORNER_ALPHA_MAX and hot <= HOT_MAGENTA_MAX and not green_flag
          and stats["rose_share"] <= ROSE_SHARE_MAX and CLEAR_MIN <= clear <= CLEAR_MAX and visible >= MIN_VISIBLE)
    return ok, stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="check every master, not just those since the cursor")
    ap.add_argument("--reset", action="store_true", help="delete the cursor and exit")
    ap.add_argument("--max-fail-rate", type=float, default=0.10)
    ap.add_argument("--dnd2e", type=Path, default=DND2E)
    args = ap.parse_args()
    if args.reset:
        CURSOR.unlink(missing_ok=True); print("cursor reset"); return 0

    log: list[str] = []
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    lines = ledger_lines()
    start = 0 if args.all else read_cursor()
    block = lines[start:]
    log.append(f"ledger lines: {len(lines)} total, {len(block)} since cursor {start}")

    # 2. block outcome from the ledger: last line per job in the block decides
    last: dict[str, dict] = {}
    for r in block:
        last[r.get("job_id", "?")] = r
    # A reviewer's rejection (revert-polish --no-restore) is an "error" line so the row reads
    # as not-generated, but it is not a failed generation attempt: leave it out of the rate.
    reviewer = {j for j, r in last.items() if "rejected by review" in r.get("error", "")}
    generated = [j for j, r in last.items() if r.get("status") == "generated"]
    refused = [j for j, r in last.items() if r.get("status") == "refused"]
    errored = [j for j, r in last.items() if r.get("status") == "error" and j not in reviewer]
    for j in sorted(reviewer): log.append(f"  reviewer rejection (not an attempt) {j}: {last[j].get('error', '')[:100]}")
    attempted = len(last) - len(reviewer)
    log.append(f"block: attempted={attempted} generated={len(generated)} refused={len(refused)} error={len(errored)}")
    for j in refused: log.append(f"  refused {j}: {last[j].get('error', '')[:100]}")
    for j in errored: log.append(f"  error   {j}: {last[j].get('error', '')[:100]}")

    stop_reasons: list[str] = []
    if attempted and (len(refused) + len(errored)) / attempted > args.max_fail_rate:
        stop_reasons.append(f"{len(refused) + len(errored)} of {attempted} attempts failed, above {args.max_fail_rate:g}")

    # 1. the intake gate
    if not art_check(log):
        stop_reasons.append("art-check reported problems")

    # 3. pixel checks on the block's masters (or all)
    if args.all:
        targets = sorted(p for p in ROOT.glob("masters/*/*.png") if "_captures" not in p.parts and "_calibration-builtin" not in p.parts)
    else:
        targets = []
        for j in generated:
            mp = last[j].get("master_path", "")
            if mp:
                p = ROOT / mp
                if p.is_file(): targets.append(p)
    bad = []
    for p in targets:
        ok, stats = pixel_check(p)
        if not ok:
            bad.append((p, stats))
    log.append(f"pixel checks: {len(targets)} masters, {len(bad)} failing")
    for p, st in bad[:20]:
        log.append(f"  FAIL {p.relative_to(ROOT).as_posix()}: {st}")
    if bad:
        stop_reasons.append(f"{len(bad)} master(s) fail pixel checks")

    verdict = "STOP" if stop_reasons else "GO"
    report = {"stamp": stamp, "verdict": verdict, "reasons": stop_reasons, "cursor_start": start,
              "ledger_total": len(lines), "attempted": attempted, "generated": len(generated),
              "refused": refused, "errored": errored, "pixel_failures": [p.relative_to(ROOT).as_posix() for p, _ in bad],
              "log": log}
    (ROOT / f"verify-{stamp}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("\n".join(log))
    print(f"\n{verdict}" + (": " + "; ".join(stop_reasons) if stop_reasons else (" (nothing attempted in this block)" if not attempted else "")))
    print(f"report: verify-{stamp}.json")
    if verdict == "GO" and not args.all:
        CURSOR.write_text(str(len(lines)), encoding="utf-8")
    return 0 if verdict == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
