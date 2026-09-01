# The three files to give the image generator

Upload all three from this folder. They are exactly what the generator's instructions
name, with the real production queue already in the workbook.

| File | What it is |
|---|---|
| `DAKKS-ULTIMATE-TOKENS-GENERIC.md` | the controlling specification |
| `Dakk-Ultimate-Tokens-Master.xlsx` | the queue and state ledger — **1,408 real rows**, all `prompt_ready` |
| `generic-sheet-01.png` | the locked visual reference (style only, never cropped) |

## Where the instruction has to live

Uploading the files gives the generator *access*; it does not make it read them. The
instruction must sit somewhere it is re-applied on every message:

- **In a ChatGPT Project** — put the text below in the project's **custom instructions**
  and upload the three files to the project. It is re-applied to every message in every
  chat in that project, so it survives long sessions and new chats. **This is the setup
  to use.**
- **In an ordinary chat** — the text is just your first message. It fades as the
  conversation grows, and a new chat starts with nothing. Workable for twenty images,
  not for 1,408.

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

## Prove it is actually reading the queue

Before generating anything, ask this once:

    Open the workbook, find row JOB-0001 on the ASSETS sheet, and reply with only:
    its display_name, its build_filename, its export_px, and the first 12 characters
    of its prompt_sha256. Do not generate an image.

The correct answer is:

    Black Dragon · black-dragon.webp · 1200 · 9e1de8734769

If it comes back with anything else — a different creature, a guess, "I cannot read the
file" — it is not using the queue, and every image it makes will be improvised. Fix that
before generating, do not push through it.

Re-run this check whenever you start a fresh chat.

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

## If it cannot read the .xlsx

Some sessions fail to parse a spreadsheet reliably. `ASSETS-universal.csv` is in this
folder as a fallback — identical rows, same columns, plain text. Upload it alongside and
say: "if the workbook will not open, read ASSETS-universal.csv instead; it is the same
queue." The workbook stays authoritative for status and history either way.

## Dark Sun

Not in this folder, deliberately. It is a separate collection with its own contract,
queue and reference sheet, and its reference has not been accepted yet. Never mix the two
in one session — the attached reference image is what holds the style.
