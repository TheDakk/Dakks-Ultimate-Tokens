#!/usr/bin/env python3
"""Turn a subject captured on a flat magenta key into a genuinely transparent RGBA PNG.

    python chroma_key.py capture.png master.png        key one file
    python chroma_key.py --inspect capture.png         say what the background is, key nothing

The image generator in use returns opaque RGB, so the prompt asks for the subject on one
flat pure-magenta fill (#FF00FF) and this keys it out. Pillow only; no numpy.

How the key is built, and why each step exists:
  1. Two alpha estimates per pixel, and the more OPAQUE one wins:
       - colour distance from the key (Chebyshev in RGB), ramped between INNER and OUTER;
       - magenta-ness, min(R,B) - G, which is linear in the blend fraction of subject over
         key and so tracks an anti-aliased painted outline closely.
     Taking the maximum protects subjects that are themselves purplish (a dragon's wing
     membrane) from being eroded: whichever estimate recognises them as subject prevails.
  2. Only pixels NEAR real background may be partially transparent. A pinkish highlight
     deep inside the subject is nowhere near a pure-key pixel and stays opaque; a real gap
     between two legs is pure key and stays clear.
  3. Spill is removed by subtracting the pixel's EXCESS magenta on the rim: where
     min(R,B) exceeds G by more than a small margin, red and blue are both reduced by the
     excess. This cannot produce green (green is never raised, red and blue never drop
     below green plus the margin), and it cannot touch a legitimate red or blue, whose
     min(R,B) is already low. Earlier versions un-mixed the key algebraically instead;
     that amplifies green whenever alpha is underestimated, which it always is on purples,
     and left green rims on wings and hair. Un-mixing is not used.

A capture whose border is NOT the key (white, checkerboard, scenery) is refused rather than
guessed at: keying the wrong colour silently ruins the master.
"""

from __future__ import annotations

import argparse
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageMath

KEY = (255, 0, 255)
INNER = 48          # colour distance at or below which a pixel is pure background
OUTER = 160         # colour distance at or above which a pixel is pure subject
BG_DEADZONE = 235   # magenta-ness at or above this is pure key      (alpha 0)
FG_DEADZONE = 20    # magenta-ness at or below this is pure subject  (alpha 255)
NEAR_BG_PX = 6      # how far from pure background a partial alpha or spill fix may reach
SPILL_MARGIN = 8    # rim pixels keep at most this much more red-and-blue than green
SPILL_PX = 3        # the spill fix reaches this far from pure background (narrower than the alpha ramp)
BLEED_MARGIN = 30        # dark/mid paint keeps at most this much more red-and-blue than green; real purples measured below 26
BLEED_MARGIN_BRIGHT = 12 # bright paint (luma above BRIGHT_LUMA) keeps far less: on white, even a little magenta reads as pink
BRIGHT_LUMA = 150
UNMIX_SHARE = 0.0        # algebraic un-mixing is OFF: even opaque-biased alpha is underestimated on pale edges and it overshoots into green
ROSE_MIN_R = 120         # rose desaturation applies only to reasonably bright pixels...
ROSE_MIN_G_SHARE = 0.68  # ...that are low in saturation (green at least this share of red)
ROSE_PULL = 0.5          # opaque rose loses half its cast; partially transparent rose (an edge blend by definition) loses all of it
SEED_MAGENTANESS = 150   # magenta-ness at or above which a pixel counts as background even if contaminated
BORDER_FRACTION = 0.03
BORDER_KEY_SHARE = 0.92


class KeyingError(RuntimeError):
    """The capture cannot be keyed safely; the reason says why."""


def _distance_from_key(rgb: Image.Image) -> Image.Image:
    """Chebyshev distance to KEY per pixel, as an L image (0..255)."""
    r, g, b = rgb.split()
    size = rgb.size
    dr = ImageChops.difference(r, Image.new("L", size, KEY[0]))
    dg = ImageChops.difference(g, Image.new("L", size, KEY[1]))
    db = ImageChops.difference(b, Image.new("L", size, KEY[2]))
    return ImageChops.lighter(ImageChops.lighter(dr, dg), db)


def _magentaness(rgb: Image.Image) -> Image.Image:
    """min(R,B) - G clamped to 0..255, as an L image. 255 = pure key, 0 = no magenta at all."""
    r, g, b = rgb.split()
    return ImageChops.subtract(ImageChops.darker(r, b), g)


def describe_background(im: Image.Image) -> dict:
    """What the border looks like: key share, and whether alpha already exists."""
    w, h = im.size
    bw, bh = max(2, int(w * BORDER_FRACTION)), max(2, int(h * BORDER_FRACTION))
    boxes = ((0, 0, w, bh), (0, h - bh, w, h), (0, 0, bw, h), (w - bw, 0, w, h))
    if "A" in im.getbands():
        alpha = im.getchannel("A")
        strips = [alpha.crop(box) for box in boxes]
        transparent = sum(sum(1 for v in a.getdata() if v <= 5) for a in strips)
        total = sum(a.size[0] * a.size[1] for a in strips)
        if transparent / total >= BORDER_KEY_SHARE:
            return {"kind": "alpha", "key_share": 0.0, "detail": "border is already transparent"}
    dist = _distance_from_key(im.convert("RGB"))
    strips = [dist.crop(box) for box in boxes]
    keyed = sum(sum(1 for v in s.getdata() if v <= INNER) for s in strips)
    total = sum(s.size[0] * s.size[1] for s in strips)
    share = keyed / total
    corner = tuple(im.convert("RGB").getpixel((2, 2)))
    kind = "magenta" if share >= BORDER_KEY_SHARE else "other"
    return {"kind": kind, "key_share": share, "detail": f"border key share {share:.2f}, corner pixel {corner}"}


