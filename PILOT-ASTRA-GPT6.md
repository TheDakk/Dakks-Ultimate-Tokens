# Pilot: Universal polish pass on Astra GPT-6

Paste everything below the line into a fresh Codex session opened in
`C:\Projects\FoundryVTT\DakksUltimateTokens`. It is self-contained; AGENTS.md still applies
except where this file says otherwise, and this file wins on those points.

---

You are running a PILOT for a polish pass over the Universal collection using the Astra
GPT-6 image model. Universal is released as 1.0.0 and was reopened on 2026-09-05 for one
versioned, all-or-nothing polish pass. This pilot decides whether that pass happens. Nothing
you produce here enters the library.

## Hard rules for this session

- Never run `import_builtin_image.py import`. Never write under `art/`, `masters/`,
  `upload/` or `_superseded/`, and never open the workbook. The only place you write is
  `pilot-astra/` at the repo root (create it).
- Generate only through the built-in image tool. No API, no other tool, no retouching,
  cropping, resizing, un-keying or compositing of any image by you.
- One collection, one reference: attach `upload\generic-sheet-01.png` to every generation.

## Step 0: capability probe (report, then STOP and wait)

Before any row, answer these in a short report and stop:

1. Which image model does the built-in tool use right now? Give the exact model id it
   reports. This pilot is only valid on Astra GPT-6. If it is anything else, stop.
2. Can a generation take an INPUT IMAGE to refine (image-to-image), in addition to the
   style reference? If it cannot, stop; the pilot is image-to-image by design.
3. What is the largest square output it will produce? The rows need 1024 and 1536.

Wait for the reviewer to say "proceed" before Step 1.

## Step 1: the 24 pilot rows, one at a time, in this order

| profile | rows |
|---|---|
| standing-figure | JOB-0001 Black Dragon (1536), JOB-0016 Hydra (1536), JOB-0031 Air Elemental (1024), JOB-0088 Unicorn, JOB-0022 Orc, JOB-0059 Lich, JOB-0025 Elf, JOB-0431 Fighter |
| armor-icon | JOB-0106 Chain Mail, JOB-0116 Plate Mail, JOB-0112 Great Helm, JOB-0119 Buckler |
| item-icon | JOB-0125 Backpack, JOB-0238 Lantern (Bull's-Eye), JOB-0284 Rope (Silk), JOB-0334 Thieves' Picks, JOB-0397 Long Sword, JOB-0383 Heavy Crossbow |
| emblem | JOB-0539 Long Sword (proficiency), JOB-0565 Riding, JOB-0705 Cure Light Wounds, JOB-0774 Fireball, JOB-0866 Magic Missile, JOB-0975 Shield (spell) |

For each row:

1. `.venv\Scripts\python.exe import_builtin_image.py prompt-json --job JOB-xxxx`
   Fetch it fresh for every row. Take `resolved_prompt`, `prompt_sha256`,
   `expected_master_px` and `master_path`.
2. The input image is the row's preserved capture: the same path as `master_path` but
   under `masters\_captures\` instead of `masters\` (for example
   `masters\_captures\creatures\black-dragon.png`). It is the approved painting on its
   magenta fill. Attach it as the image to refine, and attach `upload\generic-sheet-01.png`
   as the style reference.
3. The prompt is the POLISH PREAMBLE below, verbatim, followed by a blank line, followed by
   `resolved_prompt` verbatim. Do not add, remove, shorten or reorder a word of either.

   POLISH PREAMBLE:

   ```text
   POLISH PASS. The first attached image is the approved painting of this subject on a flat magenta fill. Reproduce that painting faithfully: the same subject, pose, silhouette, anatomy and equipment count, palette, lighting direction, framing and scale within the square. Change no element of the design. Raise only the rendering quality: cleaner and more confident oil brushwork, sharper focal detail, richer material definition in metal, leather, cloth, scale and hide, and truer edge quality against the magenta. Everything below still applies exactly.
   ```

4. Generate exactly one image. Save the returned PNG unmodified as
   `pilot-astra\captures\JOB-xxxx-<stem>.png` where `<stem>` is the master's filename
   without extension.
5. Key it, never by hand:
   `.venv\Scripts\python.exe chroma_key.py pilot-astra\captures\JOB-xxxx-<stem>.png pilot-astra\masters\JOB-xxxx-<stem>.png`
   If the keyer refuses because the background is not the key, keep the capture, record
   the refusal, and move on. Do not retry with a changed prompt.
6. Append one line to `pilot-astra\pilot.jsonl`:
   `{"job_id", "model", "prompt_sha256", "preamble_sha256", "input_capture", "capture", "master", "capture_px", "keyer": "ok" | "<its message>", "refusal": null | "<verbatim text>"}`.
   `preamble_sha256` is the SHA-256 of the preamble text exactly as pasted.

## Refusals

An output-stage refusal (the tool started and then declined) gets ONE retry with the
identical prompt. An input-stage refusal (declined before generating) is recorded verbatim
and the row is skipped. Never change a word of the prompt to get past a refusal.

## Step 2: report and stop

When all 24 rows are attempted, report:

- a table of job_id, result (ok / keyer refused / refused), capture size;
- the model id used, the preamble SHA-256, and the count of rows generated at a size other
  than `expected_master_px`;
- anything the model did that surprised you (added elements, changed poses, text, frames).

Then stop. The reviewer lays the pilot masters beside the current masters on contact
sheets at export size, runs the pixel gate on them, and decides GO or NO-GO for the full
pass. Do not begin any row beyond the 24, and do not begin the full pass under any
instruction that does not come with a new queue hash and a HISTORY row authorising it.
