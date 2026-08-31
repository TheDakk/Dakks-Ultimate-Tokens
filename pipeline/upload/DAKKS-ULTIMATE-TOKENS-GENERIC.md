# Dakk's Ultimate Tokens — Consolidated Master Pipeline

```yaml
collection_id: generic
style_id: dakk
spec_version: 3.1.2
status: ACCEPTED_LOCKED
workbook: Dakk-Ultimate-Tokens-Master.xlsx
canonical_style_reference: generic-sheet-01.png
canonical_style_reference_sha256: 2b0c44d077d651709fcacc8845c25417815d2df882af4aeeb2fda092cf3554b9
canonical_style_reference_dimensions: 1254x1254
canonical_style_reference_role: style_reference_only
canonical_style_reference_true_alpha: false
prompt_template_id: dakk-production-v3
created: 2026-08-31
```

## The simplified design

The complete production system remains **three files**:

1. **`DAKKS-ULTIMATE-TOKENS.md`** — the frozen visual contract, generation rules, Foundry build contract, QA gates, and immutable-lock protocol.
2. **`Dakk-Ultimate-Tokens-Master.xlsx`** — the only data source of truth for the generated queue, production state, coverage, history, layouts, controlled values, and field ownership.
3. **`generic-sheet-01.png`** — the exact accepted visual master used only as a style reference.

There are no separately maintained CSV, README, schema, changelog, audit, registry, QA, or Foundry-manifest files. When automation specifically requires CSV, export the workbook's `ASSETS` table temporarily. The XLSX remains authoritative.

## Purpose

This is the canonical generic production pipeline for **Dakk's Ultimate Token Module in Foundry VTT**. It scales from the included pilot examples to the generated production queue of approximately 1,765 game documents without changing the architecture.

The accepted sheet is a **style reference only**. It is never cropped into individual assets, never used as a sprite sheet, and never silently replaced. Every production image is generated independently.

## Source-of-truth hierarchy

When records disagree, use this order:

1. Approved locked image bytes and `image_sha256`
2. Exact `resolved_prompt` and `prompt_sha256`
3. Locked `ASSETS` version row
4. Selected `layout_profile` in `CONFIG`
5. Frozen `dakk` style
6. Generated source queue
7. Planning status in `COVERAGE`

A lower level never overrides a higher one.

## Non-negotiable rules

1. One `ASSETS` row produces one output image. No production contact sheets.
2. Verify the reference SHA-256 before every generation batch.
3. Approved artwork is never destroyed. Never write over an approved file in place; before a replacement is written to the clean active path, move the existing file to `_superseded/<art_dir>/<name>-<YYYY-MM-DD>.<ext>`.
4. Every accepted revision increments `ASSETS.version`, links the prior row through `supersedes_registry_id`, and remains recorded in `HISTORY`; the revision number does not appear in the filename.
5. `style_id` controls painting language; `layout_profile` controls composition and technical output.
6. **The current release uses one image per living subject.** Actors, creatures, ancestry/race depictions, class depictions, and portrait subjects use `standing-figure`.
7. Do not pair a standing render with a second overhead or portrait render of the same living subject in the current release.
8. True top-down art is used only when the asset is naturally map-oriented: props, doors, furniture, traps, hazards, area effects, vehicles, siege engines, deliberate swarms, and prone/corpse states.
9. Every production output must contain genuine transparent alpha.
10. Never improvise unrecorded anatomy, equipment, companions, scenery, or variants.
11. A locked asset may be revised only from its exact approved source. Its prior row, hashes, and archived file remain preserved before the new approved image takes the clean active path.
12. Campaign-specific visual collections use separate packages, references, workbooks, histories, batches, and output paths. They may consume generic locked assets but never overwrite them.
13. A keyed game document is wired through `foundry_key`, `art_dir`, and `build_filename`; the generator supplies all three. `art_dir` and `build_filename` are exact mapping values and are never derived, inferred, slugified, normalized, or recomputed from `foundry_key`.
14. `master_px` and `export_px` are generator-supplied row-level pixel sizes. When present, they override the selected layout profile's default master and export sizes for that row.

## Accepted reference: technical note

The reference is preserved byte-for-byte. Its PNG alpha channel is fully opaque, and its visible checkerboard is baked into RGB. It remains the locked visual reference but is not eligible for cropping or shipment as token art.

Every production image must pass true-alpha QA. Because the reference itself cannot demonstrate transparent production pixels, **the first approved production asset establishes the production true-alpha baseline** for later automated and visual checks.

