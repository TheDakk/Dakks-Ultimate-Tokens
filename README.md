# Dakk's Ultimate Tokens for Dungeons & Dragons

An **edition-agnostic art library** for Foundry VTT, packaged as an art-only module (no
packs, no scripts). One image per subject, named by slug, consumed by every D&D campaign
suite Dakk builds — 2e today, any later edition tomorrow. A goblin is a goblin in any
edition; `art/creatures/goblin.webp` serves them all.

This folder **is** the module: Foundry reaches it through a directory junction at
`Data/modules/dakks-ultimate-tokens`.

## Start here

Images are produced by **Codex's built-in image tool** under the standing rules in
**`AGENTS.md`**, one row at a time through `import_builtin_image.py` (prompt-json, generate
on a flat magenta fill, import: the importer keys the capture into a transparent master and
writes the WebP the build reads). Codex runs `verify_gate.py` after every block; Claude Code
reviews every image (`review_sheets.py`), fixes briefs in the generator, and re-queues
misses. `CLAUDE.md` holds the reviewer's exact moves; `upload/README-UPLOAD.md` the human
procedure.

Operator tools in this folder: `import_builtin_image.py` (the bridge), `chroma_key.py` (the
keyer), `verify_gate.py` (GO/STOP after a block), `rekey_rows.py` (re-apply a keyer change
from preserved captures), `review_sheets.py` (contact sheets for review). Captures live under
`masters/_captures/`, retired files under `_superseded/`, the ledger in `results-*.jsonl`.

## Collections and settings (read before adding any campaign)

The library is **one image per subject, but one collection per setting**. A setting has its
own look, and looks must never mix:

| collection | look | reference sheet | status |
|---|---|---|---|
| `universal` | the generic D&D / Forgotten Realms look: classic TSR oil painting (Brom, Parkinson, Easley) | `upload/generic-sheet-01.png`, locked | **complete (1408/1408)**; closed 2026-09-04; no further generation authorized |
| `darksun` | Athas: sun-bleached, bone and obsidian, no metal, no green | `darksun-sheet-01.png`, **not yet accepted** | blocked; no token generation until all four prerequisites below exist |

Rules that follow from this, and that every future setting inherits:

- A campaign **consumes** universal assets (a goblin is a goblin) but **never overwrites**
  one. Setting-specific subjects, and setting-specific *versions* of a shared subject (an
  Athasian dwarf), get their own rows, their own slug and their own collection.
- Each collection has its own queue, contract, reference sheet, style anchor and history.
  Dark Sun remains blocked until it has all four production prerequisites: an accepted
  `darksun-sheet` reference and its hash; its own contract; its own queue and queue hash;
  and its own handshake.
- **Never mix collections in one generation session.** The reference image attached to the
  session is what holds the style; only one can be attached. Codex works one collection at
  a time and checks the reference hash on every row.
- Verify separation numerically: the count of rows sharing a file across collections must
  be zero.

### Naming across editions and suites: aliases, not copies

Another suite (a 5e campaign, a later edition) may call a subject by a different key. The
agreed rule: **the library's slug is canonical, and differences are resolved by an alias
map, never by a second copy of the file.** Concretely:

- The library carries `art/aliases.json`: `{ "<kind>/<alias-slug>": "<canonical-slug>" }`
  (for example `"creatures/spider-giant": "giant-spider"`). Aliases never chain.
- A consuming suite's `resolveArt` tries the exact slug first, then the alias map, then
  falls back to its own placeholder icon. The DnD2E build already carries the shared slug
  rule (`tools/lib/art.mjs`) and the generator already folds spelling variants at emit time
  (`CANON_ALIASES`); the alias file extends the same idea to consumption time.
- If a file ever appears under an alias name, the intake gate should flag it: rename to the
  canonical slug and add the alias instead.
- An alias is for the *same* subject under another name. A subject that genuinely looks
  different in another setting or edition is a new row, not an alias.

## What is where

```
art/          the images themselves — art/<kind>/<slug>.webp
upload/       the package handed to the image generator (contract, workbook, reference)
reference/    the accepted style sheets and the specs that produced them
canon/        the creature-coverage datasets the queue is built from
```

`art/` is the library. The build is **existence-driven**: drop `art/creatures/goblin.webp`,
rebuild the suite, and every goblin entry upgrades from its placeholder icon
automatically; delete it and the entry falls back. No manifest, no wiring, no bookkeeping
— but the filename must be exactly the slug the queue names, because that filename *is*
the wiring.

## The controlling documents

| Document | Governs |
|---|---|
| `upload/DAKKS-ULTIMATE-TOKENS-GENERIC.md` | **the spec** — frozen `dakk` style anchor, layout profiles, QA gates, naming, locking |
| `upload/Dakk-Ultimate-Tokens-Master.xlsx` | **the queue and ledger** — one row per image, its finished prompt, and its state |
| `reference/generic-sheet-01.png` | **the locked visual reference** — style only, never cropped into art |
| `reference/GENERIC-SHEET.md` | how that reference sheet was produced, and how to iterate it |
| `STYLE-KIT-DARKSUN.md`, `reference/DARKSUN-SHEET.md` | the Dark Sun collection — **draft, not in production** |

The queue is generated from the game data by the suite, so briefs and anatomy counts
describe the creature the game actually runs. See the `foundry-art-pipeline` skill for the
rules behind all of it.

## Sources

- **Generated by Dakk** — the primary source, under the frozen `dakk` style.
- **Too Many Tokens (D&D)** — https://github.com/IsThisMyRealName/too-many-tokens-dnd —
  16,018 AI-generated creature tokens (MIT). Used here as a **name list only**, to widen
  creature coverage beyond 2e; its directory listing is `canon/tmt-names.txt`.
- **SRD 5.1 monsters** — `canon/5e-srd-monsters.json`, 334 monsters from the D&D 5.1
  Systems Reference Document (Wizards of the Coast, CC-BY-4.0). Only mechanical fields
  (size, type, speed, AC) are ever read; no descriptive prose enters any brief.

## Licence

Dakk's own generated artwork: free for personal, non-commercial use, shareable with
credit; no resale. The full terms are in `LICENSE.md` (version 1.0.0). The subject list
drew on two third-party sources that keep their own licences: the Too Many Tokens name
index (MIT) and the SRD 5.1 dataset (CC-BY-4.0, attribution Wizards of the Coast); no
image from either is included.
