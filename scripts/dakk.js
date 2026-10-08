// Dakk's Ultimate Tokens: show each pack's top level in the order the module gives it.
//
// Foundry sorts a compendium's top level alphabetically unless the world has switched that pack to manual
// order (core setting collectionSortingModes, the sort button in the pack's window), so "CR 10" lands
// before "CR 2", "Cantrip" after "9th Level" and a catalogue's "Start here" in the middle. On a GM's load
// this sets the module's packs to manual order, once per pack and only where the world has recorded no
// choice; the sort button still toggles it. A pack is switched only when manual order is safe: its top level
// is all folders, or its top-level entries each carry their own sort value (a flat pack with none stays A-Z).
Hooks.once("ready", async () => {
  if (!game.user.isGM) return;
  const MODULE = "dakks-ultimate-tokens";
  const modes = foundry.utils.deepClone(game.settings.get("core", "collectionSortingModes") ?? {});
  const switched = [];
  for (const pack of game.packs) {
    if (pack.metadata.packageName !== MODULE || pack.collection in modes) continue;
    let index;
    try { index = await pack.getIndex({ fields: ["sort", "folder"] }); } catch (err) {
      console.warn(`Dakk's Ultimate Tokens | could not read ${pack.collection} to set its order`, err);
      continue;
    }
    const roots = index.filter((e) => !e.folder);
    const sorts = new Set(roots.map((e) => e.sort ?? 0));
    if (roots.length && sorts.size < roots.length) continue;
    modes[pack.collection] = "m";
    switched.push(pack);
  }
  if (!switched.length) return;
  await game.settings.set("core", "collectionSortingModes", modes);
  for (const pack of switched) pack.initializeTree?.();
  ui.compendium?.render();
});
