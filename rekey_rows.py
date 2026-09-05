"""Re-key masters from their preserved captures with the current keyer.

    python rekey_rows.py <retire-suffix> JOB-0001 JOB-0002 ...
    python rekey_rows.py <retire-suffix> --all-captured

Existing masters/exports are moved to _superseded/<dir>/<name>-<date>-<suffix>.<ext>
(the contract's rule for replacing a file); captures are never touched; one ledger line
per row records the re-key.
"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import generate_tokens as approved            # noqa: E402
import import_builtin_image as bridge         # noqa: E402
import chroma_key                             # noqa: E402

if len(sys.argv) < 3:
    print(__doc__); raise SystemExit(2)
suffix, *jobs = sys.argv[1:]
today = date.today().isoformat()
rows, _ = approved.read_queue(ROOT / "upload" / "ASSETS-universal.csv")
prepared = {r.job_id: r for r in approved.prepare_rows(ROOT, sorted(approved.production_index(rows).values(), key=approved.job_number))}
if jobs == ["--all-captured"]:
    jobs = [r.job_id for r in prepared.values()
            if (ROOT / "masters" / "_captures" / Path(*r.art_dir.split("/")) / f"{r.master_path.stem}.png").is_file()]
results_path = ROOT / f"results-{today}.jsonl"

done = 0
for job in jobs:
    row = prepared[job]
    capture = ROOT / "masters" / "_captures" / Path(*row.art_dir.split("/")) / f"{row.master_path.stem}.png"
    if not capture.is_file():
        print(f"SKIP {job}: no capture"); continue
    for current, ext in ((row.master_path, ".png"), (row.export_path, ".webp")):
        if current.exists():
            retired = ROOT / "_superseded" / Path(*row.art_dir.split("/")) / f"{current.stem}-{today}-{suffix}{ext}"
            retired.parent.mkdir(parents=True, exist_ok=True)
            current.replace(retired)
    keyed_bytes, key_note = chroma_key.key_png_if_needed(capture.read_bytes())
    observation = bridge.inspect_builtin_png(job, keyed_bytes).observation
    if not observation.transparent_background:
        print(f"ERROR {job}: still not transparent after re-key ({observation.corner_alphas}); nothing written"); continue
    approved.atomic_write_bytes(row.master_path, keyed_bytes)
    master_sha = approved.sha256_file(row.master_path)
    approved.export_webp_premultiplied(row.master_path, row.export_path, row.export_px)
    export_sha = approved.sha256_file(row.export_path)
    bridge.write_export_copies(ROOT, row)
    approved.append_result(results_path, approved.result_record(
        row, status="generated", model_id=bridge.BUILTIN_MODEL_ID,
        master_sha256=master_sha, export_sha256=export_sha, observation=observation,
        extra_note=approved.merge_notes(f"rekey from masters/_captures; previous files retired as -{suffix}", key_note)))
    done += 1
    print(f"OK {job}: {row.export_rel} | {key_note}")
print(f"re-keyed {done} of {len(jobs)}; ledger {results_path}")
