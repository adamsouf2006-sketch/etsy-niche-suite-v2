# Génère les illustrations Ember & Oak avec l'API Agnès (une à la fois, attente sur limite, cache sur disque)
import json,os,sys,time,base64,io,urllib.request
from PIL import Image
K=os.environ.get("AGNES_API_KEY") or open(os.path.expanduser("~/.agnes_key")).read().strip()
URL="https://apihub.agnes-ai.com/v1/images/generations"
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),"art")
STYLE=", delicate hand-painted watercolor wedding stationery illustration, soft ivory, sage green, eucalyptus and dusty blush palette, elegant fine-art style, clean isolated on a plain flat white background, generous empty margin, no text, no letters, no watermark, no frame"
ART={
 "w01_corner_florals":("Corner arrangement of white garden roses, eucalyptus and olive leaves for the top-left corner of a wedding invitation","2048x2048"),
 "w02_arch_frame":("Tall arch-shaped frame made of eucalyptus, olive branches and small white flowers, empty center","2048x3072"),
 "w03_wreath":("Round greenery wreath of olive and eucalyptus leaves with a few white roses, empty center","2048x2048"),
 "w04_sprig_divider":("Single long horizontal olive sprig used as a text divider","3072x1024"),
 "w05_bouquet":("Elegant hand-tied bridal bouquet of white roses, ranunculus and eucalyptus","2048x3072"),
 "w06_greenery_swag":("Long horizontal greenery garland swag of eucalyptus and olive leaves","3072x1024"),
 "w07_venue_sketch":("Watercolor sketch of a charming countryside chateau wedding venue with trees, soft and airy","3072x2048"),
 "w08_champagne":("Two champagne glasses toasting with a small sprig of olive","2048x2048"),
 "w09_rings":("Two gold wedding rings resting on a small sprig of eucalyptus","2048x2048"),
 "w10_envelope":("Ivory envelope with a sage green wax seal and a sprig of olive","3072x2048"),
 "w11_corner_florals_blush":("Corner arrangement of blush pink peonies, white roses and eucalyptus for the bottom-right corner of a wedding invitation","2048x2048"),
 "w12_watercolor_wash":("Very soft abstract sage green watercolor wash texture, light and airy, mostly empty","3072x2048"),
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
