# Dakk's Ultimate Tokens for Dungeons & Dragons

![Dakk's Ultimate Tokens](https://raw.githubusercontent.com/TheDakk/Dakks-Ultimate-Tokens/main/art/cover.webp)

Unique painted artwork for Dungeons & Dragons in Foundry VTT, and the game compendia that use it, in one
module. 6,176 images in a single classic TSR oil-painting look,
each a transparent WebP named by its subject: a generic library of 4,899 that works in any game system,
plus the **Dark Sun (Athas)** collection (1,176) and the **Theros** collection (101).

It also carries the game compendia, each shown only in worlds of its own system:

- **D&D 5e (2014):** the SRD 5.1 monsters, spells, items, classes and character options, joined kind by
  kind with creatures, spells, magic items, subclasses, races, backgrounds and feats from further
  sourcebooks (their rules text in our own words, the numbers unchanged), and Theros.
- **AD&D 2e** on the Advanced Roleplaying System: For Gold & Glory's rules, creatures, spells and
  equipment; Dark Sun's creatures, races, classes, psionics, weapons (with their Proficient Use rules where the source gives one),
  armour, fighting styles and spells; and its first campaign, Freedom (statistics only, no adventure text).

Every actor carries its painting as portrait and token, with a female or male twin beside it where one is
painted, so the GM places the one they want. For players, every painted race, class, subclass and background
also has a ready character of each sex in a **Characters** compendium (one, sexless, for the three Dark Sun
peoples painted once: the thri-kreen, the tohr-kreen and the Marnitan lizardfolk).

## Install

**Requirements:** Foundry VTT 13 or later for the art, Art Library (All) and the 5e compendia (verified on
14.368). The 5e compendia need the D&D 5e system 5.3.3 or later, including 6.x (tested on 6.0.6,
which needs Foundry VTT 14). The 2e compendia need Foundry VTT 14 and the Advanced Roleplaying System
2026.04.27 or later (tested on 2026.10.06), with its ruleset variant set
to 2; every ARS release since 2026.04.27 requires Foundry 14. The art and Art Library (All) work in any
system.

- In Foundry VTT, open **Add-on Modules → Install Module** and paste the manifest URL
  `https://github.com/TheDakk/Dakks-Ultimate-Tokens/releases/latest/download/module.json`.
- Or download the zip from the latest release and unzip it into
  `Data/modules/dakks-ultimate-tokens`.

The download is about 315 MB, almost all of it paintings; on a hosted server, check its upload or install
limit allows a module that size.


## Getting started

1. In your world, open **Game Settings → Manage Modules**, tick **Dakk's Ultimate Tokens** and save.
2. Open the **Compendium** tab of the sidebar and find the folder **Dakk's Ultimate Tokens**.
3. **Click each folder to open it.** Foundry shows new compendium folders closed, so at first you see only
   Art Library (All) and a closed folder for your system. Everything else is inside:

```
Dakk's Ultimate Tokens
├─ Art Library (All)                  every world
├─ D&D 5e (2014)                      5e worlds only
│  ├─ Creatures                       Creatures, Creatures by Challenge, and their (Theros) twins
│  ├─ Spells
│  ├─ Items
│  ├─ Classes & Origins               characters, races, classes, subclasses, class features, backgrounds, feats
│  ├─ Reference                       monster features, trade goods, tables, rules
│  └─ Art Library (Theros)
└─ D&D 2e                             ARS worlds only
   ├─ Creatures                       For Gold & Glory, Dark Sun and Freedom
   ├─ Spells                          Wizard Spells and Priest Spells inside
   ├─ Items
   ├─ Classes & Races                 characters, classes, races, Dark Sun abilities
   ├─ Skills & Proficiencies
   ├─ Reference                       tables, documentation (Dark Sun weapons reference), the Freedom journals
   └─ Art Library (Dark Sun)
```

Each world shows only its own system's branch: a 5e world never lists the 2e compendia, and the reverse.

### Putting tokens on the map

- **Creatures:** open a Creatures compendium and drag a creature onto the scene. Its painting is already
  its portrait and its token. Where a creature has a female or male version, both are listed side by side,
  for example "Ogre" and "Ogre (female)"; drag the one you want.
- **Creatures by Challenge** holds the same creatures sorted by challenge rating (5e) or hit dice (2e),
  handy for building encounters.
- **Spells, items, classes and races** carry their paintings as their icons; drag them onto a character
  sheet as usual.
- **Player characters:** the **Characters** compendium (in Classes & Origins, or Classes & Races in 2e,
  with "(Theros)" and "(Dark Sun)" twins) holds a ready character for every painted race, class, subclass
  and background, one of each sex (one for the thri-kreen, tohr-kreen and Marnitan lizardfolk, painted
  once), such as "Hill Dwarf (male)" and "Hill Dwarf (female)", its painting already its portrait and token. The GM imports one and gives the player ownership (players cannot create
  actors unless the GM grants them that permission); the player then drops the race and class (and in 5e
  the background) on the sheet as usual; the character's biography links the race, class, subclass or background it was
  made for.
- **A painting by hand:** every race and class is painted as a man and as a woman, side by side in
  **Art Library (All) → Races** (or **Classes**), such as `dwarf.webp` and `dwarf-female.webp`. On a
  character sheet click the portrait and choose the file under `modules/dakks-ultimate-tokens/art/races/`
  or `art/classes/`, then set the same file as the token image in the token settings.

### Using any painting yourself

- Open **Art Library (All)** (or the Dark Sun or Theros library) to browse every painting as thumbnails,
  with its name and file path under each.
- To use one on your own actor, token, item or tile, click its image and in the file picker browse to
  `modules/dakks-ultimate-tokens/art/`, then the kind folder shown under the thumbnail (for example
  `creatures/ogre.webp`). The Dark Sun and Theros paintings are under `art/settings/darksun/` and
  `art/settings/theros/`.
- Updating in place is safe: filenames never change between versions.

### If something seems missing

- **Open the folders first.** A closed folder hides everything inside it, including the setting packs.
- Check the module is enabled in this world, and that the world runs the right system: D&D 5e for the 5e
  compendia, the Advanced Roleplaying System for the 2e ones.
- After installing or updating, return to Setup and launch the world again; Foundry builds the compendium
  folders when a world launches, not on a browser refresh.

The module runs one small script. It keeps each compendium's folders in their intended order (challenge
ratings numerically, Cantrip before 1st Level; a pack whose order you set with its sort button keeps your
choice), and it adds one optional world setting, **Dynamic token rings for Dakk's creatures** (Configure
Settings, off by default): tokens placed from this module's actors get Foundry's token ring with their
painting inside, and in 2e worlds the ring flashes red on damage and green on healing, as dnd5e's own rings
do in 5e.

