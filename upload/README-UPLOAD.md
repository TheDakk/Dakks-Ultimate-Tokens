# The three files to give the image generator

Upload all three from this folder. They are exactly what the generator's instructions
name, with the real production queue already in the workbook.

| File | What it is |
|---|---|
| `DAKKS-ULTIMATE-TOKENS-GENERIC.md` | the controlling specification |
| `Dakk-Ultimate-Tokens-Master.xlsx` | the queue and state ledger — **1,408 real rows**, all `prompt_ready` |
| `generic-sheet-01.png` | the locked visual reference (style only, never cropped) |

---

# THE PASTE

Upload the three files, then paste this. It is the generator's own setup line with two
additions: the rule that stops it improvising, and a check that proves it really read the
queue before any image is made.

```text
Read DAKKS-ULTIMATE-TOKENS-GENERIC.md as the controlling specification, use
Dakk-Ultimate-Tokens-Master.xlsx as the authoritative queue and state ledger, and use
generic-sheet-01.png only as the locked visual reference.

For each row, use the resolved_prompt column VERBATIM as the image prompt. Never
re-derive, rewrite, summarise or improve it from the specification — the specification is
what produced it, and prompt_sha256 is the proof. Generate exactly one image per row, in
job_id order, one at a time. Never combine rows into a single picture and never produce a
contact sheet or grid.

Save nothing and generate nothing yet. First confirm you can read the queue: open the
ASSETS sheet, find row JOB-0001, and reply with only its display_name, build_filename,
export_px, and the first 12 characters of its prompt_sha256.
```

**It must answer exactly:** `Black Dragon · black-dragon.webp · 1200 · 9e1de8734769`

Anything else — a different creature, a guess, "I cannot open the file" — means it is not
reading the queue, and every image after that would be improvised. Fix it before
continuing (see the .xlsx fallback below).

When the answer is right:

```text
Generate rows JOB-0001 through JOB-0020, one image at a time.
```

Save each result as its row's `build_filename` into `art/<art_dir>/` — e.g.
`art/creatures/black-dragon.webp`. That exact filename is the wiring; Foundry finds art by
that path, so it cannot be renamed.

---

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
