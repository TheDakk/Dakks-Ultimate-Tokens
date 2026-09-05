# Universal library image audit for Claude

Full local visual sweep completed: **1,407 active masters plus the already-retired Behir**, covering every one of the 1,408 queue rows. All 118 contact sheets were inspected. The sweep identifies gross subject/body-plan problems and confusing symbols; it is not a resolution, alpha, or intake-gate audit.

**40 active priority review candidates**, **62 watchlist rows**, **10 unresolved identity rows**, **1 explicit edition case**, and **1 retired Behir**. One initial concern was cleared at full size (Sahuagin Baron). Remaining rows have no obvious gross mismatch from this screening; they are not certified against every published illustration.

**Evidence boundary:** 30 creature counterparts were visually compared with official D&D Beyond artwork, and 8 additional rows received direct official-text comparisons. Other flagged rows are local visual observations requiring the intended-edition source check. The CSV states evidence per row. D&D Beyond generally has no unique canonical illustration for every spell, proficiency, or table; those were screened for readable subject/effect identity.

The accessible browser showed **Sign in** and did not share the user’s signed-in session. Public official pages and artwork were used. Giant Ape and Giant Sea Horse pages supplied no artwork through the inspected page links; Gazer’s inspected page did not expose artwork in this session. Those do not count as direct official-art comparisons. No claim is made to have searched the user’s entire purchased catalog.

**Scope:** universal subjects across editions. Campaign-setting-specific and third-party book content is deferred. The queue labels rows `fantasy-d20 / generic`; that is insufficient to establish an edition for ambiguous anatomy. [Note for Fable](FABLE-NOTE.md) records the user’s expectation that the core rules add-on maps edition-specific compendiums. That integration was not inspected.

No art, capture, queue, workbook, importer, aliases, or accepted version was changed. The existing `review_sheets.py` generated audit-only sheets. No generation/import or verify_gate run was needed for this read-only review.

## Review package

- [Full row ledger](full-sweep-ledger.csv) — every row, image path/hash, dimensions, revision, evidence, finding, recommendation and sheet/tile.
- [Flagged-image gallery](REVIEW-GALLERY.html) — searchable local originals with source links; click an image for full size.
- [Missing subjects and mapping candidates](missing-and-mapping-candidates.csv) — prioritized proposals, including mapping-only work.
- [Source comparison register](source-comparisons.json) and [snapshot](snapshot.json).

## Shared art direction for any follow-up
The user explicitly reconfirmed that the whole module must retain uniform art direction. Follow [AGENTS.md](../AGENTS.md), the designated [generic style sheet](../upload/generic-sheet-01.png), and the authorized per-row generation route. Every generation uses that same reference and the freshly resolved prompt verbatim. Keep the TSR oil-painting treatment and isolated subject on flat magenta for the importer.

For authorized polish, [POLISH-PASS-1.md](../POLISH-PASS-1.md) requires the approved capture first and the style sheet second. [POLISH-PREAMBLE.txt](../POLISH-PREAMBLE.txt) preserves pose, silhouette, anatomy, equipment, palette, lighting, framing and scale. It improves rendering only. Therefore a body-plan correction requires a reviewer-corrected brief and authorized reroll; the unchanged polish preamble would preserve the defect. Use D&D Beyond to establish identity and anatomy while retaining the module’s established visual style.

## Coverage by category

| Category | Queue rows | Active images screened |
|---|---:|---:|
| creatures | 349 | 348 |
| races | 6 | 6 |
| armor | 21 | 21 |
| equipment | 225 | 225 |
| weapons | 75 | 75 |
| classes | 16 | 16 |
| journals | 1 | 1 |
| proficiencies | 168 | 168 |
| skills | 9 | 9 |
| spells | 449 | 449 |
| tables | 89 | 89 |

## Review these first

Start with body-plan failures: **Basilisk, Couatl, Otyugh, Remorhaz, Salamander, Glabrezu, Hippogriff, Grick, Flameskull and Cockatrice**. These change the recognizable creature, rather than merely its paint style. Behir is already retired and should stay out of the library pending an authorized corrected generation.

