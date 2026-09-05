from __future__ import annotations

import base64
from contextlib import redirect_stdout
import csv
from io import BytesIO, StringIO
import json
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import Mock, patch

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[1]

import generate_tokens as standalone


def png_bytes(image: Image.Image) -> bytes:
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


class FakeAPIError(Exception):
    def __init__(
        self,
        status: int,
        message: str,
        *,
        code: str = "",
        error_type: str = "invalid_request_error",
        param: str = "",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status
        self.body = {
            "error": {
                "message": message,
                "code": code,
                "type": error_type,
                "param": param,
            }
        }
        self.request_id = "req-error"
        self.response = SimpleNamespace(headers=headers or {})


def raw_image_response(data: bytes) -> SimpleNamespace:
    encoded = base64.b64encode(data).decode("ascii")
    return SimpleNamespace(
        headers={"x-request-id": "req-test"},
        parse=lambda: SimpleNamespace(
            data=[SimpleNamespace(b64_json=encoded, revised_prompt=None)]
        ),
    )


class QueueAndGateTests(unittest.TestCase):
    def test_gate_one_resolves_the_exact_eight_rows(self) -> None:
        rows, _ = standalone.read_queue(
            PROJECT_ROOT / "upload" / "ASSETS-universal.csv"
        )

        selected = standalone.select_gate(rows, 1)

        self.assertEqual(
            [row["job_id"] for row in selected],
            [
                "JOB-0001",
                "JOB-0007",
                "JOB-0012",
                "JOB-0431",
                "JOB-0103",
                "JOB-0124",
                "JOB-0440",
                "JOB-0441",
            ],
        )

    def test_csv_reader_preserves_quoted_multiline_prompt_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "queue.csv"
            headers = sorted(standalone.REQUIRED_HEADERS)
            row = {header: "value" for header in headers}
            row["resolved_prompt"] = "first line\r\nsecond line\nthird line"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\r\n")
                writer.writeheader()
                writer.writerow(row)

            parsed, _ = standalone.read_queue(path)

            self.assertEqual(parsed[0]["resolved_prompt"], row["resolved_prompt"])

    def test_gate_one_dry_run_prints_plan_without_sdk_or_writes(self) -> None:
        queue = PROJECT_ROOT / "upload" / "ASSETS-universal.csv"
        reference = PROJECT_ROOT / "upload" / "generic-sheet-01.png"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = StringIO()
            with patch.object(
                standalone,
                "OpenAIImageEditor",
                side_effect=AssertionError("dry run must not create an API client"),
            ), redirect_stdout(output):
                result = standalone.main(
                    [
                        "--gate",
                        "1",
                        "--root",
                        str(root),
                        "--queue",
                        str(queue),
                        "--reference",
                        str(reference),
                    ]
                )

            lines = output.getvalue().splitlines()
            self.assertEqual(result, 0)
            self.assertEqual(lines[0], standalone.HANDSHAKE)
            self.assertEqual(lines[1], "MODEL gpt-image-2")
            self.assertEqual(lines[2], "Gate 1: 8 row(s)")
            self.assertEqual(lines[-1], "DRY RUN: no image calls or output files were created.")
            self.assertEqual(len(lines), 12)
            self.assertEqual(list(root.rglob("*")), [])


class OfficialSdkRequestTests(unittest.TestCase):
    def test_images_edit_receives_the_contract_parameters_and_exact_prompt(self) -> None:
        image_bytes = b"exact decoded response bytes"
        raw_response = raw_image_response(image_bytes)
        prompt = "line one\nline two — unchanged"
        captured: dict[str, object] = {}

        def fake_edit(**kwargs: object) -> object:
            captured.update(kwargs)
            image_file = kwargs["image"]
            self.assertEqual(image_file.read(), b"reference")
            return raw_response

        with tempfile.TemporaryDirectory() as temporary:
            reference = Path(temporary) / "reference.png"
            reference.write_bytes(b"reference")
            editor = standalone.OpenAIImageEditor("test-key", max_attempts=1)
            with patch.object(
                editor.client.images.with_raw_response,
                "edit",
                side_effect=fake_edit,
            ):
                response = editor.edit_one(reference_path=reference, prompt=prompt)

        self.assertEqual(response.png_bytes, image_bytes)
        self.assertEqual(response.request_id, "req-test")
        self.assertEqual(captured["model"], "gpt-image-2")
        self.assertEqual(captured["prompt"], prompt)
        self.assertEqual(captured["n"], 1)
        self.assertEqual(captured["size"], "1024x1024")
        self.assertEqual(captured["quality"], "high")
        self.assertEqual(captured["background"], "transparent")
        self.assertEqual(captured["output_format"], "png")
        self.assertNotIn("response_format", captured)
        self.assertEqual(captured["extra_body"], {"moderation": "low"})

    def test_unknown_moderation_parameter_retries_once_and_then_stays_omitted(self) -> None:
        calls: list[dict[str, object]] = []

        def fake_edit(**kwargs: object) -> object:
            calls.append(dict(kwargs))
            if len(calls) == 1:
                raise FakeAPIError(
                    400,
                    "Unknown parameter: 'moderation'.",
                    code="unknown_parameter",
                    param="moderation",
                )
            return raw_image_response(b"response")

        with tempfile.TemporaryDirectory() as temporary:
            reference = Path(temporary) / "reference.png"
            reference.write_bytes(b"reference")
            editor = standalone.OpenAIImageEditor("test-key", max_attempts=1)
            with patch.object(
                editor.client.images.with_raw_response,
                "edit",
                side_effect=fake_edit,
            ), patch.object(standalone.time, "sleep") as sleeper:
                first = editor.edit_one(reference_path=reference, prompt="exact")
                second = editor.edit_one(reference_path=reference, prompt="exact again")

        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0]["extra_body"], {"moderation": "low"})
        self.assertNotIn("extra_body", calls[1])
        self.assertNotIn("extra_body", calls[2])
        self.assertNotIn("response_format", calls[1])
        self.assertEqual(first.attempts, 2)
        self.assertEqual(second.attempts, 1)
        self.assertEqual(first.moderation_note, standalone.MODERATION_FALLBACK_NOTE)
        self.assertEqual(second.moderation_note, standalone.MODERATION_FALLBACK_NOTE)
        sleeper.assert_not_called()

    def test_unrelated_400_is_fatal_and_does_not_drop_moderation(self) -> None:
        error = FakeAPIError(400, "Invalid size value", code="invalid_value", param="size")
        with tempfile.TemporaryDirectory() as temporary:
            reference = Path(temporary) / "reference.png"
            reference.write_bytes(b"reference")
            editor = standalone.OpenAIImageEditor("test-key", max_attempts=4)
            with patch.object(
                editor.client.images.with_raw_response,
                "edit",
                side_effect=error,
            ) as request:
                with self.assertRaises(standalone.APIRequestFailure) as caught:
                    editor.edit_one(reference_path=reference, prompt="exact")

        self.assertTrue(caught.exception.fatal)
        self.assertEqual(caught.exception.attempts, 1)
        self.assertEqual(caught.exception.moderation_note, "")
        self.assertEqual(request.call_count, 1)

    def test_retry_after_is_honoured_and_capped_at_ninety_seconds(self) -> None:
        cases = (("17", [17.0]), ("999", [30.0, 30.0, 30.0]))
        for retry_after, expected_sleeps in cases:
            with self.subTest(retry_after=retry_after):
                error = FakeAPIError(
                    429,
                    "Rate limit",
                    code="rate_limit_exceeded",
                    headers={"Retry-After": retry_after},
                )
                with tempfile.TemporaryDirectory() as temporary:
                    reference = Path(temporary) / "reference.png"
                    reference.write_bytes(b"reference")
                    editor = standalone.OpenAIImageEditor("test-key", max_attempts=2)
                    with patch.object(
                        editor.client.images.with_raw_response,
                        "edit",
                        side_effect=[error, raw_image_response(b"response")],
                    ), patch.object(standalone.time, "sleep") as sleeper:
                        response = editor.edit_one(reference_path=reference, prompt="exact")

                self.assertEqual(response.attempts, 2)
                self.assertEqual(
                    [call.args[0] for call in sleeper.call_args_list],
                    expected_sleeps,
                )

    def test_429_and_400_fatal_classification(self) -> None:
        ordinary_429 = FakeAPIError(429, "Rate limit", code="rate_limit_exceeded")
        quota_429 = FakeAPIError(429, "Quota exhausted", code="insufficient_quota")
        ordinary_400 = FakeAPIError(400, "Bad request", code="invalid_value")
        invalid_moderation_value = FakeAPIError(
            400,
            "Invalid value for moderation",
            code="invalid_value",
            param="moderation",
        )

        self.assertFalse(standalone.is_fatal_api_error(ordinary_429, refused=False))
        self.assertTrue(standalone.is_fatal_api_error(quota_429, refused=False))
        self.assertFalse(standalone.is_transient_api_error(quota_429))
        self.assertTrue(standalone.is_fatal_api_error(ordinary_400, refused=False))
        self.assertFalse(standalone.is_fatal_api_error(ordinary_400, refused=True))
        self.assertFalse(standalone.is_unknown_moderation_parameter(invalid_moderation_value))


