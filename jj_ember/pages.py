# Ember & Oak : description de toutes les pages des 4 produits (un seul modèle, deux formats de papier).
# Les pages sont en HTML/CSS en millimètres, rendues à 240 dpi par Chromium (build.py).
import os, random
H = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(H, "art")
FONTS = os.path.join(H, "fonts")
SIZES = {"letter": (215.9, 279.4), "a4": (210.0, 297.0)}
BRAND = "Ember &amp; Oak &#183; Oakfold"
INK = "#3B2A1E"; RUST = "#9A4A24"; CREAM = "#F2E6CF"

MISSING = set()
def art(k):
    p = os.path.join(ART, k + ".png")
    if not os.path.exists(p):          # rendu d'essai seulement : la vérification finale refuse toute image manquante
        MISSING.add(k); p = os.path.join(ART, sorted(f for f in os.listdir(ART) if f.endswith(".png"))[0])
    if k.startswith("e") and os.path.exists(p):   # éléments : recadrage serré sur le dessin (fond crème retiré du cadre)
        t = os.path.join(ART, "trim", k + ".png")
        if not os.path.exists(t) or os.path.getmtime(t) < max(os.path.getmtime(p), os.path.getmtime(__file__)): _trim(p, t)
        p = t
    return "file://" + p

def _trim(src, dst):
    from PIL import Image, ImageChops, ImageFilter
    im = Image.open(src).convert("RGB"); w, h = im.size
    bg = Image.new("RGB", im.size, im.getpixel((8, 8)))
    diff = ImageChops.difference(im, bg).convert("L").filter(ImageFilter.GaussianBlur(4)).point(lambda v: 255 if v > 28 else 0)
    x0, y0, x1, y1 = diff.getbbox() or (0, 0, w, h); m = int(0.06 * max(x1 - x0, y1 - y0))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    box = (max(0, x0 - m), max(0, y0 - m), min(w, x1 + m), min(h, y1 + m))
    # fond crème -> transparent, bord adouci (le dessin se pose sur n'importe quel papier)
    d = ImageChops.difference(im, bg).convert("L").point(lambda v: max(0, min(255, (v - 10) * 9)))
    a = d.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2.5))
    out = im.convert("RGBA"); out.putalpha(a); out.crop(box).save(dst)

FONT_CSS = "".join(
    f"@font-face{{font-family:'{fam}';src:url('file://{FONTS}/{fn}');font-style:{st};font-weight:{w}}}"
    for fn in sorted(os.listdir(FONTS)) if fn.endswith(".woff2")
    for fam, w, st in [(fn.split("-")[0].replace("IMFellEnglishSC", "IM Fell English SC").replace("IMFellEnglish", "IM Fell English")
                        .replace("CormorantGaramond", "Cormorant Garamond").replace("SpecialElite", "Special Elite")
                        .replace("HomemadeApple", "Homemade Apple"), fn.split("-")[1], fn.split("-")[2][:-6])])

def doc(body, size, extra=""):
    w, h = SIZES[size]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