## Frozen style anchor — `dakk`

The current locked visual language is `style_id=dakk`. A materially different visual language becomes `dakk-2`; a number is introduced only when a second style actually exists.

The following paragraph is immutable while `style_id=dakk`:

> Classic Dungeons & Dragons oil painting in the style of the TSR masters Gerald Brom, Keith Parkinson and Jeff Easley: painterly heroic realism with visible confident oil brushwork, rich earthen colour deepened by dramatic warm-vs-cool lighting and strong chiaroscuro, grounded weighty figures in weathered leather, notched steel and worn cloth, crisp ornate detail at the focal point softening toward the edges, with Brom's macabre elegance — pale alabaster skin, bone ornament, ragged silk — surfacing in the darker subjects. Serious and mythic in tone, never cute, never cartoonish, never photorealistic, never anime. Museum-quality oil illustration, extremely high detail, sharp focus.

### Generator-portable fallback

Use the fallback only when the selected generator refuses named-artist direction.

The choice is made **once for the entire batch**, never image by image. Record `fallback_anchor_used=true` in the batch record and append a corresponding event to `HISTORY`.

> Classic late-20th-century dark heroic-fantasy oil illustration: painterly heroic realism with visible confident oil brushwork, a rich earthen palette deepened by dramatic warm-versus-cool lighting and strong chiaroscuro, grounded weighty anatomy in weathered leather, notched steel and worn cloth, crisp ornate focal detail that softens toward the edges, and macabre elegance in darker subjects through pale alabaster skin, bone ornament and ragged silk. Serious and mythic, never cute, cartoonish, photorealistic or anime. Museum-quality oil illustration, extremely detailed and sharply focused.

### Global negative anchor

> No text, letters, numbers, watermark, signature, border, frame, grid, token ring, base, pedestal, scenery, floor plane, cast shadow, drop shadow, white background, checkered background, baked transparency pattern, modern objects, science-fiction objects, photorealism, anime, chibi styling, duplicate subject, unintended companion, extra limbs, missing limbs, merged weapons, malformed hands, cropped anatomy, or contact-sheet layout. Background must contain genuine transparent alpha.

## What the reference controls

It controls oil-paint treatment, value structure, palette, material rendering, anatomy weight, silhouette language, serious mythic tone, focal-detail hierarchy, and edge softness.

The accepted reference is primarily standing full-body artwork. That is why `standing-figure` is the current default for every living subject.

## Current image-scope decision

For a living actor or creature, generate **one standing full-body image** and reuse that approved image as needed for:

- Plain Foundry token texture
- Dynamic Token subject artwork when rings are enabled
- Actor or document portrait presentation
- Class, ancestry/race, or NPC document art when the game data points to that subject

This prevents duplicate queues, keeps every subject governed by the locked reference, and avoids unreliable pseudo-overhead humanoid generations.

The profiles `top-down-actor`, `top-down-creature`, and `portrait` remain defined for forward compatibility, but they are **not used in the current release**.

## Layout profiles

| Profile | Current use | Foundry role | Master → export |
|---|---|---|---:|
| `standing-figure` | Default for every living subject | `token_texture`; optional `dynamic_subject` reuse | 1024 → 400 |
| `top-down-actor` | Defined, not used in the current release | `token_texture` | 1024 → 400 |
| `top-down-creature` | Defined, not used in the current release | `token_texture` | 1024 → 400 |
| `top-down-corpse` | Prone, unconscious, or corpse state | `token_texture` | 1024 → 400 |
| `top-down-swarm` | Deliberate swarm footprint | `token_texture` | 1024 → 400 |
| `item-icon` | Physical weapon, object, gear, treasure, or consumable | `item_icon` | 1024 → 400 |
| `emblem` | Spells, proficiencies, skills, abilities, tables, journals, and other non-physical documents | `item_icon` | 1024 → 400 |
| `armor-icon` | Empty armor piece or declared armor set | `item_icon` | 1024 → 400 |
| `top-down-prop` | Map prop, door, furniture, or trap | `tile` | 1024 → 400 |
| `top-down-effect` | Map-area spell, hazard, aura, projectile, or decal | `effect_tile` | 1024 → 400 |
| `condition-icon` | Small condition or damage symbol | `condition_icon` | 512 → 128 |
| `portrait` | Defined, not used in the current release | `actor_portrait` | 1024 → 512 |
| `top-down-vehicle` | Vehicle or siege object | `tile` | 1536 → 800 |

