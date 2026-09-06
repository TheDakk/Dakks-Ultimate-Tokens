# Universal 2.0: one pass over every row

Paste everything below the line into a Codex session opened in
`C:\Projects\FoundryVTT\DakksUltimateTokens`. AGENTS.md applies in full. When a session runs
long, open a new one and paste the same text again: the importer knows which rows are done.
Authorised by HIST-0039 and PLAN-UNIVERSAL-2.0.md; `pass-manifest.json` is the row manifest.

---

You are running Universal 2.0: every one of the 1,408 rows is revised with the new model,
in job order, JOB-0001 to JOB-1408. 107 rows get a FRESH generation on a corrected brief
(their previous painting had the wrong body plan, object or icon); the other 1,301 are
polished image-to-image with the design preserved. You do not decide which is which: the
importer tells you per row.

## Hard rules for this session

- Generate only through the built-in image tool. No retouching, cropping, resizing,
  keying, un-keying or compositing by you. Attach `upload\generic-sheet-01.png` on every
  generation.
- Never write under `art/`, `masters/`, `_superseded/` or `upload/` yourself; never open the
  workbook; never edit `art/versions.json`, `pass-manifest.json` or `POLISH-PREAMBLE.txt`.
  Your only writes are the PNGs you save before importing.
- Never change a word of a prompt. Never combine `--polish` and `--revise`.

## Per row, JOB-0001 to JOB-1408 in order

1. `.venv\Scripts\python.exe import_builtin_image.py prompt-json --job JOB-xxxx`
   Fetch it fresh for every row. Read `done_in_pass` and `route`.
   - `done_in_pass: true` means this row was already revised in this pass (an earlier
     session). Skip it and move to the next job id.
   - `route: "revise"` with `revise_reason`: a fresh generation. Use `resolved_prompt` and
     `prompt_sha256`. Attach ONLY the style sheet. Do NOT attach the previous painting.
   - `route: "polish"`: an image-to-image revision. Use `polish_prompt` and
     `polish_sha256`. Attach `input_capture` FIRST and the style sheet SECOND.
2. Generate exactly one image from the prompt, verbatim. Save the returned PNG unmodified.
3. Import with the flag that matches the route:
   - revise: `.venv\Scripts\python.exe import_builtin_image.py import --revise <revise_reason> --job JOB-xxxx --input <that.png> --sent-prompt-sha256 <prompt_sha256> --model "<model id the tool reports, or: unreported (Codex built-in)>"`
   - polish: `.venv\Scripts\python.exe import_builtin_image.py import --polish --job JOB-xxxx --input <that.png> --sent-prompt-sha256 <polish_sha256> --model "<same>"`
   The importer keys and checks the image and only then retires the current capture,
   master and export to `_superseded\`, writes the new files under the unchanged names,
   refreshes shared copies and records the new version. Keep its OK / ERROR / VERSION lines.
   An ERROR leaves the library untouched: report it and move on to the next row.

## Refusals

An output-stage refusal (the tool started and then declined) gets ONE retry with the
identical prompt and inputs. An input-stage refusal is recorded and the row is skipped:
`record-refusal --job JOB-xxxx --sent-prompt-sha256 <hash you sent> --error-base64 <base64 of the exact error>`
with `--polish` added when the route was polish. Never reword a prompt to get past a refusal.

## Checkpoints

After every 200 rows attempted, and at the end, run

    .venv\Scripts\python.exe verify_gate.py

- `GO`: continue with the next row without waiting for anyone.
- `STOP`: stop immediately and report its full output verbatim. Do not fix, re-key,
  retouch, regenerate or delete anything. The reviewer decides.

If the importer ever reports that the queue, the reference or the pass manifest changed,
stop and report.

Queue SHA-256: `b18e8eef09afb136f3018208110860781e7e1cc2dec038ab1c6338f55c74164b`.
Reference SHA-256: `2b0c44d077d651709fcacc8845c25417815d2df882af4aeeb2fda092cf3554b9`.
Preamble SHA-256: `46b18afd0760d0e286b1cf506bfa1fc7bb0801409986a664d3efb6ea07c514cf`.
Handshake (JOB-0001): `Black Dragon · black-dragon.webp · 1200 · 4e161de44abf`.

## Reporting

At each checkpoint and at the end of a session, report: the range of job ids attempted,
every ERROR and REFUSED line verbatim, the count of OK lines by route (revise / polish), the
verifier's verdict and report filename, the model id used, and anything the tool did that
surprised you. When JOB-1408 is done and the final gate says GO, stop: the reviewer takes
over (contact sheets, change log, backup, prune, release).
