# Standing instructions for Codex: Dakk's Ultimate Tokens

You generate the images for this art library. These instructions apply to every session and
every row. They are not suggestions; the reviewer (Claude Code) checks the results against
them and anything done another way is retired.

## The one procedure, per row

1. `.venv\Scripts\python.exe import_builtin_image.py prompt-json --root <this folder> --job JOB-xxxx`
   Take `resolved_prompt` and `prompt_sha256` from the output. Fetch it FRESH for every row you
   are about to generate; a prompt or hash fetched earlier may be stale.
2. Generate exactly ONE image with the built-in image tool from `resolved_prompt`, verbatim,
   with `upload\generic-sheet-01.png` attached as the style reference. Never add, remove,
   shorten, reorder or "improve" a word of the prompt.
3. Save the returned PNG unmodified.
4. `.venv\Scripts\python.exe import_builtin_image.py import --root <this folder> --job JOB-xxxx --input <that.png> --sent-prompt-sha256 <hash from step 1>`
   The importer keeps your capture under `masters\_captures\`, keys the magenta out into the
   RGBA master, writes the WebP the build reads, and appends the ledger line.

The prompt asks for the subject on a flat magenta fill. That is deliberate: the built-in tool
cannot emit alpha, and the importer produces the transparency by keying. Never key, crop,
resize, recolour, retouch, un-key or composite an image yourself. Never generate by any route
other than the built-in tool through this procedure.

## Gates and self-verification

Work in job_id order, in blocks of about 200 rows. After every block run

    .venv\Scripts\python.exe verify_gate.py

It runs the suite's intake gate (art-check) itself, reads the ledger, and pixel-checks every
new master. Do not run art-check separately.

- `GO`   -> continue with the next block.
- `STOP` -> stop immediately and report its full output verbatim. Do not fix, re-key,
           retouch, regenerate or delete anything. The reviewer decides.

## Refusals

A moderation refusal is logged and skipped; there is no second attempt in the same pass unless
the reviewer says so. Report the exact error, including the request ID and the
`moderation_stage`. Input-stage refusals are deterministic (the text itself is blocked) and
are fixed by the reviewer changing the brief, never by you rewording the prompt.

## Source-change rule

The importer verifies the queue and reference hashes on every row. If they change mid-run,
stop and report the old and new hashes. The reviewer changes the queue deliberately (brief
corrections, re-queued rows); when that happens you will be given a fresh list and the new
hash. Never continue against a changed queue on your own judgement.

## Re-rolls

When the reviewer retires a row, its master, export and capture are moved to `_superseded\`
and the row is re-queued, usually with a corrected brief. Re-roll it exactly like a new row:
fresh prompt-json, new generation, import. Never reuse, re-package or re-import an earlier
capture for a re-rolled row.

## Files you never modify

`upload\` (the queue, contract, workbook, reference, README), `Dakk-Ultimate-Tokens-Master.xlsx`
anywhere, `chroma_key.py`, `generate_tokens.py`, `import_builtin_image.py`, `verify_gate.py`,
`rekey_rows.py`, `review_sheets.py`, anything under `masters\` or `art\` except through the
importer. Do not open the workbook for writing under any circumstances; do not copy a
`dist\*.xlsx` over it.

## Reporting

After a re-roll list or a block, report: every import line verbatim (OK / ERROR / REFUSED /
SKIP), the verify_gate.py verdict and output, and any refusal's full error text. Say what was
attempted and what was not. Do not summarise away errors.

## What good looks like

One isolated figure on a flat magenta fill, in the TSR oil-painting style the reference and
the prompt describe. The reviewer looks at every image, not a sample: wrong subject, wrong
head or limb count, a second figure, a grid, a checkerboard or white background, or paint
bleeding off the subject all get the row retired. The importer and verifier catch the
technical defects; the reviewer catches the rest.

## Collections

You work on ONE collection per session. `universal` (the generic D&D / Forgotten Realms
look) is complete (1408/1408), closed, and has no further generation authorization. Dark Sun
is a separate collection and remains blocked until all four prerequisites exist: an accepted
`darksun-sheet` reference and its hash; its own contract; its own queue and queue hash; and
its own handshake. Never attach one collection's reference to another collection's rows, and
never mix rows from two collections in one session.