def key_image(im: Image.Image) -> Image.Image:
    """Key a magenta-background RGB(A) image into RGBA. Raises KeyingError if unsafe."""
    info = describe_background(im)
    if info["kind"] == "alpha":
        return im.convert("RGBA")
    if info["kind"] != "magenta":
        raise KeyingError(f"background is not the magenta key ({info['detail']}); capture refused, nothing keyed")

    rgb = im.convert("RGB")
    size = im.size
    r, g, b = rgb.split()

    # 1. two alpha estimates; the more opaque wins
    dist = _distance_from_key(rgb)
    ramp_d = [0 if d <= INNER else 255 if d >= OUTER else round((d - INNER) * 255 / (OUTER - INNER)) for d in range(256)]
    alpha_d = dist.point(ramp_d)
    m = _magentaness(rgb)
    span = BG_DEADZONE - FG_DEADZONE
    ramp_m = [255 if v <= FG_DEADZONE else 0 if v >= BG_DEADZONE else round((BG_DEADZONE - v) * 255 / span) for v in range(256)]
    alpha_m = m.point(ramp_m)
    alpha = ImageChops.lighter(alpha_d, alpha_m)

    # 2. partial alpha only near real background. Background seeds are pixels that are
    #    pure key by colour distance OR strongly magenta by magenta-ness: the fill inside a
    #    hair-strand gap or a ribbon fold is contaminated by anti-aliasing and fails the
    #    strict distance test, yet it is unmistakably key, and the prompt forbids magenta
    #    on the subject, so a hot-magenta pixel is background by contract.
    pure_bg = ImageChops.lighter(dist.point(lambda d: 255 if d <= INNER else 0),
                                 m.point(lambda v: 255 if v >= SEED_MAGENTANESS else 0))
    near_bg = pure_bg.filter(ImageFilter.MaxFilter(NEAR_BG_PX * 2 + 1))
    alpha = Image.composite(alpha, Image.new("L", size, 255), near_bg)
    #    ...and a pixel the keyer itself calls pure background is fully transparent, whatever
    #    the ramps say. Without this, the slightly darkened one-pixel frame some captures
    #    carry keyed to alpha 8-45 and failed the corner test while the rest was perfect.
    alpha = Image.composite(Image.new("L", size, 0), alpha, pure_bg)

    # 3. spill: subtract the excess magenta on a narrow rim. Physically, spill lives only in
    #    blended pixels, so the band is narrower than the alpha ramp; that keeps a purple
    #    wing membrane's interior colour intact while still clearing pink off fine light
    #    strands (hair, fur), which the distance estimate wrongly calls fully opaque.
    #    ...and every partially transparent pixel, wherever it sits: partial alpha means the
    #    pixel is a blend with the key by definition, so it carries spill. Without this, a
    #    pale swirl's soft edge a few pixels from the fill kept a dusky-mauve cast.
    partial = alpha.point(lambda v: 255 if 0 < v < 255 else 0)
    spill_zone = ImageChops.lighter(pure_bg.filter(ImageFilter.MaxFilter(SPILL_PX * 2 + 1)), partial)
    excess = ImageChops.subtract(m, Image.new("L", size, SPILL_MARGIN))   # max(0, m - margin)
    r_fixed = ImageChops.subtract(r, excess)
    b_fixed = ImageChops.subtract(b, excess)
    r = Image.composite(r_fixed, r, spill_zone)
    b = Image.composite(b_fixed, b, spill_zone)

    # 4. interior bleed: where the model painted a translucent membrane, fur or icicle over
    #    the key, magenta shows THROUGH the paint well inside the subject, beyond the reach
    #    of the rim guard. Those pixels are opaque subject as far as alpha is concerned, so
    #    the remedy is colour only: any visible pixel still carrying more than a modest
    #    magenta excess has that excess taken out of red and blue. Neutral, earthy and pure
    #    red/blue colours are untouched; a purple or pink loses a little saturation, which
    #    the contract accepts since the prompt forbids magenta and pink on the subject.
    #    The margin is tighter on BRIGHT paint: a little magenta on white swirls or pale
    #    hair reads as pink, while the same amount on a dark purple wing membrane or a
    #    wraith's smoke is just the colour of the paint. Brightness decides which rule
    #    applies, so real purples keep their saturation and pale subjects lose the cast.
    merged = Image.merge("RGB", (r, g, b))
    bright = merged.convert("L").point(lambda v: 255 if v > BRIGHT_LUMA else 0)
    margin = Image.composite(Image.new("L", size, BLEED_MARGIN_BRIGHT), Image.new("L", size, BLEED_MARGIN), bright)
    bleed = ImageChops.subtract(_magentaness(merged), margin)
    r = ImageChops.subtract(r, bleed)
    b = ImageChops.subtract(b, bleed)

    # 5. rose, measured by hue rather than magenta-ness. Key mixed into warm paint leaves
    #    rose (red high, blue a little high, green low); min(R,B)-G reads that as nearly
    #    clean while the eye reads it as pink. Two remedies:
    #    a) partially transparent pixels are blends with the key by definition, so a PARTIAL
    #       un-mix removes the key's share: green comes up, red and blue come down together.
    #       Alpha here is biased opaque (step 1), so this can only under-correct, never
    #       overshoot into green the way the first version did.
    #    b) opaque pale low-saturation rose is paint the generator tinted because the key
    #       surrounded it; the brief asked for pale grey and white, so it is pulled halfway
    #       toward neutral. Skin (hue 10-30), saturated red or pink cloth (saturation above
    #       0.3) and lavender (hue below 315) fall outside the condition and are untouched.
    rf, gf, bf, af = (c.convert("F") for c in (r, g, b, alpha))
    one = Image.new("F", size, 1.0)
    keyfrac = ImageMath.lambda_eval(lambda a: ((1 - a["af"] / 255) * (a["af"] > 0) * (a["af"] < 255)) * UNMIX_SHARE, af=af)
    denom = ImageMath.lambda_eval(lambda a: a["one"] - a["kf"], one=one, kf=keyfrac)
    rf = ImageMath.lambda_eval(lambda a: (a["c"] - a["kf"] * 255) / a["d"], c=rf, kf=keyfrac, d=denom)
    bf = ImageMath.lambda_eval(lambda a: (a["c"] - a["kf"] * 255) / a["d"], c=bf, kf=keyfrac, d=denom)
    gf = ImageMath.lambda_eval(lambda a: a["c"] / a["d"], c=gf, kf=keyfrac, d=denom)
    # b) rose condition: R is the max, B above G by a margin, bright, and low saturation
    #    (G above ROSE_MIN_G_SHARE of R). Half of the (R-G) and (B-G) distance is removed.
    rose = ImageMath.lambda_eval(
        lambda a: (a["r"] > a["b"]) * (a["b"] > a["g"] + 4) * (a["r"] > ROSE_MIN_R) * (a["g"] > a["r"] * ROSE_MIN_G_SHARE),
        r=rf, g=gf, b=bf)
    pull = ImageMath.lambda_eval(lambda a: ROSE_PULL + (1 - ROSE_PULL) * ((a["af"] > 0) * (a["af"] < 255)), af=af)
    rf = ImageMath.lambda_eval(lambda a: a["r"] - (a["r"] - a["g"]) * a["m"] * a["p"], r=rf, g=gf, m=rose, p=pull)
    bf = ImageMath.lambda_eval(lambda a: a["b"] - (a["b"] - a["g"]) * a["m"] * a["p"], b=bf, g=gf, m=rose, p=pull)
    r, g, b = (c.convert("L") for c in (rf, gf, bf))   # F -> L clamps to 0..255

    out = Image.merge("RGB", (r, g, b))
    # fully transparent pixels carry no colour at all (keeps the PNG small and halo-proof)
    solid = alpha.point(lambda v: 255 if v > 0 else 0)
    out = Image.composite(out, Image.new("RGB", size, (0, 0, 0)), solid)
    out.putalpha(alpha)
    return out


