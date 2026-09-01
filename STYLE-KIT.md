# Style kit — superseded

**The controlling specification is `upload/DAKKS-ULTIMATE-TOKENS-GENERIC.md`.** It holds
the frozen `dakk` style anchor, the layout profiles, the global negative, the QA gates and
the naming and locking rules. Read that, not this.

This file used to carry a parallel set of type blocks and pixel sizes. It was retired
because it had begun to contradict the contract — it still described a `circular portrait`
framing that the current release does not use, and export sizes that predate per-footprint
sizing. Two documents describing one style is exactly the drift the frozen anchor exists
to prevent.

What lives where now:

| Want | Look in |
|---|---|
| the style anchor, layout profiles, negative, QA gates | `upload/DAKKS-ULTIMATE-TOKENS-GENERIC.md` |
| what to actually do, step by step | `upload/README-UPLOAD.md` |
| the accepted reference sheet and how it was made | `reference/GENERIC-SHEET.md` |
| checking images you have saved | `npm run art-check` in the suite repo |

## The two practical notes that were only ever here

**An opaque background is not fixed by re-prompting.** Most image models cannot emit real
alpha on request. Ask instead for the subject "on a flat, uniform pure magenta background
(#FF00FF), no shadow, no gradient", then key it out with `rembg` (one command) or Photopea
(Select → Colour Range on the magenta, delete, Layer → Matting → Defringe 2px). Re-check
afterwards. Converting to WebP: squoosh.app or Photopea, lossless — then confirm it is
*still* transparent, because a careless export flattens onto white.

**Foundry token wildcards, if you ever want randomised variants.** Foundry matches
wildcards per directory, so a flat folder makes `orc-*` also catch `orc-shaman-*`. Give
that creature its own subfolder (`art/creatures/orc/orc-01.webp`, `orc-02.webp`, …) and set
the wildcard on the prototype token in-game. The build only resolves the flat
`art/creatures/orc.webp` path, so keep a copy there too — the subfolder is purely for the
wildcard and nothing in the build depends on it.
