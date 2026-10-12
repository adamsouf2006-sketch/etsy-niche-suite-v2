# Photos des fiches (2000 x 2500, JPEG) fabriquées en HTML à partir des vraies pages rendues.
# Usage : python3 photos.py [produit ...]
import os, sys, asyncio, json
from PIL import Image
from playwright.async_api import async_playwright
import pages as P
import build as B

H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, "out")
INK = "#33241A"; RUST = "#9A4A24"; CREAM = "#F4EAD6"; SAGE = "#6F7A5A"

def thumbs(key, w=900):
    """Réduit les pages Letter du produit pour les photos (cache)."""
    src = os.path.join(OUT, key, "pages_letter"); dst = os.path.join(OUT, key, "thumbs"); os.makedirs(dst, exist_ok=True)
    res = []
    for f in sorted(os.listdir(src)):
        o = os.path.join(dst, f)
        if not os.path.exists(o):
            im = Image.open(os.path.join(src, f)); im.thumbnail((w, w * 2)); im.save(o, quality=90)
        res.append("file://" + o)
    return res

def page_img(u, w, rot=0, x=0, y=0, z=1, shadow=True):
    sh = "box-shadow:0 18px 40px rgba(40,25,15,.35),0 3px 8px rgba(40,25,15,.25);" if shadow else ""
    return (f'<img src="{u}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);'
            f'z-index:{z};{sh}border-radius:2px">')

