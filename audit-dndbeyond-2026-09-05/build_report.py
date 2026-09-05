"""Build audit documents only; source library is read-only. No image processing."""
import csv, json, hashlib, html, re
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from PIL import Image

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
rows = sorted(csv.DictReader((ROOT/'upload/ASSETS-universal.csv').open(encoding='utf-8-sig')), key=lambda r:r['job_id'])
notes = {f'JOB-{n:04d}':(severity,note) for n,severity,note in json.loads((OUT/'reviewed-notes.json').read_text())}
refs = {r['job_id']:r for r in json.loads((OUT/'source-comparisons.json').read_text())}
versions = json.loads((ROOT/'art/versions.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ''
def dims(p):
    if not p.is_file(): return 'unavailable'
    with Image.open(p) as im: return 'x'.join(map(str,im.size))
def link(label,p): return f'[{label}](<{p.as_posix()}>)'
def csvwrite(name,data):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)

# Attribution is copied from existing generation records, never inferred from this audit's model.
gen={}
for p in sorted(ROOT.glob('results-*.jsonl')):
    for line in p.read_text(encoding='utf-8-sig').splitlines():
        try:r=json.loads(line)
        except ValueError:continue
        if r.get('status') in ('generated','ok','imported'):gen[r.get('job_id')]=r

ledger=[];positions=Counter()
for r in rows:
    job=r['job_id'];key=r['art_dir']+'/'+r['filename_stem'];p=ROOT/'masters'/f'{key}.png'
    capture=ROOT/'masters/_captures'/f'{key}.png'
    severity,note=notes.get(job,('screened','No obvious gross subject mismatch found in contact-sheet screening.'))
    ref=refs.get(job,{})
    if not p.is_file():
        assert job=='JOB-0033', f'Unexpected missing master: {job}'
        p=ROOT/'_superseded/creatures/behir-2026-09-05-polish-v2-rejected-legs.png'
        capture=ROOT/'_superseded/creatures/behir-2026-09-05-polish-v2-rejected-legs-capture.png'
        status='RETIRED';priority='P0';sheet='';tile='';recommend='Already retired. Reviewer should correct anatomical brief and authorize a new generation; do not restore this rejected image.'
    else:
        group='sheets' if r['art_dir']=='creatures' else 'other-sheets';pos=positions[group];positions[group]+=1
        sheet=f'{group}/sheet-{pos//12+1:02d}.png';tile=pos%12+1
        if severity=='cleared':status='CLEARED';priority='';recommend='Keep; close-up inspection cleared the initial concern.'
        elif job=='JOB-1318':status='EDITION_REVIEW';priority='P2';recommend='Resolve intended edition/body plan with Fable. Preserve an older variant if justified; create a separate modern variant when anatomy differs.'
        elif severity=='unmatched':status='IDENTITY_REVIEW';priority='P2';recommend='Resolve original book/edition and canonical identity before a reroll or duplicate addition.'
        elif severity=='major':status='PRIORITY_REVIEW';priority='P1';recommend='Claude should inspect the original with the cited reference or intended-edition source, correct the brief, and decide whether to retire/requeue.'
        elif severity=='review':status='WATCHLIST';priority='P2';recommend='Check at full size and against intended edition; no automatic retirement for pose, occlusion, costume, or style alone.'
        else:status='SCREENED';priority='';recommend='No reroll proposed by this sweep; this is not exhaustive canon certification.'
    evidence=ref.get('method','local_visual_only')
    if status=='CLEARED':evidence='local_full_size_and_queue_constraint'
    ledger.append(dict(job_id=job,display_name=r['display_name'],category=r['art_dir'],status=status,priority=priority,evidence=evidence,source_url=ref.get('source_url',''),reference_traits=ref.get('reference_traits',''),observation=note,recommendation=recommend,reviewed_image=str(p),master_sha256=sha(p),master_px=dims(p),capture_px=dims(capture),capture_path=str(capture) if capture.is_file() else '',accepted_version=versions.get(key,1) if status!='RETIRED' else 'rejected polish v2',generation_model_record=gen.get(job,{}).get('model','unreported in source ledger'),contact_sheet=sheet,tile=tile))
csvwrite('full-sweep-ledger.csv',ledger)
(OUT/'full-sweep-ledger.json').write_text(json.dumps(ledger,indent=2),encoding='utf-8')
counts=Counter(r['status'] for r in ledger)
snapshot=dict(created_at=datetime.now(timezone.utc).isoformat(),queue_sha256=sha(ROOT/'upload/ASSETS-universal.csv'),versions_sha256=sha(ROOT/'art/versions.json'),aliases_sha256=sha(ROOT/'art/aliases.json'),row_count=len(rows),active_masters=sum(positions.values()),contact_sheets={'creatures':29,'other':89},status_counts=dict(counts),direct_official_art_comparisons=sum(x['method']=='official_art_viewed' for x in refs.values()),direct_official_text_comparisons=sum(x['method']=='official_text_compared' for x in refs.values()))
(OUT/'snapshot.json').write_text(json.dumps(snapshot,indent=2),encoding='utf-8')

missing=[]
def add(category,names,priority,action,reason,source):
    for name in names.split('|'):
        matches=[r['job_id']+' '+r['display_name'] for r in rows if re.sub(r'[^a-z0-9]','',r['display_name'].lower())==re.sub(r'[^a-z0-9]','',name.lower())]
        missing.append(dict(category=category,subject=name,priority=priority,action=action,reason=reason,exact_name_matches='; '.join(matches),reference_url=source,scope='universal across editions; exclude setting-specific and third-party variants'))
B='https://www.dndbeyond.com/'
for name,slug in [('Displacer Beast','17130-displacer-beast'),('Intellect Devourer','17163-intellect-devourer'),('Nothic','17092-nothic'),('Myconid Adult','17183-myconid-adult'),('Flumph','17145-flumph')]:
    add('creatures',name,'A','new subject candidate','No matching subject name or confirmed alias in the current queue.',B+'monsters/'+slug)
for name,slug,existing in [('Kuo-toa','17166-kuo-toa','Archpriest, Monitor and Whip'),('Quaggoth','17193-quaggoth','Thonot'),('Mind Flayer','17104-mind-flayer','Mindflayer Arcanist')]:
    add('creatures',name,'A','base creature mapping or new art','Only '+existing+' represented. Fable should decide whether existing art also represents the base creature.',B+'monsters/'+slug)
for name,slug,existing in [('Beholder','17099-beholder','Gazer JOB-0049'),('Carrion Crawler','17138-carrion-crawler','Corpse Ravager JOB-0040'),('Umber Hulk','17205-umber-hulk','Tunnel Lurk JOB-0087')]:
    add('creatures',name,'A','identity mapping first','Possible renamed counterpart: '+existing+'. This is a hypothesis, not an established alias. Review its anatomy before sharing art.',B+'monsters/'+slug)
add('creatures','Blue Slaad|Death Slaad','B','new universal family candidates','Use generic Monster Manual forms; setting-specific individuals and variants are deferred.',B+'monsters/17112-blue-slaad')
add('creatures','Modron Monodrone|Modron Duodrone|Modron Tridrone|Modron Quadrone|Modron Pentadrone','B','new universal family candidates','Core bestiary forms only; campaign-specific planar expansions are separate.',B+'monsters/5195129-modron-monodrone')
add('creatures','Dragon wyrmling and young silhouettes','B','age variant decision','Ten dragon colors exist as one image each. Do not multiply identical art for every age stat block; add immature silhouettes only where useful.',B+'monsters/16811-blue-dragon-wyrmling')
add('races/species','Dragonborn|Tiefling|Goliath|Aasimar','A','new playable subject candidates','Current race folder contains only Dwarf, Elf, Gnome, Half-Elf, Halfling and Human.',B+'species')
add('races/species','Half-Orc|Orc','A','reuse or playable variant decision','Creature art already exists. Decide whether it suits playable-character presentation; avoid blindly duplicating it into races.',B+'species')
add('classes','Barbarian|Monk|Sorcerer|Warlock','A','new class icon candidates','No corresponding class row. Keep depiction generic rather than tied to a patron, nation, or setting.',B+'classes')
add('classes','Wizard|Rogue|Evoker','A','alias review','Likely existing class-art coverage via Mage, Thief and Invoker respectively; names and compendium rules remain edition-specific.',B+'sources/dnd/br-2024/character-classes')
add('weapons','Rapier|Greataxe|Greatclub|Maul','A','new silhouette or existing-art mapping','No exact queue name. Compare against current swords, battle axe, club and war hammer before adding distinct two-handed forms.',B+'sources/dnd/basic-rules-2014/equipment')
add('equipment','Crowbar|Caltrops|Ball Bearings|Manacles|Healer’s Kit|Component Pouch|Holy Water|Shovel','A','new equipment icon candidates','No exact subject row found; generic bags, spell icons or tools in proficiency art are not automatically item coverage.',B+'sources/dnd/basic-rules-2014/equipment')
add('equipment','Tinderbox|Waterskin|Thieves’ Tools|Alchemist’s Fire','B','alias or expanded kit review','Potential coverage via Flint and Steel, Wineskin, Thieves’ Picks, and Greek Fire. Verify kit contents and identity before adding art.',B+'sources/dnd/basic-rules-2014/equipment')
add('spells','Mage Hand|Eldritch Blast|Guidance|Sacred Flame|Thaumaturgy|Prestidigitation|Fire Bolt|Ray of Frost|Healing Word|Misty Step|Counterspell|Revivify|Spirit Guardians|Hunter’s Mark','A','new spell-effect candidates','No exact spell row. Keep utility hand distinct from Spectral Hand, and spell effects distinct from similar-colored existing icons.',B+'sources/dnd/basic-rules-2014/spells')
add('skills','Athletics|Deception|Insight|Intimidation|Investigation|Perception|Persuasion','B','modern skill icon or mapping decision','No exact-name row in skills/proficiencies. Existing older skills may partially cover the visual concept; Fable decides semantic mapping.',B+'sources/dnd/br-2024/character-classes')
add('skills','Arcana|Medicine|Nature|Performance|Stealth|Sleight of Hand','B','mapping before new art','Compare Spellcraft, Healing, Animal Lore, Perform, Hide in Shadows/Move Silently, and Pick Pockets. Similarity is not automatic rules equivalence.',B+'sources/dnd/br-2024/character-classes')
add('magic items','Potion of Healing|Bag of Holding|Portable Hole','B','dedicated item coverage review','Potion/table icons and generic bags exist, but named item rows do not. Define item coverage separately from random-table category art.',B+'magic-items')
reference_overrides = {
    'Death Slaad': B+'monsters/17113-death-slaad',
    'Modron Duodrone': B+'monsters/5195128-modron-duodrone',
    'Modron Monodrone': B+'monsters/5195129-modron-monodrone',
    'Modron Pentadrone': B+'monsters/5195130-modron-pentadrone',
    'Modron Quadrone': B+'monsters/5195131-modron-quadrone',
    'Modron Tridrone': B+'monsters/5195132-modron-tridrone',
    'Potion of Healing': B+'magic-items/8960641-potion-of-healing',
    'Bag of Holding': B+'magic-items/9228356-bag-of-holding',
    'Portable Hole': B+'magic-items/9228932-portable-hole',
}
for candidate in missing:
    if candidate['subject'] in reference_overrides:
        candidate['reference_url'] = reference_overrides[candidate['subject']]
csvwrite('missing-and-mapping-candidates.csv',missing)

fable='''# Note for Fable: universal art mapping across editions

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
'''
(OUT/'FABLE-NOTE.md').write_text(fable,encoding='utf-8')

report=['# Universal library image audit for Claude','',
'Full local visual sweep completed: **1,407 active masters plus the already-retired Behir**, covering every one of the 1,408 queue rows. All 118 contact sheets were inspected. The sweep identifies gross subject/body-plan problems and confusing symbols; it is not a resolution, alpha, or intake-gate audit.',
'',f'**{counts["PRIORITY_REVIEW"]} active priority review candidates**, **{counts["WATCHLIST"]} watchlist rows**, **{counts["IDENTITY_REVIEW"]} unresolved identity rows**, **{counts["EDITION_REVIEW"]} explicit edition case**, and **1 retired Behir**. One initial concern was cleared at full size (Sahuagin Baron). Remaining rows have no obvious gross mismatch from this screening; they are not certified against every published illustration.',
'','**Evidence boundary:** 30 creature counterparts were visually compared with official D&D Beyond artwork, and 8 additional rows received direct official-text comparisons. Other flagged rows are local visual observations requiring the intended-edition source check. The CSV states evidence per row. D&D Beyond generally has no unique canonical illustration for every spell, proficiency, or table; those were screened for readable subject/effect identity.',
'','The accessible browser showed **Sign in** and did not share the user’s signed-in session. Public official pages and artwork were used. Giant Ape and Giant Sea Horse pages supplied no artwork through the inspected page links; Gazer’s inspected page did not expose artwork in this session. Those do not count as direct official-art comparisons. No claim is made to have searched the user’s entire purchased catalog.',
'','**Scope:** universal subjects across editions. Campaign-setting-specific and third-party book content is deferred. The queue labels rows `fantasy-d20 / generic`; that is insufficient to establish an edition for ambiguous anatomy. [Note for Fable](FABLE-NOTE.md) records the user’s expectation that the core rules add-on maps edition-specific compendiums. That integration was not inspected.',
'','No art, capture, queue, workbook, importer, aliases, or accepted version was changed. The existing `review_sheets.py` generated audit-only sheets. No generation/import or verify_gate run was needed for this read-only review.',
'','## Review package','',
'- [Full row ledger](full-sweep-ledger.csv) — every row, image path/hash, dimensions, revision, evidence, finding, recommendation and sheet/tile.',
'- [Flagged-image gallery](REVIEW-GALLERY.html) — searchable local originals with source links; click an image for full size.',
'- [Missing subjects and mapping candidates](missing-and-mapping-candidates.csv) — prioritized proposals, including mapping-only work.',
'- [Source comparison register](source-comparisons.json) and [snapshot](snapshot.json).',
'','## Shared art direction for any follow-up',
'The user explicitly reconfirmed that the whole module must retain uniform art direction. Follow [AGENTS.md](../AGENTS.md), the designated [generic style sheet](../upload/generic-sheet-01.png), and the authorized per-row generation route. Every generation uses that same reference and the freshly resolved prompt verbatim. Keep the TSR oil-painting treatment and isolated subject on flat magenta for the importer.',
'', 'For authorized polish, [POLISH-PASS-1.md](../POLISH-PASS-1.md) requires the approved capture first and the style sheet second. [POLISH-PREAMBLE.txt](../POLISH-PREAMBLE.txt) preserves pose, silhouette, anatomy, equipment, palette, lighting, framing and scale. It improves rendering only. Therefore a body-plan correction requires a reviewer-corrected brief and authorized reroll; the unchanged polish preamble would preserve the defect. Use D&D Beyond to establish identity and anatomy while retaining the module’s established visual style.',
'','## Coverage by category','', '| Category | Queue rows | Active images screened |','|---|---:|---:|']
for cat,total in Counter(r['art_dir'] for r in rows).items():report.append(f'| {cat} | {total} | {total-(1 if cat=="creatures" else 0)} |')
report += ['','## Review these first','',
'Start with body-plan failures: **Basilisk, Couatl, Otyugh, Remorhaz, Salamander, Glabrezu, Hippogriff, Grick, Flameskull and Cockatrice**. These change the recognizable creature, rather than merely its paint style. Behir is already retired and should stay out of the library pending an authorized corrected generation.',
'','Then address wrong-object/effect icons: **Hand Quarrel, Light Quarrel, Morning Star proficiency, Man Catcher and its proficiency, scale barding, Chill Touch, Hold Person and Rope Trick**. Arquebus Shot also needs the intended historical/edition reference. Review equipment and matching proficiency together.',
'','The source comparison establishes a discrepancy with the linked edition, not a blanket requirement to copy that illustration. Costume differences, an obscured limb, a different pose, or a different valid form do not alone justify retirement. Quasit, fiend equipment, and older-edition creatures especially need that judgment.',
'','## Priority candidates and retired Behir','', '| Job / image | Evidence | Finding | Official reference |','|---|---|---|---|']
for x in ledger:
    if x['status'] not in ('PRIORITY_REVIEW','RETIRED'):continue
    source=f'[D&D Beyond]({x["source_url"]})' if x['source_url'] else 'Intended-edition source still needed'
    report.append(f'| {link(x["job_id"]+" "+x["display_name"],Path(x["reviewed_image"]))} | {x["evidence"]} | {x["observation"]} | {source} |')
report += ['','## Watchlist and identity decisions','',
'These are review prompts, not a reroll order. Several are older-edition or naming issues. The local originals and contact-sheet locations are included in the ledger.',
'','| Job / image | Status | Observation |','|---|---|---|']
for x in ledger:
    if x['status'] in ('WATCHLIST','IDENTITY_REVIEW','EDITION_REVIEW'):
        report.append(f'| {link(x["job_id"]+" "+x["display_name"],Path(x["reviewed_image"]))} | {x["status"]} | {x["observation"]} |')
report += ['','**Cleared:** JOB-1360 Sahuagin Baron has four arms and two legs in the full-size master. Withdraw the initial sheet-level concern; do not reroll it for arm count. Xorn remains only a visibility review because a rear limb could be occluded.',
'','## Likely causes and recommended correction process','',
'The following is an inference from the queue and images, not a model-internal diagnosis. Several anatomy briefs appear derived from attack entries, and generic armor language is overriding distinctive body plans. For example, Basilisk’s brief names a biting head and hard shell but not eight legs; Couatl’s brief explicitly introduces a clawed limb; Remorhaz gets a biting head and fused plating without a segmented many-legged body. Conversely, Glabrezu’s two fists/two pincers were specified but were not all rendered, so prompt completeness alone is not sufficient.',
'','Chill Touch’s brief explicitly asks for frost, so an unchanged reroll is likely to preserve its misleading cold cue. Hand Quarrel’s brief calls it an unadorned piercing weapon without identifying it as crossbow ammunition. Rope Trick’s hanging-rope brief needs a clearer refuge/climbing cue rather than a loop that reads as a noose. The Leprechaun spell group may illustrate a renamed proper noun literally; establish the source mapping first.',
'','1. Claude/Fable establish canonical identity, source edition and any legitimate alternate body plan.',
'2. Claude corrects subject briefs with physical anatomy separately from attack count: total arms/legs/heads, attachment locations, rear-body type, wings, surface material and defining silhouette.',
'3. Specify what must remain visible. Avoid relying on an unseen rear limb where the count defines the creature.',
'4. Review original-size candidate, official reference and corrected brief together; authorize an explicit reroll list. Keep style/reference requirements unchanged.',
'5. Run the established importer/gate workflow only during the separately authorized generation pass. A sharper polish does not repair an incorrect design.',
'','## Missing universal subjects and mapping proposals','',
'This is a prioritized expansion shortlist, not an exhaustive difference against every D&D Beyond listing. Exact-name absence was checked against the entire queue, including creatures stored as equipment. Possible aliases and existing specialist forms are explicitly separated from new art.',
'','| Area | Recommendation | Reference |','|---|---|---|',
'| Creatures, first | Displacer Beast, Intellect Devourer, Nothic, Myconid Adult and Flumph. | Individual catalog links in CSV |',
'| Base creatures | Resolve base Kuo-toa, Quaggoth and Mind Flayer: specialist forms already exist. | Individual catalog links in CSV |',
'| Identity first | Resolve Beholder/Gazer, Carrion Crawler/Corpse Ravager, Umber Hulk/Tunnel Lurk. These are unconfirmed proposed mappings, not established aliases. | Individual catalog links in CSV |',
'| Further core families | Generic slaadi and core modrons; dragon immature silhouettes only if a shared adult painting is insufficient. | Core catalog links in CSV |',
'| Playable species | Dragonborn, Tiefling, Goliath, Aasimar; decide reuse versus playable variants for existing Orc and Half-Orc. | [Official species catalog](https://www.dndbeyond.com/species) |',
'| Classes | Barbarian, Monk, Sorcerer, Warlock. Map Mage/Wizard, Thief/Rogue and Invoker/Evoker before adding duplicates. | [Official classes](https://www.dndbeyond.com/classes) |',
'| Weapons | Rapier; consider distinct Greataxe, Greatclub and Maul silhouettes after checking existing related art. | [Official equipment](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/equipment) |',
'| Gear | Crowbar, caltrops, ball bearings, manacles, healer’s kit, component pouch, holy water and shovel. Check kit/alias coverage before adding Tinderbox, Waterskin, Thieves’ Tools or Alchemist’s Fire. | [Official equipment](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/equipment) |',
'| Spells | Mage Hand, Eldritch Blast, Guidance, Sacred Flame, Thaumaturgy, Prestidigitation, Fire Bolt, Ray of Frost, Healing Word, Misty Step, Counterspell, Revivify, Spirit Guardians, Hunter’s Mark. | [Official spell lists](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/spells) |',
'| Skills | Add or map modern skill labels. Existing older proficiencies cover some concepts; do not duplicate Arcana/Spellcraft, Medicine/Healing or Performance/Perform without a reason. | [Core class skill lists](https://www.dndbeyond.com/sources/dnd/br-2024/character-classes) |',
'| Magic items | Named Potion of Healing, Bag of Holding and Portable Hole coverage. Random-table icons do not prove a dedicated item image exists. | [Official item catalog](https://www.dndbeyond.com/magic-items) |',
'','Keep named campaign monsters, setting-specific peoples/gear/spells, and third-party manuals on separate future lists. Artificer and other options with source/scope ambiguity can wait for an explicit universal expansion decision. No new background/feat system is proposed by this image audit.',
'','## Handoff decisions requested from Claude','',
'Approve or reject each priority candidate; resolve the identity/edition rows with Fable; approve a canonical mapping table and a bounded universal additions list. The audit ledger preserves dimensions from saved files (`capture_px` included), and source generation model labels are copied from historical ledgers rather than guessed. This audit made no image-tool call, so it provides no new claim about the tool’s model or interface relative to the earlier generation runs.',
'',f'Queue snapshot SHA-256: `{snapshot["queue_sha256"]}`. Per-image hashes record the files present when the ledger was built. Contact sheets were created earlier during this sweep; these records are not a transaction lock or a start-to-finish source-change check.']
(OUT/'CLAUDE-REVIEW.md').write_text('\n'.join(report)+'\n',encoding='utf-8')

cards=[]
for x in ledger:
    if x['status']=='SCREENED':continue
    rel='../'+Path(x['reviewed_image']).relative_to(ROOT).as_posix()
    source=f'<a href="{html.escape(x["source_url"])}" target="_blank">Official reference</a>' if x['source_url'] else 'Source identity/edition check needed'
    cards.append('<article data-search="'+html.escape((x['job_id']+' '+x['display_name']+' '+x['category']+' '+x['status']).lower())+'"><a href="'+rel+'"><img loading="lazy" src="'+rel+'" alt="'+html.escape(x['display_name'])+'"></a><h2>'+html.escape(x['job_id']+' '+x['display_name'])+'</h2><b>'+x['status']+'</b><p>'+html.escape(x['observation'])+'</p><small>'+html.escape(x['evidence'])+'</small><p>'+source+'</p></article>')
gallery='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Universal library audit</title><style>body{font:16px system-ui;background:#17191d;color:#eee;margin:24px}a{color:#97c9ff}header{max-width:1000px}input{font:inherit;padding:12px;width:90%;max-width:700px;margin:12px 0}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}article{background:#272b31;padding:16px;border-radius:10px}img{width:100%;height:320px;object-fit:contain;background:#605c54}h2{font-size:18px}small{color:#bbc4ce}[hidden]{display:none}</style><header><h1>Universal library audit for Claude</h1><p>Flagged candidates and one cleared finding. All 1,407 active masters were screened. Only entries marked official_art_viewed were directly compared to official artwork. These are review recommendations, not retirement decisions.</p><p><a href="CLAUDE-REVIEW.md">Report</a> · <a href="full-sweep-ledger.csv">All rows</a> · <a href="missing-and-mapping-candidates.csv">Additions and mapping</a> · <a href="FABLE-NOTE.md">Fable note</a></p><label>Filter by name, job, category or status<br><input id="filter" placeholder="e.g. couatl, spells, PRIORITY_REVIEW"></label><p id="count"></p></header><main>'''+''.join(cards)+'''</main><script>const input=document.getElementById('filter'),cards=[...document.querySelectorAll('article')];function filter(){let n=0;for(const card of cards){card.hidden=!card.dataset.search.includes(input.value.toLowerCase());if(!card.hidden)n++}document.getElementById('count').textContent=n+' review entries shown'}input.addEventListener('input',filter);filter()</script></html>'''
(OUT/'REVIEW-GALLERY.html').write_text(gallery,encoding='utf-8')
assert len(ledger)==1408 and len({r['job_id'] for r in ledger})==1408
assert sum(positions.values())==1407
assert all(Path(r['reviewed_image']).is_file() for r in ledger)
assert all((OUT/r['contact_sheet']).is_file() for r in ledger if r['contact_sheet'])
print(json.dumps({'status_counts':dict(counts),'active_images':sum(positions.values()),'source_comparisons':len(refs),'missing_mapping_proposals':len(missing),'report':str(OUT/'CLAUDE-REVIEW.md')},indent=2))