Then address wrong-object/effect icons: **Hand Quarrel, Light Quarrel, Morning Star proficiency, Man Catcher and its proficiency, scale barding, Chill Touch, Hold Person and Rope Trick**. Arquebus Shot also needs the intended historical/edition reference. Review equipment and matching proficiency together.

The source comparison establishes a discrepancy with the linked edition, not a blanket requirement to copy that illustration. Costume differences, an obscured limb, a different pose, or a different valid form do not alone justify retirement. Quasit, fiend equipment, and older-edition creatures especially need that judgment.

## Priority candidates and retired Behir

| Job / image | Evidence | Finding | Official reference |
|---|---|---|---|
| [JOB-0002 Blue Dragon](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/blue-dragon.png>) | official_art_viewed | Blue dragon lacks clear single nasal horn; generic spiky dragon. | [D&D Beyond](https://www.dndbeyond.com/monsters/16765-adult-blue-dragon) |
| [JOB-0006 Chimera](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/chimera.png>) | official_art_viewed | Three heads are present, but the middle head reads as a horned feline/goat hybrid and the torso is a plated dragon biped. DDB art shows lion-bodied quadruped with distinct lion, goat and dragon heads. | [D&D Beyond](https://www.dndbeyond.com/monsters/16823-chimera) |
| [JOB-0032 Basilisk](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/basilisk.png>) | official_art_viewed | Basilisk rendered four-legged reptile; eight-legged identity absent. | [D&D Beyond](https://www.dndbeyond.com/monsters/16801-basilisk) |
| [JOB-0033 Behir](<C:/Projects/FoundryVTT/DakksUltimateTokens/_superseded/creatures/behir-2026-09-05-polish-v2-rejected-legs.png>) | official_art_viewed | Rejected v2 Behir has only a few forebody legs, generic spiky brown-black dragon head; official art has long blue body with legs along its length. Active master missing; already retired. | [D&D Beyond](https://www.dndbeyond.com/monsters/16804-behir) |
| [JOB-0034 Black Pudding](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/black-pudding.png>) | official_art_viewed | Black Pudding has distinct head eyes toothy mouth and arm-like limbs. | [D&D Beyond](https://www.dndbeyond.com/monsters/16808-black-pudding) |
| [JOB-0039 Cockatrice](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/cockatrice.png>) | official_art_viewed | Cockatrice has separate foreclaws/hindlegs plus wings, mostly dragon body. | [D&D Beyond](https://www.dndbeyond.com/monsters/16828-cockatrice) |
| [JOB-0041 Couatl](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/couatl.png>) | official_art_viewed | Couatl rendered legged feathered dragon instead of winged serpent. | [D&D Beyond](https://www.dndbeyond.com/monsters/16832-couatl) |
| [JOB-0043 Dretch](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/dretch.png>) | official_art_viewed | Dretch rendered armored reptile. | [D&D Beyond](https://www.dndbeyond.com/monsters/16846-dretch) |
| [JOB-0046 Efreeti](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/efreeti.png>) | official_art_viewed | Efreeti has bat wings, resembles devil. | [D&D Beyond](https://www.dndbeyond.com/monsters/16854-efreeti) |
| [JOB-0060 Manticore](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/manticore.png>) | official_art_viewed | Manticore lion face rather than humanlike face, scorpionlike tail. | [D&D Beyond](https://www.dndbeyond.com/monsters/16951-manticore) |
| [JOB-0062 Medusa](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/medusa.png>) | official_art_viewed | Medusa snake lower body (5e counterpart has legs). | [D&D Beyond](https://www.dndbeyond.com/monsters/16954-medusa) |
| [JOB-0069 Otyugh](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/otyugh.png>) | official_art_viewed | Otyugh looks quadruped shell beast with two facial tubes; eye stalk absent. | [D&D Beyond](https://www.dndbeyond.com/monsters/16973-otyugh) |
| [JOB-0075 Remorhaz](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/remorhaz.png>) | official_art_viewed | Remorhaz four-legged armored beast; centipede body absent. | [D&D Beyond](https://www.dndbeyond.com/monsters/16995-remorhaz) |
| [JOB-0076 Salamander](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/salamander.png>) | official_art_viewed | Salamander biped reptile rather than humanoid torso serpent tail. | [D&D Beyond](https://www.dndbeyond.com/monsters/17004-salamander) |
| [JOB-0086 Triton](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/triton.png>) | local_visual_only | Triton fish tail rather than legs (modern counterpart). | Intended-edition source still needed |
| [JOB-0129 Barding, Full Scale](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/equipment/barding-full-scale.png>) | official_text_compared | Full Scale Barding appears made of large solid plates, without overlapping scale construction. | [D&D Beyond](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/equipment) |
| [JOB-0132 Barding, Half Scale](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/equipment/barding-half-scale.png>) | official_text_compared | Half Scale Barding appears made of large solid plates, without overlapping scale construction. | [D&D Beyond](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/equipment) |
| [JOB-0350 Arquebus Shot](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/arquebus-shot.png>) | local_visual_only | Arquebus Shot is a pointed modern bullet rather than an early firearm round ball. | Intended-edition source still needed |
| [JOB-0399 Man Catcher](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/man-catcher.png>) | local_visual_only | Man Catcher is a pointed spear with one small side hook; no neck-catching enclosure. | Intended-edition source still needed |
| [JOB-0403 Hand Quarrel (10)](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/quarrel-hand.png>) | official_text_compared | Hand Quarrel is depicted as a double-ended war pick, not a hand-crossbow bolt. | [D&D Beyond](https://www.dndbeyond.com/equipment/3-crossbow-bolts) |
| [JOB-0405 Light Quarrel (10)](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/quarrel-light.png>) | official_text_compared | Light Quarrel looks like an unfletched spear, not a crossbow bolt. | [D&D Beyond](https://www.dndbeyond.com/equipment/3-crossbow-bolts) |
| [JOB-0541 Man Catcher](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/man-catcher.png>) | local_visual_only | Man Catcher proficiency looks like a chained spiked shield/trap, without a pole or catching jaws. | Intended-edition source still needed |
| [JOB-0552 Morning Star](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/morning-star.png>) | local_visual_only | Morning Star proficiency is a chained flail; equipment row JOB-0401 correctly uses a fixed spiked head. | Intended-edition source still needed |
| [JOB-0672 Chill Touch](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/chill-touch.png>) | official_text_compared | Chill Touch is an icy hand with a snowflake, strongly signaling cold damage rather than necromantic life-draining magic. | [D&D Beyond](https://www.dndbeyond.com/spells/2026-chill-touch) |
| [JOB-0813 Hold Person](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/hold-person.png>) | official_text_compared | Hold Person uses broken, opening shackles, suggesting release from restraint rather than paralysis. | [D&D Beyond](https://www.dndbeyond.com/spells/2619153-hold-person) |
| [JOB-0959 Rope Trick](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/rope-trick.png>) | official_text_compared | Rope Trick is a hanging rope with a noose-like loop and no entrance or extradimensional-space cue; easily reads as execution equipment instead of a climbing rope into a refuge. | [D&D Beyond](https://www.dndbeyond.com/spells/2235-rope-trick) |
| [JOB-1173 Balor](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/balor.png>) | official_art_viewed | Balor flail and chain instead of sword and flaming whip. | [D&D Beyond](https://www.dndbeyond.com/monsters/16797-balor) |
| [JOB-1185 Bone Devil](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/bone-devil.png>) | official_art_viewed | Bone devil bat wings/heavy bone armor instead of insect wings and gaunt body. | [D&D Beyond](https://www.dndbeyond.com/monsters/16813-bone-devil) |
| [JOB-1212 Dragon Turtle](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/dragon-turtle.png>) | official_art_viewed | Dragon Turtle has tall land-beast posture, clawed limbs rather than aquatic flippers. | [D&D Beyond](https://www.dndbeyond.com/monsters/16845-dragon-turtle) |
| [JOB-1224 Erinyes](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/erinyes.png>) | official_art_viewed | Erinyes bat wings/horns rather than feathered fallen angel. | [D&D Beyond](https://www.dndbeyond.com/monsters/16858-erinyes) |
| [JOB-1225 Ettercap](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/ettercap.png>) | official_art_viewed | Ettercap has four arms plus two legs. | [D&D Beyond](https://www.dndbeyond.com/monsters/16859-ettercap) |
| [JOB-1228 Flameskull](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/flameskull.png>) | official_art_viewed | Flameskull has arms/hands and partial torso. | [D&D Beyond](https://www.dndbeyond.com/monsters/17091-flameskull) |
| [JOB-1235 Giant Ape](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/giant-ape.png>) | local_visual_only | Giant Ape wears complex rope harness, metal hooks and clothing; reads humanoid fighter. | Intended-edition source still needed |
| [JOB-1255 Giant Sea Horse](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/giant-sea-horse.png>) | local_visual_only | Giant Sea Horse has articulated arms and clawlike hands. | Intended-edition source still needed |
| [JOB-1264 Glabrezu](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/glabrezu.png>) | official_art_viewed | Glabrezu only two pincer arms, missing small humanoid arm pair. | [D&D Beyond](https://www.dndbeyond.com/monsters/16902-glabrezu) |
| [JOB-1275 Grick](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/grick.png>) | official_art_viewed | Grick appears five thin mouth tentacles instead of four thick lobed tentacles. | [D&D Beyond](https://www.dndbeyond.com/monsters/16912-grick) |
| [JOB-1285 Hippogriff](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/hippogriff.png>) | official_art_viewed | Hippogriff has lion hindquarters with paws and lion tail rather than horse hindquarters and hooves. | [D&D Beyond](https://www.dndbeyond.com/monsters/16924-hippogriff) |
| [JOB-1305 Lemure](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/lemure.png>) | official_art_viewed | Lemure is upright humanoid with two separate legs rather than melting blob lower body. | [D&D Beyond](https://www.dndbeyond.com/monsters/16942-lemure) |
| [JOB-1346 Quasit](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/quasit.png>) | official_art_viewed | Bat wings make this read as an imp. DDB Quasit reference shows a small horned, wingless biped; verify default form versus an intentional transformation. | [D&D Beyond](https://www.dndbeyond.com/monsters/16988-quasit) |
| [JOB-1356 Rug of Smothering](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/rug-of-smothering.png>) | official_art_viewed | Rug of Smothering has enormous toothed maw, looks like a rug mimic. | [D&D Beyond](https://www.dndbeyond.com/monsters/17000-rug-of-smothering) |
| [JOB-1398 Vrock](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/vrock.png>) | official_art_viewed | Vrock has batlike membrane wings and armored reptilian body rather than feathered vulture demon. | [D&D Beyond](https://www.dndbeyond.com/monsters/17047-vrock) |

## Watchlist and identity decisions

These are review prompts, not a reroll order. Several are older-edition or naming issues. The local originals and contact-sheet locations are included in the ledger.

| Job / image | Status | Observation |
|---|---|---|
| [JOB-0001 Black Dragon](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/black-dragon.png>) | WATCHLIST | Generic spiky black dragon; check swept-forward skull horns. |
| [JOB-0003 Brass Dragon](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/brass-dragon.png>) | WATCHLIST | Brass dragon generic spiky head, missing characteristic head plate. |
| [JOB-0004 Bronze Dragon](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/bronze-dragon.png>) | WATCHLIST | Bronze dragon generic horned silhouette. |
| [JOB-0007 Cloud Giant](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/cloud-giant.png>) | WATCHLIST | Cloud giant looks rock-skinned; distinguish from elemental/stone giant. |
| [JOB-0018 Lizard, Minotaur](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/lizard-minotaur.png>) | IDENTITY_REVIEW | Minotaur lizard rendered bull-headed quadruped; older-edition name needs reference. |
| [JOB-0023 Troll](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/troll.png>) | WATCHLIST | Troll heavily armored/stocky rather than lean long-nosed troll. |
| [JOB-0035 Brown Pudding](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/brown-pudding.png>) | IDENTITY_REVIEW | Brown Pudding has toothy face and defined limbs. |
| [JOB-0036 Brownie](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/brownie.png>) | IDENTITY_REVIEW | Brownie portrayed goblinlike armored creature. |
| [JOB-0040 Corpse Ravager](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/corpse-ravager.png>) | IDENTITY_REVIEW | Corpse Ravager tentacled floating maw; clarify source/name. |
| [JOB-0049 Gazer](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/gazer.png>) | IDENTITY_REVIEW | Large winged, many-eyestalk Gazer may be an older renamed beholder concept. Modern DDB Gazer is a different candidate; resolve identity before deciding anatomy or adding Beholder. |
| [JOB-0052 Gorgimera](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/gorgimera.png>) | IDENTITY_REVIEW | Gorgimera humanoid reptile chimera form; need older counterpart. |
| [JOB-0053 Griffon](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/griffon.png>) | WATCHLIST | Griffon scaled armored body and reptilian tail, little lion body. |
| [JOB-0066 Night Hag](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/night-hag.png>) | WATCHLIST | Night hag reads pale vampire sorceress, lacks bulky hag character. |
| [JOB-0067 Nixie](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/nixie.png>) | IDENTITY_REVIEW | Nixie fishlike biped rather than small water fey; source needed. |
| [JOB-0070 Owlbear](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/owlbear.png>) | WATCHLIST | Owlbear body plated/scaly, limited bear fur. |
| [JOB-0074 Rakshasa](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/rakshasa.png>) | WATCHLIST | Rakshasa reads lion not tiger; reversed palms unclear. |
| [JOB-0081 Spigazu](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/spigazu.png>) | IDENTITY_REVIEW | Spigazu winged reptile humanoid; source needed. |
| [JOB-0082 Sprite](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/sprite.png>) | WATCHLIST | Sprite reptilian goblinlike rather than tiny winged person. |
| [JOB-0087 Tunnel Lurk](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/tunnel-lurk.png>) | IDENTITY_REVIEW | Tunnel Lurk armored grub with claw limbs; source needed. |
| [JOB-0095 Winter Wolf](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/winter-wolf.png>) | WATCHLIST | Winter Wolf has reptilian armor/spines. |
| [JOB-0096 Wolfwere](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/wolfwere.png>) | IDENTITY_REVIEW | Wolfwere pictured wolf-man hybrid; older counterpart needed. |
| [JOB-0100 Xorn](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/xorn.png>) | WATCHLIST | Xorn three eyes but only two clear arms/legs; rear limb visibility unresolved. |
| [JOB-0101 Yeti](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/yeti.png>) | WATCHLIST | Yeti carries club and tailored gear, closer to giant than wild yeti. |
| [JOB-0107 Field Plate](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/armor/field-plate.png>) | WATCHLIST | Field Plate is just a breastplate; category may imply a fuller suit in older rules. |
| [JOB-0122 Splint Mail](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/armor/splint-mail.png>) | WATCHLIST | Splint Mail uses broad horizontal rectangular plates rather than clear narrow vertical splints. |
| [JOB-0191 Curragh](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/equipment/curragh.png>) | WATCHLIST | Curragh looks like a carved dugout; verify older-edition boat construction reference. |
| [JOB-0238 Lantern, Bull's-Eye](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/equipment/lantern-bullseye.png>) | WATCHLIST | Bull's-Eye Lantern looks like an all-around lantern; directional lens/reflector is not clear. |
| [JOB-0342 Water Clock](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/equipment/water-clock.png>) | WATCHLIST | Water Clock appears to use a sealed hourglass arrangement; verify a readable water-flow clock mechanism. |
| [JOB-0349 Arquebus](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/arquebus.png>) | WATCHLIST | Arquebus resembles a later flintlock musket; check intended older firearm illustration. |
| [JOB-0353 Awl Pike](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/awl-pike.png>) | WATCHLIST | Awl Pike appears to have dagger proportions and a short hand grip; long pike shaft absent. |
| [JOB-0354 Bardiche](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/bardiche.png>) | WATCHLIST | Bardiche has a small halberd-like axe head rather than a long attached cleaver blade. |
| [JOB-0358 Bec de Corbin](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/bec-de-corbin.png>) | WATCHLIST | Bec de Corbin appears double-axed rather than beaked hammer/pick. |
| [JOB-0377 Guisarme](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/guisarme.png>) | WATCHLIST | Guisarme reads as another halberd; characteristic hooked blade unclear. |
| [JOB-0378 Guisarme-Voulge](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/guisarme-voulge.png>) | WATCHLIST | Guisarme-Voulge reads as another halberd; specialist polearm identity unclear. |
| [JOB-0389 Khopesh](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/khopesh.png>) | WATCHLIST | Khopesh reads as a recurved sword rather than a clear sickle-shaped khopesh. |
| [JOB-0392 Jousting Lance](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/lance-jousting.png>) | WATCHLIST | Jousting Lance resembles a sharp spear; tournament lance head and hand protection unclear. |
| [JOB-0398 Lucern Hammer](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/lucern-hammer.png>) | WATCHLIST | Lucern Hammer is a short-handled hammer rather than a long pole hammer. |
| [JOB-0402 Partisan](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/partisan.png>) | WATCHLIST | Partisan has a halberd axe blade instead of a symmetric spearhead with side projections. |
| [JOB-0417 Spetum](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/weapons/spetum.png>) | WATCHLIST | Spetum is a plain spear; distinctive side prongs absent. |
| [JOB-0441 Acrobatics](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/acrobatics.png>) | WATCHLIST | Acrobatics icon emphasizes lute and juggling props; performance is more prominent than balance/tumbling. |
| [JOB-0449 Arquebus](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/arquebus.png>) | WATCHLIST | Arquebus proficiency repeats a later flintlock-like firearm. |
| [JOB-0452 Awl Pike](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/awl-pike.png>) | WATCHLIST | Awl Pike proficiency repeats a short-handled spike. |
| [JOB-0454 Bardiche](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/bardiche.png>) | WATCHLIST | Bardiche proficiency repeats a generic halberd-like head. |
| [JOB-0488 Fauchard](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/fauchard.png>) | WATCHLIST | Fauchard proficiency is a perpendicular farming-scythe silhouette, unlike its equipment counterpart. |
| [JOB-0499 Guisarme](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/guisarme.png>) | WATCHLIST | Guisarme proficiency repeats a halberd-like axe head. |
| [JOB-0500 Guisarme-Voulge](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/guisarme-voulge.png>) | WATCHLIST | Guisarme-Voulge proficiency repeats a halberd-like head. |
| [JOB-0540 Lucern Hammer](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/lucern-hammer.png>) | WATCHLIST | Lucern Hammer proficiency is a short barrel-headed mallet rather than pole hammer. |
| [JOB-0582 Spetum](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/proficiencies/spetum.png>) | WATCHLIST | Spetum proficiency repeats a plain spear, missing side prongs. |
| [JOB-0627 Animal Growth](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/animal-growth.png>) | WATCHLIST | Animal Growth uses a mouse with a bear-shaped shadow, suggesting species change rather than enlargement. |
| [JOB-0657 Blink](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/blink.png>) | WATCHLIST | Blink uses duplicated bells; may read as sound/illusion rather than intermittent disappearance. |
| [JOB-0797 Glass Steel](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/glass-steel.png>) | WATCHLIST | Glass Steel shows shattered glass beside a sword; may imply brittle glass rather than glass strengthened to steel (older-edition effect needs confirmation). |
| [JOB-0845 Leprechaun’s Lamentable Belaborment](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/leprechauns-lamentable-belaborment.png>) | WATCHLIST | Leprechaun naming drives shamrock/Ireland imagery. Confirm whether this is an intentional homebrew identity or a renamed Leomund spell; avoid treating an alias as new spell lore. |
| [JOB-0846 Leprechaun’s Secret Chest](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/leprechauns-secret-chest.png>) | WATCHLIST | Leprechaun naming drives shamrock/Ireland imagery. Confirm whether this is an intentional homebrew identity or a renamed Leomund spell; avoid treating an alias as new spell lore. |
| [JOB-0847 Leprechaun’s Secure Shelter](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/leprechauns-secure-shelter.png>) | WATCHLIST | Leprechaun naming drives shamrock/Ireland imagery. Confirm whether this is an intentional homebrew identity or a renamed Leomund spell; avoid treating an alias as new spell lore. |
| [JOB-0848 Leprechaun’s Tiny Hut](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/leprechauns-tiny-hut.png>) | WATCHLIST | Leprechaun naming drives shamrock/Ireland imagery. Confirm whether this is an intentional homebrew identity or a renamed Leomund spell; avoid treating an alias as new spell lore. |
| [JOB-0849 Leprechaun’s Trap](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/leprechauns-trap.png>) | WATCHLIST | Leprechaun naming drives shamrock/Ireland imagery. Confirm whether this is an intentional homebrew identity or a renamed Leomund spell; avoid treating an alias as new spell lore. |
| [JOB-0908 Pass Without Trace](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/spells/pass-without-trace.png>) | WATCHLIST | Pass Without Trace shows a deep, clear footprint in snow; consider a disappearing footprint so the effect does not read backwards. |
| [JOB-1168 Awakened Tree](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/awakened-tree.png>) | WATCHLIST | Awakened Tree looks treant warrior; tree silhouette heavily anthropomorphized. |
| [JOB-1179 Bearded Devil](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/bearded-devil.png>) | WATCHLIST | Bearded devil ordinary beard and axelike weapon, compare tentacular beard/glaive. |
| [JOB-1196 Constrictor Snake](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/constrictor-snake.png>) | WATCHLIST | Constrictor snake has large venom fangs. |
| [JOB-1199 Crawling Claw](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/crawling-claw.png>) | WATCHLIST | Crawling claw fingers appear elongated/spiderlike; count needs close inspection. |
| [JOB-1209 Dire Wolf](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/dire-wolf.png>) | WATCHLIST | Dire Wolf wears substantial metal armor. |
| [JOB-1240 Giant Constrictor Snake](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/giant-constrictor-snake.png>) | WATCHLIST | Giant Constrictor Snake has prominent venom fangs. |
| [JOB-1270 Gold Dragon](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/gold-dragon.png>) | WATCHLIST | Gold dragon generic spiky silhouette; whiskers/sail traits absent. |
| [JOB-1273 Green Dragon](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/green-dragon.png>) | WATCHLIST | Green dragon generic silhouette; distinctive high neck crest unclear. |
| [JOB-1276 Grimlock](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/grimlock.png>) | WATCHLIST | Grimlock eye sockets dark but blindness not clearly apparent. |
| [JOB-1298 Killer Whale](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/killer-whale.png>) | WATCHLIST | Killer Whale retains orca pattern but has sharklike triangular teeth and enormous monster mouth. |
| [JOB-1300 Kraken](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/kraken.png>) | WATCHLIST | Kraken resembles armored squid; edition variation needs review. |
| [JOB-1318 Merrow](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/merrow.png>) | EDITION_REVIEW | Merrow has two legs and separate tail rather than aquatic serpentine lower body. |
| [JOB-1370 Silver Dragon](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/silver-dragon.png>) | WATCHLIST | Silver Dragon generic spiky dragon; characteristic tall head frill unclear. |
| [JOB-1377 Stone Giant](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/stone-giant.png>) | WATCHLIST | Stone Giant rendered as craggy rock elemental/golem rather than gray-skinned giant. |
| [JOB-1402 Water Elemental](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/water-elemental.png>) | WATCHLIST | Water Elemental wears solid metal shoulder armor and belt; fluid body remains recognizable. |
| [JOB-1407 White Dragon](<C:/Projects/FoundryVTT/DakksUltimateTokens/masters/creatures/white-dragon.png>) | WATCHLIST | White Dragon has generic spiky head; characteristic swept-back crest unclear. |

**Cleared:** JOB-1360 Sahuagin Baron has four arms and two legs in the full-size master. Withdraw the initial sheet-level concern; do not reroll it for arm count. Xorn remains only a visibility review because a rear limb could be occluded.

## Likely causes and recommended correction process

The following is an inference from the queue and images, not a model-internal diagnosis. Several anatomy briefs appear derived from attack entries, and generic armor language is overriding distinctive body plans. For example, Basilisk’s brief names a biting head and hard shell but not eight legs; Couatl’s brief explicitly introduces a clawed limb; Remorhaz gets a biting head and fused plating without a segmented many-legged body. Conversely, Glabrezu’s two fists/two pincers were specified but were not all rendered, so prompt completeness alone is not sufficient.

Chill Touch’s brief explicitly asks for frost, so an unchanged reroll is likely to preserve its misleading cold cue. Hand Quarrel’s brief calls it an unadorned piercing weapon without identifying it as crossbow ammunition. Rope Trick’s hanging-rope brief needs a clearer refuge/climbing cue rather than a loop that reads as a noose. The Leprechaun spell group may illustrate a renamed proper noun literally; establish the source mapping first.

1. Claude/Fable establish canonical identity, source edition and any legitimate alternate body plan.
2. Claude corrects subject briefs with physical anatomy separately from attack count: total arms/legs/heads, attachment locations, rear-body type, wings, surface material and defining silhouette.
3. Specify what must remain visible. Avoid relying on an unseen rear limb where the count defines the creature.
4. Review original-size candidate, official reference and corrected brief together; authorize an explicit reroll list. Keep style/reference requirements unchanged.
5. Run the established importer/gate workflow only during the separately authorized generation pass. A sharper polish does not repair an incorrect design.

## Missing universal subjects and mapping proposals

This is a prioritized expansion shortlist, not an exhaustive difference against every D&D Beyond listing. Exact-name absence was checked against the entire queue, including creatures stored as equipment. Possible aliases and existing specialist forms are explicitly separated from new art.

| Area | Recommendation | Reference |
|---|---|---|
| Creatures, first | Displacer Beast, Intellect Devourer, Nothic, Myconid Adult and Flumph. | Individual catalog links in CSV |
| Base creatures | Resolve base Kuo-toa, Quaggoth and Mind Flayer: specialist forms already exist. | Individual catalog links in CSV |
| Identity first | Resolve Beholder/Gazer, Carrion Crawler/Corpse Ravager, Umber Hulk/Tunnel Lurk. These are unconfirmed proposed mappings, not established aliases. | Individual catalog links in CSV |
| Further core families | Generic slaadi and core modrons; dragon immature silhouettes only if a shared adult painting is insufficient. | Core catalog links in CSV |
| Playable species | Dragonborn, Tiefling, Goliath, Aasimar; decide reuse versus playable variants for existing Orc and Half-Orc. | [Official species catalog](https://www.dndbeyond.com/species) |
| Classes | Barbarian, Monk, Sorcerer, Warlock. Map Mage/Wizard, Thief/Rogue and Invoker/Evoker before adding duplicates. | [Official classes](https://www.dndbeyond.com/classes) |
| Weapons | Rapier; consider distinct Greataxe, Greatclub and Maul silhouettes after checking existing related art. | [Official equipment](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/equipment) |
| Gear | Crowbar, caltrops, ball bearings, manacles, healer’s kit, component pouch, holy water and shovel. Check kit/alias coverage before adding Tinderbox, Waterskin, Thieves’ Tools or Alchemist’s Fire. | [Official equipment](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/equipment) |
| Spells | Mage Hand, Eldritch Blast, Guidance, Sacred Flame, Thaumaturgy, Prestidigitation, Fire Bolt, Ray of Frost, Healing Word, Misty Step, Counterspell, Revivify, Spirit Guardians, Hunter’s Mark. | [Official spell lists](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/spells) |
| Skills | Add or map modern skill labels. Existing older proficiencies cover some concepts; do not duplicate Arcana/Spellcraft, Medicine/Healing or Performance/Perform without a reason. | [Core class skill lists](https://www.dndbeyond.com/sources/dnd/br-2024/character-classes) |
| Magic items | Named Potion of Healing, Bag of Holding and Portable Hole coverage. Random-table icons do not prove a dedicated item image exists. | [Official item catalog](https://www.dndbeyond.com/magic-items) |

Keep named campaign monsters, setting-specific peoples/gear/spells, and third-party manuals on separate future lists. Artificer and other options with source/scope ambiguity can wait for an explicit universal expansion decision. No new background/feat system is proposed by this image audit.

## Handoff decisions requested from Claude

Approve or reject each priority candidate; resolve the identity/edition rows with Fable; approve a canonical mapping table and a bounded universal additions list. The audit ledger preserves dimensions from saved files (`capture_px` included), and source generation model labels are copied from historical ledgers rather than guessed. This audit made no image-tool call, so it provides no new claim about the tool’s model or interface relative to the earlier generation runs.

Queue snapshot SHA-256: `a40ba311267728a971feaa1748226fbec70b4f023b808766f2301e3c6e5f1f8b`. Per-image hashes record the files present when the ledger was built. Contact sheets were created earlier during this sweep; these records are not a transaction lock or a start-to-finish source-change check.
