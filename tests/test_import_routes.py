"""End-to-end importer routes on an isolated fixture: first import, polish, revise, a row
emptied by review, and rejected inputs that must leave the library untouched."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image, ImageDraw  # noqa: E402

import generate_tokens as approved  # noqa: E402
import import_builtin_image as builtin  # noqa: E402


def magenta_capture(size: int = 256, colour=(70, 50, 40)) -> bytes:
    """A subject on the flat magenta key, as the generator returns it."""
    im = Image.new("RGB", (size, size), (255, 0, 255))
    d = ImageDraw.Draw(im)
    d.ellipse((size // 4, size // 5, size * 3 // 4, size * 4 // 5), fill=colour)
    d.rectangle((size // 2 - 10, size * 4 // 5 - 4, size // 2 + 10, size * 9 // 10), fill=colour)
    buf = BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue()


class Fixture:
    """A throwaway library root with one queue row and the files a route needs."""

    def __init__(self, tmp: str):
        self.root = Path(tmp).resolve()
        (self.root / "upload").mkdir()
        (self.root / "art").mkdir()
        (self.root / "masters").mkdir()
        (self.root / builtin.POLISH_PREAMBLE_FILE).write_bytes(b"POLISH PASS. Keep the design.")
        self.queue = self.root / "upload" / "ASSETS-universal.csv"
        self.queue.write_bytes(b"queue")
        self.reference = self.root / "upload" / "generic-sheet-01.png"
        self.reference.write_bytes(b"ref")
        self.row = approved.PreparedRow(
            source={"notes": ""}, job_id="JOB-0777", display_name="Test Beast", prompt="PROMPT",
            prompt_sha256=approved.sha256_bytes(b"PROMPT"), art_dir="creatures", build_filename="test-beast.webp",
            export_px=100, master_px=256,
            master_path=self.root / "masters" / "creatures" / "test-beast.png",
            export_path=self.root / "art" / "creatures" / "test-beast.webp",
            master_rel="masters/creatures/test-beast.png", export_rel="art/creatures/test-beast.webp", note="",
        )
        self.context = builtin.GateContext(self.root, self.queue, approved.sha256_file(self.queue), self.reference, self.row)

    def capture(self, name: str, **kw) -> Path:
        p = self.root / name
        p.write_bytes(magenta_capture(**kw))
        return p

    def ledger(self) -> list[dict]:
        out = []
        for f in sorted(self.root.glob("results-*.jsonl")):
            out += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        return out


def run(fx: Fixture, fn, *a, **kw):
    """verify_sources compares hashes of the real queue/reference; here they are stubs."""
    with mock.patch.object(approved, "verify_sources", lambda *args, **kwargs: None):
        return fn(fx.context, *a, **kw)


class ImportRouteTests(unittest.TestCase):
    def test_first_import_then_polish_then_revise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            # first import: files appear, version stays 1 (absent)
            rc = run(fx, builtin.import_png, fx.capture("a.png"), fx.row.prompt_sha256)
            self.assertEqual(rc, 0)
            self.assertTrue(fx.row.master_path.exists() and fx.row.export_path.exists())
            self.assertTrue(builtin.capture_path_for(fx.root, fx.row).exists())
            self.assertEqual(builtin.load_versions(fx.root), {})
            master_v1 = fx.row.master_path.read_bytes()
            # polish: needs the polish hash, retires v1, records v2
            _, polish_hash, _ = builtin.polish_prompt(fx.root, fx.row)
            rc = run(fx, builtin.import_png, fx.capture("b.png", colour=(90, 60, 40)), polish_hash, polish=True)
            self.assertEqual(rc, 0)
            self.assertEqual(builtin.load_versions(fx.root), {"creatures/test-beast": 2})
            retired = builtin.retired_set(fx.root, fx.row, 1)
            self.assertEqual(sorted(retired), ["capture", "export", "master"])
            self.assertEqual(retired["master"].read_bytes(), master_v1)
            self.assertTrue(retired["capture"].name.endswith("-polish-v1-capture.png"))
            self.assertNotEqual(fx.row.master_path.read_bytes(), master_v1)
            # revise: plain prompt hash, retires v2 under its reason, records v3
            rc = run(fx, builtin.import_png, fx.capture("c.png", colour=(40, 80, 60)), fx.row.prompt_sha256, revise="anatomy")
            self.assertEqual(rc, 0)
            self.assertEqual(builtin.load_versions(fx.root), {"creatures/test-beast": 3})
            retired2 = builtin.retired_set(fx.root, fx.row, 2)
            self.assertTrue(retired2["master"].name.endswith("-anatomy-v2.png"))
            notes = [r["note"] for r in fx.ledger() if r["status"] == "generated"]
            self.assertEqual(len(notes), 3)
            self.assertIn("polish v2", notes[1])
            self.assertIn("revise:anatomy v3", notes[2])

    def test_polish_and_revise_are_mutually_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            with self.assertRaises(approved.GeneratorError):
                run(fx, builtin.import_png, fx.capture("a.png"), fx.row.prompt_sha256, polish=True, revise="x")

    def test_revise_on_a_row_emptied_by_review_records_a_revision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            # the row's files are absent (retired earlier by the reviewer); a revise still works
            rc = run(fx, builtin.import_png, fx.capture("a.png"), fx.row.prompt_sha256, revise="legs")
            self.assertEqual(rc, 0)
            self.assertTrue(fx.row.export_path.exists())
            self.assertEqual(builtin.load_versions(fx.root), {"creatures/test-beast": 2})
            self.assertIn("row emptied by review", fx.ledger()[-1]["note"])

    def test_plain_import_never_overwrites_and_polish_needs_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            run(fx, builtin.import_png, fx.capture("a.png"), fx.row.prompt_sha256)
            before = fx.row.master_path.read_bytes()
            rc = run(fx, builtin.import_png, fx.capture("b.png", colour=(1, 2, 3)), fx.row.prompt_sha256)
            self.assertEqual(rc, 0)  # SKIP
            self.assertEqual(fx.row.master_path.read_bytes(), before)
            fx2 = Fixture(tempfile.mkdtemp())
            _, polish_hash, _ = builtin.polish_prompt(fx2.root, fx2.row)
            with self.assertRaises(approved.GeneratorError):
                run(fx2, builtin.import_png, fx2.capture("a.png"), polish_hash, polish=True)

    def test_rejected_revision_leaves_library_and_versions_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            run(fx, builtin.import_png, fx.capture("a.png"), fx.row.prompt_sha256)
            before = (fx.row.master_path.read_bytes(), fx.row.export_path.read_bytes(),
                      builtin.capture_path_for(fx.root, fx.row).read_bytes())
            # a capture that is not on the key: the keyer refuses
            bad = fx.root / "bad.png"
            im = Image.new("RGB", (256, 256), (255, 255, 255))
            ImageDraw.Draw(im).ellipse((60, 60, 190, 190), fill=(30, 30, 30))
            im.save(bad)
            rc = run(fx, builtin.import_png, bad, fx.row.prompt_sha256, revise="anatomy")
            self.assertEqual(rc, 1)
            after = (fx.row.master_path.read_bytes(), fx.row.export_path.read_bytes(),
                     builtin.capture_path_for(fx.root, fx.row).read_bytes())
            self.assertEqual(before, after)
            self.assertEqual(builtin.load_versions(fx.root), {})
            self.assertEqual(list((fx.root / "_superseded").rglob("*")) if (fx.root / "_superseded").exists() else [], [])
            self.assertEqual(fx.ledger()[-1]["status"], "error")

    def test_wrong_hash_is_refused_before_anything_is_written(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            with self.assertRaises(approved.GeneratorError):
                run(fx, builtin.import_png, fx.capture("a.png"), "0" * 64, revise="anatomy")
            self.assertFalse(fx.row.master_path.exists())

    def test_a_crash_inside_the_tool_lands_on_the_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            cap = fx.capture("a.png")
            with mock.patch.object(builtin, "load_gate_context", lambda root, job: fx.context), \
                 mock.patch.object(builtin, "import_png", side_effect=RuntimeError("boom")):
                rc = builtin.main(["import", "--root", str(fx.root), "--job", "JOB-0777", "--input", str(cap),
                                   "--sent-prompt-sha256", fx.row.prompt_sha256])
            self.assertEqual(rc, 3)
            last = fx.ledger()[-1]
            self.assertEqual(last["status"], "error")
            self.assertIn("RuntimeError: boom", last["error"])


if __name__ == "__main__":
    unittest.main()
