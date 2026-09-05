"""The keyer's four guarantees, each checked on a synthetic capture where the truth is known."""

from __future__ import annotations

import sys
import unittest
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chroma_key  # noqa: E402


def capture(size=256, subject=(40, 90, 60), soft=True) -> Image.Image:
    """A dark-green disc on pure magenta, with an anti-aliased edge if soft."""
    scale = 4 if soft else 1
    big = Image.new("RGB", (size * scale, size * scale), chroma_key.KEY)
    d = ImageDraw.Draw(big)
    r = size * scale * 0.3
    c = size * scale / 2
    d.ellipse((c - r, c - r, c + r, c + r), fill=subject)
    return big.resize((size, size), Image.Resampling.LANCZOS) if soft else big


class ChromaKeyTests(unittest.TestCase):
    def test_background_becomes_fully_transparent_and_subject_stays_opaque(self):
        out = chroma_key.key_image(capture())
        a = out.getchannel("A")
        self.assertEqual(a.getpixel((3, 3)), 0, "corner must be fully clear")
        self.assertEqual(a.getpixel((128, 128)), 255, "centre must be fully opaque")
        self.assertEqual(out.getpixel((128, 128))[:3], (40, 90, 60), "subject colour untouched")

    def test_edge_is_soft_not_aliased(self):
        out = chroma_key.key_image(capture())
        hist = out.getchannel("A").histogram()
        partial = sum(hist[1:255])
        # a supersampled disc has ~2*pi*r edge pixels; a good share must be partial
        self.assertGreater(partial, 100, "an anti-aliased outline must produce partial alpha")

    def test_no_magenta_fringe_after_despill(self):
        out = chroma_key.key_image(capture())
        a = out.getchannel("A")
        # every partially transparent pixel must not lean magenta: red and blue must not
        # both exceed green by a wide margin once the key's share is removed
        fringe = 0
        for x in range(128, 256):
            v = a.getpixel((x, 128))
            if 0 < v < 255:
                r, g, b, _ = out.getpixel((x, 128))
                if r > g + 60 and b > g + 60:
                    fringe += 1
        self.assertEqual(fringe, 0, "despill must remove the magenta cast from edge pixels")

    def test_pink_highlight_inside_subject_is_not_a_hole(self):
        im = capture(soft=False)
        d = ImageDraw.Draw(im)
        d.ellipse((120, 120, 136, 136), fill=(230, 120, 220))   # near-magenta highlight, well inside
        out = chroma_key.key_image(im)
        self.assertEqual(out.getchannel("A").getpixel((128, 128)), 255, "interior pink must stay opaque")

    def test_enclosed_pure_key_region_stays_transparent(self):
        im = capture(soft=False)
        d = ImageDraw.Draw(im)
        d.ellipse((112, 112, 144, 144), fill=chroma_key.KEY)      # a hole through the subject
        out = chroma_key.key_image(im)
        self.assertEqual(out.getchannel("A").getpixel((128, 128)), 0, "a real gap must stay clear")

    def test_non_magenta_background_is_refused(self):
        im = Image.new("RGB", (128, 128), (254, 254, 254))
        ImageDraw.Draw(im).ellipse((40, 40, 88, 88), fill=(30, 30, 30))
        with self.assertRaises(chroma_key.KeyingError):
            chroma_key.key_image(im)

    def test_already_transparent_input_passes_through(self):
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((40, 40, 88, 88), fill=(30, 30, 30, 255))
        buf = BytesIO(); im.save(buf, format="PNG")
        out, note = chroma_key.key_png_if_needed(buf.getvalue())
        self.assertEqual(out, buf.getvalue())
        self.assertIn("already transparent", note)

    def test_png_roundtrip_reports_transparent_fraction(self):
        buf = BytesIO(); capture().save(buf, format="PNG")
        out, note = chroma_key.key_png_if_needed(buf.getvalue())
        with Image.open(BytesIO(out)) as keyed:
            self.assertEqual(keyed.mode, "RGBA")
        self.assertIn("key=magenta", note)


if __name__ == "__main__":
    unittest.main()
