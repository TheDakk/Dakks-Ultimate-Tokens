# Universal 2.0, blocks 2 to 8: polish every remaining row

Paste everything below the line into a fresh Codex session opened in
`C:\Projects\FoundryVTT\DakksUltimateTokens`, one session per block. AGENTS.md applies in
full, including its polish-route section. Do not start before the reviewer says block 1 is
accepted. Authorised by HIST-0039 and PLAN-UNIVERSAL-2.0.md.

---

You are running the POLISH blocks of Universal 2.0: every row that was NOT re-rolled in
block 1 (PASS-2-REROLL.md) is revised image-to-image with the new model, in job order, in
blocks of about 200. The design of each painting is preserved; only its rendering improves.
The pilot (HIST-0035) and pass 1 (HIST-0038) proved the route.

## Hard rules for this session

- The polish route only: `prompt-json --polish`, `import --polish`,
  `record-refusal --polish`. Never the plain `import`, never `--revise` in these blocks.
  Never write under `art/`, `masters/`, `_superseded/` or `upload/` yourself; never open the
  workbook; never edit `art/versions.json` or `POLISH-PREAMBLE.txt`.
- Generate only through the built-in image tool. No retouching, cropping, resizing, keying,
  un-keying or compositing by you.
- Skip every row listed in PASS-2-REROLL.md: they were re-rolled in block 1 and are not
  polished again. Skip a row whose `prompt-json --polish` reports `version` of 2 or more
  and a `next_version` above 2 unless the reviewer's block list names it explicitly.
- Work only the block you were given. Stop at its last row.

## Per row

1. `.venv\Scripts\python.exe import_builtin_image.py prompt-json --polish --job JOB-xxxx`
   Take `polish_prompt`, `polish_sha256` and `input_capture`.
2. Attach `input_capture` FIRST (the approved painting on its magenta fill) and
   `upload\generic-sheet-01.png` SECOND. The prompt is `polish_prompt`, verbatim.
3. Generate exactly one image and save the returned PNG unmodified.
4. `.venv\Scripts\python.exe import_builtin_image.py import --polish --job JOB-xxxx --input <that.png> --sent-prompt-sha256 <polish_sha256> --model "<model id the tool reports, or: unreported (Codex built-in)>"`
   Keep its OK / ERROR / VERSION lines. An ERROR leaves the library untouched.

## Refusals

One identical retry for an output-stage refusal; `record-refusal --polish ...` and skip for
an input-stage refusal. Never change a word of the prompt.

## The blocks (job order, re-roll rows excluded)

| block | rows |
|---|---|
| 2 | JOB-0005 to JOB-0250 |
| 3 | JOB-0251 to JOB-0500 |
| 4 | JOB-0501 to JOB-0750 |
| 5 | JOB-0751 to JOB-1000 |
| 6 | JOB-1001 to JOB-1200 |
| 7 | JOB-1201 to JOB-1408 |

Queue SHA-256: `d04e9ac3224e86391819ef76095c61274b05026807aaf675d534f7affa8ccd8a`.
Reference SHA-256: `2b0c44d077d651709fcacc8845c25417815d2df882af4aeeb2fda092cf3554b9`.
Preamble SHA-256: `46b18afd0760d0e286b1cf506bfa1fc7bb0801409986a664d3efb6ea07c514cf`.
Handshake (JOB-0001): `Black Dragon · black-dragon.webp · 1200 · bfe60d6a8251`.
If the importer reports that the queue or reference changed, stop and report.

## After each block

Run `.venv\Scripts\python.exe verify_gate.py` and report every importer line verbatim, the
verdict and report filename, the model id, and anything surprising. On GO the reviewer
releases the next block; on STOP, stop and wait.