## What is inside

```
art/creatures/      monsters, animals, NPC types
art/races/          player races
art/classes/        classes and subclasses
art/backgrounds/    backgrounds
art/abilities/      feat, class feature, monster feature and racial trait emblems
art/spells/         spell emblems
art/weapons/        weapons, magic weapons included
art/armor/          armour, shields and barding, magic armour included
art/equipment/      adventuring gear, mounts, services and magic items
art/proficiencies/  proficiency emblems
art/skills/         thief skills
art/tables/         treasure and encounter table emblems
art/journals/       journal art
art/aliases.json    alternate names that resolve to the same image
art/settings/darksun/   the Dark Sun (Athas) collection
art/settings/theros/    the Theros collection
packs/              the game compendia and the three Art Library catalogues
scripts/dakk.js     the folder-order and token-ring script
```

People come in both sexes: `dwarf.webp` and `dwarf-female.webp` side by side. Every image is a square WebP
with real transparency, exported at the size its token footprint needs (400 px for a 1×1 subject, 800 px
for 2×2, 1200 px for 3×3). See `CHANGELOG.md` for what changed in each release.

## Sources

- Generated by Dakk, under a frozen style contract so images made months apart still match.
- Game content: the System Reference Document 5.1 (Wizards of the Coast, CC-BY-4.0) and For Gold & Glory
  (Justen Brown, Open Game License v1.0a); sourcebook rules are written in our own words from the
  mechanics. *For Gold & Glory™ and FG&G™ are trademarks of Justen Brown. This work is not affiliated with
  Justen Brown.*

## Licence

The artwork is free for personal, non-commercial use, shareable with credit; no resale. Game content is
under its own licences. The full terms are in `LICENSE.md`.
