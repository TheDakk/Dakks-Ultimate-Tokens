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

## Summary

Behaviour, framing rules, QA gates, the build contract and the generated/owner column split are
all unchanged. This edits identifier strings and the master filename pattern only.
