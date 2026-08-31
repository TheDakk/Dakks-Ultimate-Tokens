# Dakk Style Kit — GENERIC sheet

The master prompts for the library's generic D&D artwork — every worklist row whose
`style` column says `generic`. Rows marked `darksun` swap in the Athas anchor from
**STYLE-KIT-DARKSUN.md** (everything else on this sheet still applies to them).

**style_id: `dakk`** — the frozen
name for the STYLE ANCHOR below, built on the three **TSR masters: Gerald Brom** (Dark
Sun), **Keith Parkinson** (Forgotten Realms) and **Jeff Easley** (the AD&D 2e core book
covers) — the classic D&D oil-painting look. Any future revision of the anchor is a NEW
style_id (`dakk-2`), never an edit in place; images made under a style_id stay valid
forever.

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
   **CALIBRATION.md** has all eight fully assembled, ready to paste. Only when the set
   holds together is the style locked — then start real batches.
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
attach the master reference and say "match this exact style". **The master reference is
the accepted GENERIC sample sheet at `reference/generic-sheet-01.png`** (its editable
prompt spec is `reference/GENERIC-SHEET.md`) — the multi-subject sheet the owner
approved to lock this style. Attach it (or one accepted single image) at the top of
every new session; never crop tokens out of the sheet itself (per-figure resolution is
far too low) — it is a reference, not a source. If your tool supports seeds, fix one
per batch. The Dark Sun sheet is separate (`reference/DARKSUN-SHEET.md`) and never
appears in a generic session.

**Foundry wildcard note (optional, GM-side):** Foundry's token wildcard
(`art/creatures/orc/*.webp`) matches per-directory, and a flat folder would make `orc-*`
also catch `orc-shaman-*`. If you want randomized token variants, give that creature its
own subfolder (`art/creatures/orc/orc-01.webp`, `orc-02.webp`, …) and set the wildcard on
the prototype token in-game. The build only resolves the flat `art/creatures/orc.webp`
path, so keep (or copy) the plain file at the flat path — the subfolder is purely for the
wildcard, and nothing in the build depends on it.

### STYLE ANCHOR (every image, verbatim — this text IS `dakk`)

> Classic Dungeons & Dragons oil painting in the style of the TSR masters Gerald Brom,
> Keith Parkinson and Jeff Easley: painterly heroic realism with visible confident oil
> brushwork, rich earthen colour deepened by dramatic warm-vs-cool lighting and strong
> chiaroscuro, grounded weighty figures in weathered leather, notched steel and worn
> cloth, crisp ornate detail at the focal point softening toward the edges, with Brom's
> macabre elegance — pale alabaster skin, bone ornament, ragged silk — surfacing in the
> darker subjects. Serious and mythic in tone, never cute, never cartoonish, never
> photorealistic, never anime. Museum-quality oil illustration, extremely high detail,
> sharp focus.

If your generator refuses artist names, drop the words "in the style of the TSR masters
Gerald Brom, Keith Parkinson and Jeff Easley" and keep everything else — the descriptive
clauses are written to carry the style on their own. Do that consistently for the whole
batch, not per image.

### TYPE BLOCK 1 — standing full-body token (kind: monster)

> The whole figure standing as a full-body tabletop game token, seen from the front or
> a three-quarter view, centred and filling about 80 percent of a square frame with
> clear margin on all sides, silhouette clearly readable at small size, posed with
> weight and attitude as if mid-stride or braced for a fight. Fully transparent
> background — no ground, no base, no ring, no shadow.

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

### Verify before filing (30 seconds per image)

Check the PNG **before** converting to webp or marking the row locked:

- **Genuinely transparent background, not white** (tokens and icons — the portrait
  vignette is the one type that keeps a background). Most previews composite onto
  white, so open it on a dark background; a crisp white square means it's opaque.
- **No white halo** — a 1–3 px light fringe from a white-background cutout glows on a
  dark Foundry scene.
- **Centred with margin** — nothing clipped at the frame edge; Foundry's ring and
  status icons need the corners.
- **Square, at the size the row implies** (512 / 1024 / 1536), **no text, no
  signature, no baked shadow, one subject only.**

Mechanical check (run from the DnD2E repo root, where `pngjs` is installed):

```powershell
node -e "const{PNG}=require('pngjs'),fs=require('fs');const f=process.argv[1];const p=PNG.sync.read(fs.readFileSync(f));let clear=0,x0=1e9,y0=1e9,x1=-1,y1=-1;for(let y=0;y<p.height;y++)for(let x=0;x<p.width;x++){const a=p.data[((p.width*y+x)<<2)+3];if(a<16)clear++;else{if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}}console.log(f,p.width+'x'+p.height,'| transparent '+(100*clear/(p.width*p.height)).toFixed(1)+'%','| subject '+(100*Math.max(x1-x0,y1-y0)/p.width).toFixed(0)+'% of frame','| margins L'+x0+' R'+(p.width-1-x1)+' T'+y0+' B'+(p.height-1-y1));" path\to\image.png
```

Good token output looks like `transparent ~25–55% | subject ~80% of frame | margins
roughly equal`. `transparent 0.0%` means an opaque background.

**If the background comes back white or opaque**, re-prompting rarely fixes it — most
models can't emit real alpha. Instead ask for the subject "on a flat, uniform pure
magenta background (#FF00FF), no shadow, no gradient", then key it out with `rembg`
(one command) or Photopea (Select → Color Range, delete, Layer → Matting → Defringe
2px), and re-run the check. Converting to webp: squoosh.app or Photopea, lossless,
and confirm it's STILL transparent after export — a careless export flattens to white.

