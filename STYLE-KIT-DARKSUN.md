# Dakk Style Kit — DARK SUN sheet

The Athas-themed style sheet. **style_id: `dakk-athas-v1`** — used by every worklist
row whose `style` column says `darksun` (the Dark Sun module and every Dark Sun
campaign). Rows marked `generic` use the main sheet, **STYLE-KIT.md**. Same freeze
rule: any revision is a NEW style_id (`dakk-athas-v2`), never an edit in place.

**Assembly per image** — identical to the generic sheet, only the anchor swaps:
`ATHAS ANCHOR (below) + TYPE BLOCK (from STYLE-KIT.md) + visual_brief + NEGATIVE
(from STYLE-KIT.md) + ATHAS NEGATIVE (below)`

Everything else — the studio workflow, lock discipline, variants, drift rule, sizes,
file handling, verification — is in STYLE-KIT.md and applies unchanged here.

**This sheet's world reference** is `reference/DARKSUN-SHEET.md` (image:
`reference/darksun-sheet-01.png` once accepted). In an Athas session attach that sheet
plus one accepted Athas token — and NEVER the generic sheet; the two settings stay in
separate sessions and separate batches.

### ATHAS ANCHOR (every darksun-row image, verbatim — this text IS `dakk-athas-v1`)

> Classic Dungeons & Dragons oil painting in the style of the TSR masters Gerald Brom,
> Keith Parkinson and Jeff Easley, leaning hardest on Brom's Dark Sun plates: painterly
> heroic realism with visible confident oil brushwork and dramatic warm-vs-cool
> chiaroscuro, a sun-bleached post-apocalyptic desert world — muted ochre, bone white,
> rust red and dust grey under a harsh low crimson sun — lean sinewy weathered figures,
> skin burnt and wind-scoured, gear of bone, obsidian, chitin, stone and hide rather
> than metal, every surface cracked, dusted and lashed with cord. Serious and mythic in
> tone, never cute, never cartoonish, never photorealistic, never anime. Museum-quality
> oil illustration, extremely high detail, sharp focus.

If your generator refuses artist names, drop "in the style of the TSR masters Gerald
Brom, Keith Parkinson and Jeff Easley" (keep "leaning hardest on" as "leaning on the
look of the Dark Sun sourcebook plates") — consistently for the whole batch.

### ATHAS NEGATIVE (append after the shared negative, every darksun image)

> No green vegetation, no lush foliage, no standing water, no rivers or lakes, no steel
> or polished metal, no shine or chrome, no snow, no grey European stone castle.

The materials rule matters most on weapons and armour: an Athasian blade is chipped
obsidian or knapped stone, armour is bone plates and chitin lashed with hide cord.
Naming the replacement material in the prompt works better than "no metal" alone.

### Athas calibration (run AFTER the generic set in CALIBRATION.md is locked)

Four to six subjects, assembled exactly like CALIBRATION.md but with the anchor above.
All are real worklist rows — accepted images are keepers:

| Subject | Type block | Size | Save as |
|---|---|---|---|
| Thri-Kreen | circular portrait | 512 | `art/races/thri-kreen.webp` (+ copy in `art/creatures/`) |
| Mul | circular portrait | 512 | `art/races/mul.webp` (+ copy in `art/creatures/`) |
| Athasian Dwarf | circular portrait | 512 | `art/races/athasian-dwarf.webp` |
| Id Fiend | standing full-body token | 512 | `art/creatures/id-fiend.webp` |
| Crodlu | standing full-body token | 512 | `art/creatures/crodlu.webp` |

Judge it two ways: the five hold together as one Athas, AND they still sit beside the
generic calibration set as work by the same hand — same brushwork and lighting, hotter
and dustier world. Check each row's `visual_brief` in worklist.csv before assembling.
