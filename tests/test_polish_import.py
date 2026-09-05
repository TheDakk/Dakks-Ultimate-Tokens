"""The importer's shared-file copies, polish preamble hashing and per-row versioning."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generate_tokens as approved  # noqa: E402
import import_builtin_image as builtin  # noqa: E402


def make_row(root: Path, notes: str = "") -> approved.PreparedRow:
    master = root / "masters" / "races" / "dwarf.png"
    export = root / "art" / "races" / "dwarf.webp"
    return approved.PreparedRow(
        source={"notes": notes},
        job_id="JOB-0024",
        display_name="Dwarf",
        prompt="PROMPT",
        prompt_sha256=approved.sha256_bytes(b"PROMPT"),
        art_dir="races",
        build_filename="dwarf.webp",
        export_px=400,
        master_px=1024,
        master_path=master,
        export_path=export,
        master_rel="masters/races/dwarf.png",
        export_rel="art/races/dwarf.webp",
        note="",
    )


class SharedFileCopyTests(unittest.TestCase):
    def test_copy_directories_come_from_the_queue_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            row = make_row(root, notes=(
                "also drop a copy at C:/Projects/FoundryVTT/DakksUltimateTokens/art/creatures/dwarf.webp "
                "\u2014 the 'creatures' pack resolves art from its own directory; playable race"
            ))
            paths = builtin.extra_export_paths(root, row)
            self.assertEqual(paths, [root / "art" / "creatures" / "dwarf.webp"])

    def test_rows_without_the_note_have_no_copies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            self.assertEqual(builtin.extra_export_paths(root, make_row(root, "playable race")), [])

    def test_copies_are_written_only_when_missing_or_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            row = make_row(root, notes="also drop a copy at /lib/art/creatures/dwarf.webp \u2014 x")
            row.export_path.parent.mkdir(parents=True)
            row.export_path.write_bytes(b"WEBP-1")
            copy = root / "art" / "creatures" / "dwarf.webp"
            self.assertEqual(builtin.write_export_copies(root, row), [copy])
            self.assertEqual(copy.read_bytes(), b"WEBP-1")
            self.assertEqual(builtin.write_export_copies(root, row), [])
            row.export_path.write_bytes(b"WEBP-2")
            self.assertEqual(builtin.write_export_copies(root, row), [copy])
            self.assertEqual(copy.read_bytes(), b"WEBP-2")


class PolishPromptTests(unittest.TestCase):
    def test_polish_prompt_is_preamble_blank_line_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / builtin.POLISH_PREAMBLE_FILE).write_bytes(b"POLISH PASS. Keep it.")
            full, full_hash, pre_hash = builtin.polish_prompt(root, make_row(root))
            self.assertEqual(full, "POLISH PASS. Keep it.\n\nPROMPT")
            self.assertEqual(full_hash, approved.sha256_bytes(full.encode("utf-8")))
            self.assertEqual(pre_hash, approved.sha256_bytes(b"POLISH PASS. Keep it."))

    def test_repo_preamble_matches_the_pilot_hash(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(
            approved.sha256_bytes(builtin.polish_preamble(root).encode("utf-8")),
            "46b18afd0760d0e286b1cf506bfa1fc7bb0801409986a664d3efb6ea07c514cf",
        )

    def test_a_preamble_with_a_trailing_newline_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / builtin.POLISH_PREAMBLE_FILE).write_bytes(b"POLISH PASS.\n")
            with self.assertRaises(approved.GeneratorError):
                builtin.polish_preamble(root)


class VersionRecordTests(unittest.TestCase):
    def test_versions_round_trip_and_absent_means_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "art").mkdir()
            self.assertEqual(builtin.load_versions(root), {})
            builtin.save_versions(root, {"creatures/black-dragon": 2})
            self.assertEqual(builtin.load_versions(root), {"creatures/black-dragon": 2})
            body = json.loads(builtin.versions_path(root).read_text(encoding="utf-8"))
            self.assertIn("_format", body)

    def test_a_version_below_two_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "art").mkdir()
            builtin.versions_path(root).write_text(json.dumps({"creatures/orc": 1}), encoding="utf-8")
            with self.assertRaises(approved.GeneratorError):
                builtin.load_versions(root)

    def test_retire_never_overwrites_and_keeps_the_stem(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            row = make_row(root)
            row.master_path.parent.mkdir(parents=True)
            row.master_path.write_bytes(b"v1")
            first = builtin.retire(root, row, row.master_path, "polish-v1")
            self.assertTrue(first.name.startswith("dwarf-") and first.name.endswith("-polish-v1.png"))
            self.assertEqual(first.parent, root / "_superseded" / "races")
            self.assertFalse(row.master_path.exists())
            row.master_path.write_bytes(b"v1-again")
            second = builtin.retire(root, row, row.master_path, "polish-v1")
            self.assertNotEqual(first, second)
            self.assertEqual(first.read_bytes(), b"v1")
            self.assertEqual(second.read_bytes(), b"v1-again")
            self.assertIsNone(builtin.retire(root, row, row.master_path, "polish-v1"))


if __name__ == "__main__":
    unittest.main()