The exact composition prompts, margins, facing rules, and readability gates are stored in `CONFIG`.

### Row-level pixel-size overrides

`master_px` and `export_px` are generated row-level columns in `ASSETS`.

- When populated, they override the selected `layout_profile`'s default PNG-master and WebP-export pixel sizes for that row.
- For footprint-driven creature and actor tokens, the generator supplies them from the token footprint:
  - 1×1 squares → `master_px` 1024, `export_px` 400
  - 2×2 squares → `master_px` 1024, `export_px` 800
  - 3×3 squares → `master_px` 1536, `export_px` 1200
- If the source queue does not provide a creature or actor footprint, the generator defaults that row to 1×1 and supplies `1024 / 400`.
- Non-footprint assets may leave these columns blank and inherit the layout profile defaults.


## Foundry build contract

The module resolves art by checking the exact build path supplied by the generator for each game document. `foundry_key` is the stable document identity; `art_dir` and `build_filename` are independent generator-supplied mapping values. A document with:

```text
foundry_key: npc.orc
art_dir: creatures
build_filename: orc.webp
```

publishes to:

```text
art/creatures/orc.webp
```

### Required build columns

| Column | Required when | Meaning |
|---|---|---|
| `foundry_key` | The image serves a game document | Exact document key, such as `npc.orc` or `item.long-sword` |
| `art_dir` | Same | Exact generator-supplied build directory. Preserve it verbatim; never derive, infer, normalize, or recompute it from `foundry_key`, `asset_id`, `asset_type`, or `build_filename` |
| `build_filename` | Same | Exact generator-supplied build-facing WebP filename. Preserve it verbatim; never derive, slugify, normalize, or recompute it from `foundry_key`, `asset_id`, `display_name`, `art_dir`, or any other workbook field |

Props, area effects, conditions, vehicles, state variants, and other assets without a game document leave these fields blank.


### Build-column validation

Before a row may enter `prompt_ready`, `approved_locked`, or `export_ready`:

- `foundry_key` must be empty or match this lower-case dotted-key pattern:

  ```regex
  ^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+$
  ```

- `foundry_key`, `art_dir`, and `build_filename` must be **all present or all empty**.
- `module_relative_path` may remain populated for an unkeyed asset.
- The workbook applies blocking data validation to the three build columns and visually flags invalid pasted or imported values.
- The generator/import process must reject invalid mappings rather than shifting values into adjacent columns.


### Stable identity rule

When `foundry_key` exists:

```text
asset_id = foundry_key with each "." replaced by "-"
```

Examples:

```text
npc.orc          -> npc-orc
item.long-sword  -> item-long-sword
spell.lightning-bolt -> spell-lightning-bolt
```

This keeps queue regeneration stable and prevents identifier churn.

### Clean active names, preserved history

`art_dir` and `build_filename` remain exact generator-supplied values. The workbook never reconstructs either one.

For a keyed document, the active PNG master mirrors the exact build-facing directory and filename stem:

```text
foundry_key: npc.orc
art_dir: creatures
build_filename: orc.webp

active master: masters/creatures/orc.png
Foundry copy:  art/creatures/orc.webp
```

The active master and build copy use the same directory name and stem; only the root and extension differ. Active names contain no revision suffix, double underscore, or transport-only suffix.

For an unkeyed asset, the generator supplies a clean `module_relative_path` and a matching `output_folder` plus `filename_stem`. For example:

```text
active master: masters/props/wooden-door.png
Foundry copy:  art/props/wooden-door.webp
```

Before writing any replacement, move the existing file to:

```text
_superseded/<art_dir>/<name>-<YYYY-MM-DD>.<ext>
```

For keyed assets, this archive-before-replace rule uses the exact generator-supplied `art_dir`. Unkeyed assets use their matching clean directory. It applies to each existing PNG or WebP being replaced. The prior `ASSETS` row, hashes, registry linkage, and `HISTORY` events remain append-only.

`ASSETS.version` remains an integer used for row identity, review lineage, and the `HISTORY` ledger. It never appears in an active filename.

`module_relative_path` records the clean build-facing WebP path. `output_folder` and `filename_stem` record the clean active PNG-master location. The approved WebP derivative is created from the approved PNG without repainting.

## Workbook: simple front end, complete backend

### `START_HERE`

Dashboard, live counts, hash verification, daily workflow, immutable-lock rule, and Foundry publish rule.

### `ASSETS`

The only production table. Each row is one image version and combines:

