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

// Optional dynamic token rings (core, Foundry 12+; off by default). When the world setting is on, a token
// placed from one of this module's actors gets the core ring with its own painting as the ring subject, unless
// the token already carries ring settings someone chose. In an ARS world the ring also flashes red on a loss
// of hit points and green on a gain, as dnd5e does for its own tokens (ARS has no ring code; dnd5e flashes
// rings itself, so no flash is added there). Every API is guarded: where the ring schema is missing, nothing.
const DAKK_MODULE = "dakks-ultimate-tokens";
const DAKK_RINGS = "dynamicRings";
// The painting's size relative to the ring's frame, written to ring.subject.scale (core minimum 0.5). Core
// draws the subject over the ring and never clips it, and an explicit subject texture turns off core's own
// fit, so at 1 a figure painted edge to edge (most of ours reach the square's edges) covers the ring band at
// head and feet and spills past it. Core's ring art puts the ring's outer edge at about 0.79 of the frame
// (ringThickness 0.127 + subject 0.667, TokenRing#subjectScaleAdjustment), so 0.8 sets the painting's square
// on the ring's outer edge: the band shows round the figure, the head and feet just overlap it. The ratio is
// the same at every token size because ring and subject scale together, so one value serves all sizes.
// Tune by eye.
const DAKK_RING_SCALE = 0.8;

Hooks.once("init", () => {
  game.settings.register(DAKK_MODULE, DAKK_RINGS, {
    name: "Dynamic token rings for Dakk's creatures",
    hint: "Tokens placed from this module's compendium actors get Foundry's dynamic token ring, with the "
      + "painting as the ring subject. Tokens that already have ring settings, and tokens of other modules, "
      + "are left alone. In an AD&D 2e (ARS) world the ring also flashes red on damage and green on healing.",
    scope: "world",
    config: true,
    type: Boolean,
    default: false,
  });
});

/** True when the actor was imported from one of this module's compendia (v12+ _stats, older sourceId flag). */
function dakkFromModule(actor) {
  const prefix = `Compendium.${DAKK_MODULE}.`;
  const sources = [actor?._stats?.compendiumSource, actor?._stats?.duplicateSource, actor?.flags?.core?.sourceId];
  return sources.some((s) => typeof s === "string" && s.startsWith(prefix));
}

function dakkRingsOn() {
  try { return game.settings.get(DAKK_MODULE, DAKK_RINGS) === true; } catch { return false; }
}

Hooks.on("preCreateToken", (token, data, options, userId) => {
  try {
    if (userId !== game.user.id || !dakkRingsOn()) return;
    const ring = token._source?.ring;
    if (!ring?.subject || !("enabled" in ring)) return;
    // Any choice already made on the prototype or the dropped data wins: enabled, a subject, a scale, colours.
    if (ring.enabled || ring.subject.texture || (ring.subject.scale ?? 1) !== 1
      || ring.colors?.ring || ring.colors?.background) return;
    const actor = token.actor ?? game.actors?.get(token.actorId);
    if (!dakkFromModule(actor)) return;
    const src = token._source.texture?.src;
    if (!src) return;
    token.updateSource({ "ring.enabled": true, "ring.subject.texture": src, "ring.subject.scale": DAKK_RING_SCALE });
  } catch (err) {
    console.warn("Dakk's Ultimate Tokens | could not set the token ring", err);
  }
});

// ARS keeps hit points at system.attributes.hp.value and temporary ones at system.attributes.hp.temp.hp.value.
// The old total travels in the update options (set where the update starts, read on every client), the way
// dnd5e carries its own; a synthetic token actor fires the same Actor hooks with the options passed through.
const dakkHp = (actor) => {
  const hp = actor?.system?.attributes?.hp;
  const v = Number(hp?.value), t = Number(hp?.temp?.hp?.value ?? 0);
  return Number.isFinite(v) ? v + (Number.isFinite(t) ? t : 0) : null;
};

Hooks.on("preUpdateActor", (actor, changes, options) => {
  try {
    if (game.system?.id !== "ars" || !dakkRingsOn()) return;
    if (!foundry.utils.hasProperty(changes, "system.attributes.hp")) return;
    const hp = dakkHp(actor);
    // keyed by actor, since one update operation can carry several actors
    if (hp !== null) ((options[DAKK_MODULE] ??= {}).hp ??= {})[actor.uuid] = hp;
  } catch { /* never block an update */ }
});

Hooks.on("updateActor", (actor, changed, options) => {
  try {
    if (game.system?.id !== "ars" || !dakkRingsOn() || !canvas?.ready) return;
    const before = options?.[DAKK_MODULE]?.hp?.[actor.uuid];
    const after = dakkHp(actor);
    if (typeof before !== "number" || after === null || after === before) return;
    const Color = foundry.utils.Color;
    const easing = foundry.canvas?.placeables?.tokens?.TokenRing?.easeTwoPeaks;
    const loss = after < before;
    // dnd5e's tokenRingColors: damage 0xFF0000 (500 ms, two peaks), healing 0x00FF00 (core default timing)
    const color = Color.from(loss ? 0xFF0000 : 0x00FF00);
    const anim = loss ? { duration: 500, ...(easing ? { easing } : {}) } : {};
    for (const t of actor.getActiveTokens?.(true) ?? []) {
      if (!t?.visible || !t.document?.ring?.enabled || typeof t.ring?.flashColor !== "function") continue;
      t.ring.flashColor(color, { ...anim }).catch?.(() => {});
    }
  } catch (err) {
    console.warn("Dakk's Ultimate Tokens | could not flash the token ring", err);
  }
});