*{{box-sizing:border-box;margin:0;padding:0}}html,body{{width:{w}mm;height:{h}mm;overflow:hidden;background:#fff}}
.pg{{position:relative;width:{w}mm;height:{h}mm;overflow:hidden}}
.fell{{font-family:'IM Fell English',serif}}.sc{{font-family:'IM Fell English SC',serif}}
.cor{{font-family:'Cormorant Garamond',serif}}.typ{{font-family:'Special Elite',monospace}}
{extra}</style></head><body><div class="pg">{body}</div></body></html>"""

# ---------- papiers pleine page ----------
PAPERS = [f"p{i:02d}" for i in range(1, 21)]
PAPER_KEYS = {
 "p01": "p01_maple_parchment", "p02": "p02_ledger_leaves", "p03": "p03_fern_forest_dark", "p04": "p04_owl_moon",
 "p05": "p05_mushroom_plate", "p06": "p06_moth_specimens", "p07": "p07_letters_postmarks", "p08": "p08_crow_branches",
 "p09": "p09_pumpkin_harvest", "p10": "p10_damask_rust", "p11": "p11_botanical_pattern_sage", "p12": "p12_plaid_autumn",
 "p13": "p13_library_books", "p14": "p14_sheet_music_leaves", "p15": "p15_map_autumn", "p16": "p16_apothecary",
 "p17": "p17_pinecone_berries", "p18": "p18_dark_leaves_scatter", "p19": "p19_tea_stained_plain", "p20": "p20_dark_plain"}

def paper_page(k, size):
    return doc(f'<div style="position:absolute;inset:0;background:url({art(PAPER_KEYS[k])}) center/cover no-repeat"></div>', size)

# ---------- enveloppes et pochettes ----------
CUTOUT = False   # True : rendu des seules pièces, fond transparent (photos de la fiche)
def _sheet(svg_body, title, size, note):
    w, h = SIZES[size]
    if CUTOUT:
        return doc(f'<svg width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" style="position:absolute;inset:0">{svg_body}</svg>', size,
                   "html,body{background:transparent!important}")
    return doc(f"""
<div style="position:absolute;inset:0;background:#FBF7EF"></div>
<svg width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" style="position:absolute;inset:0">{svg_body}</svg>
<div class="sc" style="position:absolute;left:0;right:0;bottom:9.5mm;text-align:center;font-size:8.5pt;color:{INK};letter-spacing:.06em">{title}</div>
<div class="cor" style="position:absolute;left:0;right:0;bottom:5.5mm;text-align:center;font-size:7pt;color:#7a6650;font-style:italic">{note} &#183; {BRAND}</div>""", size)

CUT = 'fill="none" stroke="#5a4636" stroke-width="0.25"'
FOLD = 'fill="none" stroke="#5a4636" stroke-width="0.25" stroke-dasharray="1.6 1.2"'

def _fill(pid, key, x, y, w, h):
    return (f'<pattern id="{pid}" patternUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}">'
            f'<image href="{art(key)}" x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/></pattern>')

def envelope_pointed(size, key, note):
    W, Hh = SIZES[size]; bw, bh = 120, 82          # corps de l'enveloppe fermée
    cx, cy = W / 2, (Hh - 14) / 2; x0, y0 = cx - bw / 2, cy - bh / 2; x1, y1 = x0 + bw, y0 + bh
    sf = 36; tf = 58; bf = 54                        # rabats côté, haut, bas
    path = (f"M{x0},{y0} L{cx},{y0-tf} L{x1},{y0} L{x1+sf},{cy} L{x1},{y1} L{cx},{y1+bf} L{x0},{y1} L{x0-sf},{cy} Z")
    defs = _fill("f", key, x0 - sf, y0 - tf, bw + 2 * sf, bh + tf + bf)
    body = (f"<defs>{defs}</defs><path d='{path}' fill='url(#f)' {CUT}/>"
            f"<rect x='{x0}' y='{y0}' width='{bw}' height='{bh}' {FOLD}/>")
    return _sheet(body, "Pointed Flap Envelope", size, note + " &#183; cut on solid line, fold on dashed lines")

def envelope_square(size, key, note):
    W, Hh = SIZES[size]; s = 100; r = 46
    cx, cy = W / 2, (Hh - 14) / 2; x0, y0 = cx - s / 2, cy - s / 2; x1, y1 = x0 + s, y0 + s
    path = (f"M{x0},{y0} C{x0+8},{y0-r} {x1-8},{y0-r} {x1},{y0} C{x1+r},{y0+8} {x1+r},{y1-8} {x1},{y1} "
            f"C{x1-8},{y1+r} {x0+8},{y1+r} {x0},{y1} C{x0-r},{y1-8} {x0-r},{y0+8} {x0},{y0} Z")
    defs = _fill("f", key, x0 - r, y0 - r, s + 2 * r, s + 2 * r)
    body = f"<defs>{defs}</defs><path d='{path}' fill='url(#f)' {CUT}/><rect x='{x0}' y='{y0}' width='{s}' height='{s}' {FOLD}/>"
    return _sheet(body, "Rounded Square Envelope", size, note + " &#183; cut on solid line, fold on dashed lines")

def envelope_wallet(size, key, note):
    W, Hh = SIZES[size]; bw, bh = 150, 80; tf = 45; bf = 62; sf = 18
    cx = W / 2; x0 = cx - bw / 2; x1 = x0 + bw; y0 = (Hh - 14 - (bh + tf + bf)) / 2 + tf; y1 = y0 + bh
    path = (f"M{x0},{y0} L{x0+6},{y0-tf} L{x1-6},{y0-tf} L{x1},{y0} L{x1+sf},{y0+6} L{x1+sf},{y1-6} L{x1},{y1} "
            f"L{x1},{y1+bf} L{x0},{y1+bf} L{x0},{y1} L{x0-sf},{y1-6} L{x0-sf},{y0+6} Z")
    defs = _fill("f", key, x0 - sf, y0 - tf, bw + 2 * sf, bh + tf + bf)
    body = (f"<defs>{defs}</defs><path d='{path}' fill='url(#f)' {CUT}/><rect x='{x0}' y='{y0}' width='{bw}' height='{bh}' {FOLD}/>")
    return _sheet(body, "Wallet Envelope", size, note + " &#183; cut on solid line, fold on dashed lines")

def library_pockets(size, key, note):
    W, Hh = SIZES[size]; pw, ph = 72, 110; tab = 12; bt = 16
    out = []; defs = []
    for i, cx in enumerate((W / 2 - 50, W / 2 + 50)):  # 2 x (72 + 24) mm, 4 mm d'écart
        x0 = cx - pw / 2; x1 = x0 + pw; y0 = (Hh - 14 - ph - bt) / 2; y1 = y0 + ph
        path = (f"M{x0},{y0} L{cx-14},{y0} A14,14 0 0 0 {cx+14},{y0} L{x1},{y0} L{x1},{y0+8} L{x1+tab},{y0+14} L{x1+tab},{y1-6} L{x1},{y1} "
                f"L{x1-4},{y1+bt} L{x0+4},{y1+bt} L{x0},{y1} L{x0-tab},{y1-6} L{x0-tab},{y0+14} L{x0},{y0+8} Z")
        defs.append(_fill(f"f{i}", key, x0 - tab, y0, pw + 2 * tab, ph + bt))
        out.append(f"<path d='{path}' fill='url(#f{i})' {CUT}/><path d='M{x0},{y0+8} L{x0},{y1} L{x1},{y1} L{x1},{y0+8}' {FOLD}/>"
                   f"<rect x='{x0+10}' y='{y0+30}' width='{pw-20}' height='22' fill='#F4EBD8' stroke='#5a4636' stroke-width='0.3' rx='1.5'/>"
                   f"<text x='{cx}' y='{y0+43}' text-anchor='middle' font-family='IM Fell English SC' font-size='5.2' fill='{INK}'>"
                   f"{'Keepsakes' if i == 0 else 'Autumn Notes'}</text>")
    return _sheet(f"<defs>{''.join(defs)}</defs>{''.join(out)}", "Library Card Pockets (2)", size, note + " &#183; cut, fold the tabs back and glue")

def tuck_pocket(size, key, note):
    W, Hh = SIZES[size]; pw, ph = 170, 100; tab = 14; flap = 30
    cx = W / 2; x0 = cx - pw / 2; x1 = x0 + pw; y0 = (Hh - 14 - ph - flap) / 2 + flap; y1 = y0 + ph
    path = (f"M{x0},{y0} C{x0+20},{y0-flap} {x1-20},{y0-flap} {x1},{y0} L{x1+tab},{y0+8} L{x1+tab},{y1-8} L{x1},{y1} L{x0},{y1} "
            f"L{x0-tab},{y1-8} L{x0-tab},{y0+8} Z")
    defs = _fill("f", key, x0 - tab, y0 - flap, pw + 2 * tab, ph + flap)
    body = (f"<defs>{defs}</defs><path d='{path}' fill='url(#f)' {CUT}/><path d='M{x0},{y0} L{x0},{y1} M{x1},{y0} L{x1},{y1} M{x0},{y0} L{x1},{y0}' {FOLD}/>")
    return _sheet(body, "Tuck-In Page Pocket", size, note + " &#183; cut, fold side tabs back and glue to your page")

def tags_sheet(size, key, note):
    W, Hh = SIZES[size]; tw, th = 42, 112; c = 10
    out = []; defs = []; xs = [W / 2 - 1.5 * 48 + 48 * i for i in range(4)]
    for i, cx in enumerate(xs):
        x0 = cx - tw / 2; x1 = x0 + tw; y0 = (Hh - 14 - th) / 2; y1 = y0 + th
        defs.append(_fill(f"f{i}", key, x0 - i * 9, y0 - i * 14, tw * 3, th * 1.6))
        out.append(f"<path d='M{x0+c},{y0} L{x1-c},{y0} L{x1},{y0+c} L{x1},{y1} L{x0},{y1} L{x0},{y0+c} Z' fill='url(#f{i})' {CUT}/>"
                   f"<circle cx='{cx}' cy='{y0+10}' r='3' fill='#FBF7EF' stroke='#5a4636' stroke-width='0.3'/>"
                   f"<circle cx='{cx}' cy='{y0+10}' r='5.2' fill='none' stroke='#C9A86A' stroke-width='1.2'/>")
    return _sheet(f"<defs>{''.join(defs)}</defs>{''.join(out)}", "Tall Pocket Tags (4)", size, note + " &#183; cut on solid line, punch the hole")

def belly_bands(size, key, note):
    W, Hh = SIZES[size]; bw, bh = 185, 42
    out = []; defs = []
    for i in range(4):
        x0 = (W - bw) / 2; y0 = 22 + i * (bh + 14)
        defs.append(_fill(f"f{i}", key, x0 - i * 20, y0 - i * 30, bw * 1.2, bw * 1.8))
        out.append(f"<rect x='{x0}' y='{y0}' width='{bw}' height='{bh}' fill='url(#f{i})' {CUT}/>"
                   f"<rect x='{x0+bw/2-28}' y='{y0+bh/2-7}' width='56' height='14' fill='#F4EBD8' stroke='#5a4636' stroke-width='0.3' rx='7'/>"
                   f"<text x='{x0+bw/2}' y='{y0+bh/2+2}' text-anchor='middle' font-family='IM Fell English SC' font-size='5' fill='{INK}'>"
                   f"{['Gathered Leaves','Ember &amp; Oak','Autumn Days','Little Things'][i]}</text>")
    return _sheet(f"<defs>{''.join(defs)}</defs>{''.join(out)}", "Belly Bands (4)", size, note + " &#183; cut, wrap around a signature or card")

ENVELOPES = [
 ("env01", envelope_pointed, "p02_ledger_leaves", "Ledger Leaves"),
 ("env02", envelope_pointed, "p04_owl_moon", "Owl Moon"),
 ("env03", envelope_square, "p10_damask_rust", "Rust Damask"),
 ("env04", envelope_square, "p11_botanical_pattern_sage", "Sage Botanical"),
 ("env05", envelope_wallet, "p14_sheet_music_leaves", "Sheet Music"),
 ("env06", envelope_wallet, "p03_fern_forest_dark", "Fern Hollow"),
 ("poc07", library_pockets, "p12_plaid_autumn", "Harvest Plaid"),
 ("poc08", library_pockets, "p07_letters_postmarks", "Old Letters"),
 ("poc09", tuck_pocket, "p01_maple_parchment", "Maple Parchment"),
 ("poc10", tuck_pocket, "p18_dark_leaves_scatter", "Dark Leaves"),
 ("poc11", tags_sheet, "p05_mushroom_plate", "Mushroom Plate"),
 ("poc12", belly_bands, "p15_map_autumn", "Old Map"),
]

def env_page(k, size):
    for kk, fn, key, note in ENVELOPES:
        if kk == k: return fn(size, key, note)

# ---------- cartes de journaling ----------
WORDS = ["Autumn Notes", "Gathered", "Remember", "Harvest Moon", "Dear Diary", "Little Things", "Wander", "Field Notes",
         "Ember &amp; Oak", "Slow Days", "Hello Autumn", "Keepsake", "Moonlit", "Forest Walk", "Notes to Self", "Cozy Season",
         "Collected", "Fallen Leaves", "Golden Hour", "Once Upon", "Stories", "Hearth", "Wild Things", "Thankful"]
ELEMS = ["e01_oak_acorns", "e02_maple", "e03_fern", "e04_mushrooms", "e05_moth", "e06_owl", "e07_key_watch", "e08_crow",
         "e09_pumpkin", "e10_bottle", "e11_feather", "e12_wreath", "e13_books", "e14_pressed_flowers"]
BG = ["p01_maple_parchment", "p02_ledger_leaves", "p05_mushroom_plate", "p07_letters_postmarks", "p10_damask_rust",
      "p11_botanical_pattern_sage", "p12_plaid_autumn", "p14_sheet_music_leaves", "p15_map_autumn", "p19_tea_stained_plain"]

def _card(w, h, i, kind):
    r = random.Random(i * 7 + 3); bg = BG[i % len(BG)]; el = ELEMS[i % len(ELEMS)]; word = WORDS[i % len(WORDS)]
    bx, by = r.randint(5, 95), r.randint(5, 95)
    frame = (f'<div style="position:absolute;inset:3mm;background:#F6EEDC;border:0.3mm solid #8a6a4a;'
             f'box-shadow:0 0 0 0.8mm #F6EEDC,0 0 0 1.1mm #8a6a4a"></div>')
    if kind == "art":   # illustration dans une fenêtre en arche sur le papier, titre sur une étiquette
        frame = ""
        inner = (f'<div style="position:absolute;left:{w*0.12}mm;right:{w*0.12}mm;top:{h*0.07}mm;height:{h*0.62}mm;background:#F6EEDC;'
                 f'border-radius:{w*0.38}mm {w*0.38}mm 2mm 2mm;border:0.35mm solid #8a6a4a;box-shadow:0 0 0 1mm #F6EEDC,0 0 0 1.3mm #8a6a4a"></div>'
                 f'<div style="position:absolute;left:{w*0.16}mm;right:{w*0.16}mm;top:{h*0.12}mm;height:{h*0.54}mm;background:url({art(el)}) center/contain no-repeat;mix-blend-mode:multiply"></div>'
                 f'<div class="fell" style="position:absolute;left:{w*0.08}mm;right:{w*0.08}mm;top:{h*0.76}mm;padding:1.6mm 0;background:#F6EEDC;'
                 f'border:0.35mm solid #8a6a4a;text-align:center;font-size:{w*0.2}pt;color:{INK}">{word}</div>')
    else:
        lines = "".join(f'<div style="position:absolute;left:7mm;right:7mm;top:{h*0.34+j*6.2}mm;border-bottom:0.25mm solid #b49a78"></div>'
                        for j in range(int((h * 0.56) / 6.2)))
        inner = (f'<div style="position:absolute;left:5mm;top:4.5mm;width:{h*0.3}mm;height:{h*0.3}mm;background:url({art(el)}) center/contain no-repeat;mix-blend-mode:multiply"></div>'
                 f'<div class="sc" style="position:absolute;left:{h*0.3+5}mm;right:5mm;top:{h*0.1}mm;font-size:{w*0.17}pt;color:{RUST}">{word}</div>'
                 f'<div class="cor" style="position:absolute;left:{h*0.3+5}mm;right:5mm;top:{h*0.1+7}mm;font-size:7pt;font-style:italic;color:#7a6650">date &#8212;&#8212;&#8212;&#8212;</div>{lines}')
    return (f'<div style="position:relative;width:{w}mm;height:{h}mm;background:url({art(bg)}) {bx}% {by}%/260% no-repeat;'
            f'outline:0.25mm solid #5a4636;overflow:hidden">{frame}{inner}</div>')

def cards_page(sheet, size):
    W, Hh = SIZES[size]
    if sheet < 6:            # 9 cartes ATC 2,5 x 3,5 po
        cw, ch, cols, rows = 63.5, 88.9, 3, 3; kind = "art" if sheet % 2 == 0 else "lined"
        label = f"Journaling Cards &#183; 2.5 x 3.5 in &#183; sheet {sheet+1} of 8"
    else:                    # 4 cartes 3 x 4 po lignées
        cw, ch, cols, rows = 76.2, 101.6, 2, 2; kind = "lined"; label = f"Journaling Cards &#183; 3 x 4 in &#183; sheet {sheet+1} of 8"
    gap = 2.5
    gw = cols * cw + (cols - 1) * gap; gh = rows * ch + (rows - 1) * gap
    cells = "".join(f'<div style="position:absolute;left:{(W-gw)/2+c*(cw+gap)}mm;top:{(Hh-12-gh)/2+rr*(ch+gap)}mm">'
                    f'{_card(cw, ch, sheet*9+rr*cols+c, kind)}</div>' for rr in range(rows) for c in range(cols))
    return doc(f'<div style="position:absolute;inset:0;background:#FBF7EF"></div>{cells}'
               f'<div class="sc" style="position:absolute;left:0;right:0;bottom:5.5mm;text-align:center;font-size:8pt;color:{INK}">{label} &#183; {BRAND}</div>', size)

def lined_page(n, size):
    W, Hh = SIZES[size]; bg = ["p19_tea_stained_plain", "p01_maple_parchment", "p02_ledger_leaves", "p20_dark_plain"][n]
    dark = n == 3; col = "#e8d9bd" if dark else "#7d6249"
    lines = "".join(f'<div style="position:absolute;left:22mm;right:22mm;top:{58+j*9}mm;border-bottom:0.3mm solid {col};opacity:.8"></div>'
                    for j in range(int((Hh - 82) / 9)))
    return doc(f'<div style="position:absolute;inset:0;background:url({art(bg)}) center/cover"></div>'
               + ("" if dark or n == 0 else '<div style="position:absolute;inset:16mm 16mm;background:rgba(246,238,220,.86);border-radius:1mm"></div>')
               + f'<div style="position:absolute;inset:14mm;border:0.4mm solid {col};opacity:.7"></div>'
               f'<div class="fell" style="position:absolute;left:0;right:0;top:28mm;text-align:center;font-size:30pt;color:{"#f2e6cf" if dark else INK}">'
               f'{["Autumn Notes","Gathered Thoughts","Field Journal","Moonlit Pages"][n]}</div>{lines}', size)

# ---------- éphémères à découper (kit) ----------
def ephemera_page(n, size):
    W, Hh = SIZES[size]; els = ELEMS[n * 3 % 14:] + ELEMS
    pos = [(8, 10, 95, 125), (108, 10, 95, 125), (30, 140, 150, 125)]
    cells = "".join(f'<div style="position:absolute;left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm;background:url({art(els[i])}) center/contain no-repeat;mix-blend-mode:multiply"></div>'
                    for i, (x, y, w, h) in enumerate(pos))
    return doc(f'<div style="position:absolute;inset:0;background:url({art("p19_tea_stained_plain")}) center/cover"></div>{cells}'
               f'<div class="sc" style="position:absolute;left:0;right:0;bottom:5.5mm;text-align:center;font-size:8pt;color:{INK}">Cut-Apart Ephemera &#183; sheet {n+1} of 6 &#183; {BRAND}</div>', size)

# ---------- guide START HERE ----------
def start_page(product, n, size):
    W, Hh = SIZES[size]
    items = "".join(f"<li>{x}</li>" for x in product["contents"])
    if n == 0:
        body = f"""<div class="sc" style="font-size:12pt;letter-spacing:.2em;color:{RUST}">The Ember &amp; Oak Collection</div>
<div class="fell" style="font-size:34pt;line-height:1.2;margin:4mm 0 2mm">{product['name']}</div>
<div class="cor" style="font-size:14pt;font-style:italic;color:#6d5640;margin-bottom:8mm">Start here &#8212; thank you for your purchase!</div>
<div class="sc" style="font-size:13pt;color:{RUST};margin-bottom:2mm">What's inside</div>
<ul class="cor" style="font-size:13pt;line-height:1.45;padding-left:6mm">{items}</ul>
<div class="sc" style="font-size:13pt;color:{RUST};margin:7mm 0 2mm">Your files</div>
<div class="cor" style="font-size:13pt;line-height:1.45">{product['files_note']}</div>"""
    else:
        body = f"""<div class="sc" style="font-size:13pt;color:{RUST};margin-bottom:2mm">Printing tips</div>
<ul class="cor" style="font-size:13pt;line-height:1.45;padding-left:6mm">
<li>Print at <b>100% / Actual size</b> (not &#8220;Fit to page&#8221;) so templates keep their measurements.</li>
<li>Choose the file that matches your paper: US Letter (8.5 x 11 in) or A4.</li>
<li>Matte paper or 120&#8211;200 gsm cardstock gives the richest vintage look; inkjet printers work best for full-color pages.</li>
<li>Colors vary slightly between screens and printers.</li>
<li>You can also use the pages digitally in GoodNotes, Procreate or any app that opens PDF files.</li></ul>
<div class="sc" style="font-size:13pt;color:{RUST};margin:7mm 0 2mm">How to use</div>
<div class="cor" style="font-size:13pt;line-height:1.45">{product['howto']}</div>
<div class="sc" style="font-size:13pt;color:{RUST};margin:7mm 0 2mm">Terms of use</div>
<div class="cor" style="font-size:13pt;line-height:1.45">Personal use, and handmade items you sell as physical products (journals, cards, scrapbooks) are welcome.
Do not resell, share or redistribute the digital files, in whole or in part. Some artwork was created with the help of AI tools and finished by hand.
Questions? Message Oakfold on Etsy &#8212; I'm happy to help.</div>"""
    return doc(f'<div style="position:absolute;inset:0;background:url({art("p19_tea_stained_plain")}) center/cover"></div>'
               f'<div style="position:absolute;inset:12mm;border:0.4mm solid #8a6a4a"></div>'
               f'<div style="position:absolute;inset:24mm 24mm;color:{INK}">{body}</div>', size)


def card_cutout(i, kind, w=63.5, h=88.9):
    """Une carte seule, fond transparent (photos)."""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{w}mm;height:{h}mm;background:transparent;overflow:hidden}}
.fell{{font-family:'IM Fell English',serif}}.sc{{font-family:'IM Fell English SC',serif}}.cor{{font-family:'Cormorant Garamond',serif}}</style></head>
<body>{_card(w, h, i, kind)}</body></html>"""