- Identity and generated-queue linkage
- Classification and rights metadata
- Workflow and lock state
- Art brief and mechanical count constraints
- Clean active master naming with `_superseded` archival
- Foundry document-key wiring
- Optional row-level pixel-size overrides
- Exact prompt and prompt hash
- QA, approval, registry, and export state

### `COVERAGE`

The campaign-complete checklist. It includes living subjects, physical items, map-native assets, conditions, effects, and the non-physical document-emblem group.

### `HISTORY`

The single append-only ledger for generation, QA, approval, revision, deprecation, batch fallback selection, and schema changes.

### `CONFIG`

The locked style, clean naming defaults, 13 layout profiles, prompt settings, batch records, controlled values, field definitions, and per-column ownership rules.

## Generated queue and workbook state

The production generator creates the real rows from game data. That source supplies accurate document keys, size categories, attack-derived anatomy or equipment constraints, and document-specific briefs.

The included pilot rows demonstrate the schema. They are replaced by the approximately 1,765 generated production rows when the actual game-data queue is imported.

### Columns regenerated from game data

Regeneration may update only these columns:

```text
job_id
asset_id
variant_id
display_name
family
asset_type
priority
style_id
layout_profile
foundry_role
subject_count
subject_brief
anatomy_count_constraints
must_include
must_exclude
scale_relationship
output_folder
filename_stem
foundry_key
art_dir
build_filename
module_relative_path
master_px
export_px
resolved_prompt
prompt_sha256
```

### Columns owned by the workbook

Regeneration must never overwrite:

```text
status
lock_state
batch_id
generator
model_version
seed
image_sha256
registry_id
qa_status
qa_notes
approved_by
approved_at
supersedes_registry_id
revision_type
export_ready
notes
```

`version` and all remaining columns are `initialize_only`: the generator may populate them when creating a new row, but later regeneration preserves owner edits.

### Round-trip matching rule

Regeneration matches an existing row on:

```text
asset_id + variant_id + version
```

It then updates only fields marked `generated` in the `CONFIG` field guide.

An `approved_locked` row is never updated by regeneration under any circumstance.

`resolved_prompt` and `prompt_sha256` are computed together by the same generation script, so the `prompt_ready` gate is automatic rather than a manual 1,765-row task.

### `catalog_id`

`catalog_id` is an optional source-queue or game-data concept identifier. It does **not** refer to a separately maintained `catalog.csv`.

## Priority mapping

The game-data queue uses three source bands:

| Source priority | Workbook priority | Expected rows |
|---|---|---:|
| `P1` | `1-critical` | 94 |
| `P2` | `2-high` | 250 |
| `P3` | `3-normal` | 1,421 |

There is no fourth production band.

## Required fields before generation

A row may enter `prompt_ready` only when it has:

- `job_id`, `asset_id`, `variant_id`, and `version`
- `display_name`, `family`, and `asset_type`
- `priority`, `status`, `style_id`, `layout_profile`, and `foundry_role`
- `subject_count`, `subject_brief`, `must_include`, and `must_exclude`
- `output_folder`, `filename_stem`, and `reference_file`
- `resolved_prompt` and `prompt_sha256`
- `foundry_key`, `art_dir`, and `build_filename` when it serves a game document

Characters and creatures also require meaningful `anatomy_count_constraints`.

## Production prompt assembly

The generation script builds the exact prompt in this order:

```text
REFERENCE LOCK
Match the exact visual language of the attached approved reference
`generic-sheet-01.png`, style_id `dakk`. Do not redesign or reinterpret the style.

FROZEN STYLE
{CONFIG.frozen_style_anchor}

SUBJECT
Generate exactly {ASSETS.subject_count} isolated subject(s):
{ASSETS.display_name}.
{ASSETS.subject_brief}

ACCURACY
Anatomy/count constraints: {ASSETS.anatomy_count_constraints}.
Must include: {ASSETS.must_include}.
Must exclude: {ASSETS.must_exclude}.
Scale relationship: {ASSETS.scale_relationship}.

LAYOUT
{CONFIG.layout_profile.composition_prompt}
Default facing: {CONFIG.layout_profile.default_facing}.
Framing and safe margin come from the selected profile unless the row overrides them.

TECHNICAL OUTPUT
Create the profile-controlled square PNG master with genuine transparent alpha.
The approved WebP derivative is created later without repainting.

NEGATIVE
{CONFIG.global_negative_anchor}
```

Store the exact final text in `resolved_prompt` and compute its SHA-256 in the same operation.