def frame(body, bg="#EFE3CC"):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{P.FONT_CSS}
*{{box-sizing:border-box;margin:0;padding:0}}body{{width:2000px;height:2500px;overflow:hidden;background:{bg};color:{INK}}}
.fell{{font-family:'IM Fell English',serif}}.sc{{font-family:'IM Fell English SC',serif}}.cor{{font-family:'Cormorant Garamond',serif}}
.abs{{position:absolute}}</style></head><body><div style="position:relative;width:2000px;height:2500px;overflow:hidden">{body}</div></body></html>"""

def paper_bg(key, dim=0.0):
    calm = '<div class="abs" style="inset:0;background:rgba(244,234,214,.45)"></div>' if key == "p19_tea_stained_plain" else ""
    return (f'<div class="abs" style="inset:0;background:url({P.art(key)}) center/cover"></div>{calm}'
            + (f'<div class="abs" style="inset:0;background:rgba(30,18,10,{dim})"></div>' if dim else ""))

def badge(text1, text2, x, y, d=330, bg=RUST, fg=CREAM):
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;border-radius:50%;background:{bg};color:{fg};'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,.3);'
            f'border:6px double {fg};z-index:50"><div class="fell" style="font-size:{d*.36}px;line-height:1">{text1}</div>'
            f'<div class="sc" style="font-size:{d*.11}px;letter-spacing:.08em">{text2}</div></div>')

FORMATS = "US Letter + A4 &#183; Printable PDF &#183; Instant Download"

def piece(u, w, rot, x, y, z=5):
    return (f'<img src="{u}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z};'
            f'filter:drop-shadow(0 16px 22px rgba(40,25,15,.38)) drop-shadow(0 3px 5px rgba(40,25,15,.3))">')

def hero(key, info, t, dark=False):
    """Zone produit de la photo principale : pièces découpées pour enveloppes/cartes/kit, pages en éventail pour les papiers."""
    c = CUT.get(key) or {}
    if key == "envelopes":
        return (piece(c["env02"], 760, -8, 120, 760, 2) + piece(c["poc11"], 700, 6, 1120, 820, 3) + piece(c["env03"], 640, 4, 640, 1320, 4)
                + piece(c["poc07"], 760, -4, 120, 1500, 5) + piece(c["env06"], 600, -10, 1250, 1450, 6))
    if key == "cards":
        return "".join(piece(c[f"card{i:02d}"], 470, r, x, y, i) for i, (r, x, y) in enumerate(
            [(-12, 120, 900), (-5, 470, 820), (3, 830, 800), (9, 1190, 860), (-7, 300, 1440), (5, 760, 1420), (11, 1220, 1460)]))
    if key == "kit":
        return (page_img(t[2], 760, -7, 120, 780, 1) + page_img(t[6], 760, 6, 1120, 800, 2)
                + piece(c["env02"], 640, -6, 620, 1160, 4) + piece(c["poc11"], 560, 8, 1250, 1450, 5)
                + piece(c["card00"], 400, -10, 150, 1520, 6) + piece(c["card02"], 400, 4, 470, 1600, 7))
    hero_ = [t[i] for i in info["hero"]]
    return page_img(hero_[0], 820, -9, 170, 820, 1) + page_img(hero_[1], 820, 7, 1010, 840, 2) + page_img(hero_[2], 900, -1, 550, 760, 3)

CUT = {}
# ---------- photo principale : 3 variantes ----------
def plaque(title, sub, top, w=1500, dark=False):
    bg, fg, ac = ("#2B1D14", CREAM, "#E2B887") if dark else ("#F6EEDC", INK, RUST)
    return (f'<div class="abs" style="left:{(2000-w)//2}px;top:{top}px;width:{w}px;padding:46px 40px 40px;background:{bg};border:5px solid {ac};'
            f'outline:3px solid {bg};outline-offset:10px;box-shadow:0 20px 50px rgba(0,0,0,.45);text-align:center;z-index:60">'
            f'<div class="sc" style="font-size:150px;line-height:1;color:{fg}">{title}</div>'
            f'<div class="cor" style="font-size:66px;font-style:italic;color:{ac};margin-top:18px">{sub}</div></div>')

def ribbon(text, bottom, bg=RUST, fg=CREAM):
    return (f'<div class="abs sc" style="left:0;right:0;bottom:{bottom}px;height:150px;background:{bg};color:{fg};display:flex;align-items:center;'
            f'justify-content:center;font-size:60px;letter-spacing:.04em;box-shadow:0 -8px 30px rgba(0,0,0,.3);z-index:60">{text}</div>')

SAFE_T, SAFE_B = 250, 2250   # Etsy recadre la miniature au carré : tout ce qui compte reste entre ces deux lignes

def main_variants(key, info):
    t = thumbs(key); title, sub, n1, n2 = info["title"].replace("<br>", " "), info["sub"], info["num"], info["unit"]
    zone = lambda sc: (f'<div class="abs" style="left:0;right:0;top:{SAFE_T+120}px;height:2000px;transform:scale({sc});transform-origin:50% 38%">'
                       f'<div class="abs" style="left:0;right:0;top:-560px;height:2500px">{hero(key, info, t)}</div></div>')
    # V1 : table sombre, plaque crème, bandeau des formats
    v1 = frame(paper_bg("p20_dark_plain") + '<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 55%,transparent 40%,rgba(0,0,0,.55))"></div>'
        + zone(0.98) + plaque(title, sub, SAFE_T + 40) + badge(n1, n2, 1520, 1600, 420) + ribbon(FORMATS, 2500 - SAFE_B))
    # V2 : papier fougères plein cadre, bandeau rouille
    v2 = frame(paper_bg("p03_fern_forest_dark", 0.25)
        + f'<div class="abs sc" style="left:0;right:0;top:{SAFE_T}px;height:420px;background:{RUST};color:{CREAM};text-align:center;padding-top:60px;'
          f'box-shadow:0 10px 40px rgba(0,0,0,.45);z-index:60"><div style="font-size:150px;line-height:1">{title}</div>'
          f'<div class="cor" style="font-size:66px;font-style:italic;color:#F6D9B4;margin-top:16px">{sub}</div></div>'
        + zone(0.98) + badge(n1, n2, 80, 1640, 420, CREAM, INK) + ribbon(FORMATS, 2500 - SAFE_B, "#2B1D14"))
    # V3 : fond clair encadré de papiers de la collection, plaque centrale
    frame_papers = "".join(page_img(P.art(P.PAPER_KEYS[p]), 640, r, x, y, 0) for p, r, x, y in
        [("p04", -12, -200, 60), ("p05", 9, 1560, 40), ("p10", 8, -240, 1700), ("p09", -10, 1580, 1700), ("p06", 5, -360, 900), ("p17", -6, 1740, 880)])
    v3 = frame(paper_bg("p19_tea_stained_plain") + frame_papers
        + zone(0.92) + plaque(title, sub, SAFE_T + 50, 1420) + badge(n1, n2, 1500, 1640, 420) + ribbon(FORMATS, 2500 - SAFE_B))
    return [v1, v2, v3]

# ---------- 9 autres photos ----------
def what_you_get(key, info):
    t = thumbs(key)
    items = "".join(f'<div style="display:flex;gap:34px;align-items:baseline;margin-bottom:34px"><div class="fell" style="font-size:96px;color:{RUST};width:90px;text-align:right">{i}</div>'
                    f'<div class="cor" style="font-size:66px;line-height:1.15">{x}</div></div>' for i, x in enumerate(info["get"], 1))
    return frame(paper_bg("p19_tea_stained_plain") +
        f'<div class="abs sc" style="left:0;right:0;top:110px;text-align:center;font-size:120px">What You Get</div>'
        f'<div class="abs" style="left:150px;right:150px;top:340px">{items}</div>'
        + "".join(page_img(t[j], 520, [-5, 3, -2, 5][i], 40 + i * 470, 1560 - (i % 2) * 50, i) for i, j in enumerate(info["strip"]))
    )

def all_pages(key, info, start=2, n=None, title="Every Page Included"):
    t = thumbs(key)[start:]; t = t[:n] if n else t
    cols = 5 if len(t) > 20 else 4; w = (1760 - (cols - 1) * 30) // cols; h = int(w * 11 / 8.5)
    cells = "".join(f'<img src="{u}" class="abs" style="left:{120+(i%cols)*(w+30)}px;top:{330+(i//cols)*(h+30)}px;width:{w}px;box-shadow:0 6px 16px rgba(0,0,0,.25)">'
                    for i, u in enumerate(t) if 330 + (i // cols) * (h + 30) + h < 2440)
    return frame(f'<div class="abs" style="inset:0;background:#E9DCC2"></div><div class="abs sc" style="left:0;right:0;top:110px;text-align:center;font-size:110px">{title}</div>{cells}')

def closeup(key, info):
    f = sorted(os.listdir(os.path.join(OUT, key, "pages_letter")))[info["zoom"]]
    u = "file://" + os.path.join(OUT, key, "pages_letter", f)
    return frame(f'<div class="abs" style="inset:0;background:url({u}) {info.get("zpos","40% 35%")}/260% no-repeat"></div>'
        f'<div class="abs" style="left:0;right:0;bottom:0;height:420px;background:linear-gradient(transparent,rgba(30,18,10,.85))"></div>'
        f'<div class="abs sc" style="left:0;right:0;bottom:200px;text-align:center;font-size:110px;color:{CREAM}">Rich, Print-Ready Detail</div>'
        f'<div class="abs cor" style="left:0;right:0;bottom:110px;text-align:center;font-size:66px;font-style:italic;color:#F0D5B0">high-resolution pages &#183; shown here zoomed in</div>')

def sizes(key, info):
    l = "file://" + os.path.join(OUT, key, "thumbs", sorted(os.listdir(os.path.join(OUT, key, "thumbs")))[info["hero"][0]])
    a4 = os.path.join(OUT, key, "pages_a4", sorted(os.listdir(os.path.join(OUT, key, "pages_a4")))[info["hero"][0]])
    a4t = a4.replace("pages_a4", "thumbs_a4"); os.makedirs(os.path.dirname(a4t), exist_ok=True)
    if not os.path.exists(a4t): im = Image.open(a4); im.thumbnail((900, 1800)); im.save(a4t, quality=90)
    return frame(paper_bg("p19_tea_stained_plain") +
        f'<div class="abs sc" style="left:0;right:0;top:110px;text-align:center;font-size:120px">Two Paper Sizes</div>'
        f'<div class="abs cor" style="left:0;right:0;top:270px;text-align:center;font-size:64px;font-style:italic;color:{RUST}">Print on the paper you already have</div>'
        + page_img(l, 820, 0, 120, 600) + page_img("file://" + a4t, 791, 0, 1060, 568) +
        f'<div class="abs sc" style="left:120px;width:820px;top:1740px;text-align:center;font-size:72px">US Letter</div>'
        f'<div class="abs cor" style="left:120px;width:820px;top:1830px;text-align:center;font-size:56px">8.5 x 11 in</div>'
        f'<div class="abs sc" style="left:1060px;width:791px;top:1740px;text-align:center;font-size:72px">A4</div>'
        f'<div class="abs cor" style="left:1060px;width:791px;top:1830px;text-align:center;font-size:56px">210 x 297 mm</div>'
        f'<div class="abs cor" style="left:0;right:0;top:2080px;text-align:center;font-size:60px">{info["files"]}</div>')

def how_to(key, info):
    t = thumbs(key)
    steps = info["steps"]
    cells = "".join(f'<div class="abs" style="left:{110+i*460}px;top:520px;width:420px;text-align:center">'
                    f'<div class="fell" style="font-size:150px;color:{RUST};line-height:1">{i+1}</div>'
                    f'<div class="sc" style="font-size:64px;margin:10px 0 14px">{s[0]}</div><div class="cor" style="font-size:46px;line-height:1.2">{s[1]}</div></div>'
                    for i, s in enumerate(steps))
    return frame(paper_bg("p19_tea_stained_plain") + f'<div class="abs sc" style="left:0;right:0;top:110px;text-align:center;font-size:120px">How It Works</div>{cells}'
                 + page_img(t[info["hero"][0]], 700, -4, 260, 1350, 1) + page_img(t[info["hero"][1]], 700, 5, 1040, 1380, 2))

def spread(key, info):
    t = thumbs(key)
    return frame(paper_bg("p20_dark_plain", 0.15) +
        "".join(page_img(t[j], 760, [-8, 6, -3, 9, -5, 4][i], [100, 1120, 620, 160, 1050, 600][i], [220, 260, 700, 1300, 1280, 1500][i], i)
                for i, j in enumerate(info["spread"]))
        + f'<div class="abs sc" style="left:0;right:0;bottom:0;height:260px;display:flex;align-items:center;justify-content:center;font-size:96px;color:{CREAM};background:rgba(43,29,20,.88);z-index:99">{info["spread_title"]}</div>')

def cut_spread(key, info, title):
    c = CUT[key]
    if key == "envelopes":
        ps = [("env01", 720, -6, 90, 380), ("env04", 640, 5, 1180, 300), ("poc08", 760, 3, 560, 820), ("poc12", 680, -4, 1180, 1230),
              ("env05", 760, -3, 80, 1300), ("poc10", 720, 6, 640, 1650)]
    else:
        ps = [(f"card{i:02d}", 460, r, x, y) for i, (r, x, y) in enumerate(
            [(-8, 120, 330), (4, 590, 300), (-3, 1060, 340), (7, 1460, 380), (5, 200, 1050), (-6, 680, 1000), (3, 1150, 1060), (-9, 1500, 1120)])]
    return frame(paper_bg("p20_dark_plain", 0.1) + "".join(piece(c[k], w, r, x, y, i) for i, (k, w, r, x, y) in enumerate(ps))
        + f'<div class="abs sc" style="left:0;right:0;bottom:0;height:260px;display:flex;align-items:center;justify-content:center;font-size:96px;color:{CREAM};background:rgba(43,29,20,.88);z-index:99">{title}</div>')

def collection(key, info):
    names = [("kit", "Junk Journal Kit"), ("papers", "Paper Pack"), ("envelopes", "Envelopes &amp; Pockets"), ("cards", "Journaling Cards")]
    cells = ""
    for i, (k, n) in enumerate(names):
        if not os.path.isdir(os.path.join(OUT, k, "pages_letter")):
            raise SystemExit(f"collection : le produit {k} n'est pas encore construit")
        u = thumbs(k)[PHOTO[k]["hero"][0]]
        x = 140 + (i % 2) * 900; y = 420 + (i // 2) * 1000
        cells += (page_img(u, 620, 0, x + 50, y) + f'<div class="abs sc" style="left:{x}px;width:720px;top:{y+830}px;text-align:center;font-size:58px;'
                  f'{"color:" + RUST if k == key else ""}">{n}{" &#8226; this listing" if k == key else ""}</div>')
    return frame(paper_bg("p19_tea_stained_plain") + f'<div class="abs sc" style="left:0;right:0;top:110px;text-align:center;font-size:110px">The Ember &amp; Oak Collection</div>'
                 f'<div class="abs cor" style="left:0;right:0;top:250px;text-align:center;font-size:60px;font-style:italic;color:{RUST}">Every piece is designed to match</div>{cells}')

def good_to_know(key, info):
    pts = ["Digital download &#8212; nothing is shipped", info["files"], "Print at home or at a print shop, at 100% / actual size",
           "Download from Etsy Purchases in a web browser", "Personal use and physical handmade items you sell are welcome",
           "Some artwork created with AI tools, finished by hand"]
    items = "".join(f'<div style="display:flex;gap:30px;margin-bottom:46px"><div style="color:{RUST};font-size:70px">&#10087;</div>'
                    f'<div class="cor" style="font-size:66px;line-height:1.2">{p}</div></div>' for p in pts)
    return frame(paper_bg("p19_tea_stained_plain") + f'<div class="abs sc" style="left:0;right:0;top:110px;text-align:center;font-size:120px">Good to Know</div>'
                 f'<div class="abs" style="left:170px;right:170px;top:420px">{items}</div>')

PHOTO = {
 "kit": dict(title="Autumn Junk<br>Journal Kit", tl=2, sub="vintage botanical &#183; dark academia", num="124", unit="pieces", hero=[2, 22, 30],
   get=["20 full-page vintage papers", "6 sheets of cut-apart ephemera", "12 envelope &amp; pocket templates (20 pieces)", "62 journaling cards in 2 sizes",
        "4 lined journaling pages", "Start-here guide &amp; printing tips"], strip=[3, 24, 33, 42],
   files="4 PDF files: Part 1 + Part 2, in US Letter and A4", zoom=22, zpos="50% 30%",
   steps=[("Print", "on matte paper or light cardstock"), ("Cut", "papers, ephemera and cards"), ("Fold", "envelopes and pockets"), ("Create", "your autumn journal")],
   spread=[3, 30, 24, 45, 6, 34], spread_title="Everything Matches"),
 "papers": dict(title="Autumn Paper<br>Pack", tl=2, sub="20 vintage botanical papers", num="20", unit="papers", hero=[2, 5, 4],
   get=["20 full-page autumn vintage papers", "Botanical focal papers, patterns and solids", "Full bleed, high resolution", "Start-here guide &amp; printing tips"],
   strip=[3, 6, 11, 14], files="2 PDF files: US Letter and A4", zoom=4, zpos="45% 40%",
   steps=[("Print", "full page, at 100%"), ("Cut", "pages, mats or tags"), ("Layer", "papers and ephemera"), ("Create", "your journal")],
   spread=[2, 5, 9, 12, 15, 18], spread_title="Layer Them Together"),
 "envelopes": dict(title="Envelopes<br>&amp; Pockets", tl=2, sub="printable junk journal templates", num="20", unit="pieces", hero=[2, 8, 12],
   get=["6 envelopes in 3 shapes", "4 library card pockets", "2 tuck-in page pockets", "4 tall pocket tags", "4 belly bands", "Start-here guide &amp; folding tips"],
   strip=[3, 6, 9, 13], files="2 PDF files: US Letter and A4", zoom=3, zpos="50% 50%",
   steps=[("Print", "at 100% / actual size"), ("Cut", "on the solid line"), ("Fold", "on the dashed lines"), ("Glue", "the tabs and fill it")],
   spread=[2, 4, 6, 8, 10, 12], spread_title="Pockets for Every Page"),
 "cards": dict(title="Journaling<br>Cards", tl=2, sub="autumn vintage &#183; printable", num="62", unit="cards", hero=[2, 3, 8],
   get=["54 cards, 2.5 x 3.5 in (ATC size)", "27 illustrated + 27 lined", "8 lined cards, 3 x 4 in", "4 full-page lined journaling pages", "Start-here guide &amp; printing tips"],
   strip=[2, 3, 8, 10], files="2 PDF files: US Letter and A4", zoom=2, zpos="20% 15%",
   steps=[("Print", "at 100% / actual size"), ("Cut", "on the outer line"), ("Write", "your memories"), ("Tuck", "into pockets")],
   spread=[2, 3, 4, 5, 8, 10], spread_title="62 Cards to Write On"),
}

def photo_set(key, skip_collection=False):
    info = PHOTO[key]
    extra = all_pages(key, info, 22, None, "Part 2 Pages") if key == "kit" else (
        all_pages(key, info, 2, None, "All 20 Papers") if key == "papers" else cut_spread(key, info, "Cut Out, Ready to Fill" if key == "envelopes" else "Write, Tuck and Layer"))
    return [what_you_get(key, info), all_pages(key, info, 2, 20 if key == "kit" else None, "Part 1 Pages" if key == "kit" else "Every Page Included"),
            closeup(key, info), sizes(key, info), how_to(key, info), spread(key, info), (frame("") if skip_collection else collection(key, info)), extra, good_to_know(key, info)]

async def _cut(jobs):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=B.CHROME)
        for html, out, w, h in jobs:
            pg = await b.new_page(viewport={"width": round(w / 25.4 * 96), "height": round(h / 25.4 * 96)}, device_scale_factor=2)
            tmp = out + ".html"; open(tmp, "w").write(html)
            await pg.goto("file://" + tmp); await pg.wait_for_load_state("networkidle"); await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=out, omit_background=True); await pg.close(); os.remove(tmp)
            im = Image.open(out).convert("RGBA"); im.crop(im.getchannel("A").getbbox()).save(out)
        await b.close()

def cutouts(key):
    """Pièces découpées (fond transparent) : enveloppes/pochettes et cartes, pour les photos."""
    d = os.path.join(OUT, key, "cutouts"); os.makedirs(d, exist_ok=True); jobs = []
    if key in ("envelopes", "kit"):
        P.CUTOUT = True
        for k, *_ in P.ENVELOPES: jobs.append((P.env_page(k, "letter"), os.path.join(d, k + ".png"), *P.SIZES["letter"]))
        P.CUTOUT = False
    if key in ("cards", "kit"):
        for i in range(12): jobs.append((P.card_cutout(i, "art" if i % 2 == 0 else "lined"), os.path.join(d, f"card{i:02d}.png"), 63.5, 88.9))
    asyncio.run(_cut(jobs))
    return {os.path.basename(j[1])[:-4]: "file://" + j[1] for j in jobs}

async def shoot(jobs):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=B.CHROME)
        for html, out in jobs:
            pg = await b.new_page(viewport={"width": 2000, "height": 2500})
            tmp = out + ".html"; open(tmp, "w").write(html)
            await pg.goto("file://" + tmp); await pg.wait_for_load_state("networkidle"); await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=out, type="jpeg", quality=90); await pg.close(); os.remove(tmp)
        await b.close()

def run(key, skip_collection=False):
    d = os.path.join(OUT, key, "photos"); os.makedirs(d, exist_ok=True)
    if key != "papers": CUT[key] = cutouts(key)
    jobs = [(h, os.path.join(d, f"main_v{i}.jpg")) for i, h in enumerate(main_variants(key, PHOTO[key]), 1)]
    jobs += [(h, os.path.join(d, f"photo_{i:02d}.jpg")) for i, h in enumerate(photo_set(key, skip_collection), 2)]
    asyncio.run(shoot(jobs)); print(key, "photos ok", flush=True)

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(PHOTO)): run(k)


def board(key):
    """Planche : nos 3 variantes (cadre rouge) au milieu des 10 miniatures concurrentes, en tuiles de 300 px."""
    cj = json.load(open(os.path.join(H, "concurrents", "concurrents.json")))[key][:10]
    ours = [os.path.join(OUT, key, "photos", f"main_v{i}.jpg") for i in (1, 2, 3)]
    tiles = [(os.path.join(H, "concurrents", c["f"]), False) for c in cj]
    for i, o in enumerate(ours): tiles.insert([2, 6, 10][i], (o, True))
    W, Hh, cols = 300, 300, 5
    c = Image.new("RGB", (cols * (W + 16) + 16, ((len(tiles) + cols - 1) // cols) * (Hh + 16) + 16), "white")
    from PIL import ImageOps, ImageDraw
    for i, (f, mine) in enumerate(tiles):
        im = ImageOps.fit(Image.open(f).convert("RGB"), (W, Hh)); x, y = 16 + (i % cols) * (W + 16), 16 + (i // cols) * (Hh + 16)
        c.paste(im, (x, y))
        if mine: ImageDraw.Draw(c).rectangle([x - 6, y - 6, x + W + 5, y + Hh + 5], outline=(210, 30, 30), width=6)
    out = os.path.join(OUT, key, "photos", "board.jpg"); c.save(out, quality=90); return out
