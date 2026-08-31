# Change request — drop the version numbers and the camera jargon

The schema in 3.1.1 is accepted and nothing about its behaviour needs to change. This is a
**naming change only**: identifiers should read in plain English, and version numbers should
exist only where something is actually versioned.

The owner's note: *"I don't think we need version numbers. I don't know why you have 3q and
version numbers and all that."*

## 1. Layout profile ids — plain names, no `-v1`, no `3q`

`3q` is photography shorthand for a three-quarter view and means nothing at a glance. The
trailing `-v1` records which composition rules an asset was made under, which is archival
bookkeeping this project does not need — this is a single-owner library, and a composition
change would simply be applied.

| Current | New |
|---|---|
| `subject-fullbody-3q-v1` | `standing-figure` |
| `item-isolated-3q-v1` | `item-icon` |
| `armor-isolated-v1` | `armor-icon` |
| `emblem-sigil-v1` | `emblem` |
| `prop-topdown-v1` | `top-down-prop` |
| `effect-topdown-v1` | `top-down-effect` |
| `condition-icon-v1` | `condition-icon` |
| `swarm-overhead-v1` | `top-down-swarm` |
| `corpse-overhead-v1` | `top-down-corpse` |
| `vehicle-overhead-south-v1` | `top-down-vehicle` |
| `actor-overhead-south-v1` (not used in v1) | `top-down-actor` |
| `creature-overhead-south-v1` (not used in v1) | `top-down-creature` |
| `portrait-bust-v1` (not used in v1) | `portrait` |

Definitions, composition prompts, framing percentages and export sizes are unchanged — only
the identifier strings.

## 2. Master filenames — drop `__v001` and the double underscores

The versioned master name never reaches Foundry: the build-facing file is already plain
`art/creatures/orc.webp`. The version suffix only ever existed inside the masters archive.

| Current | New |
|---|---|
| `creature-orc-warrior__spiked-armor-greataxe__v001.png` | `masters/creatures/orc.png` |
| `creature-orc-warrior__spiked-armor-greataxe__v001__fvtt.webp` | `art/creatures/orc.webp` *(already correct)* |

The master mirrors the build path — same directory name, same stem, PNG instead of WebP. One
name to reason about instead of three.

**Replacing the one thing `__v001` protected:** so that a bad re-roll cannot destroy a good
approved image, the rule becomes — before writing a replacement, move the existing file to
`_superseded/<art_dir>/<name>-<YYYY-MM-DD>.<ext>`. History is preserved where history is
actually needed, and normal filenames stay clean.

`ASSETS.version` may remain as an integer column for the `HISTORY` ledger; it simply stops
appearing in filenames.

## 3. Style id — keep the concept, drop the leading version

The style id is the one genuine freeze and should survive: it records which visual language a
batch was painted under, so that if the look ever really changes, existing images stay valid
instead of becoming wrong. But it does not need to ship pre-versioned.

| Current | New |
|---|---|
| `dakk-v1` | `dakk` |
| `dakk-athas-v1` | `athas` |

If the look ever materially changes, the next one is `dakk-2` — a number that appears only when
a second thing actually exists.

## 4. What keeps a number, deliberately

`variant_id` numbering for wildcard alternates stays exactly as it is: `orc-01`, `orc-02`,
`orc-03`. That number names a **different picture of the same subject**, not a revision of one
picture — it is what Foundry's token wildcard matches on, and adding `orc-03` must never
disturb `orc-01`.

## 5. Export size must follow the token footprint (one behavioural change)

`standing-figure` currently fixes export at 400 px for every subject. Token footprint is not
constant: in the generic queue alone, **31 figures are Huge (2×2 squares) and 16 are Gargantuan
(3×3)**. A 400 px image stretched across four or nine grid squares is visibly soft — this is the
same class of error that previously put dragons on one-square footprints.

**Add a per-row override**, supplied by the generator from the creature's size category:

| Token footprint | Master | Foundry export |
|---|---:|---:|
| 1×1 (Tiny–Large) | 1024 | 400 |
| 2×2 (Huge) | 1024 | 800 |
| 3×3 (Gargantuan) | 1536 | 1200 |

Add `master_px` and `export_px` as generated, row-level columns that override the layout
profile's defaults when present. Subjects with no size in the source data default to 1×1 / 400,
and the row says so explicitly rather than guessing silently.

## 6. Collection separation — confirming, no change needed

Rule 10 (campaign collections are their own package) is being taken literally: the universal
build contains **no campaign-specific subjects at all**. Verified against the queue — of the
1,408 universal rows, **zero** share a file with a Dark Sun entry, so the two collections are
fully independent. Dark Sun ships as its own collection, with its own workbook, contract,
reference sheet and history, and consumes universal locked assets without ever overwriting them.

## Summary

Items 1–4 and 6 edit identifier strings and confirm existing rules. Item 5 is the only
behavioural change: per-row export sizing so large tokens are not upscaled from a 400 px master.
