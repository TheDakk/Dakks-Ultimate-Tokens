# Feedback on spec_version 3.0.0 — changes needed before production

Reviewed the consolidated package (`DAKKS-ULTIMATE-TOKENS.md`, `Dakk-Ultimate-Tokens-Master.xlsx`,
`generic-sheet-01.png`). The reference SHA-256 was independently verified and matches
(`2b0c44d077d651709fcacc8845c25417815d2df882af4aeeb2fda092cf3554b9`). The architecture is
adopted as-is except for the numbered changes below.

**Adopted without change:** layout profiles as a separate axis from `style_id`; the frozen
`dakk-v1` anchor and generator-portable fallback; the global negative anchor; append-only
versioning with `supersedes_registry_id`; the QA gates (especially true-alpha); deterministic
naming; `HISTORY` as the single ledger; rule 10 (campaign collections are separate packages);
reference-is-style-only with no cropping.

---

## 1. BLOCKING — add `foundry_key`; nothing auto-wires without it

The consuming Foundry module resolves art by **existence at a derived path**: for a document
whose key is `npc.orc`, the build looks for `art/creatures/orc.webp` and swaps it in on the
next build. Drop a file, rebuild, done — no manifest, no per-asset wiring.

The v3 naming (`creature-orc-warrior__spiked-armor-greataxe__v001.webp` under
`assets/generic/dakk-v1/creatures/`) carries no link back to a document. Checked all 49
`ASSETS` columns: there is none. `catalog_id` points at a `catalog.csv` that the package
explicitly says no longer exists.

**Consequence as written: none of the ~1,765 module entries resolve.** Every asset would need
hand-placement in Foundry, and hand-placed art is destroyed by the next build.

**Add these `ASSETS` columns:**

| Column | Required when | Content |
|---|---|---|
| `foundry_key` | the asset serves a game document | the document key, e.g. `npc.orc`, `ds.race.thri-kreen`, `item.long-sword` |
| `art_dir` | same | the kind directory the build reads: `creatures`, `races`, `weapons`, `armor`, `equipment`, `spells`, `classes`, `skills`, `proficiencies`, `tables`, `abilities`, `journals`, `npcs` |
| `build_filename` | same | the build-facing resolved name: the key's slug + `.webp` (e.g. `orc.webp`) |

Props, effects, conditions, vehicles and other assets with no game document leave these blank.

**Add a rule:** the versioned master keeps the deterministic name; a publish step writes/copies
the approved master to `art/{art_dir}/{build_filename}`. Two names, one image, full history
preserved. `module_relative_path` should point at that resolved path, not the versioned one.

**Add a rule:** `asset_id` is derived from `foundry_key` where one exists, so regenerating the
queue is stable and does not churn identifiers.

## 2. Scope decision — ONE image per subject; standing full-body for anything alive

The pilot pairs a standing and a true-overhead render of the same subject (JOB-0001/0002,
JOB-0006/0007). **Do not do this.** For v1, actors, creatures, races, classes and portraits get
exactly one image, in `subject-fullbody-3q-v1`.

Reasons, in order of weight:

1. **The accepted reference is standing full-body.** Generating true 90° overhead art means
   generating art the locked reference does not govern — the one thing the whole style lock
   exists to prevent.
2. **Image models are unreliable at true bird's-eye humanoids.** They drift to high
   three-quarter, which fails the spec's own rule 6 and QA composition gate. That is a re-roll
   loop on every actor row.
3. Standing figures on transparency are a fully valid Foundry token texture and the dominant
   modern style.
4. It halves the queue: ~1,765 images instead of ~2,900.

**Keep true top-down only where the subject genuinely is top-down** — props, doors, furniture,
traps, hazards, area effects, vehicles, siege engines. Models handle these well and tiles
require it.

