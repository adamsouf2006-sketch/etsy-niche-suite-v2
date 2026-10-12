# Vérification complète des 4 produits Ember & Oak avant mise en brouillon. Sortie : liste des échecs (0 = OK).
import os, re, json, subprocess, sys
from PIL import Image
from pypdf import PdfReader
from spellchecker import SpellChecker
import pages as P, build as B, listings as L

H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "out")
FAIL = []; INFO = []
def fail(m): FAIL.append(m)

# 1. illustrations
import gen_art_list
for k in gen_art_list.KEYS:
    p = os.path.join(P.ART, k + ".png")
    if not os.path.exists(p): fail(f"illustration manquante : {k}"); continue
    if Image.open(p).size != (2048, 3072): fail(f"illustration {k} : taille {Image.open(p).size}")

EXPECT = {"papers": dict(pages=22, files=2), "envelopes": dict(pages=14, files=2), "cards": dict(pages=14, files=2), "kit": dict(pages=52, files=4)}
PT = {"letter": (612.0, 792.0), "a4": (595.28, 841.89)}
PX = {"letter": (2550, 3300), "a4": (2481, 3509)}
# comptes réels, recalculés depuis le modèle
n_cards = 6 * 9 + 2 * 4
n_pieces = sum({"envelope_pointed": 1, "envelope_square": 1, "envelope_wallet": 1, "library_pockets": 2, "tuck_pocket": 1,
                "tags_sheet": 4, "belly_bands": 4}[fn.__name__] for _, fn, _, _ in P.ENVELOPES)
n_eph_designs = len({e for n in range(6) for e in (P.ELEMS[n * 3 % 14:] + P.ELEMS)[:3]})
INFO.append(f"cartes={n_cards} pièces={n_pieces} motifs éphémères={n_eph_designs}")
if n_cards != 62: fail(f"cartes : {n_cards} au lieu de 62")
if n_pieces != 20: fail(f"pièces enveloppes/pochettes : {n_pieces} au lieu de 20")
if n_eph_designs != 14: fail(f"motifs éphémères : {n_eph_designs} au lieu de 14")

sp = SpellChecker(); sp.word_frequency.load_words(["journaling", "journalers", "ephemera", "scrapbookers", "scrapbook", "scrapbooks", "dpi", "oakfold",
    "ember", "goodnotes", "procreate", "cardstock", "gsm", "inkjet", "botanicals", "cottagecore", "atc", "pdf", "pdfs", "etsy", "printables",
    "junk", "apothecary", "damask", "pinecones", "walnut", "signatures", "mats", "full", "bleed", "tuck", "fall", "memory", "keepers", "keepsakes",
    "keepsake", "moonlit", "lined", "app", "crafters", "html", "a4", "us", "x", "in", "mm", "ai", "faq", "printable", "foxing", "academia", "sepia", "ochre", "rowan", "e-mail"])

def spell(text, where):
    words = re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r"&\w+;|<[^>]+>", " ", text))
    bad = sp.unknown([w.lower().strip("'-") for w in words if len(w) > 2])
    if bad: fail(f"orthographe {where} : {sorted(bad)}")
    if "fiche" in where and re.search(r"\S  +\S", text): fail(f"espace double {where}")
    for bad_us in ["colour", "favourite", "cancelled", "centre", "grey"]:
        if bad_us in text.lower(): fail(f"orthographe non américaine {where} : {bad_us}")