class ExecuteGateTests(unittest.TestCase):
    def prepared_row(self, root: Path) -> standalone.PreparedRow:
        prompt = "exact prompt"
        return standalone.PreparedRow(
            source={"layout_profile": "standing-figure"},
            job_id="JOB-TEST",
            display_name="Opaque Test",
            prompt=prompt,
            prompt_sha256=standalone.sha256_bytes(prompt.encode("utf-8")),
            art_dir="tests",
            build_filename="opaque.webp",
            export_px=32,
            master_px=1536,
            master_path=root / "masters" / "tests" / "opaque.png",
            export_path=root / "art" / "tests" / "opaque.webp",
            master_rel="masters/tests/opaque.png",
            export_rel="art/tests/opaque.webp",
            note="master below spec: 1024",
        )

    def test_model_preflight_precedes_edit_and_opaque_master_is_kept_without_export(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            row = self.prepared_row(root)
            opaque = Image.new("RGBA", (1024, 1024), (255, 255, 255, 255))
            response_bytes = png_bytes(opaque)
            opaque.close()
            events: list[str] = []

            model_result = SimpleNamespace(id="gpt-image-2", object="model")
            models = SimpleNamespace(
                retrieve=Mock(
                    side_effect=lambda model: events.append(f"model:{model}") or model_result
                )
            )

            class FakeEditor:
                moderation_note = ""

                def __init__(self) -> None:
                    self.client = SimpleNamespace(models=models)

                def edit_one(self, *, reference_path: Path, prompt: str) -> object:
                    events.append("edit")
                    return standalone.ImageResponse(
                        response_bytes,
                        "req-test",
                        1,
                        "",
                        "",
                    )

            fake_editor = FakeEditor()
            queue = PROJECT_ROOT / "upload" / "ASSETS-universal.csv"
            reference = PROJECT_ROOT / "upload" / "generic-sheet-01.png"
            queue_hash = standalone.sha256_file(queue)
            stdout = StringIO()

            with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), patch.object(
                standalone,
                "OpenAIImageEditor",
                return_value=fake_editor,
            ), redirect_stdout(stdout):
                result = standalone.execute_gate(
                    root=root,
                    gate=1,
                    rows=[row],
                    queue_path=queue,
                    queue_hash=queue_hash,
                    reference_path=reference,
                    max_attempts=1,
                )

            self.assertEqual(result, 1)
            self.assertEqual(events, ["model:gpt-image-2", "edit"])
            self.assertIn("MODEL_RETRIEVE", stdout.getvalue())
            self.assertEqual(row.master_path.read_bytes(), response_bytes)
            self.assertFalse(row.export_path.exists())
            results_path = next(root.glob("results-*.jsonl"))
            records = [json.loads(line) for line in results_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(records), 1)
            record = records[0]
            self.assertEqual(record["status"], "error")
            self.assertEqual(record["master_sha256"], standalone.sha256_bytes(response_bytes))
            self.assertEqual(record["export_sha256"], "")
            self.assertIn("master kept; export not written", record["note"])
            self.assertIn("transparent_background=no", record["note"])
            self.assertIn("checkerboard_baked=no", record["note"])

    def test_model_preflight_failure_stops_before_image_or_result_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            row = self.prepared_row(root)
            edit_one = Mock()
            fake_editor = SimpleNamespace(
                client=SimpleNamespace(
                    models=SimpleNamespace(
                        retrieve=Mock(
                            side_effect=FakeAPIError(
                                404,
                                "Model not found",
                                code="model_not_found",
                            )
                        )
                    )
                ),
                edit_one=edit_one,
                moderation_note="",
            )
            queue = PROJECT_ROOT / "upload" / "ASSETS-universal.csv"
            reference = PROJECT_ROOT / "upload" / "generic-sheet-01.png"

            with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), patch.object(
                standalone,
                "OpenAIImageEditor",
                return_value=fake_editor,
            ):
                with self.assertRaisesRegex(standalone.GeneratorError, "model preflight failed"):
                    standalone.execute_gate(
                        root=root,
                        gate=1,
                        rows=[row],
                        queue_path=queue,
                        queue_hash=standalone.sha256_file(queue),
                        reference_path=reference,
                        max_attempts=1,
                    )

            edit_one.assert_not_called()
            self.assertEqual(list(root.rglob("*")), [])