## Workflow states

```text
planned
  -> prompt_ready
  -> generated
  -> qa_review
  -> needs_revision -> generated
  -> approved_locked
```

Terminal alternatives are `rejected` and `deprecated`. `approved_locked` is immutable.

## Approval and locking

### Initial approval

1. Review the native PNG master and the Foundry-size WebP derivative.
2. Record generator, model version, seed, reference hash, exact prompt, and prompt hash.
3. Compute the final PNG master `image_sha256`.
4. Assign a unique `registry_id`.
5. Set `qa_status=pass`.
6. Set `status=approved_locked` and `lock_state=approved_locked`.
7. Record approver and approval time.
8. Write the approved PNG to its clean active master path and the approved WebP derivative to its clean build-facing path.
9. Verify `module_relative_path`.
10. Set `export_ready=true`.
11. Append the approval event to `HISTORY`.

### Revising an approved asset

1. Duplicate the locked row.
2. Increment `version`.
3. Link the prior registry row in `supersedes_registry_id`.
4. Set `revision_type` to `targeted_edit`, `postprocess_only`, or `regenerate_new_version`.
5. Use the exact approved image as the edit source for targeted changes.
6. Before writing the replacement, move each existing active PNG or WebP to `_superseded/<art_dir>/<name>-<YYYY-MM-DD>.<ext>`.
7. Write the newly approved PNG and WebP to the same clean active paths.
8. Run full QA and verify the resolved build path.
9. Append all events to `HISTORY`.
10. Retain the prior row, hashes, registry record, prompt, and archived files permanently.

## QA gates

Every output is reviewed at native resolution and Foundry export size.

**Style:** exact `dakk`; serious mythic painterly realism; no cartoon, anime, chibi, or photoreal drift.

**Subject:** correct species or object silhouette; exact anatomy and equipment counts; mandatory details present; forbidden details absent; no duplicate or unrequested subjects.

**Composition:** correct layout profile; full silhouette inside the square; safe margin on every side; readable at export size; no accidental contact-sheet composition. Every living subject must be standing full-body three-quarter.

**Transparency:** actual alpha channel; transparent pixels present; no white matte or baked checkerboard; no text, watermark, signature, border, ring, base, or shadow unless explicitly permitted.

**Foundry:** PNG master present at the clean `masters/` path; WebP derivative created without repainting; clean resolved path correct; readable at normal grid zoom; build file exists at the supplied path; any replaced prior file is present under `_superseded/`.

**Locking:** image hash, prompt hash, registry ID, approval, and `HISTORY` event recorded before `approved_locked`.

## Default outputs

- Standing subjects, items, emblems, armor, props, effects, and most state masters: 1024 × 1024 PNG
- Vehicle masters: 1536 × 1536 PNG
- Condition masters: 512 × 512 PNG
- Typical Foundry derivative: 400 × 400 WebP
- Vehicle derivative: 800 × 800 WebP
- Condition derivative: 128 × 128 WebP
- When `master_px` and `export_px` are populated on a row, those values override the layout profile defaults for that specific output.
- For footprint-driven creature and actor tokens, the generator supplies row overrides from token footprint: 1×1 → 1024/400, 2×2 → 1024/800, 3×3 → 1536/1200.
- If a creature or actor row has no supplied footprint, the generator defaults it to 1×1 and supplies 1024/400.
- Genuine transparent alpha required for every production output
- Exactly one subject unless a swarm, rider/mount set, or explicit grouped profile permits more

## CSV use

`ASSETS` is a flat machine-readable table. Export it only when a transport CSV is required. Regenerated rows round-trip back into the workbook under the column-ownership rules above. Do not maintain a second CSV source of truth.

## Accepted sample-sheet prompt — provenance only

This reproduces the reference concept and is not the per-asset production prompt:

