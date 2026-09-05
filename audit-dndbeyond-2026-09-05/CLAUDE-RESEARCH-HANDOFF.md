# Universal 2.0 — reference research and audit reconciliation

Research date: 2026-09-05. Prepared for Claude Code and Fable.

This is the saved handoff version of Codex's full research response. No artwork was generated or imported during this research. Saving this report was requested after the research-only response; the original audit ledger, queue, briefs, importer, workbook and library assets remain unchanged.

## Decisions supplied by Nick

1. Universal art is edition-agnostic and follows the most recognizable current D&D Beyond depiction, including for the 2e suite. Edition names map to universal slugs through core-rules modules and `art/aliases.json`; do not create duplicate edition art.
2. Gazer, Corpse Ravager, Tunnel Lurk and Spigazu are deliberate For Gold & Glory stand-ins for beholder, carrion crawler, umber hulk and spinagon. Retain their names and judge their anatomy from FG&G text. The five Leprechaun spells are Leomund renames and are briefed by effect.
3. Re-roll the approved anatomy/identity, weapon-identity, spell, gear-wearing and style-watchlist rows. Sahuagin Baron and Xorn are cleared for anatomy.
4. Every remaining row receives image-to-image polish. Re-rolls are logged as redesigns; large polish deltas as changes; the rest as polish.
5. Expansion is a later bounded phase. Campaign-setting and third-party subjects stay separate.

Claude owns briefs, queue, importer and review. Codex owns generation and import after the corrected briefs and new queue hash are published. This report is research, not a generation manifest or authorization to alter the queue.

## Scope and evidence

The named scope resolves to **107 existing rows**, interpreting the listed weapon/proficiency counterparts and the eight dragons from the original watchlist literally: 33 anatomy, 31 equipment/weapon, 12 spell, five gear-removal and 26 style rows. This expands the approximate “95”; Claude's corrected queue should establish the final exact manifest.

D&D Beyond supplies subject references. The module's established TSR oil-painting direction remains the rendering standard. Colors below describe reference appearances, not necessarily exclusive biological requirements. Limb totals describe body plans; an obscured limb is not evidence of an absent limb.

The research browser exposed public listings and their artwork but did not inherit Nick's authenticated session. Paywalled text was not treated as read. Explicit local-source fallbacks and the outstanding Triton full-body source check are noted below.

### Findings that change earlier audit assumptions

