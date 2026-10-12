# Génère les illustrations Ember & Oak avec l'API Agnès (une à la fois, attente sur limite, cache sur disque)
import json,os,sys,time,base64,io,urllib.request
from PIL import Image
K=os.environ.get("AGNES_API_KEY") or open(os.path.expanduser("~/.agnes_key")).read().strip()
URL="https://apihub.agnes-ai.com/v1/images/generations"
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),"art")
STYLE=", antique 19th century hand-colored engraving style, muted rust, ochre, burnt orange, sage green and sepia palette, dark academia autumn mood, high detail, flat even lighting, no text, no letters, no watermark, no border, no frame"
PAGE="Full-page vintage junk journal background paper, "
EL="Single isolated vintage illustration centered on a plain flat warm cream paper background with generous empty margin, "
ART={
 # papiers pleine page (2:3)
 "p01_maple_parchment":(PAGE+"aged parchment with foxing and soft tea stains, faded handwritten script lines, a large red maple branch with falling leaves","2048x3072"),
 "p02_ledger_leaves":(PAGE+"antique accounting ledger page with faint ruled columns and handwritten ink numbers only, pressed oak, ginkgo and birch leaves, coffee ring stains, no people, no figures, no characters","2048x3072"),
 "p03_fern_forest_dark":(PAGE+"dark umber background, gold-toned ferns, toadstool mushrooms and moths on the forest floor","2048x3072"),
 "p04_owl_moon":(PAGE+"deep burgundy and black aged paper, barn owl perched on an oak branch under a crescent moon, falling leaves, muted gold accents","2048x3072"),
 "p05_mushroom_plate":(PAGE+"natural history plate of many different woodland mushrooms arranged in rows on cream paper","2048x3072"),
 "p06_moth_specimens":(PAGE+"entomology specimen plate with rows of brown and rust moths pinned on aged cream paper","2048x3072"),
 "p07_letters_postmarks":(PAGE+"layered old envelopes, handwritten letters, wax seal and faded postmarks in sepia, a few autumn leaves","2048x3072"),
 "p08_crow_branches":(PAGE+"black crows on bare autumn branches against a misty sepia sky, aged paper texture","2048x3072"),
 "p09_pumpkin_harvest":(PAGE+"heirloom pumpkins, gourds and wheat sheaves still life on cream paper","2048x3072"),
 "p10_damask_rust":("Seamless vintage wallpaper pattern, rust and cream damask with small oak leaves and acorns, worn aged paper texture","2048x3072"),
 "p11_botanical_pattern_sage":("Seamless vintage wallpaper pattern, sage green background with small scattered ferns, berries and leaves, worn aged paper texture","2048x3072"),
 "p12_plaid_autumn":("Seamless vintage woven plaid fabric texture in rust, mustard, brown and cream, slightly faded and worn","2048x3072"),
 "p13_library_books":(PAGE+"stacked antique leather books, a brass key, dried flowers and a candle, warm sepia","2048x3072"),
 "p14_sheet_music_leaves":(PAGE+"aged antique sheet music page with musical staves, scattered dried maple and oak leaves","2048x3072"),
 "p15_map_autumn":(PAGE+"faded antique hand-drawn map of an imaginary forest region with rivers, hills and tiny trees, a decorative compass star with no letters, sepia, autumn leaves in the corner, no words, no labels","2048x3072"),
 "p16_apothecary":(PAGE+"apothecary shelf with antique glass bottles, dried herbs and botanical sprigs, sepia and amber","2048x3072"),
 "p17_pinecone_berries":(PAGE+"pinecones, rose hips and rowan berries on branches, cream paper","2048x3072"),
 "p18_dark_leaves_scatter":(PAGE+"scattered pressed autumn leaves on a very dark brown aged paper, moody","2048x3072"),
 "p19_tea_stained_plain":(PAGE+"plain aged tea-stained paper with soft foxing and subtle grunge edges, nearly empty, light cream","2048x3072"),
 "p20_dark_plain":(PAGE+"plain dark walnut brown aged paper texture with subtle grunge, nearly empty","2048x3072"),
 # éléments (2:3 aussi, sur fond crème)
 "e01_oak_acorns":(EL+"oak leaves branch with acorns","2048x3072"),
 "e02_maple":(EL+"three red and orange maple leaves","2048x3072"),
 "e03_fern":(EL+"a curled fern frond","2048x3072"),
 "e04_mushrooms":(EL+"a cluster of brown woodland mushrooms with moss","2048x3072"),
 "e05_moth":(EL+"a single large brown and rust moth with open wings","2048x3072"),
 "e06_owl":(EL+"a small barn owl standing","2048x3072"),
 "e07_key_watch":(EL+"an antique brass skeleton key and a closed engraved brass pocket watch with the lid shut, no dial, no numbers visible","2048x3072"),
 "e08_crow":(EL+"a black crow standing in profile","2048x3072"),
 "e09_pumpkin":(EL+"a small heirloom pumpkin with leaves","2048x3072"),
 "e10_bottle":(EL+"an antique amber apothecary bottle with a cork and dried lavender","2048x3072"),
 "e11_feather":(EL+"a long brown pheasant feather","2048x3072"),
 "e12_wreath":(EL+"an autumn wreath of oak leaves, berries and wheat, empty center","2048x3072"),
 "e13_books":(EL+"a small stack of three antique books with a candle","2048x3072"),
 "e14_pressed_flowers":(EL+"pressed dried wildflowers and grasses","2048x3072"),
}
def call(model,prompt,size):
    req=urllib.request.Request(URL,data=json.dumps({"model":model,"prompt":prompt,"size":size,"response_format":"b64_json"}).encode(),
        headers={"Authorization":"Bearer "+K,"Content-Type":"application/json"})
    try: j=json.load(urllib.request.urlopen(req,timeout=400))
    except urllib.error.HTTPError as e: j=json.loads(e.read() or b"{}")
    return j
def log(*a): print(time.strftime("%H:%M:%S"),*a,flush=True)
todo=[k for k in ART if not os.path.exists(os.path.join(D,k+".png"))]
log("a generer",len(todo))
wait=60
for k in todo:
    p,s=ART[k]; prompt=p+STYLE
    for model in ("agnes-image-2.5-flash","agnes-image-2.1-flash"):
        while True:
            j=call(model,prompt,s); err=(j.get("error") or {})
            if err.get("code")=="rate_limit_exceeded":
                log("limite, attente",wait,"s"); time.sleep(wait); wait=min(wait*2,900); continue
            break
        b=((j.get("data") or [{}])[0]).get("b64_json")
        if b:
            im=Image.open(io.BytesIO(base64.b64decode(b))).convert("RGB"); im.save(os.path.join(D,k+".png"))
            json.dump({"model":model,"prompt":prompt,"size":im.size},open(os.path.join(D,k+".json"),"w"))
            log("ok",k,model,im.size); wait=60; break
        log("echec",k,model,str(j)[:200])
log("fini")
