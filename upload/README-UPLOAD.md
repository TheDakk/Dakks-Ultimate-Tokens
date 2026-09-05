# How to run this — start here

**Universal is complete (1408/1408) and closed as of 2026-09-04; no further Universal
generation is authorized.** What follows is the procedure that produced it, kept for the
next collection (Dark Sun, once its four prerequisites exist) and for re-rolls the reviewer
explicitly hands out.

Two tools, two pastes. **Claude Code** manages the queue and checks your results.
**ChatGPT** makes the images. This file is the whole procedure.

The loop, once round:

1. Paste **#1** into a new Claude Code conversation → it tells you what's outstanding.
2. Paste **#2** into a new ChatGPT chat (with the files attached) → it proves it can read
   the queue.
3. Paste **#3** → it generates images.
4. Save each PNG unmodified and hand it to the importer (see "Saving what comes back");
   it keys the magenta out and writes the master, the WebP under `art\` and the ledger line.
5. Tell Claude Code you're done → it verifies them and wires them into Foundry.

## How it runs now (Codex, September 2026)

The chat-paste procedure below still works as a fallback, but production runs through
**Codex** reading `../AGENTS.md`, so nothing needs pasting each session. The loop, once round:

1. Codex generates a block (about 200 rows) one at a time: `prompt-json`, the built-in image
   tool with the subject on a flat magenta fill, save, `import` (keys it, writes master,
   WebP and ledger line).
2. Codex runs `verify_gate.py`; on GO it continues, on STOP it reports and waits.
3. Claude Code reviews every image of the block on contact sheets (`review_sheets.py`),
   retires misses to `_superseded/`, fixes the brief *class* in the generator, regenerates
   the queue, updates the workbook and HISTORY, and hands Codex the re-roll list with the
   new queue hash.
4. Repeat until `npm run art-status` says 0 to go; then `npm run build` with Foundry closed.
   For Universal this happened on 2026-09-04; the loop only runs again for a re-roll list
   the reviewer hands out, or for a new collection.

The handshake row still proves any reader is on the real queue:

    Black Dragon · black-dragon.webp · 1200 · bfe60d6a8251

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

Every image is a square PNG of the subject on one flat, uniform, pure magenta fill
(#FF00FF), exactly as its resolved_prompt says; the transparent master is produced
afterwards by keying the magenta out. Never paint a checkerboard or a white background.

The ASSETS sheet is the only queue. Ignore any pilot, sample or example rows and any
batch record whose id contains PILOT — they are superseded and none of them are to be
generated. If a row you are asked for is not in ASSETS, say so and stop rather than
answering from the specification or the reference image.

Generate nothing yet. First confirm you can read the queue: open the ASSETS sheet, find
row JOB-0001, and reply with only its display_name, build_filename, export_px, and the
first 12 characters of its prompt_sha256.
```

**It must answer exactly:**

    Black Dragon · black-dragon.webp · 1200 · bfe60d6a8251

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

**Never save an image straight into `art\`.** Every image comes back on a magenta fill, and
the build would show it exactly that way. Save the PNG unmodified anywhere, then hand it to
the importer from `C:\Projects\FoundryVTT\DakksUltimateTokens`:

    .venv\Scripts\python.exe import_builtin_image.py import --job JOB-0001 --input <that.png> --sent-prompt-sha256 <the row's prompt_sha256>

The importer keeps the untouched capture under `masters\_captures\`, keys the magenta out
into the RGBA master under `masters\`, writes the WebP the build reads at
`art\<art_dir>\<build_filename>` (for example `art\creatures\black-dragon.webp`) and
appends the ledger line. The filename *is* the wiring — Foundry finds art by that exact
path — which is why the importer names the file from the row and never from you. A capture
whose background is not the key is refused, never guessed at; a row whose file already
exists is skipped, never overwritten (retire it to `_superseded\` first if it is a re-roll).

---

## Finishing a run — back in Claude Code

```text
I've imported a batch of images through import_builtin_image.py. Run npm run art-check,
fix or tell me what's broken, then rebuild.
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
