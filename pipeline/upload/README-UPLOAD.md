# The three files to give the image generator

Upload all three from this folder. They are exactly what the generator's instructions
name, with the real production queue already in the workbook.

| File | What it is |
|---|---|
| `DAKKS-ULTIMATE-TOKENS-GENERIC.md` | the controlling specification |
| `Dakk-Ultimate-Tokens-Master.xlsx` | the queue and state ledger — **1,408 real rows**, all `prompt_ready` |
| `generic-sheet-01.png` | the locked visual reference (style only, never cropped) |

## Add this one line to the generator's instructions

The spec lets a reader assemble a prompt from its rules, and the workbook also carries a
finished prompt per row. Both must not happen, or two interpreters will drift apart over
1,408 images. So pin it:

> For each row, use the `resolved_prompt` column **verbatim** as the image prompt. Never
> re-derive, rewrite, summarise, or "improve" it from the specification — the
> specification is what produced it, and `prompt_sha256` is the proof. Generate one image
> per row, in `job_id` order, and never combine rows into one picture.

With that line, the two ends agree: the spec governs how rows were built, and the row is
what gets generated.

## Then just ask for work

    Generate rows JOB-0001 through JOB-0020.

Each result is saved as its row's `build_filename` into `art/<art_dir>/`, e.g.
`art/creatures/black-dragon.webp`. That filename is the wiring — Foundry finds art by
that exact path, so it cannot be renamed.

## Regenerating this folder

From the suite repo (`C:\Projects\FoundryVTT\DnD2E`):

    npm run art-worklist      # rebuild the queue from the game data
    npm run art-upload        # write the queue into the workbook here

`art-upload` never touches the template in `pipeline/` — it reads it, replaces only the
ASSETS data rows, and writes the copy here. COVERAGE, HISTORY, CONFIG, the dropdowns and
the validation all come through untouched.

## Dark Sun

Not in this folder, deliberately. It is a separate collection with its own contract,
queue and reference sheet, and its reference has not been accepted yet. Never mix the two
in one session — the attached reference image is what holds the style.
