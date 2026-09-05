# Style kit — SUPERSEDED; DO NOT USE

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
| the approved per-row procedure | `AGENTS.md` |
| the accepted reference sheet and how it was made | `reference/GENERIC-SHEET.md` |
| checking images you have saved | `npm run art-check` in the suite repo |

No operational image-processing or export instructions remain here. The former manual
background-removal, conversion, and wildcard notes were retired because they bypassed the
approved importer or described behavior outside the current build contract.