- Bronze Dragon now has a broad hammerhead-like skull. [Current reference](https://www.dndbeyond.com/monsters/5198155-adult-bronze-dragon)
- Erinyes can be heavily armored with fiery wings; red armor alone does not establish wrong identity. [Current reference](https://www.dndbeyond.com/monsters/5194988-erinyes)
- Bone Devil has wings in current artwork. [Current reference](https://www.dndbeyond.com/monsters/5194930-bone-devil)
- Kraken's current art supports an armored cephalopod-like silhouette. [Current reference](https://www.dndbeyond.com/monsters/5195097-kraken)
- Flameskull artwork includes different flame colors; green is not an unconditional requirement. [Current reference](https://www.dndbeyond.com/monsters/5194995-flameskull)

## A. Canonical notes for the re-roll scope

### Anatomy and identity — 33 rows

| Job | Subject and source | One-line body-plan note |
|---|---|---|
| JOB-0006 | [Chimera](https://www.dndbeyond.com/monsters/5194943-chimera) | One quadrupedal body, three distinct lion/goat/dragon heads, two membranous wings and one tail; mixed leonine fur and reptilian anatomy. |
| JOB-0032 | [Basilisk](https://www.dndbeyond.com/monsters/5194919-basilisk) | Low, broad reptile with eight short legs, one head and tail, no wings; current art uses blue-gray scales and crystalline dorsal spikes. |
| JOB-0033 | [Behir](https://www.dndbeyond.com/monsters/5194921-behir) | Long blue serpentine body with six pairs of legs, one horned head and tapering tail; no wings. |
| JOB-0034 | [Black Pudding](https://www.dndbeyond.com/monsters/5194925-black-pudding) | Amorphous black ooze with irregular lobes and extensible pseudopods; no fixed head, face, skeleton or limb count. |
| JOB-0036 | Brownie — FG&G, printed p. 305 | Tiny, roughly one-foot elf-like humanoid with pointed ears and ordinary humanoid limbs; wings are not prescribed by the text. |
| JOB-0039 | [Cockatrice](https://www.dndbeyond.com/monsters/5194949-cockatrice) | Rooster-like head and feathered body, two taloned legs, two wings and a long serpentine tail; current wings combine feathers and membrane. |
| JOB-0040 | Corpse Ravager — FG&G, printed p. 308 | Grub-like elongated body, numerous centipede-like legs and eight cuttlefish-like tentacles; a living crawler, with no prescribed color. |
| JOB-0041 | [Couatl](https://www.dndbeyond.com/monsters/5194953-couatl) | One elongated serpent with two rainbow-feathered wings and a tapering tail; no walking legs or humanoid arms. |
| JOB-0043 | [Dretch](https://www.dndbeyond.com/monsters/5194974-dretch) | Squat, bloated demon with two arms, two legs, clawed digits and large pointed ears; mottled green-gray flesh, no wings. |
| JOB-0046 | [Efreeti](https://www.dndbeyond.com/monsters/5194981-efreeti) | Muscular red/orange humanoid with two arms and two legs, curled horns and fiery hair; ornate clothing and a flame weapon suit the current depiction. |
| JOB-0049 | Gazer — FG&G, printed p. 320 | Levitating five-foot sphere with malleable eyes and toothed mouths; can manifest one dominant plus ten smaller eyes; wingless, without mandatory fixed eyestalks. |
| JOB-0060 | [Manticore](https://www.dndbeyond.com/monsters/5195115-manticore) | Leonine quadruped with a manlike face, shaggy mane, two batlike wings and a long tail ending in a cluster of spikes. |
| JOB-0062 | [Medusa](https://www.dndbeyond.com/monsters/5195118-medusa) | Humanlike body with two arms and two legs, one head and living snakes for hair; no obligatory serpentine lower body. |
| JOB-0067 | Nixie — FG&G, printed p. 339 | Small green-skinned aquatic humanoid with pointed ears, webbed fingers and toes, two arms and two legs; no fish tail. |
| JOB-0069 | [Otyugh](https://www.dndbeyond.com/monsters/5195151-otyugh) | Bulky, low body with three legs, two long grasping tentacles, a separate eye-bearing stalk and a huge toothed mouth; muddy gray-brown. |
| JOB-0075 | [Remorhaz](https://www.dndbeyond.com/monsters/5195181-remorhaz) | Long segmented blue insectile body with many paired legs, mandibles and broad lateral fins; orange heat glows between dorsal plates. |
| JOB-0076 | [Salamander](https://www.dndbeyond.com/monsters/5195193-salamander) | Red-orange humanoid upper body with two arms over a long serpentine lower body; no legs, with fiery spines and a spear. |
| JOB-0082 | [Sprite](https://www.dndbeyond.com/monsters/4775845-sprite) | Tiny pointed-eared humanoid with two arms, two legs and translucent insect wings; leaflike clothing and a small bow suit the reference. |
| JOB-0086 | [Triton](https://www.dndbeyond.com/species/1026405-triton) | Blue/green aquatic humanoid, two arms and two legs rather than a merfolk tail; public portrait verified, full-body details require Claude's accessible source check. |
| JOB-0087 | Tunnel Lurk — FG&G, printed p. 353 | Hulking ape-like body in black chitin, four-eyed beetle head with strong pincers, muscular clawed limbs; use an ape-like two-arm/two-leg arrangement. |
| JOB-1199 | [Crawling Claw](https://www.dndbeyond.com/monsters/5194954-crawling-claw) | One detached, withered hand and wrist, four fingers plus a thumb; no complete arm, torso or additional spider legs. |
| JOB-1224 | [Erinyes](https://www.dndbeyond.com/monsters/5194988-erinyes) | Winged humanoid with two arms, two legs and two feather-structured wings; current red-black armor, fiery wings, blade and binding implement are valid. |
| JOB-1225 | [Ettercap](https://www.dndbeyond.com/monsters/5194989-ettercap) | Hunched spider-faced humanoid with two arms and two legs, clustered eyes and mandibles; blue-purple chitin, no extra walking arms. |
| JOB-1228 | [Flameskull](https://www.dndbeyond.com/monsters/5194995-flameskull) | One floating disembodied skull surrounded by supernatural flame; no torso or limbs, and flame color can vary. |
| JOB-1255 | [Giant Sea Horse / Giant Seahorse](https://www.dndbeyond.com/monsters/4775820-giant-seahorse) | Upright seahorse body with tubular snout, segmented trunk, fins and a tightly curled tail; no horse legs, hooves or humanoid arms. |
| JOB-1264 | [Glabrezu](https://www.dndbeyond.com/monsters/5195041-glabrezu) | Four arms—two enormous pincer arms plus two smaller humanoid arms—two legs and one horned, canine-like head; reddish-brown, wingless. |
| JOB-1275 | [Grick](https://www.dndbeyond.com/monsters/5195061-grick) | Serpentine worm body with four tentacles around a central hard mouth/beak; current tentacles have suckers and clawlike tips; no walking legs. |
| JOB-1285 | [Hippogriff](https://www.dndbeyond.com/monsters/5195075-hippogriff) | Eagle head, two feathered wings and two taloned forelegs joined to a horse body with two hoofed hindlegs and a horsehair tail. |
| JOB-1305 | [Lemure](https://www.dndbeyond.com/monsters/5195105-lemure) | Slumped, melted mass of pink-gray flesh with a distorted face and amorphous lower body; clearly separated human arms are not mandatory in current art. |
| JOB-1318 | [Merrow](https://www.dndbeyond.com/monsters/5195121-merrow) | Monstrous aquatic humanoid upper body with two clawed arms and one elongated fishlike tail; no legs, blue-gray skin and reddish fins. |
| JOB-1346 | [Quasit](https://www.dndbeyond.com/monsters/4775835-quasit) | Small green horned demon with two clawed arms, two legs and a long thin tail; its default form is wingless. |
| JOB-1356 | [Rug of Smothering](https://www.dndbeyond.com/monsters/5194896-animated-rug-of-smothering) | Animated rectangular patterned textile that curls and wraps; no anatomical teeth, mouth, eyes or limbs are required. |
| JOB-1398 | [Vrock](https://www.dndbeyond.com/monsters/5195255-vrock) | Vulture-headed demon with two humanoid arms, two taloned legs and two feathered wings; gray-black plumage and a largely bare avian head. |

FG&G sources: [For Gold & Glory PDF](</C:/Projects/FoundryVTT/DnD2E/docs/For Gold & Glory.pdf>) and [local bestiary text](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/creatures/bestiary.yml). Printed pages are ten lower than PDF page numbers. Brownie and Nixie are local-source fallbacks because suitable public official D&D Beyond counterparts were not established.

The fourth stand-in was requested for reference but is not named in the 33-row reroll list:

| Job | Subject | FG&G body-plan note |
|---|---|---|
| JOB-0081 | Spigazu — printed p. 309 | Small, roughly three-foot spiked humanoid with leathery wings; humanoid arms and legs, with no mandatory color or tail specified. Twelve launchable spines do not prescribe the total number of body projections. |

Gazer's old “four small eyes” expectation and Corpse Ravager's old undead-beast interpretation are superseded. Neither should inherit anatomy from a similarly named WotC creature. Gazer's eleven eyes are a possible fully manifested arrangement, not a requirement for fixed WotC-style stalks.

### Weapons, ammunition, barding and proficiency counterparts — 31 rows

Each paired job receives the same silhouette note. Older weapons often lack exact D&D Beyond entries; the references distinguish historical form and FG&G item identity.

| Job(s) | Subject | Distinguishing silhouette and source |
|---|---|---|
| JOB-0129 | Full Scale Barding | Horse armor made of visibly overlapping small scales over backing, with full coverage; avoid large continuous plate panels. [D&D Beyond armor description](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/equipment) |
| JOB-0132 | Half Scale Barding | Overlapping-scale construction with reduced coverage; distinguish coverage from material rather than turning scales into plate panels. [D&D Beyond armor description](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/equipment) |
| JOB-0349, JOB-0449 | Arquebus | Long-barreled, wood-stocked matchlock with a visible slow-match mechanism; avoid a modern cartridge rifle. FG&G equipment/weapons text. |
| JOB-0350 | Arquebus Shot | Round lead ball ammunition, without cartridge casing or modern pointed bullet profile. FG&G weapons text. |
| JOB-0353, JOB-0452 | Awl Pike | Very long straight shaft with a narrow piercing spike; no axe blade or hook. [Historical description](https://www.1eonline.info/7ua/pike.htm) |
| JOB-0354, JOB-0454 | Bardiche | Large elongated curved axe/cleaver blade extending down the haft, commonly attached at two points. [Historical description](https://www.1eonline.info/7ua/bardiche.htm) |
| JOB-0358, JOB-0457 | Bec de Corbin | Dominant heavy crow's-beak pick, opposing hammer face and short top spike; distinguish it from Lucern's longer spike. [Historical description](https://www.1eonline.info/7ua/becdecorbin.htm) |
| JOB-0370, JOB-0488 | Fauchard | Curving scythe/sickle-derived blade mounted along the pole end for cutting and thrusting. [Historical description](https://www.1eonline.info/7ua/fauchard.htm) |
| JOB-0377, JOB-0499 | Guisarme | Pronounced recurved pruning-hook head with a cutting edge; the hook dominates the silhouette. [Historical description](https://www.1eonline.info/7ua/guisarme.htm) |
| JOB-0378, JOB-0500 | Guisarme-Voulge | Broad pole-cleaver blade combined with a substantial pulling hook; preserve both features. [Historical description](https://www.1eonline.info/7ua/guisarmevoulge.htm) |
| JOB-0389, JOB-0522 | Khopesh | One-handed sickle sword: straight lower blade transitions into a broad forward-curving hook, sharpened on its convex edge. FG&G identity; historical-form interpretation. |
| JOB-0392 | Jousting Lance | Long, heavy tapered lance with a deliberately blunted tournament tip; a hand guard can clarify mounted-jousting identity. FG&G weapons text. |
| JOB-0398, JOB-0540 | Lucern Hammer | Pronged hammer face, opposing beak and conspicuously long top spike; not a broad halberd axe. [Historical description](https://www.1eonline.info/7ua/lucernhammer.htm) |
| JOB-0399, JOB-0541 | Man Catcher | Long pole ending in open spring-loaded capturing jaws/arms, visibly designed to enclose a target. FG&G weapons text. |
| JOB-0402, JOB-0554 | Partisan | Broad central spear blade with paired small winglike/axe-shaped projections at its base. [Historical description](https://www.1eonline.info/7ua/partisan.htm) |
| JOB-0403 | Hand Quarrel | Short, stout fletched crossbow bolt with pointed head, scaled for a hand crossbow; no firearm cartridge. FG&G weapons text. |
| JOB-0405 | Light Quarrel | Fletched light-crossbow bolt, larger than the hand-crossbow version; retain compact bolt proportions. FG&G weapons text. |
| JOB-0417, JOB-0582 | Spetum | Long central spear point with two shorter side blades projecting diagonally forward; three clearly separated points. [Historical description](https://www.1eonline.info/7ua/spetum.htm) |
| JOB-0552 | Morning Star proficiency | Rigid haft with a fixed spiked striking head; a chain between head and handle would identify a flail. [Historical description](https://www.1eonline.info/7ua/xt.htm) |

FG&G sources: [weapons](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/weapons/weapons.yml), [equipment](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/equipment/equipment.yml), and the PDF equipment chapter. Historical links reproduce older polearm nomenclature; they are not current D&D Beyond rules entries. Quarrel package quantity “(10)” does not determine image subject count; the corrected brief and contract determine composition.

### Spell effects — 12 rows

These are effect requirements and suggested visual readings, not claims that the rules prescribe one official icon.

| Job | Spell | Canonical effect and visual implication |
|---|---|---|
| JOB-0627 | Animal Growth | Enlarges the same animal while preserving species and anatomy; a mouse becoming bear-shaped communicates a different effect. [FG&G text](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/spells-arcane/spells.yml:3539) |
| JOB-0657 | Blink | Repeated disappearance into, and return from, the Ethereal Plane; use fading/phasing rather than duplicated bells. [D&D Beyond](https://www.dndbeyond.com/spells/2618939-blink) |
| JOB-0672 | Chill Touch | Necromantic life-draining touch; a spectral or skeletal hand is readable, while snowflakes and ice imply the wrong damage identity. [D&D Beyond legacy description](https://www.dndbeyond.com/spells/2026-chill-touch) |
| JOB-0797 | Glass Steel | Glass or crystal retains its transparent appearance while becoming steel-strong; show an intact strengthened object, not shattered glass. [FG&G text](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/spells-arcane/spells.yml:5829) |
| JOB-0813 | Hold Person | Paralyzes a humanoid; communicate immobilization, not opened shackles or escape. [D&D Beyond](https://www.dndbeyond.com/spells/2619153-hold-person) |
| JOB-0845 | Leprechaun's Lamentable Belaborment | Compelled discourse progresses through fascination, confusion and rage; the concept is overwhelming argument, not physical beating or shamrocks. [FG&G text](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/spells-arcane/spells.yml:3938) |
| JOB-0846 | Leprechaun's Secret Chest | A full-sized chest is hidden on the Ethereal Plane and recalled through a miniature replica; a fading chest and replica communicate the effect. [FG&G text](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/spells-arcane/spells.yml:3959), [D&D Beyond counterpart](https://www.dndbeyond.com/spells/2240-secret-chest) |
| JOB-0847 | Leprechaun's Secure Shelter | Creates a substantial small dwelling with protected entrances; use a sturdy house/shelter, distinct from Tiny Hut's magical field. [FG&G text](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/spells-arcane/spells.yml:3035) |
| JOB-0848 | Leprechaun's Tiny Hut | Stationary protective sphere/dome, opaque from outside and transparent within; use a magical enclosure rather than a wooden cottage. [FG&G text](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/spells-arcane/spells.yml:2258), [D&D Beyond counterpart discussion](https://www.dndbeyond.com/posts/1969-wizard-201-best-spells-for-wizards) |
| JOB-0849 | Leprechaun's Trap | Gives an object the false appearance of being trapped; suggest deceptive magical detection around a lock, not an actual explosive trap. [FG&G text](/C:/Projects/FoundryVTT/DnD2E/src/ad2e-core/spells-arcane/spells.yml:1418) |
| JOB-0908 | Pass Without Trace | Conceals passage and leaves no tracks; disappearing traces suit the effect, while a deep intact footprint reads backward. [D&D Beyond](https://www.dndbeyond.com/spells/2618849-pass-without-trace) |
| JOB-0959 | Rope Trick | Suspended climbing rope reaches an extradimensional refuge; indicate an upper entrance and avoid a hanging-noose silhouette. [D&D Beyond](https://www.dndbeyond.com/spells/2235-rope-trick) |

Animal Growth, Glass Steel, Lamentable Belaborment, Secure Shelter and Trap did not yield equivalent current public official D&D Beyond spell entries. Their supplied FG&G effects are the appropriate sources rather than unrelated modern spells or homebrew pages.

### Beasts/elements wearing gear — five rows

| Job | Subject and source | Body-plan note |
|---|---|---|
| JOB-0101 | [Yeti](https://www.dndbeyond.com/monsters/5195275-yeti) | Hulking white-furred ape-like creature with two arms, two legs, curved horns and long claws; remove tailored clothing and manufactured gear. |
| JOB-1209 | [Dire Wolf](https://www.dndbeyond.com/monsters/4775812-dire-wolf) | Large shaggy wolf with four legs, one canine head and one tail; natural fur without harness or armor. |
| JOB-1235 | [Giant Ape](https://www.dndbeyond.com/monsters/5195010-giant-ape) | Gorilla-like animal with two powerful arms, two legs and no tail; dark fur and bare chest/face, without worn gear. |
| JOB-1282 | [Hell Hound](https://www.dndbeyond.com/monsters/5195071-hell-hound) | Dark infernal canine with four legs, one head and one tail, fiery eyes/mouth; no wings or manufactured armor. |
| JOB-1402 | [Water Elemental](https://www.dndbeyond.com/monsters/5195261-water-elemental) | Cohesive moving water with wave/foam contours and optional fluid face/arms; no fixed solid skeleton or worn armor. |

### Style re-roll-and-compare — 26 rows

| Job | Subject and source | Body-plan and silhouette note |
|---|---|---|
| JOB-0001 | [Black Dragon](https://www.dndbeyond.com/monsters/5194869-adult-black-dragon) | Four legs, two wings and one tail; black scales, pale skull-like face and prominent forward-curving horns. |
| JOB-0002 | [Blue Dragon](https://www.dndbeyond.com/monsters/5194870-adult-blue-dragon) | Four legs, two wings and one tail; blue scales and a dominant curved nasal horn, rather than only paired brow horns. |
| JOB-0003 | [Brass Dragon](https://www.dndbeyond.com/monsters/5194871-adult-brass-dragon) | Four legs, two broad scalloped wings and one tail; brass-gold scales, long neck and broad head/cheek plates. |
| JOB-0004 | [Bronze Dragon](https://www.dndbeyond.com/monsters/5198155-adult-bronze-dragon) | Four legs, two wings and one tail; bronze scales, aquatic fins and the current broad hammerhead-like skull. |
| JOB-0007 | [Cloud Giant](https://www.dndbeyond.com/monsters/5194947-cloud-giant) | Huge humanoid with two arms and two legs, smooth pale-gray skin, white hair and fine clothing; no rock-golem body. |
| JOB-0023 | [Troll](https://www.dndbeyond.com/monsters/5195241-troll) | Lean, hunched green humanoid with two long arms, two legs, claws, patchy hair and an elongated hooked nose. |
| JOB-0053 | [Griffon](https://www.dndbeyond.com/monsters/5195062-griffon) | Eagle head, two feathered wings and two taloned forelegs; lion hindquarters with two paws and a leonine tail. |
| JOB-0066 | [Night Hag](https://www.dndbeyond.com/monsters/5195142-night-hag) | Horned, clawed humanoid with two arms and two legs; current blue skin and red hair are valid, and a bulky body is not mandatory. |
| JOB-0070 | [Owlbear](https://www.dndbeyond.com/monsters/5195152-owlbear) | Heavy bear body with four clawed limbs, owl facial disk and beak, feathered neck and furry body; no wings. |
| JOB-0074 | [Rakshasa](https://www.dndbeyond.com/monsters/5195178-rakshasa) | Tiger-headed humanoid with two arms, two legs and reversed hands; fine clothing, with white or orange tiger coloration acceptable. |
| JOB-0095 | [Winter Wolf](https://www.dndbeyond.com/monsters/5195272-winter-wolf) | White-gray wolf with four legs, one head and one tail; fur and icy breath/eyes, without reptilian armor plates. |
| JOB-1168 | [Awakened Tree](https://www.dndbeyond.com/monsters/5194906-awakened-tree) | Living tree trunk, branching crown and mobile roots; a subtle face is valid, but no fixed humanoid limb count is required. |
| JOB-1173 | [Balor](https://www.dndbeyond.com/monsters/5194911-balor) | Massive horned demon with two arms, two legs and two membranous wings; dark molten-looking flesh, sword and fiery whip. |
| JOB-1179 | [Bearded Devil](https://www.dndbeyond.com/monsters/5194920-bearded-devil) | Two-armed, two-legged humanoid devil with conspicuous writhing/tentacular beard and pole weapon; current purple flesh is valid. |
| JOB-1185 | [Bone Devil](https://www.dndbeyond.com/monsters/5194930-bone-devil) | Skeletal humanoid with two arms, two legs, wings and a long segmented stinging tail; pale exposed bone structure. |
| JOB-1196 | [Constrictor Snake](https://www.dndbeyond.com/monsters/4775809-constrictor-snake) | One continuous muscular snake body with no limbs or wings; patterned scales without exaggerated venom-delivery fangs. |
| JOB-1212 | [Dragon Turtle](https://www.dndbeyond.com/monsters/5194973-dragon-turtle) | Massive shelled aquatic reptile with one dragonlike head, four swimming limbs and a tail; spiked shell, gray-green scales and steam breath. |
| JOB-1240 | [Giant Constrictor Snake](https://www.dndbeyond.com/monsters/5195015-giant-constrictor-snake) | Enlarged boa/python-like snake with heavy coils and no limbs; current green patterned scales without oversized venom fangs. |
| JOB-1270 | [Gold Dragon](https://www.dndbeyond.com/monsters/5194873-adult-gold-dragon) | Four limbs, two flowing sail-like wings and a long tail; elongated golden body with whisker/streamer features around the head. |
| JOB-1273 | [Green Dragon](https://www.dndbeyond.com/monsters/5194874-adult-green-dragon) | Four legs, two wings and one long tail; slender green dragon with an elongated neck and reptilian head. |
| JOB-1276 | [Grimlock](https://www.dndbeyond.com/monsters/5195063-grimlock) | Pale blind humanoid with two arms and two legs, conspicuously sealed/absent eyes and coarse hair; no functional eyeballs. |
| JOB-1298 | [Killer Whale](https://www.dndbeyond.com/monsters/5195095-killer-whale) | Black-and-white orca with rounded head, two pectoral flippers, dorsal fin and horizontal tail flukes; no walking limbs. |
| JOB-1300 | [Kraken](https://www.dndbeyond.com/monsters/5195097-kraken) | Huge armored cephalopod-like body with numerous powerful tentacles; do not invent a fixed visible tentacle count from overlapping art. |
| JOB-1370 | [Silver Dragon](https://www.dndbeyond.com/monsters/5194876-adult-silver-dragon) | Four legs, two wings and one tail; silver scales, tall head/neck crest and pointed chin-beard silhouette. |
| JOB-1377 | [Stone Giant](https://www.dndbeyond.com/monsters/5195220-stone-giant) | Tall, lean, bald gray humanoid with two arms and two legs; continuous skin anatomy rather than assembled rock blocks. |
| JOB-1407 | [White Dragon](https://www.dndbeyond.com/monsters/5194877-adult-white-dragon) | Four legs, two wings and one tail; white icy scales, heavy neck and layered swept-back head crest. |

## B. Expansion mapping — all 78 original candidates

The requested three categories are not exhaustive. This table uses:

- **S**: included in SRD 5.1, usable under its applicable license.
- **PI**: explicitly named Product Identity in the SRD 5.1 OGL declaration; follow Nick's stand-in/alias policy.
- **N**: not an SRD 5.1 entry; absence alone does not establish PI or “2e-only.”
- **S52**: outside 5.1 but included in SRD 5.2.1.

Sources: [SRD 5.1 Creative Commons](https://media.dndbeyond.com/compendium-images/srd/5.1/SRD_CC_v5.1.pdf), [SRD 5.1 OGL Product Identity declaration](https://media.dndbeyond.com/compendium-images/srd/5.1/SRD-OGL_V5.1.pdf), [SRD 5.2.1](https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf).

None of these 78 candidates is accurately classified as “2e-only.” These classifications concern source content; they do not license reproduction of D&D Beyond illustrations. Alias proposals are art mappings, not declarations that the underlying rules are interchangeable.

Targets are existing logical paths beneath `art/`, with `.webp` omitted. “New” means a candidate for the later bounded additions queue. Candidate reuse requires visual/semantic review; it is not an implemented alias.

| # | Missing-list name | Class | Proposed coverage / recommendation |
|---:|---|:---:|---|
| 1 | Displacer Beast | PI | No confirmed existing stand-in; separate stand-in proposal before additions. |
| 2 | Intellect Devourer | N | No confirmed target; separate source/license review. |
| 3 | Nothic | N | No confirmed target; separate source/license review. |
| 4 | Myconid Adult | N | No target; the SRD's passing mention of myconids is not the Adult stat block. |
| 5 | Flumph | N | No confirmed target; separate source/license review. |
| 6 | Kuo-toa | N | Candidate `creatures/kuo-toa-monitor`; Fable should check whether specialist presentation suits the base creature. |
| 7 | Quaggoth | N | Candidate `creatures/quaggoth-thonot`; reuse if distinguishing features are not exclusively the specialist's. |
| 8 | Mind Flayer | PI | Candidate `creatures/mindflayer-arcanist`; review coverage before adding duplicate base art. |
| 9 | Beholder | PI | Confirmed mapping to `creatures/gazer`; FG&G anatomy governs the file. |
| 10 | Carrion Crawler | PI | Confirmed mapping to `creatures/corpse-ravager`. |
| 11 | Umber Hulk | PI | Confirmed mapping to `creatures/tunnel-lurk`. |
| 12 | Blue Slaad | N | No confirmed target; later source/stand-in decision. |
| 13 | Death Slaad | N | No confirmed target; later source/stand-in decision. |
| 14 | Modron Monodrone | N | No confirmed target; later source/stand-in decision. |
| 15 | Modron Duodrone | N | No confirmed target; later source/stand-in decision. |
| 16 | Modron Tridrone | N | No confirmed target; later source/stand-in decision. |
| 17 | Modron Quadrone | N | No confirmed target; later source/stand-in decision. |
| 18 | Modron Pentadrone | N | No confirmed target; later source/stand-in decision. |
| 19 | Dragon wyrmling and young silhouettes | S | Map to existing color files by default; genuinely different age silhouettes are later optional additions, not edition duplicates. |
| 20 | Dragonborn | S | New playable-species art. |
| 21 | Tiefling | S | New playable-species art. |
| 22 | Goliath | S52 | New candidate using SRD 5.2.1 provenance; do not label it SRD 5.1. |
| 23 | Aasimar | N | No confirmed target; source/license review, not “2e-only.” |
| 24 | Half-Orc | S | Candidate `creatures/half-orc`; check suitability as a player-facing portrait. |
| 25 | Orc | S | Candidate `creatures/orc`; 5.1 contains the monster, current playable-species treatment is in 5.2.1. |
| 26 | Barbarian | S | New class art. |
| 27 | Monk | S | New class art. |
| 28 | Sorcerer | S | New class art. |
| 29 | Warlock | S | New class art. |
| 30 | Wizard | S | `classes/mage`. |
| 31 | Rogue | S | `classes/thief`. |
| 32 | Evoker | S | `classes/invoker`; 5.1 provides School of Evocation, while Evoker is the later subclass label. |
| 33 | Rapier | S | New distinct slender thrusting-sword silhouette. |
| 34 | Greataxe | S | New two-handed axe silhouette unless existing art clearly supplies that form. |
| 35 | Greatclub | S | Candidate `weapons/club` for a generic icon; size alone need not require duplicate art. |
| 36 | Maul | S | New two-handed hammer silhouette; do not automatically equate it with a one-handed war hammer. |
| 37 | Crowbar | S | New equipment icon. |
| 38 | Caltrops | S | New equipment icon. |
| 39 | Ball Bearings | S | New equipment icon. |
| 40 | Manacles | S | New equipment icon. |
| 41 | Healer's Kit | S | New equipment kit icon. |
| 42 | Component Pouch | S | Candidate `equipment/belt-pouch-small`; use new art if visible components are needed. |
| 43 | Holy Water | S | New identifiable item icon. |
| 44 | Shovel | S | New equipment icon. |
| 45 | Tinderbox | S | Candidate `equipment/flint-and-steel`; representative tools, though not the entire kit. |
| 46 | Waterskin | S | `equipment/wineskin`. |
| 47 | Thieves' Tools | S | Candidate `equipment/thieves-picks`; representative tools rather than every kit component. |
| 48 | Alchemist's Fire | S | Candidate `equipment/oil-greek-fire`; shared incendiary-flask art, with rules remaining separate. |
| 49 | Mage Hand | S | New utility-hand effect; avoid automatically reusing Spectral Hand. |
| 50 | Eldritch Blast | S | New force-blast effect. |
| 51 | Guidance | S | New guidance/assistance effect. |
| 52 | Sacred Flame | S | New radiant effect, distinguishable from ordinary fire. |
| 53 | Thaumaturgy | S | New supernatural-sign/omen effect. |
| 54 | Prestidigitation | S | Candidate `spells/cantrip`; existing tiny magical-trick concept is a plausible art match. |
| 55 | Fire Bolt | S | New directed fire-projectile effect. |
| 56 | Ray of Frost | S | New directed cold-ray effect. |
| 57 | Healing Word | S | New spoken-healing effect. |
| 58 | Misty Step | S | New short teleport effect; Blink is not an exact effect match. |
| 59 | Counterspell | S | New interrupted-casting effect; avoid automatically reusing Dispel Magic. |
| 60 | Revivify | S | New immediate revival effect; distinguish from general resurrection art. |
| 61 | Spirit Guardians | S | New protective spiritual-presence effect. |
| 62 | Hunter's Mark | S | New marked-quarry effect. |
| 63 | Athletics | S | New general physical-exertion icon; climbing alone is partial coverage. |
| 64 | Deception | S | New deception icon; disguise alone is partial coverage. |
| 65 | Insight | S | New motive-reading/social-perception icon. |
| 66 | Intimidation | S | New intimidation icon. |
| 67 | Investigation | S | New deliberate examination/deduction icon. |
| 68 | Perception | S | New general awareness icon; hearing-only art is partial coverage. |
| 69 | Persuasion | S | New persuasion icon; etiquette is not an exact equivalent. |
| 70 | Arcana | S | `proficiencies/spellcraft`. |
| 71 | Medicine | S | `proficiencies/healing`. |
| 72 | Nature | S | Candidate `proficiencies/animal-lore`; current track/snare imagery is partial, so broader art may be preferable. |
| 73 | Performance | S | `proficiencies/perform`. |
| 74 | Stealth | S | Candidate `skills/move-silently`; select one representative image rather than duplicating older subskills. |
| 75 | Sleight of Hand | S | Candidate `skills/pick-pockets`; existing purse motif represents one important application. |
| 76 | Potion of Healing | S | New dedicated item icon; potion-table art does not establish healing-potion identity. |
| 77 | Bag of Holding | S | New dedicated magic-item icon; a generic pouch does not establish extradimensional storage. |
| 78 | Portable Hole | S | New dedicated magic-item icon. |

Classification totals: **58 S, five PI, 14 N and one S52**.

### Additional mappings outside the original 78-name list

| Incoming name | Existing universal target |
|---|---|
| Spinagon | `creatures/spigazu` |
| Leomund's Lamentable Belaborment | `spells/leprechauns-lamentable-belaborment` |
| Leomund's Secret Chest / Secret Chest | `spells/leprechauns-secret-chest` |
| Leomund's Secure Shelter / Secure Shelter | `spells/leprechauns-secure-shelter` |
| Leomund's Tiny Hut / Tiny Hut | `spells/leprechauns-tiny-hut` |
| Leomund's Trap | `spells/leprechauns-trap` |
| Animated Rug of Smothering | `creatures/rug-of-smothering` |
| Giant Seahorse | `creatures/giant-sea-horse` |

For Fable: resolve names through a category-aware alias mapping to one existing file. Cross-category cases, such as playable Orc using creature art, need explicit support. Art aliases must not merge edition-specific mechanics. WotC's Gazer homonym needs source-aware handling so it does not override FG&G Gazer identity.

## C. Full-sweep ledger reconciliation

The [original CSV ledger](/C:/Projects/FoundryVTT/DakksUltimateTokens/audit-dndbeyond-2026-09-05/full-sweep-ledger.csv) remains unchanged. This is the complete decision overlay for Claude to append; preserve original observations, evidence, hashes, dimensions and model records.

| Decision | Exact assignment | Rows |
|---|---|---:|
| `reroll` | Every job in the five re-roll tables in section A | 107 |
| `cleared` | JOB-0100 Xorn; JOB-1360 Sahuagin Baron | 2 |
| `polish` | Every other existing ledger row | 1,299 |
| `deferred` | No existing Universal row under the stated decisions | 0 |
| **Total** | | **1,408** |

Assignments were checked against the ledger in memory. Counts reconcile without duplicate assignments. The extra Spigazu reference table is not a reroll table: JOB-0081 defaults to polish.

For machine-readable reconciliation, these are the exact numeric job suffixes used in the research interpretation:

```json
{
  "anatomy_reroll": [6,32,33,34,36,39,40,41,43,46,49,60,62,67,69,75,76,82,86,87,1199,1224,1225,1228,1255,1264,1275,1285,1305,1318,1346,1356,1398],
  "weapon_reroll": [129,132,349,350,353,354,358,370,377,378,389,392,398,399,402,403,405,417,449,452,454,457,488,499,500,522,540,541,552,554,582],
  "spell_reroll": [627,657,672,797,813,845,846,847,848,849,908,959],
  "gear_reroll": [101,1209,1235,1282,1402],
  "style_reroll": [1,2,3,4,7,23,53,66,70,74,95,1168,1173,1179,1185,1196,1212,1240,1270,1273,1276,1298,1300,1370,1377,1407],
  "cleared": [100,1360],
  "default_existing_row_decision": "polish"
}
```

Cleared concerns still receive polish. Xorn and Sahuagin Baron are cleared for anatomy but covered by “every remaining row is polished.” Execution therefore comprises **107 redesign candidates and 1,301 polish candidates**.

Deferred applies to the later expansion lists, including setting and third-party work. An earlier identity-review flag does not itself defer an existing Universal row.

Retain a separate outcome field: rerolls are `redesign`; accepted image-to-image revisions become `change` or `polish` according to measured magnitude. Style-watchlist candidates remain subject to compare-and-keep-only-if-better review.

## Review handoff and supporting audit record

Claude should reconcile the 107-job interpretation against the final approved manifest, resolve the marked Triton full-body source check, apply the decision overlay without overwriting original audit evidence, and publish corrected briefs and the new queue hash before generation resumes.

The research interpretation includes the named weapon/proficiency pairs and eight flagged dragons, not an automatic expansion to every polearm or every dragon color. The exact published queue takes precedence once reviewed.

Supporting files from the original full sweep:

- [Original full-sweep review](/C:/Projects/FoundryVTT/DakksUltimateTokens/audit-dndbeyond-2026-09-05/CLAUDE-REVIEW.md)
- [Full-sweep ledger CSV — all 1,408 rows](/C:/Projects/FoundryVTT/DakksUltimateTokens/audit-dndbeyond-2026-09-05/full-sweep-ledger.csv)
- [Full-sweep ledger JSON](/C:/Projects/FoundryVTT/DakksUltimateTokens/audit-dndbeyond-2026-09-05/full-sweep-ledger.json)
- [Original 78 missing/mapping candidates](/C:/Projects/FoundryVTT/DakksUltimateTokens/audit-dndbeyond-2026-09-05/missing-and-mapping-candidates.csv)
- [Original Fable note](/C:/Projects/FoundryVTT/DakksUltimateTokens/audit-dndbeyond-2026-09-05/FABLE-NOTE.md)
- [Review gallery](/C:/Projects/FoundryVTT/DakksUltimateTokens/audit-dndbeyond-2026-09-05/REVIEW-GALLERY.html)

Earlier reference assumptions in those audit files remain historical evidence. The user decisions and current-reference corrections in this handoff supersede them for planning; the original files were not rewritten.
