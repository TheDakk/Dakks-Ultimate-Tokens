# DARK SUN sample sheet — Dakk's Ultimate Tokens

**This is the DARK SUN sheet** (style_id `dakk-athas-v1`). The generic D&D sheet is a
SEPARATE document — `GENERIC-SHEET.md` in this folder — and the two are never mixed:
not in one prompt, not in one batch, not in one chat session.

**Status: DRAFT — in progress.** The first render was close but had canon misses (the
corrections are already folded into the roster below). When a version is accepted,
save it here as `darksun-sheet-01.png` and update this status line.

This sheet is a WORLD REFERENCE — a poster of what Athas things are. Its aged-
parchment poster register is fine for that job. Actual token generations still open
with the `dakk-athas-v1` anchor from STYLE-KIT-DARKSUN.md; in an Athas session attach
BOTH this sheet (what things are) and one accepted Athas token (how they're painted).

---

## The sheet prompt

Paste the whole block below. To change the sheet, edit the roster lines — the opening
style paragraph is the frozen `dakk-athas-v1` anchor.

> Classic Dungeons & Dragons oil painting in the style of the TSR masters Gerald Brom,
> Keith Parkinson and Jeff Easley, leaning hardest on Brom's Dark Sun plates:
> painterly heroic realism with visible confident oil brushwork and dramatic
> warm-vs-cool chiaroscuro, a sun-bleached post-apocalyptic desert world — muted
> ochre, bone white, rust red and dust grey under a harsh low crimson sun — lean
> sinewy weathered figures, skin burnt and wind-scoured, gear of bone, obsidian,
> chitin, stone and hide rather than metal, every surface cracked, dusted and lashed
> with cord. Serious and mythic in tone, never cute, never cartoonish, never
> photorealistic, never anime. Museum-quality oil illustration, extremely high
> detail, sharp focus.
>
> A reference poster on aged sun-scorched parchment, organised in labelled panels,
> hand-drawn sourcebook plate style.
>
> Panel: PLAYER RACES, a height-chart line-up of nine standing figures: a lean
> sun-scoured human; a completely bald and beardless dwarf, heavy-muscled; a feral
> predatory halfling with wild eyes and bone ornaments; a tall long-legged desert elf
> built for running; a half-elf; a hairless heavy-muscled mul; a towering half-giant;
> a mantis-like thri-kreen with four arms and a blade-jawed head; a bird-headed
> winged aarakocra.
>
> Panel: CLASSES, a line-up: fighter, gladiator, ranger, thief, bard with hidden
> blades, templar, druid, an elemental cleric wreathed in one element, psionicist,
> preserver, and a defiler with ash and dead ground at his feet.
>
> Panel: WEAPONS, all of chipped obsidian, knapped stone, polished bone, wood and
> lashed chitin — never grey steel: a double-bladed polearm, a thrown crystal wedge,
> a jawbone axe, a three-pronged polearm, a rope-and-hook weapon, wrist razors, a
> spear, javelins, a sling and a staff sling.
>
> Panel: ARMOR AND GEAR: leather armour, chitin-plate armour, bone-studded hide,
> woven cloth wraps, a waterskin, a rope, carved bone slit-goggles, dried rations, a
> torch, a repair needle and cord, a sun helmet, a cloth silt mask, a backpack.
>
> Panel: CREATURES OF THE WASTES: a bipedal ostrich-like riding reptile with a
> saddle; a giant docile chitinous ant-beetle mount; a tentacled horror rising from
> grey dust; a four-armed giant; a small toothy reptilian pack-beast; a spine-shelled
> beetle; a squat reptilian id fiend radiating menace.
>
> Panel: LANDS OF ATHAS, small vista strips: stony tablelands, white salt flats, a
> sea of grey silt, rocky badlands, black obsidian plains — all under a huge dull
> crimson sun, no green vegetation, no standing water anywhere.
>
> Bottom banner text: NO METAL. ONLY BONE, OBSIDIAN, WOOD, CHITIN, LEATHER, HIDE,
> SHELL, CORD, CLOTH AND CRYSTAL.
>
> No steel or polished metal anywhere, no green plants, no water, no snow, no
> European stone castles, no glowing psionic effects on the figures, no watermark,
> no signature, no photorealism, no anime.

If the generator refuses artist names, drop "in the style of the TSR masters Gerald
Brom, Keith Parkinson and Jeff Easley" (keep "leaning on the look of the Dark Sun
sourcebook plates") — consistently for the whole iteration.

Labels on THIS poster are allowed (it is a reference sheet, not token art) — let the
generator name the panels; correct any misspelled labels in the next iteration rather
than fighting them.

---

## Corrections already folded in (from the first draft's review)

- Dwarf: completely bald and beardless (the first render had hair and a beard)
- Halfling: feral and predatory, not a friendly villager
- Crodlu: bipedal ostrich-like riding reptile, not a horned quadruped
- Kank: giant chitinous ant-beetle, not a rhino-like mammal
- B'rohg: four arms
- "Aviarag" removed (not a real creature) — id fiend in its place
- Races: half-elf and aarakocra added
- Classes: thief and elemental cleric added
- All weapons recoloured bone/obsidian/chitin — no steel-grey sheen
- Psionic glow kept OFF the figures (poster diagrams were fine; tokens never glow)

## How we iterate ("merge our changes")

Same loop as GENERIC-SHEET.md: the owner edits roster lines and generates; on
acceptance, save the image here (`darksun-sheet-01.png`), tell Claude what changed,
and this file is updated to match. The anchor only changes with a new style_id in
STYLE-KIT-DARKSUN.md.