> Classic Dungeons & Dragons oil painting in the style of the TSR masters Gerald Brom, Keith Parkinson and Jeff Easley: painterly heroic realism with visible confident oil brushwork, rich earthen colour deepened by dramatic warm-vs-cool lighting and strong chiaroscuro, grounded weighty figures in weathered leather, notched steel and worn cloth, crisp ornate detail at the focal point softening toward the edges, with Brom's macabre elegance — pale alabaster skin, bone ornament, ragged silk — surfacing in the darker subjects. Serious and mythic in tone, never cute, never cartoonish, never photorealistic, never anime. Museum-quality oil illustration, extremely high detail, sharp focus.
>
> A single square sample sheet on a fully transparent background: five clean rows, even spacing, every subject a standing full-body figure (items and beasts in profile), all rendered in the same painterly style, consistent scale within each row, no labels, no text, no borders, no scenery.
>
> Row 1 — eight adventurers: a human knight with longsword and shield; a woman archer in ranger greens drawing a longbow; a dwarf warrior in a horned helm with a battleaxe; an old bearded wizard in robes and pointed hat with a staff; a hooded assassin with a dagger; a bald cleric in white-and-crimson vestments with a mace; a bare-chested barbarian with a spear, a grey wolf at his side.
>
> Row 2 — seven monstrous humanoids: a massive orc in spiked armour with a great axe; a goblin with shield and blade; a white-haired drow with twin curved swords; a horned fiendish sorcerer conjuring flame; a lizardfolk warrior with a spear; a halfling in travelling leathers; a red-bearded dwarf berserker with a two-handed axe.
>
> Row 3 — seven undead and night creatures: an armed skeleton with a round shield; a shambling zombie; a hooded wraith of tattered sea-green shreds; a pale vampire lord in a red-lined cloak; a mummy trailing loose wrappings; a hulking werewolf; a winged red devil.
>
> Row 4 — an armoury and equipment spread: longswords, daggers, a battleaxe, a mace, a morningstar, spears and polearms, a longbow with arrows, crossbows, a quiver, round and heater shields, coiled rope, red and blue potion flasks, wizard staves and wands, a lantern, a belt pouch, scrolls, a spellbook, and a treasure chest spilling coins.
>
> Row 5 — seven beasts: a brown bear, a giant spider, a black panther, a striking eagle, a wild boar, a coiled serpent, a red dragon.
>
> No text, no letters, no watermark, no signature, no border, no frame, no grid, no drop shadow, no white or checkered background, no photorealism, no anime or chibi styling, no modern or sci-fi objects, no duplicate subjects, nothing cropped at the frame edge. Genuinely transparent background with real alpha.

## Change control

- Wording or master-reference changes require a new prompt-template version when the template itself materially changes.
- A material art-direction change requires a new `style_id`: the current style remains `dakk`, and the next materially different style would be `dakk-2`.
- A composition-rule change is deliberately applied to the existing plain-English layout profile after owner approval; it does not create an automatic `-vN` identifier.
- A workbook schema change requires a new `spec_version` and a `pipeline_change` event in `HISTORY`.
- Existing approved rows remain independently reproducible through their exact `resolved_prompt`, hashes, registry linkage, and archived source files even if a current profile definition later changes.

## Spec 3.1.1 patch record

- Corrected `JOB-0022` through `JOB-0027` and `JOB-0029` so their WebP paths reside in `module_relative_path`, with `foundry_key`, `art_dir`, and `build_filename` empty.
- Moved `style reference only; not delivery eligible` for `STYLE-REF-0001` into `notes`.
- Added blocking dotted-key and all-present/all-empty build-triplet validation.
- Clarified that `art_dir` and `build_filename` are exact generator-supplied values and must never be derived or normalized.
- Retained the existing rule that `asset_id` may be derived from `foundry_key`.

## Spec 3.1.2 naming-only patch record

- Renamed all 13 layout-profile identifiers to plain English without photography shorthand or pre-emptive version suffixes.
- Changed the generic style identifier to `dakk`; a later materially different style would become `dakk-2`.
- Replaced legacy suffixed and double-underscore active filenames with clean mirrored paths such as `masters/creatures/orc.png` and `art/creatures/orc.webp`.
- Kept `ASSETS.version` for row lineage and `HISTORY`, while removing it from filenames.
- Added the mandatory archive-before-replace path `_superseded/<art_dir>/<name>-<YYYY-MM-DD>.<ext>`.
- Preserved all framing rules, composition prompts, QA gates, Foundry mapping semantics, and generated-versus-owner column behavior.


## Spec 3.1.3 row-size-override patch record

- Added generated `master_px` and `export_px` columns to `ASSETS` as row-level pixel-size overrides.
- Documented that populated row overrides take precedence over the selected layout profile's default output sizes.
- Defined generator footprint mapping for creature and actor tokens: 1×1 → 1024/400, 2×2 → 1024/800, and 3×3 → 1536/1200.
- Documented that when a creature or actor row has no supplied footprint, the generator defaults it to 1×1 and supplies 1024/400.
- Left every other accepted 3.1.2 naming, build-mapping, QA, and lock rule unchanged.
