# Universal 2.0, block 1: the 107 re-rolls on corrected briefs

Paste everything below the line into a fresh Codex session opened in
`C:\Projects\FoundryVTT\DakksUltimateTokens`. AGENTS.md applies in full; this file names the
rows, the route and the stop. Authorised by HIST-0039 and PLAN-UNIVERSAL-2.0.md.

---

You are running BLOCK 1 of Universal 2.0: 107 rows whose briefs were corrected after the
2026-09-05 audits (wrong body plans, wrong objects, misleading spell icons, beasts wearing
gear, and a style set to compare). Each is a FRESH generation on its new prompt, imported
as a versioned revision so the previous painting is retired, never overwritten.

## Hard rules for this session

- Route: `prompt-json` (plain), generate, `import --revise <reason>`. Never `--polish` in
  this block; never the plain `import` without `--revise`. Never write under `art/`,
  `masters/`, `_superseded/` or `upload/` yourself; never open the workbook; never edit
  `art/versions.json`.
- Generate only through the built-in image tool. No retouching, cropping, resizing,
  keying, un-keying or compositing by you. Attach `upload\generic-sheet-01.png` on every
  generation. Do NOT attach the previous painting: this block replaces designs.
- Only the 107 rows below, in the order listed. Stop after the last one.

## Per row

1. `.venv\Scripts\python.exe import_builtin_image.py prompt-json --job JOB-xxxx`
   Fetch it fresh for every row. Take `resolved_prompt` and `prompt_sha256`.
2. Generate exactly one image from `resolved_prompt`, verbatim, with the style sheet
   attached. Save the returned PNG unmodified.
3. `.venv\Scripts\python.exe import_builtin_image.py import --revise <reason> --job JOB-xxxx --input <that.png> --sent-prompt-sha256 <prompt_sha256> --model "<model id the tool reports, or: unreported (Codex built-in)>"`
   `<reason>` is the row's tag from the table below (one word, no spaces). The importer
   keys and checks the image and only then retires the current capture, master and export
   to `_superseded\<dir>\<stem>-<date>-<reason>-v<N>.<ext>`, writes the new files under the
   unchanged names, refreshes shared copies, and records version N+1 in `art\versions.json`.
   Read its OK / ERROR / VERSION lines and keep them for the report. An ERROR leaves the
   library untouched: report it and move on; never retry a changed prompt.

## Refusals

An output-stage refusal gets ONE retry with the identical prompt. An input-stage refusal is
recorded with `record-refusal --job JOB-xxxx --sent-prompt-sha256 <prompt_sha256> --error-base64 <base64 of the exact error>`
and the row is skipped. Never change a word of the prompt.

## The 107 rows

| reason tag | rows |
|---|---|
| `anatomy` | JOB-0006 Chimera, 0032 Basilisk, 0033 Behir, 0034 Black Pudding, 0036 Brownie, 0039 Cockatrice, 0040 Corpse Ravager, 0041 Couatl, 0043 Dretch, 0046 Efreeti, 0049 Gazer, 0060 Manticore, 0062 Medusa, 0067 Nixie, 0069 Otyugh, 0075 Remorhaz, 0076 Salamander, 0082 Sprite, 0086 Triton, 0087 Tunnel Lurk, 1199 Crawling Claw, 1224 Erinyes, 1225 Ettercap, 1228 Flameskull, 1255 Giant Sea Horse, 1264 Glabrezu, 1275 Grick, 1285 Hippogriff, 1305 Lemure, 1318 Merrow, 1346 Quasit, 1356 Rug of Smothering, 1398 Vrock |
| `weapon` | JOB-0129 Barding Full Scale, 0132 Barding Half Scale, 0349 Arquebus, 0350 Arquebus Shot, 0353 Awl Pike, 0354 Bardiche, 0358 Bec de Corbin, 0370 Fauchard, 0377 Guisarme, 0378 Guisarme-Voulge, 0389 Khopesh, 0392 Jousting Lance, 0398 Lucern Hammer, 0399 Man Catcher, 0402 Partisan, 0403 Hand Quarrel, 0405 Light Quarrel, 0417 Spetum, 0449 Arquebus (prof), 0452 Awl Pike (prof), 0454 Bardiche (prof), 0457 Bec de Corbin (prof), 0488 Fauchard (prof), 0499 Guisarme (prof), 0500 Guisarme-Voulge (prof), 0522 Khopesh (prof), 0540 Lucern Hammer (prof), 0541 Man Catcher (prof), 0552 Morning Star (prof), 0554 Partisan (prof), 0582 Spetum (prof) |
| `spell` | JOB-0627 Animal Growth, 0657 Blink, 0672 Chill Touch, 0797 Glass Steel, 0813 Hold Person, 0845 Lamentable Belaborment, 0846 Secret Chest, 0847 Secure Shelter, 0848 Tiny Hut, 0849 Trap, 0908 Pass Without Trace, 0959 Rope Trick |
| `gear` | JOB-0101 Yeti, 1209 Dire Wolf, 1235 Giant Ape, 1282 Hell Hound, 1402 Water Elemental |
| `style` | JOB-0001 Black Dragon, 0002 Blue Dragon, 0003 Brass Dragon, 0004 Bronze Dragon, 0007 Cloud Giant, 0023 Troll, 0053 Griffon, 0066 Night Hag, 0070 Owlbear, 0074 Rakshasa, 0095 Winter Wolf, 1168 Awakened Tree, 1173 Balor, 1179 Bearded Devil, 1185 Bone Devil, 1196 Constrictor Snake, 1212 Dragon Turtle, 1240 Giant Constrictor Snake, 1270 Gold Dragon, 1273 Green Dragon, 1276 Grimlock, 1298 Killer Whale, 1300 Kraken, 1370 Silver Dragon, 1377 Stone Giant, 1407 White Dragon |

Queue SHA-256: `d04e9ac3224e86391819ef76095c61274b05026807aaf675d534f7affa8ccd8a`.
Reference SHA-256: `2b0c44d077d651709fcacc8845c25417815d2df882af4aeeb2fda092cf3554b9`.
Handshake (JOB-0001): `Black Dragon · black-dragon.webp · 1200 · bfe60d6a8251`.
If the importer reports that the queue or reference changed, stop and report.

## After the last row

Run `.venv\Scripts\python.exe verify_gate.py` and report:

- every importer OK / ERROR / REFUSED / VERSION line, verbatim, in row order;
- the verifier's verdict and report filename;
- the model id used, and anything the tool did that surprised you.

Then stop. The reviewer lays every new painting beside its retired predecessor and decides,
row by row, whether the redesign stays or is reverted. Block 2 (the polish of every other
row) starts only when the reviewer hands you PASS-2-POLISH.md with its go-ahead.
