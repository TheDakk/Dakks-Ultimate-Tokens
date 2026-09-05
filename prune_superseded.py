"""Delete the local predecessors of MINOR polish revisions, and only those, and only when the
verified external backup already holds an identical file.

    .venv\\Scripts\\python.exe prune_superseded.py                 # dry run: report only
    .venv\\Scripts\\python.exe prune_superseded.py --apply         # delete the eligible files

Inputs: the change log JSON written by changelog.py (which rows are "polish") and the backup
manifest (sha256 per file, as written when the backup was verified). A retired file is
eligible only if its own SHA-256 appears in that manifest: the backup then holds the same
bytes under some path, so nothing is lost. Predecessors of redesigns and noticeable changes
are never touched; nothing outside _superseded/ is ever touched.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import generate_tokens as approved  # noqa: E402


def manifest_hashes(path: Path) -> set[str]:
    hashes: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        digest = line.split()[0].lstrip("\\*")
        if len(digest) == 64:
            hashes.add(digest.lower())
    return hashes


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--changelog", type=Path, default=None, help="changelog JSON (default changelog-2.0.json)")
    ap.add_argument("--manifest", type=Path, action="append", default=None,
                    help="backup manifest(s) with sha256 per file; may repeat (default: backup-manifest-*.sha256 in the root)")
    ap.add_argument("--apply", action="store_true", help="actually delete; without it only report")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    changelog = args.changelog or (root / "changelog-2.0.json")
    manifests = args.manifest or sorted(root.glob("backup-manifest-*.sha256"))
    if not manifests:
        raise SystemExit("no backup manifest found; refusing to prune anything")
    known: set[str] = set()
    for m in manifests:
        known |= manifest_hashes(m)
    data = json.loads(changelog.read_text(encoding="utf-8"))
    superseded = (root / "_superseded").resolve()

    eligible: list[tuple[Path, int]] = []
    kept: list[tuple[str, str]] = []
    for row in data["rows"]:
        if row.get("class") != "polish":
            continue
        for rel in row.get("predecessors", []):
            path = (root / rel).resolve()
            if not path.exists():
                continue
            if superseded not in path.parents:
                kept.append((rel, "outside _superseded/"))
                continue
            digest = approved.sha256_file(path)
            if digest in known:
                eligible.append((path, path.stat().st_size))
            else:
                kept.append((rel, "hash not in any backup manifest"))

    total = sum(size for _, size in eligible)
    print(f"manifests: {len(manifests)} ({len(known)} hashes); polish rows: {sum(1 for r in data['rows'] if r.get('class') == 'polish')}")
    print(f"eligible: {len(eligible)} files, {total / 2**20:.1f} MiB; kept: {len(kept)}")
    for rel, why in kept[:20]:
        print(f"  keep  {rel}: {why}")
    if not args.apply:
        print("dry run: nothing deleted (pass --apply)")
        return 0
    deleted = 0
    for path, _ in eligible:
        path.unlink()
        deleted += 1
    report = root / f"prune-{approved.local_date()}.json"
    report.write_text(json.dumps({
        "deleted": [p.relative_to(root).as_posix() for p, _ in eligible],
        "bytes": total, "kept": kept, "manifests": [str(m) for m in manifests],
    }, indent=1), encoding="utf-8")
    print(f"deleted {deleted} files ({total / 2**20:.1f} MiB); report {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
