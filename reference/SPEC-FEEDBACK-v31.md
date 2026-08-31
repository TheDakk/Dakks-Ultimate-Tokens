# Feedback on spec_version 3.1.0 — two fixes for v3.2

v3.1 was verified against the workbook itself, not the changelog. **All six items from the
previous round are correctly implemented:**

- `foundry_key`, `art_dir`, `build_filename` added (columns 28–30) and populated on keyed rows;
  `npc.orc` → `creatures` → `orc.webp` → publishes to `art/creatures/orc.webp`
- Rule 7 added; the duplicate overhead rows (old JOB-0002 / JOB-0007) are gone;
  `actor-overhead-south-v1`, `creature-overhead-south-v1` and `portrait-bust-v1` are marked
  defined-but-not-used-in-v1
- `subject-fullbody-3q-v1` now carries `foundry_role: token_texture` with `dynamic_subject` as
  optional reuse
- `emblem-sigil-v1` added with a full composition prompt (74% framing / 12% margin, 1024 → 400),
  demonstrated by JOB-0030
- Round-trip contract: generated vs workbook-owned column lists, matching on
  `asset_id` + `variant_id` + `version`, `approved_locked` never regenerated
- `catalog_id` no longer implies a separate `catalog.csv`
- Bonus, both good: the stable identity rule (`asset_id` = key with `.` → `-`) and the priority
  mapping with expected counts (94 / 250 / 1,421)
- Reference PNG is byte-identical (`2b0c44d0…`), so the style lock carries forward unbroken

Two things to fix. Neither blocks queue generation.

---

## FIX 1 — `module_relative_path` is being written into `foundry_key` on unkeyed rows

On every row **without** a game document, the versioned module path was placed in column 28
(`foundry_key`) instead of column 31 (`module_relative_path`). Columns 29–31 are left empty.
Keyed rows are correct, so this is specific to the blank-key path.

**Why it matters:** any tooling that tests "does this row have a `foundry_key`?" to decide
whether to publish will treat these as keyed and attempt to publish to a nonsense path — the
exact failure the new columns were added to prevent.

**Correction:** move the value from column 28 to column 31; leave 28, 29 and 30 empty.

| job_id | col 28 `foundry_key` | col 31 `module_relative_path` |
|---|---|---|
| JOB-0022 | *(empty)* | `assets/generic/dakk-v1/props/prop-wooden-door__closed-reinforced__v001__fvtt.webp` |
| JOB-0023 | *(empty)* | `assets/generic/dakk-v1/props/prop-campfire__burning__v001__fvtt.webp` |
| JOB-0024 | *(empty)* | `assets/generic/dakk-v1/props/vehicles/vehicle-covered-wagon__empty-intact__v001__fvtt.webp` |
| JOB-0025 | *(empty)* | `assets/generic/dakk-v1/props/vehicles/vehicle-ballista__loaded-intact__v001__fvtt.webp` |
| JOB-0026 | *(empty)* | `assets/generic/dakk-v1/effects/effect-fire-burst__circular-intense__v001__fvtt.webp` |
| JOB-0027 | *(empty)* | `assets/generic/dakk-v1/effects/conditions/condition-poisoned__serpent-droplet__v001__fvtt.webp` |
| JOB-0029 | *(empty)* | `assets/generic/dakk-v1/creatures/creature-orc-warrior-corpse__spiked-armor-greataxe-prone__v001__fvtt.webp` |

**Also STYLE-REF-0001:** its `foundry_key` contains the note text
`style reference only; not delivery eligible`. That belongs in `notes`; `foundry_key` must be
empty.

**Add a validation rule:** `foundry_key` matches `^[a-z0-9-]+(\.[a-z0-9-]+)+$` or is empty —
it is a document key, never a path, never prose. A row with a non-empty `foundry_key` must also
have `art_dir` and `build_filename`; a row with an empty one must have all three empty.

## FIX 2 — `build_filename` is generator-supplied, not derived from the key

The current wording ("Final key slug plus `.webp`") reads as a rule the workbook could
recompute. It must not be recomputed, because the slug rule has deliberate exceptions that the
key alone does not express:

- **Setting-specific art splits.** The five Athasian standard races resolve to their own files
  so Athas art never collides with the core races:
  `ds.race.dwarf` → `athasian-dwarf.webp` (not `dwarf.webp`), and likewise
  `athasian-human`, `athasian-elf`, `athasian-half-elf`, `athasian-halfling`.
- **Single-character final segments fold their parent.** `table.treasure.a` → `treasure-a.webp`,
  never a bare `a.webp` that eight unrelated sub-tables would collide on.
- **Apostrophes are dropped, not hyphenated.** `Cha'thrang` → `chathrang`, `Will O' Wisp` →
  `will-o-wisp`.
- **Shared files.** Where a race and a creature resolve to the same slug (`thri-kreen` is both
  `ds.race.thri-kreen` and `npc.thri-kreen`), one image serves both, and some rows additionally
  need the same file copied into a second `art_dir`.

**Correction:** change the `build_filename` definition to *"the build-facing filename supplied by
the generating queue; usually the key's last segment plus `.webp`, but authoritative as
supplied — never recomputed from `foundry_key`."* Same for `art_dir`.

`asset_id` may still be derived from `foundry_key` — that rule is fine and stays.

---

## Ready to proceed

With those two applied, the schema is accepted and the queue can be generated: ~1,765 rows with
layout profiles assigned per kind, `foundry_key` / `art_dir` / `build_filename` filled from the
existing slug rule, briefs and anatomy constraints derived from game data, and
`resolved_prompt` + `prompt_sha256` computed at emit time.
