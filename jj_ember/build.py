# Construit les 4 produits Ember & Oak : pages JPEG 240 dpi -> PDF (US Letter + A4) -> dossiers de livraison.
# Usage : python3 build.py [produit ...]   (sans argument : tous)
import os, sys, asyncio, shutil, json
from playwright.async_api import async_playwright
import img2pdf
from PIL import Image
import pages as P

H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, "out")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
DPI = 240
ART_DPI = 240            # pages pleine illustration : résolution native des images (2048 px sur 8,5 po)
ART_KINDS = ("paper", "eph", "lined", "start")
ART_Q = 82
JPEG_Q = 82

ENV_KEYS = [e[0] for e in P.ENVELOPES]
PRODUCTS = {
 "papers": dict(name="Printable Paper Pack", slug="EmberOak_Paper_Pack",
   contents=["20 full-page autumn vintage papers (backgrounds, botanicals, patterns and solids)", "2 START HERE pages (this guide)"],
   files_note="One PDF for US Letter (8.5 x 11 in) and one for A4. Every page is full bleed, at the full resolution of the artwork.",
   howto="Print, cut and layer the papers as journal pages, page backgrounds, signatures, covers, mats and collage pieces.",
   pages=[("paper", k) for k in P.PAPERS]),
 "envelopes": dict(name="Printable Envelopes &amp; Pockets", slug="EmberOak_Envelopes_Pockets",
   contents=["6 envelope templates in 3 shapes (pointed flap, rounded square, wallet)", "2 sheets of library card pockets (4 pockets)",
             "2 tuck-in page pockets", "1 sheet of 4 tall pocket tags", "1 sheet of 4 belly bands", "2 START HERE pages (this guide)"],
   files_note="One PDF for US Letter (8.5 x 11 in) and one for A4. Templates are printed ready to cut: solid line = cut, dashed line = fold.",
   howto="Print at actual size, cut on the solid line, score and fold on the dashed lines, then glue the side tabs. Tuck cards, tags and photos inside.",
   pages=[("env", k) for k in ENV_KEYS]),
 "cards": dict(name="Journaling Cards &amp; Pages", slug="EmberOak_Journaling_Cards",
   contents=["54 journaling cards, 2.5 x 3.5 in (27 illustrated + 27 lined)", "8 lined journaling cards, 3 x 4 in",
             "4 full-page lined journaling pages", "2 START HERE pages (this guide)"],
   files_note="One PDF for US Letter (8.5 x 11 in) and one for A4. Cards print at their true size on both papers.",
   howto="Print, cut the cards on their outer line, then write, stamp, tuck them into pockets or glue them onto your pages.",
   pages=[("cards", i) for i in range(8)] + [("lined", i) for i in range(4)]),
}
PRODUCTS["kit"] = dict(name="Junk Journal Kit", slug="EmberOak_Junk_Journal_Kit",
   contents=["20 full-page papers", "12 envelope and pocket templates (16 pieces)", "62 journaling cards (2 sizes)", "4 lined journaling pages",
             "6 sheets of cut-apart ephemera (18 pieces, 14 designs)", "2 START HERE pages (this guide)"],
   files_note="Two PDFs per paper size (Part 1: papers, Part 2: ephemera, envelopes, pockets, cards and pages), for US Letter (8.5 x 11 in) and A4.",
   howto="Use the papers as pages and covers, build pockets and envelopes from the templates, then fill them with cards, tags and ephemera.",
   pages=PRODUCTS["papers"]["pages"] + [("eph", i) for i in range(6)] + PRODUCTS["envelopes"]["pages"] + PRODUCTS["cards"]["pages"],
   split=22)

def html_for(kind, k, size, prod):
    if kind == "paper": return P.paper_page(k, size)
    if kind == "env": return P.env_page(k, size)
    if kind == "cards": return P.cards_page(k, size)
    if kind == "lined": return P.lined_page(k, size)
    if kind == "eph": return P.ephemera_page(k, size)
    if kind == "start": return P.start_page(prod, k, size)

CHECKS = {}
# Contrôles dans la page rendue : formes et textes dans la marge de 4 mm, aucun texte coupé, polices chargées.
CHECK_JS = """(m) => {
 const W = innerWidth, H = innerHeight, bad = [];
 const inside = (r) => r.left >= m - 0.5 && r.top >= m - 0.5 && r.right <= W - m + 0.5 && r.bottom <= H - m + 0.5;
 document.querySelectorAll('svg path, svg rect, svg circle, svg text').forEach(e => { if (!inside(e.getBoundingClientRect())) bad.push('forme hors marge: ' + e.tagName + ' ' + (e.textContent || '').slice(0, 20)); });
 document.querySelectorAll('.pg *').forEach(e => {
   if (e.closest('svg') || e.children.length || !e.textContent.trim()) return;
   const rg = document.createRange(); rg.selectNodeContents(e); const r = rg.getBoundingClientRect();
   if (!inside(r)) bad.push('texte hors marge: ' + e.textContent.trim().slice(0, 30));
   if (e.scrollWidth > e.clientWidth + 1) bad.push('texte coupé: ' + e.textContent.trim().slice(0, 30));
   const fam = getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '').trim();
   const cs = getComputedStyle(e); if (!document.fonts.check(cs.fontStyle + ' ' + cs.fontWeight + ' 12px "' + fam + '"', e.textContent)) bad.push('police non chargée: ' + fam);
 });
 document.fonts.forEach(f => { if (f.status === 'error') bad.push('police en erreur: ' + f.family); });
 const imgs = [...document.querySelectorAll('image')].filter(i => !i.href.baseVal);
 if (imgs.length) bad.push('image vide');
 return bad;
}"""