for key, exp in EXPECT.items():
    d = os.path.join(OUT, key)
    man = json.load(open(os.path.join(d, "manifest.json")))
    # 2. pages
    if len(man["pages"]) != exp["pages"]: fail(f"{key} : {len(man['pages'])} pages au lieu de {exp['pages']}")
    if man["missing_art"]: fail(f"{key} : rendu avec images manquantes {man['missing_art']}")
    for k, v in man["checks"].items(): fail(f"{key} {k} : {v}")
    for size in ("letter", "a4"):
        fs = sorted(os.listdir(os.path.join(d, "pages_" + size)))
        if len(fs) != exp["pages"]: fail(f"{key} {size} : {len(fs)} images de pages")
        for f in fs:
            s = Image.open(os.path.join(d, "pages_" + size, f)).size
            dpi = B.ART_DPI if any(f"_{k}_" in f for k in B.ART_KINDS) else B.DPI
            ex = (P.SIZES[size][0] / 25.4 * dpi, P.SIZES[size][1] / 25.4 * dpi)
            if abs(s[0] - ex[0]) > 2 or abs(s[1] - ex[1]) > 2: fail(f"{key} {size} {f} : {s} au lieu de {ex}")
            im = Image.open(os.path.join(d, "pages_" + size, f)).convert("L").resize((60, 80))
            if max(im.getdata()) - min(im.getdata()) < 25: fail(f"{key} {size} {f} : page presque vide")
    # 3. PDF
    if len(man["files"]) != exp["files"] or len(man["files"]) > 5: fail(f"{key} : {len(man['files'])} fichiers")
    total = 0
    for f in man["files"]:
        p = os.path.join(d, f); sz = os.path.getsize(p)
        if sz > 20e6: fail(f"{key} {f} : {sz/1e6:.1f} Mo > 20 Mo")
        r = PdfReader(p); total += len(r.pages)
        size = "a4" if "_A4" in f else "letter"
        for pg in r.pages:
            w, h = float(pg.mediabox.width), float(pg.mediabox.height)
            if abs(w - PT[size][0]) > 1 or abs(h - PT[size][1]) > 1: fail(f"{key} {f} : page {w}x{h} pt"); break
    INFO.append(f"{key} : {len(man['files'])} PDF, {total} pages PDF au total")
    exp_pdf_pages = exp["pages"] * 2 + (4 if key == "kit" else 0)   # le kit répète les 2 pages START HERE dans la partie 2
    if total != exp_pdf_pages: fail(f"{key} : {total} pages dans les PDF au lieu de {exp_pdf_pages}")
    # 4. fiche
    li = L.LISTINGS[key]; t = li["title"]; tags = li["tags"]; desc = li["description"]
    if len(t) > 140: fail(f"{key} titre {len(t)} caractères")
    if t.count("&") > 1 or t.count("%") > 1 or t.count(":") > 1: fail(f"{key} titre : caractères spéciaux")
    if sum(1 for w in t.split() if w.isupper() and len(w) > 1) > 3: fail(f"{key} titre : trop de majuscules")
    if len(tags) != 13 or len(set(tags)) != 13: fail(f"{key} : {len(tags)} tags ({len(set(tags))} uniques)")
    for g in tags:
        if len(g) > 20: fail(f"{key} tag trop long : {g}")
        if not re.fullmatch(r"[a-z0-9 ]+", g): fail(f"{key} tag caractères : {g}")
        if g in ("digital download", "instant download", "printable", "editable template", "pdf"): fail(f"{key} tag générique : {g}")
    m = re.search(r"WHAT YOU GET: (\d+) printable pages", desc)
    if not m or int(m.group(1)) != exp["pages"]: fail(f"{key} description : nombre de pages {m and m.group(1)} au lieu de {exp['pages']}")
    if f"You receive {['', '', '2', '', '4'][exp['files']]} PDF files" not in desc: fail(f"{key} description : nombre de fichiers")
    for num, lab in [("62", "journaling cards"), ("16", "pieces")]:
        if key in ("kit", "cards") and lab == "journaling cards" and f"{num} journaling cards" not in desc: fail(f"{key} description : 62 cartes")
    if key == "kit" and "124 pieces in total" not in desc: fail("kit description : 124 pièces")
    if key == "kit" and 20 + 18 + n_pieces + n_cards + 4 != 124: fail("kit : le total de 124 pièces ne correspond plus au contenu")
    if key == "envelopes" and "20 pieces" not in desc: fail("envelopes description : 20 pièces")
    if key in ("kit",) and "(20 pieces)" not in desc: fail("kit description : 20 pièces")
    if key in ("kit", "papers") and "20 full-page papers" not in desc: fail(f"{key} description : 20 papiers")
    if t[:28].lower() in desc[:200].lower(): fail(f"{key} : la description recopie le titre")
    spell(t + " " + " ".join(tags) + " " + desc, f"{key} fiche")
    # 5. photos
    ph = os.path.join(d, "photos"); sel = json.load(open(os.path.join(ph, "selection.json")))
    if len(sel) != 10: fail(f"{key} : {len(sel)} photos")
    for f in sel:
        im = Image.open(os.path.join(ph, f))
        if im.size != (2000, 2500): fail(f"{key} photo {f} : {im.size}")
        if os.path.getsize(os.path.join(ph, f)) > 10e6: fail(f"{key} photo {f} trop lourde")
    # 6. vidéo
    v = os.path.join(d, "video.mp4")
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", v], capture_output=True, text=True).stdout)
    vs = [s for s in pr["streams"] if s["codec_type"] == "video"]; au = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    dur = float(pr["format"]["duration"])
    if not vs or vs[0]["codec_name"] != "h264" or (vs[0]["width"], vs[0]["height"]) != (1080, 1080) or vs[0]["pix_fmt"] != "yuv420p": fail(f"{key} vidéo : format")
    if not au: fail(f"{key} vidéo : pas de piste audio")
    if not 3 <= dur <= 15: fail(f"{key} vidéo : durée {dur}")
    if os.path.getsize(v) > 100e6: fail(f"{key} vidéo trop lourde")

# 7. textes des pages (guide START HERE, étiquettes)
txt = " ".join(" ".join(p["contents"]) + " " + p["files_note"] + " " + p["howto"] + " " + p["name"] for p in B.PRODUCTS.values())
txt += " " + " ".join(P.WORDS) + " " + open(os.path.join(H, "pages.py")).read().split("def start_page")[1].split("def card_cutout")[0]
spell(re.sub(r"\{[^}]*\}|f\"\"\"|\"\"\"|style=\"[^\"]*\"|class=\"[^\"]*\"|[A-Za-z_]+\(|\b(?:div|li|ul|b|br|mm|pt|px|sc|cor|fell|abs|size|body|product|doc|art|inset|url|center|cover|solid|border|font|color|margin|padding|left|line|height|absolute|position|background|bottom|top|text|align|style|weight|normal|italic|letter|spacing|em|return|else|if|def|in|for|self|key|bold)\b", " ", txt), "pages")

print("\n".join(INFO))
print(f"\n{len(FAIL)} échec(s)")
for f in FAIL: print(" -", f)
sys.exit(1 if FAIL else 0)
