# GENERIC sample sheet — Dakk's Ultimate Tokens

**This is the GENERIC D&D sheet** (style_id `dakk`). The Dark Sun sheet is a
SEPARATE document — `DARKSUN-SHEET.md` in this folder — and the two are never mixed:
not in one prompt, not in one batch, not in one chat session.

**Status: ACCEPTED and LOCKED.** The approved image is `generic-sheet-01.png` in this
folder (SHA-256 `2b0c44d077d651709fcacc8845c25417815d2df882af4aeeb2fda092cf3554b9`,
1254×1254) — the canonical style reference for every `generic` row. Attach it at the
top of every generation session ("match this exact style"). It is a reference, never a
source: production images are generated one subject at a time, never cropped out of
the sheet. Note its checkerboard is baked into the pixels — the file has no real
alpha, which is fine for a style reference and disqualifying for anything else.

**Production is driven by the package in `upload/`** —
`DAKKS-ULTIMATE-TOKENS-GENERIC.md` (the contract: frozen `dakk` anchor, layout profiles
`standing-figure` / `item-icon` / `armor-icon` / `emblem` / the `top-down-*` family,
QA gates, `masters/` + `art/` naming, `_superseded/` archival) and
`Dakk-Ultimate-Tokens-Master.xlsx` (the ASSETS queue, COVERAGE, HISTORY, CONFIG).
Per-asset prompts come from the workbook's `resolved_prompt` column, not from this
file. THIS file governs the sample sheet only: what the accepted reference depicts,
and how to iterate it if the roster ever changes.

---

## The sheet prompt

Paste the whole block below into the image generator (attach `generic-sheet-01.png`
when iterating on an accepted version). To change the sheet, edit the roster lines —
never the opening style paragraph, which is the frozen `dakk` anchor.

> Classic Dungeons & Dragons oil painting in the style of the TSR masters Gerald Brom,
> Keith Parkinson and Jeff Easley: painterly heroic realism with visible confident oil
> brushwork, rich earthen colour deepened by dramatic warm-vs-cool lighting and strong
> chiaroscuro, grounded weighty figures in weathered leather, notched steel and worn
> cloth, crisp ornate detail at the focal point softening toward the edges, with
> Brom's macabre elegance — pale alabaster skin, bone ornament, ragged silk —
> surfacing in the darker subjects. Serious and mythic in tone, never cute, never
> cartoonish, never photorealistic, never anime. Museum-quality oil illustration,
> extremely high detail, sharp focus.
>
> A single square sample sheet on a fully transparent background: five clean rows,
> even spacing, every subject a standing full-body figure (items and beasts in
> profile), all rendered in the same painterly style, consistent scale within each
> row, no labels, no text, no borders, no scenery.
>
> Row 1 — eight adventurers: a human knight with longsword and shield; a woman archer
> in ranger greens drawing a longbow; a dwarf warrior in a horned helm with a
> battleaxe; an old bearded wizard in robes and pointed hat with a staff; a hooded
> assassin with a dagger; a bald cleric in white-and-crimson vestments with a mace; a
> bare-chested barbarian with a spear, a grey wolf at his side.
>
> Row 2 — seven monstrous humanoids: a massive orc in spiked armour with a great axe;
> a goblin with shield and blade; a white-haired drow with twin curved swords; a
> horned fiendish sorcerer conjuring flame; a lizardfolk warrior with a spear; a
> halfling in travelling leathers; a red-bearded dwarf berserker with a two-handed
> axe.
>
> Row 3 — seven undead and night creatures: an armed skeleton with a round shield; a
> shambling zombie; a hooded wraith of tattered sea-green shreds; a pale vampire lord
> in a red-lined cloak; a mummy trailing loose wrappings; a hulking werewolf; a
> winged red devil.
>
> Row 4 — an armoury and equipment spread: longswords, daggers, a battleaxe, a mace,
> a morningstar, spears and polearms, a longbow with arrows, crossbows, a quiver,
> round and heater shields, coiled rope, red and blue potion flasks, wizard staves
> and wands, a lantern, a belt pouch, scrolls, a spellbook, and a treasure chest
> spilling coins.
>
> Row 5 — seven beasts: a brown bear, a giant spider, a black panther, a striking
> eagle, a wild boar, a coiled serpent, a red dragon.
>
> No text, no letters, no watermark, no signature, no border, no frame, no grid, no
> drop shadow, no white or checkered background, no photorealism, no anime or chibi
> styling, no modern or sci-fi objects, no duplicate subjects, nothing cropped at the
> frame edge. Genuinely transparent background with real alpha.

If the generator refuses artist names, drop "in the style of the TSR masters Gerald
Brom, Keith Parkinson and Jeff Easley" and keep everything else — consistently for
the whole iteration.

---

## How we iterate ("merge our changes")

1. The owner pastes the prompt above (with the accepted image attached), edits roster
   lines to taste, and generates.
2. When a new version is accepted, save it in this folder as the next number
   (`generic-sheet-02.png`, keeping 01), and tell Claude what changed — the roster
   lines here get updated to match, so this file and the accepted image never drift
   apart.
3. The anchor paragraph only ever changes with a new style_id in
   `upload/DAKKS-ULTIMATE-TOKENS-GENERIC.md` — never as part of a sheet iteration.