async def render_all(jobs):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME)
        for html, out, size in jobs:
            w, h = P.SIZES[size]
            dpi = ART_DPI if any(f"_{k}_" in os.path.basename(out) for k in ART_KINDS) else DPI
            pg = await b.new_page(viewport={"width": round(w / 25.4 * 96), "height": round(h / 25.4 * 96)}, device_scale_factor=dpi / 96)
            tmp = out + ".html"; open(tmp, "w").write(html)
            await pg.goto("file://" + tmp); await pg.wait_for_load_state("networkidle"); await pg.evaluate("document.fonts.ready")
            CHECKS[out] = await pg.evaluate(CHECK_JS, 4 / 25.4 * 96)
            await pg.screenshot(path=out + ".png", full_page=False); await pg.close(); os.remove(tmp)
            im = Image.open(out + ".png").convert("RGB"); im.save(out, quality=ART_Q if dpi == ART_DPI else JPEG_Q, dpi=(dpi, dpi), optimize=True); os.remove(out + ".png")
        await b.close()

LIMIT = 19.5e6   # Etsy : 20 Mo par fichier
def make_pdf(imgs, size, path, q=None):
    """PDF sans réencodage (img2pdf insère les JPEG tels quels), page au format exact ; recompression si > 19,5 Mo."""
    w, h = P.SIZES[size]; tmp = []
    src = []
    for im in imgs:
        if q:
            t = im + f".q{q}.jpg"; Image.open(im).save(t, quality=q, dpi=Image.open(im).info.get("dpi", (DPI, DPI)), optimize=True); tmp.append(t); im = t
        src.append(im)
    layout = img2pdf.get_layout_fun((img2pdf.mm_to_pt(w), img2pdf.mm_to_pt(h)), fit=img2pdf.FitMode.exact)
    with open(path, "wb") as f:
        f.write(img2pdf.convert(src, layout_fun=layout, title=os.path.basename(path)[:-4].replace("_", " "), author="Oakfold"))
    for t in tmp: os.remove(t)
    if os.path.getsize(path) > LIMIT:
        nq = (q or JPEG_Q) - 4
        if nq < 70: raise SystemExit(f"{path} : toujours > 20 Mo à la qualité 70")
        return make_pdf(imgs, size, path, nq)
    return q or JPEG_Q

def build(key):
    prod = PRODUCTS[key]; pages = [("start", 0), ("start", 1)] + prod["pages"]
    d = os.path.join(OUT, key); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    jobs = []
    for size in ("letter", "a4"):
        os.makedirs(os.path.join(d, "pages_" + size))
        for n, (kind, k) in enumerate(pages, 1):
            jobs.append((html_for(kind, k, size, prod), os.path.join(d, "pages_" + size, f"{n:02d}_{kind}_{k}.jpg"), size))
    asyncio.run(render_all(jobs))
    files = []; qs = {}
    for size, lab in (("letter", "US_Letter"), ("a4", "A4")):
        imgs = sorted(os.path.join(d, "pages_" + size, f) for f in os.listdir(os.path.join(d, "pages_" + size)))
        parts = [imgs] if "split" not in prod else [imgs[:prod["split"]], imgs[:2] + imgs[prod["split"]:]]
        for i, part in enumerate(parts, 1):
            fn = f"{prod['slug']}_{lab}" + (f"_Part{i}" if len(parts) > 1 else "") + ".pdf"
            qs[fn] = make_pdf(part, size, os.path.join(d, fn)); files.append(fn)
    checks = {os.path.relpath(k, d): v for k, v in CHECKS.items() if v and k.startswith(d)}
    json.dump({"pages": [f"{kind}:{k}" for kind, k in pages], "files": files, "jpeg_quality": qs, "missing_art": sorted(P.MISSING), "checks": checks}, open(os.path.join(d, "manifest.json"), "w"), indent=1)
    print(key, len(pages), "pages", [(f, round(os.path.getsize(os.path.join(d, f)) / 1e6, 1)) for f in files], flush=True)

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(PRODUCTS)): build(k)
