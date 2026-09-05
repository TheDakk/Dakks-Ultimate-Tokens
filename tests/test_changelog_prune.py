"""Change-magnitude classification, retired-set lookup for revise suffixes, prune eligibility."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image  # noqa: E402

import changelog  # noqa: E402
import import_builtin_image as builtin  # noqa: E402
import prune_superseded as prune  # noqa: E402
from test_polish_import import make_row  # noqa: E402


class ClassifyTests(unittest.TestCase):
    def test_a_revise_is_always_a_redesign(self) -> None:
        self.assertEqual(changelog.classify("redesign", 0.1, 1.0, 12, 0.05), "redesign")

    def test_small_polish_deltas_are_polish_and_large_ones_change(self) -> None:
        self.assertEqual(changelog.classify("polish", 3.5, 1.01, 12, 0.05), "polish")
        self.assertEqual(changelog.classify("polish", 14.0, 1.0, 12, 0.05), "change")
        self.assertEqual(changelog.classify("polish", 2.0, 1.06, 12, 0.05), "change")

    def test_an_unmeasurable_polish_is_never_called_minor(self) -> None:
        self.assertEqual(changelog.classify("polish", None, None, 12, 0.05), "change")

    def test_measure_reports_zero_for_identical_images(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            for x in range(16, 48):
                for y in range(16, 48):
                    im.putpixel((x, y), (200, 100, 50, 255))
            a, b = Path(tmp) / "a.png", Path(tmp) / "b.png"
            im.save(a)
            im.save(b)
            mad, scale = changelog.measure(a, b)
            self.assertEqual(mad, 0.0)
            self.assertEqual(scale, 1.0)


class RetiredSetRevise(unittest.TestCase):
    def test_a_revise_suffix_is_found_like_a_polish_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            row = make_row(root)
            folder = root / "_superseded" / "races"
            folder.mkdir(parents=True)
            Image.new("RGB", (8, 8)).save(folder / "dwarf-2026-09-06-legs-v1-capture.png")
            Image.new("RGBA", (8, 8)).save(folder / "dwarf-2026-09-06-legs-v1.png")
            (folder / "dwarf-2026-09-06-legs-v1.webp").write_bytes(b"w")
            found = builtin.retired_set(root, row, 1)
            self.assertEqual(sorted(found), ["capture", "export", "master"])


class PruneTests(unittest.TestCase):
    def test_manifest_hashes_parse_both_sha256sum_layouts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            m = Path(tmp) / "m.sha256"
            m.write_text("a" * 64 + "  masters/x.png\n" + "b" * 64 + " *art/y.webp\n\nnot a hash line\n", encoding="utf-8")
            self.assertEqual(prune.manifest_hashes(m), {"a" * 64, "b" * 64})


if __name__ == "__main__":
    unittest.main()
