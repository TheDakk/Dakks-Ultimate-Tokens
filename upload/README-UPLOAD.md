# How to run this — start here

Two tools, two pastes. **Claude Code** manages the queue and checks your results.
**ChatGPT** makes the images. This file is the whole procedure.

The loop, once round:

1. Paste **#1** into a new Claude Code conversation → it tells you what's outstanding.
2. Paste **#2** into a new ChatGPT chat (with the files attached) → it proves it can read
   the queue.
3. Paste **#3** → it generates images.
4. Save each image into `art\<folder>\` under its exact filename.
5. Tell Claude Code you're done → it verifies them and wires them into Foundry.

---

## PASTE 1 — starting a Claude Code conversation

Open a new conversation in `C:\Projects\FoundryVTT\DnD2E` and paste this:

```text
Use the foundry-art-pipeline skill. I'm working on Dakk's Ultimate Tokens — the art
library is C:\Projects\FoundryVTT\DakksUltimateTokens and the suite that consumes it is
C:\Projects\FoundryVTT\DnD2E.

Run npm run art-status and npm run art-check, then tell me where the library stands:
how many images exist, how many are left, and anything that came back broken. If the
upload folder needs rebuilding, say so. Don't change anything until I tell you to.
```

That's all it needs — the skill carries the rules, and the two commands read the real
state off disk.

---

## PASTE 2 — setting up ChatGPT

Start a new chat (or a Project — see below). **Attach these three files from this
folder:**

- `DAKKS-ULTIMATE-TOKENS-GENERIC.md`
- `Dakk-Ultimate-Tokens-Master.xlsx`
- `generic-sheet-01.png`

Then paste:

```text
Read DAKKS-ULTIMATE-TOKENS-GENERIC.md as the controlling specification, use
Dakk-Ultimate-Tokens-Master.xlsx as the authoritative queue and state ledger, and use
generic-sheet-01.png only as the locked visual reference.

For each row, use the resolved_prompt column VERBATIM as the image prompt. Never
re-derive, rewrite, summarise or improve it from the specification — the specification is
what produced it, and prompt_sha256 is the proof. Generate exactly one image per row, in
job_id order, one at a time. Never combine rows into a single picture and never produce a
contact sheet or grid.

Every image must be a square PNG with a genuinely transparent background at the row's
export_px size.

Generate nothing yet. First confirm you can read the queue: open the ASSETS sheet, find
row JOB-0001, and reply with only its display_name, build_filename, export_px, and the
first 12 characters of its prompt_sha256.
```

**It must answer exactly:**

    Black Dragon · black-dragon.webp · 1200 · 9e1de8734769

Anything else — a different creature, a guess, "I can't open the file" — means it is not
reading the queue, and every image after that would be invented. Do not continue. Try
uploading `ASSETS-universal.csv` as well and say "read the CSV instead, it is the same
queue."

---

## PASTE 3 — asking for images

```text
Generate rows JOB-0001 through JOB-0020, one image at a time. After each image, tell me
its build_filename and art_dir so I know where to save it, then wait for me to say next.
```

Work in runs of about 20. When a chat gets long or the style starts drifting, start a
fresh chat, redo **Paste 2**, and say `resume from JOB-0021`.

### Saving what comes back

Save each image into the art library using the **exact** `build_filename` from its row:

    C:\Projects\FoundryVTT\DakksUltimateTokens\art\<art_dir>\<build_filename>

For example `art\creatures\black-dragon.webp`. The filename *is* the wiring — Foundry
finds art by that exact path — so it can't be renamed or tidied up. A misspelled file
isn't an error; it just silently never appears.

---

## Finishing a run — back in Claude Code

```text
I've saved a batch of images into the art folder. Run npm run art-check, fix or tell me
what's broken, then rebuild.
```

Claude Code will verify every file (real transparency, no white halo, square, right size,
nothing clipped, filename matches a row), then run the build so the art appears in
Foundry. **Close Foundry first** — the compiler can't write to open packs.

---

## The commands, if you'd rather run them yourself

All from `C:\Projects\FoundryVTT\DnD2E` (that's where `package.json` lives — npm won't
work from the art library):

| Command | When |
|---|---|
| `npm run art-status` | how many images are done and how many are left |
| `npm run art-check` | after saving images — verifies them and flags bad filenames |
| `npm run build` | after art-check passes, with Foundry closed |
| `npm run art-upload` | rebuild this folder for a fresh upload |
| `npm run art-upload-clean` | once an upload is verified, drops the CSV fallback |

---

## Notes

**Use a ChatGPT Project if you can.** Put Paste 2 in the project's custom instructions and
upload the three files to the project. Instructions there are re-applied to every message
in every chat, so the rules survive long sessions and new chats. In a plain chat, Paste 2
fades as the conversation grows — fine for twenty images, not for 1,408.

**This folder cleans itself.** `npm run art-upload` removes stale files it generated
earlier, and reports (never deletes) anything it doesn't recognise. Artwork never lives
here — it goes to `art\`.

**Dark Sun is not in this folder on purpose.** It's a separate collection with its own
contract, queue and reference sheet, and its reference hasn't been accepted yet. Never mix
the two in one chat — the attached reference image is what holds the style.
