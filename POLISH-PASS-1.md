# Polish pass 1: the large tokens that read soft

Paste everything below the line into a fresh Codex session opened in
`C:\Projects\FoundryVTT\DakksUltimateTokens`. AGENTS.md applies in full, including its
polish-route section; this file names the rows and the stop.

---

You are running POLISH PASS 1 over the Universal collection: 21 large-footprint rows whose
current painting reads soft at its 800 or 1200 px export. The pilot (HIST-0035) proved the
route: image-to-image from the preserved capture, same style, faithful design, real gain
only where the pixels show. This pass is authorized by HIST-0037 for exactly these rows.

## Hard rules for this session

- The polish route only: `prompt-json --polish`, `import --polish`,
  `record-refusal --polish`. Never the plain `import`; never write under `art/`,
  `masters/`, `_superseded/` or `upload/` yourself; never open the workbook; never edit
  `art/versions.json` or `POLISH-PREAMBLE.txt`. The importer retires the approved files
  and records the new version. Your only writes are the PNGs you save before importing.
- Generate only through the built-in image tool. No retouching, cropping, resizing,
  keying, un-keying or compositing by you.
- One collection, one reference: `upload\generic-sheet-01.png` on every generation.
- Only the 21 rows below, in this order. Stop after the last one.

## Per row

1. `.venv\Scripts\python.exe import_builtin_image.py prompt-json --polish --job JOB-xxxx`
   Fetch it fresh for every row. Take `polish_prompt`, `polish_sha256`, `input_capture`
   and `expected_master_px`.
2. Attach `input_capture` FIRST (the approved painting on its magenta fill, the image to
   refine) and `upload\generic-sheet-01.png` SECOND (the style reference).
3. The prompt is `polish_prompt`, verbatim. It already begins with the polish preamble.
   Do not add, remove, shorten or reorder a word.
4. Generate exactly one image and save the returned PNG unmodified.
5. `.venv\Scripts\python.exe import_builtin_image.py import --polish --job JOB-xxxx --input <that.png> --sent-prompt-sha256 <polish_sha256> --model "<model id the tool reports, or: unreported (Codex built-in)>"`
   It keys the image, checks it, and only then retires the current capture, master and
   export to `_superseded\<dir>\<stem>-<date>-polish-v1.<ext>`, writes the new files under
   the unchanged names, refreshes any shared-file copy, and records version 2 in
   `art\versions.json`. Read its OK / ERROR / VERSION lines and keep them for the report.
   An ERROR leaves the library untouched: report it and move on; never retry a changed prompt.

## Refusals

An output-stage refusal (the tool started and then declined) gets ONE retry with the
identical prompt and inputs. An input-stage refusal is recorded with
`record-refusal --polish --job JOB-xxxx --sent-prompt-sha256 <polish_sha256> --error-base64 <base64 of the exact error>`
and the row is skipped. Never change a word of the prompt to get past a refusal.

## The 21 rows

| profile | export | rows |
|---|---|---|
| standing-figure | 1200 | JOB-0001 Black Dragon, JOB-1344 Purple Worm, JOB-0033 Behir, JOB-1354 Roc, JOB-1212 Dragon Turtle, JOB-0084 Titan, JOB-0017 Lizard (Fire), JOB-0099 Wyvern |
| standing-figure | 800 | JOB-1298 Killer Whale, JOB-1222 Elephant, JOB-1315 Mammoth, JOB-1256 Giant Shark, JOB-1244 Giant Elk, JOB-1350 Red Dragon, JOB-1284 Hill Giant, JOB-1240 Giant Constrictor Snake, JOB-1235 Giant Ape, JOB-1173 Balor, JOB-0009 Fire Giant, JOB-1377 Stone Giant, JOB-1168 Awakened Tree |

Queue SHA-256: `7a6feef2d7c0cae556649f84f0f688110d6c4b2c341af0b92af484d4c2902a17`.
Reference SHA-256: `2b0c44d077d651709fcacc8845c25417815d2df882af4aeeb2fda092cf3554b9`.
Preamble SHA-256: `46b18afd0760d0e286b1cf506bfa1fc7bb0801409986a664d3efb6ea07c514cf`.
If the importer reports that the queue or reference changed, stop and report.

## After the last row

Run `.venv\Scripts\python.exe verify_gate.py` (it pixel-checks every master written since
the last GO) and report:

- every importer OK / ERROR / REFUSED / VERSION line, verbatim, in row order;
- the verifier's verdict and report filename;
- the model id used, and anything the tool did that surprised you (added elements,
  changed poses, text, frames, a size other than 1254).

Then stop. The reviewer lays every new master beside its retired version on contact
sheets at export size and decides, row by row, whether the revision stays or is reverted
from `_superseded/`. Do not begin any row beyond the 21, and do not repeat a row.
