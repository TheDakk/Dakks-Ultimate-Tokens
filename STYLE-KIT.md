# Dakk Style Kit

The master prompts for every image in the library.

Every image in the library uses the SAME style anchor, verbatim, plus one of the three
type blocks, plus that row's `visual_brief` from art-worklist.csv. Never improvise the
anchor — consistency across ~1,900 images generated over months depends on it being
byte-identical every time.

**Assembly per image:**  `STYLE ANCHOR + TYPE BLOCK + visual_brief + NEGATIVE`

**Drift control:** generate in batches of 8–12; when starting a new session, attach one
previously accepted image and say "match this exact style". If your tool supports seeds,
fix one per batch.

### STYLE ANCHOR (every image, verbatim)

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

Save as the exact `filename` in art-worklist.csv (PNG is fine — the build accepts it;
webp preferred if your tool exports it), drop into
`dakks-ultimate-tokens/art/<kind-directory>/`, then `npm run build`. The entry upgrades
on the next Foundry reload. A misnamed file simply does nothing — check the name against
the CSV if an image doesn't appear.

