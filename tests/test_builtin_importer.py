from __future__ import annotations

from io import BytesIO
import unittest

from PIL import Image, ImageDraw

import generate_tokens as approved
import import_builtin_image as builtin


def png_bytes(image: Image.Image) -> bytes:
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


class BuiltinCheckerboardDetectionTests(unittest.TestCase):
    def test_border_periodicity_catches_checker_hidden_from_global_histogram(self) -> None:
        size = 256
        tile = 12
        image = Image.new("RGB", (size, size))
        pixels = image.load()
        for y in range(size):
            for x in range(size):
                value = 246 if (x // tile + y // tile) % 2 == 0 else 230
                pixels[x, y] = (value, value, value)
        ImageDraw.Draw(image).rectangle((16, 16, 239, 239), fill=(60, 45, 35))

        self.assertFalse(
            approved.background_metrics(image)["checkerboard_baked"],
            "the fixture must exercise the importer border fallback",
        )
        observation = builtin.inspect_builtin_png("JOB-CHECKER", png_bytes(image))

        self.assertTrue(observation.observation.checkerboard_baked)
        image.close()

    def test_plain_solid_mattes_are_not_checkerboards(self) -> None:
        for colour in ((255, 255, 255), (238, 238, 238), (244, 241, 236)):
            with self.subTest(colour=colour):
                image = Image.new("RGB", (256, 256), colour)
                ImageDraw.Draw(image).ellipse((64, 48, 192, 208), fill=(65, 50, 40))

                observation = builtin.inspect_builtin_png("JOB-SOLID", png_bytes(image))

                self.assertFalse(observation.observation.checkerboard_baked)
                image.close()

    def test_one_direction_stripes_are_not_checkerboards(self) -> None:
        image = Image.new("RGB", (256, 256), (246, 246, 246))
        draw = ImageDraw.Draw(image)
        for x in range(0, 256, 24):
            draw.rectangle((x + 12, 0, x + 23, 255), fill=(230, 230, 230))

        self.assertFalse(builtin._border_checkerboard_baked(image))
        image.close()


if __name__ == "__main__":
    unittest.main()
