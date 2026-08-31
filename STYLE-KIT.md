# Dakk Style Kit

The master prompts for every image in the library. **style_id: `dakk-v1`** — the frozen
name for the STYLE ANCHOR below. Any future revision of the anchor is a NEW style_id
(`dakk-v2`), never an edit in place; images made under `dakk-v1` stay valid forever.

Every image in the library uses the SAME style anchor, verbatim, plus one of the three
type blocks, plus that row's `visual_brief` from worklist.csv. Never improvise the
anchor — consistency across ~1,900 images generated over months depends on it being
byte-identical every time.

**Assembly per image:**  `STYLE ANCHOR + TYPE BLOCK + visual_brief + NEGATIVE`

## The studio workflow

**The library is the source of truth, not the generator.** Foundry points at files;
regeneration is never part of the loop once a file is accepted.

1. **Calibrate first.** Before any real batch, generate this calibration set and iterate
   until all of them feel like plates from the same book: **human, orc, goblin, skeleton,
   wolf, dragon, mundane sword, potion** (6–8 subjects spanning all three type blocks).
   Only when the set holds together is the style locked — then start real batches.
2. **Generate → accept → save → lock.** Generate a candidate; when one is accepted, save
   it at the row's exact save path (the `notes` cell), then mark that row **locked**
   (add a `locked` column value — the regenerator preserves any columns you add to
   worklist.csv beyond the canonical eight, matched by filename). A locked filename is
   **never regenerated and never asked about again**.
3. **Variants add, never replace.** Wildcard-style variants live beside the original with
   a numeric suffix: wanting a third orc warrior means adding `orc-warrior-03`, never
   rerolling `-01` or `-02`. One mundane item file (`longsword.webp`) is shared by every
   entry that shows a longsword — variants are for creatures and NPCs, not mundane gear.
4. **On drift, go forward.** If a batch drifts off-style: tighten this bible (as a new
   style_id) and continue forward, or replace ONLY the drifted filenames. **We do not
   redo the library.**

**Drift control in-session:** generate in batches of 8–12; when starting a new session,
attach one previously accepted image and say "match this exact style". If your tool
supports seeds, fix one per batch.

**Foundry wildcard note (optional, GM-side):** Foundry's token wildcard
(`art/creatures/orc/*.webp`) matches per-directory, and a flat folder would make `orc-*`
also catch `orc-shaman-*`. If you want randomized token variants, give that creature its
own subfolder (`art/creatures/orc/orc-01.webp`, `orc-02.webp`, …) and set the wildcard on
the prototype token in-game. The build only resolves the flat `art/creatures/orc.webp`
path, so keep (or copy) the plain file at the flat path — the subfolder is purely for the
wildcard, and nothing in the build depends on it.

### STYLE ANCHOR (every image, verbatim — this text IS `dakk-v1`)

> Classic high-fantasy tabletop RPG illustration in the tradition of 1990s Dungeons &
> Dragons sourcebook plates: painterly oil-illustration rendering with visible confident
> brushwork, rich saturated colour, dramatic warm-vs-cool lighting with strong
> chiaroscuro, crisp detail at the focal point softening toward the edges, grounded
> heroic realism — weathered leather, notched steel, worn cloth, lived-in gear. Serious
> and mythic in tone, never cute, never cartoonish, never photorealistic, never anime.
> Museum-quality digital painting, extremely high detail, sharp focus.

### TYPE BLOCK 1 — top-down creature token (kind: monster)

> Viewed from directly overhead as a tabletop game token. The full body centred and
> filling about 80 percent of a square frame with clear margin on all sides, limbs and
> silhouette clearly readable at small size, posed mid-motion as if seen from a bird's
> eye. Fully transparent background — no ground, no base, no ring, no shadow.

Sizes (the CSV `size` column decides): Tiny/Small/Medium/Large → **512×512** ·
Huge → **1024×1024** · Gargantuan → **1536×1536**. PNG with alpha.

### TYPE BLOCK 2 — circular portrait (kind: npc, playable races, classes)

> A head-and-shoulders character portrait composed for a circular frame: subject centred,
> face angled slightly off-camera, eyes lit and in sharpest focus, shoulders cropped
> below the collarbone, all critical detail inside the central circle of the square
> canvas. Background is a plain deep-shadow gradient vignette, darker at the edges, no
> scenery.

**512×512** PNG.

### TYPE BLOCK 3 — item icon (kind: weapon, armor, gear, magic item; also spells,
proficiencies, skills, tables)

> A single object rendered as a game inventory icon: three-quarter or profile view,
> centred, filling about 75 percent of the frame, lit by one warm key light with a subtle
> cool rim light so the silhouette pops, no hands, no character, no scene. Fully
> transparent background.

For **spells**, depict the spell's *effect* as the object — a contained burst of fire, a
coil of lightning, a glowing sigil — still centred on transparency. For **tables**, a
small evocative emblem of the subject (a treasure pile, crossed dice). **512×512** PNG.

### NEGATIVE (append to every prompt)

> No text, no letters, no watermark, no signature, no border, no frame, no grid, no drop
> shadow, no white or checkered background, no photorealism, no anime or chibi styling,
> no modern or sci-fi objects, no extra limbs beyond those described, no duplicate
> subjects, no cropping of the subject at the frame edge.

### File handling

Save as the exact `filename` in worklist.csv (PNG is fine — the build accepts it; webp
preferred if your tool exports it), at the row's save path in `notes`
(`art/<kind-directory>/<filename>`), then mark the row locked and `npm run build` in the
suite. The entry upgrades on the next Foundry reload. A misnamed file simply does
nothing — check the name against the CSV if an image doesn't appear.

