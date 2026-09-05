# Note for Fable: universal art mapping across editions

The user confirmed that this audit covers the generic/universal campaign library across editions. Setting-specific subjects and third-party bestiary books will be handled separately. Do not promote those into this pass.

The user expects the core rules add-on and its compendiums to handle edition-specific creature mapping. That integration has not been verified by this image audit.

- Resolve each compendium record by edition, source book, canonical subject and visual variant. Shared art is appropriate when the subject looks the same; differing statistics alone do not require another image.
- Keep aliases for genuinely identical visual subjects. The repository README already requires a new row when a subject looks different across editions/settings. Do not flatten anatomy differences into an alias.
- Decide Merrow explicitly: this library has a biped, while the inspected D&D Beyond reference has a serpentine lower body. An intended older aquatic-ogre version needs an edition-qualified mapping, not automatic replacement.
- Resolve Gazer before mapping Beholder. The five-foot queue brief suggests a possible renamed older concept; it must not silently map to the modern tiny Gazer. Corpse Ravager/Carrion Crawler and Tunnel Lurk/Umber Hulk are also hypotheses requiring confirmation. Spigazu needs its original source identity.
- Consider Mage/Wizard, Thief/Rogue and Invoker/Evoker; spell aliases such as Improved Invisibility/Greater Invisibility, ESP/Detect Thoughts and Free Action/Freedom of Movement require effect checks. Similar names do not prove identical rules or art semantics.
- Check base Kuo-toa, Quaggoth and Mind Flayer coverage before creating duplicates of the existing specialist variants. Same for Orc and Half-Orc creature art versus playable species presentation.
- A cross-category reuse needs an explicit resolved image path or a supported mapping mechanism. The existing art/aliases.json format is same-category; do not assume it supports cross-category aliases.
- Add mapping validation in the core rules add-on: every mapped target exists, aliases do not chain/cycle, unresolved canonical names are visible, and edition-specific body plans resolve to the intended variant.
- Separate mapping-only work, canonical design corrections, genuinely missing universal subjects, and future setting/third-party collections. This audit does not authorize code or library mutations.

For Claude: approve the identity/source table first, then briefs and any reroll list. Preserve the generic TSR style; use official references to establish subject identity rather than copy their composition.