class ImageIntegrityTests(unittest.TestCase):
    def test_transparency_and_checkerboard_inspection(self) -> None:
        transparent = Image.new("RGBA", (1024, 1024), (238, 238, 238, 0))
        transparent_draw = ImageDraw.Draw(transparent)
        transparent_draw.rectangle((300, 300, 724, 724), fill=(120, 20, 20, 255))
        transparent_observation = standalone.inspect_png_bytes(
            "JOB-TEST", png_bytes(transparent)
        )
        transparent.close()

        checkerboard = Image.new("RGBA", (1024, 1024), (238, 238, 238, 255))
        checker_draw = ImageDraw.Draw(checkerboard)
        block = 64
        for y in range(0, 1024, block):
            for x in range(0, 1024, block):
                colour = (
                    (205, 205, 205, 255)
                    if (x // block + y // block) % 2
                    else (238, 238, 238, 255)
                )
                checker_draw.rectangle((x, y, x + block - 1, y + block - 1), fill=colour)
        checker_observation = standalone.inspect_png_bytes(
            "JOB-CHECKER", png_bytes(checkerboard)
        )
        checkerboard.close()

        self.assertTrue(transparent_observation.has_alpha_channel)
        self.assertTrue(transparent_observation.transparent_background)
        self.assertFalse(transparent_observation.checkerboard_baked)
        self.assertFalse(checker_observation.transparent_background)
        self.assertTrue(checker_observation.checkerboard_baked)

    def test_master_bytes_and_premultiplied_webp_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            master = root / "masters" / "subject.png"
            export = root / "art" / "subject.webp"
            source = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
            ImageDraw.Draw(source).rectangle((16, 16, 47, 47), fill=(255, 0, 0, 255))
            source_bytes = png_bytes(source)
            source.close()

            standalone.atomic_write_bytes(master, source_bytes)
            standalone.export_webp_premultiplied(master, export, 37)

            self.assertEqual(master.read_bytes(), source_bytes)
            self.assertEqual(standalone.sha256_file(master), standalone.sha256_bytes(source_bytes))
            with Image.open(export) as verified:
                verified.load()
                self.assertEqual(verified.format, "WEBP")
                self.assertEqual(verified.size, (37, 37))
                self.assertIn("A", verified.getbands())
                with verified.convert("RGBA") as rgba:
                    self.assertLess(rgba.getchannel("A").getextrema()[0], 255)


if __name__ == "__main__":
    unittest.main()