**Change needed:** `subject-fullbody-3q-v1` must permit `foundry_role: token_texture`, not only
`dynamic_subject`. Dynamic token rings are a per-world option; the same standing art serves as
the plain token texture when rings are off. Keep `actor-overhead-south-v1` and
`creature-overhead-south-v1` defined in `CONFIG` but mark them **not used in v1**, available if
a later collection wants them.

## 3. Missing layout profile — non-physical subjects (~797 rows, the single largest group)

Spells, weapon and non-weapon proficiencies, skills, class abilities, random tables and journal
entries all need an icon, and there is no profile for them. `effect-topdown-v1` is wrong: that
is a map-area effect lying on the ground, not an inventory/sheet icon.

**Add `emblem-sigil-v1`:** role `item_icon`; an item-icon-style sigil or contained effect —
a coil of lightning, a glowing rune, a well-worn practice sword for a proficiency, a small
evocative emblem for a table — isolated on transparency, same framing discipline as
`item-isolated-3q-v1`. Master 1024 → export 400.

## 4. Row source: the generator produces the real rows; the workbook owns state

`ASSETS` will be populated with the real production rows (~1,765), replacing the 28 pilot rows.
Those rows are derived programmatically from the game data, which is what makes the briefs
accurate — anatomy counts come from actual attack routines, sizes from the size category that
drives the token footprint, and so on.

So the split is:

- **Generated per row** (regenerating must not clobber owner edits): `job_id`, `asset_id`,
  `variant_id`, `display_name`, `family`, `asset_type`, `priority`, `style_id`,
  `layout_profile`, `foundry_role`, `subject_count`, `subject_brief`,
  `anatomy_count_constraints`, `must_include`, `must_exclude`, `scale_relationship`,
  `output_folder`, `filename_stem`, `foundry_key`, `art_dir`, `build_filename`,
  `module_relative_path`, `resolved_prompt`, `prompt_sha256`.
- **Owned by the workbook, never overwritten**: `status`, `lock_state`, `batch_id`, `generator`,
  `model_version`, `seed`, `image_sha256`, `registry_id`, `qa_status`, `qa_notes`,
  `approved_by`, `approved_at`, `supersedes_registry_id`, `revision_type`, `export_ready`,
  `notes`.

**Change needed:** state the round-trip explicitly — regeneration updates only the generated
columns, matched on `asset_id` + `variant_id` + `version`, and never touches an
`approved_locked` row. Drop `catalog_id`'s reference to a non-existent `catalog.csv`, or define
it as the generated queue.

`resolved_prompt` and `prompt_sha256` are computed at generation time by the same script, so
the "required before `prompt_ready`" gate is satisfied automatically rather than by hand across
1,765 rows.

## 5. Priority values

Map to the existing three-band scheme so the queue keeps its meaning:
`P1 → 1-critical` (94 rows, generate first), `P2 → 2-high` (250), `P3 → 3-normal` (1,421 —
these already have a usable placeholder icon in-game, so they are the unified-look tail).

## 6. Dark Sun package

Per rule 10 the Athas collection is separate and already drafted on our side:
`collection_id: darksun`, `style_id: dakk-athas-v1`, its own anchor, its own negative (no green,
no standing water, no steel), its own reference sheet, its own workbook and `HISTORY`. It
consumes generic locked assets but never overwrites them. Three of its subjects deliberately
diverge from the generic file where the setting demands it (`athasian-dwarf`, `athasian-elf`,
`athasian-halfling`, etc.). No change requested — confirming the split is understood and
already in place.

## 7. Minor

- **Reference alpha:** `true_alpha: false` is correct and well caught — the checkerboard is
  baked into RGB. Add that the first approved production asset establishes the true-alpha
  baseline, since the reference itself cannot serve as one.
- **Artist names:** the fallback anchor must be applied per batch, not per image, and recorded
  in `HISTORY` (already specified — flagging that it will be used often, as several of the
  named artists are living and many generators refuse the direction).
- **Export format:** confirm the build-facing resolved copy is the WebP derivative; the PNG
  master stays in the versioned path only.
