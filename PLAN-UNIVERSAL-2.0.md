# Universal 2.0: full re-render, corrected designs, edition mapping

Decided by Nick on 2026-09-05 after two independent audits (Claude's anatomy sweep of all
371 figures, ChatGPT's audit of all 1,408 rows against D&D Beyond). This file is the plan of
record; HISTORY carries the events, `CHANGELOG.md` will carry the per-row outcome.

## Decisions

1. **Edition.** Universal art is edition-agnostic. Where editions disagree on a creature's
   body plan, the most recognisable current depiction (D&D Beyond) is used, including for
   the 2e suite. Edition-specific naming is handled by the core-rules modules mapping their
   documents onto universal slugs (art/aliases.json), never by duplicate art.
2. **Anatomy and identity re-rolls: approved (33 rows).** Behir (queued), Chimera, Basilisk,
   Brownie, Cockatrice, Couatl, Efreeti, Otyugh, Remorhaz, Salamander, Triton, Ettercap,
   Giant Sea Horse, Glabrezu, Flameskull, Hippogriff, Crawling Claw, Gazer, Corpse Ravager,
   Tunnel Lurk, Grick, Manticore, Dretch, Vrock, Erinyes, Lemure, Quasit, Rug of Smothering,
   Black Pudding, Sprite, Nixie, Merrow, Medusa (legs, per decision 1).
3. **Weapon identity re-rolls: approved (~25 rows).** The 2e polearm set and their
   proficiency icons (Awl Pike, Bardiche, Bec de Corbin, Guisarme, Guisarme-Voulge,
   Partisan, Spetum, Lucern Hammer, Man Catcher, Fauchard, Morning Star proficiency), Hand
   and Light Quarrel, Arquebus and Arquebus Shot, Khopesh, Jousting Lance, both scale
   bardings.
4. **Spell icon re-rolls: approved (12 rows).** Hold Person, Rope Trick, the five
   Leprechaun's spells (brief the effect, never the name), Chill Touch, Blink, Animal
   Growth, Glass Steel, Pass Without Trace.
5. **Beasts wearing gear: approved (5 rows).** Giant Ape, Dire Wolf, Hell Hound, Water
   Elemental, Yeti.
6. **Style watchlist: re-roll and compare (about 20 rows).** The dragons' head shapes,
   Troll, Night Hag, Stone Giant, Cloud Giant, Rakshasa, Owlbear, Griffon, Winter Wolf,
   Killer Whale, Bearded Devil, Awakened Tree, Kraken, Bone Devil, Dragon Turtle, Balor
   (sword and whip), Grimlock, both constrictor snakes (no fangs). Kept only if better.
7. **Expansion: approved in principle, as a separate phase.** Product-Identity creatures
   that already have For Gold & Glory stand-ins (beholder -> gazer, carrion crawler ->
   corpse-ravager, umber hulk -> tunnel-lurk, spinagon -> spigazu) are served by aliases,
   never new files. Genuinely missing universal subjects become a "Universal additions"
   queue after the re-render. Campaign-setting and third-party subjects stay separate.
8. **Everything gets the new model.** Every row not re-rolled is polished image-to-image
   (the route proven in pass 1). Revisions are versioned per row; filenames never change.
9. **Change log by magnitude.** A re-roll is always a logged redesign. A polish is measured
   against its predecessor; a large change is logged as such, a small one as "polish".
10. **Disk.** Every version-1 file already lives, hash-verified, in the external backup
    `D:\Backups\DakksUltimateTokens\universal-closed-2026-09-04`. After the pass is
    accepted and version 2 is backed up the same way, local `_superseded/` keeps only the
    predecessors of logged redesigns and large changes; minor-polish predecessors are
    deleted locally, but only when their hash is present in the verified backup manifest.

## Manifest and hashes

Decision overlay: `audit-dndbeyond-2026-09-05/full-sweep-ledger-decisions.csv` (107 reroll,
2 cleared, 1,299 polish). Corrected queue SHA-256
`d04e9ac3224e86391819ef76095c61274b05026807aaf675d534f7affa8ccd8a`; changed prompt set proven
equal to the 107 (106 new plus the Behir already in the prior queue). Handshake is now
`Black Dragon · black-dragon.webp · 1200 · bfe60d6a8251`. Eight re-roll rows already at
version 2 from pass 1 become version 3.

## Phases

0. **Reviewer prep (Claude).** Hand-written looks for every re-roll row, anatomy stated
   apart from the attack routine; queue regenerated with the changed-hash set proven equal
   to the approved list; `import --revise` for versioned re-rolls; change-magnitude
   classifier and `CHANGELOG.md` generator; `prune-superseded` guarded by the backup
   manifest; aliases for the stand-ins.
1. **Re-roll block (Codex).** 107 rows (33 anatomy, 31 weapon and proficiency, 12 spell,
   5 gear, 26 style), fresh generation on corrected briefs through `import --revise`,
   verify_gate after the block. PASS-2-REROLL.md.
2. **Polish blocks (Codex).** The remaining 1,301 rows (Xorn and Sahuagin Baron included),
   polish route, six blocks in job order with the gate after each. PASS-2-POLISH.md.
3. **Review and release (Claude).** Every re-roll beside its predecessor on contact sheets;
   polish rows by metrics with eyes on every large change; CHANGELOG; backup v2; prune;
   `npm run art-upload`; build; GitHub release 2.0.0.
4. **Additions (later).** The mapping table and the bounded additions queue.

## Roles

- Claude Code: pipeline, briefs, queue, review, release.
- Codex: generation and import only, per AGENTS.md and the pass files.
- ChatGPT: reference research against public D&D Beyond pages and the audit ledger; no
  generation, no repo writes.