def key_png_if_needed(png_bytes: bytes) -> tuple[bytes, str]:
    """Bytes in, RGBA PNG bytes out, plus a note for the results ledger.

    An input that already has a transparent background passes through untouched.
    """
    with Image.open(BytesIO(png_bytes)) as im:
        im.load()
        info = describe_background(im)
        if info["kind"] == "alpha":
            return png_bytes, "key=none; source already transparent"
        keyed = key_image(im)
    buf = BytesIO()
    keyed.save(buf, format="PNG", optimize=True)
    hist = keyed.getchannel("A").histogram()
    clear = sum(hist[:6]) / (keyed.size[0] * keyed.size[1])
    return buf.getvalue(), f"key=magenta-v3.9; border key share {info['key_share']:.2f}; keyed transparent fraction {clear:.2f}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("capture", type=Path)
    ap.add_argument("master", type=Path, nargs="?")
    ap.add_argument("--inspect", action="store_true", help="report the background, key nothing")
    args = ap.parse_args(argv)
    with Image.open(args.capture) as im:
        im.load()
        info = describe_background(im)
        print(f"{args.capture.name}: {im.size[0]}x{im.size[1]} {im.mode} | background {info['kind']} | {info['detail']}")
        if args.inspect:
            return 0
        if not args.master:
            print("master path required unless --inspect", file=sys.stderr)
            return 2
        try:
            out = key_image(im)
        except KeyingError as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 1
    args.master.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.master, format="PNG", optimize=True)
    print(f"wrote {args.master}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
