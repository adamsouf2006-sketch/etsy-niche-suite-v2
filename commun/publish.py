# Publie un produit sur Etsy à partir de son listing.json (photos, vidéo, fichiers).
# Usage: ETSY_KEY="keystring:secret" python3 commun/publish.py produit_xxx [--draft]
import json,os,sys,uuid,urllib.request,urllib.parse
D=sys.argv[1]; DRAFT="--draft" in sys.argv
K=os.environ["ETSY_KEY"]; A="https://openapi.etsy.com/v3/application/"
TOK="/tmp/etsy_oauth.json"
if os.path.exists(TOK): O=json.load(open(TOK))
elif os.path.exists("/tmp/claude-0/oauth.json"): O=json.load(open("/tmp/claude-0/oauth.json"))
else: O={"tok":{"refresh_token":os.environ["ETSY_REFRESH_TOKEN"]},"shop":os.environ.get("ETSY_SHOP_ID")}
def refresh():
    b=urllib.parse.urlencode({"grant_type":"refresh_token","client_id":K.split(":")[0],"refresh_token":O["tok"]["refresh_token"]}).encode()
    O["tok"]=json.load(urllib.request.urlopen(urllib.request.Request("https://api.etsy.com/v3/public/oauth/token",data=b,method="POST"))); json.dump(O,open(TOK,"w"))
refresh(); H={"x-api-key":K,"Authorization":"Bearer "+O["tok"]["access_token"]}
def call(path,data=None,files=None,method=None):
    h=dict(H); body=None
    if files:
        b=uuid.uuid4().hex; parts=[f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k,v in (data or {}).items()]
        for k,(fn,c,ct) in files.items(): parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: {ct}\r\n\r\n'.encode()+c+b"\r\n")
        body=b"".join(parts)+f"--{b}--\r\n".encode(); h["Content-Type"]="multipart/form-data; boundary="+b
    elif data is not None: body=urllib.parse.urlencode(data,doseq=True).encode(); h["Content-Type"]="application/x-www-form-urlencoded"
    try: return json.load(urllib.request.urlopen(urllib.request.Request(A+path,data=body,headers=h,method=method)))
    except urllib.error.HTTPError as e: sys.exit(f"{path}: {e.code} {e.read()[:300]}")
shop=O.get("shop") or os.environ.get("ETSY_SHOP_ID") or call(f"users/{O['tok']['access_token'].split('.')[0]}/shops")["shop_id"]
L=json.load(open(f"{D}/listing.json"))
lid=call(f"shops/{shop}/listings",{"quantity":999,"title":L["title"],"description":L["description"],"price":L["price"],"who_made":"i_did","when_made":"2020_2026",
  "taxonomy_id":L["taxonomy_id"],"type":"download","is_supply":"false","tags":",".join(L["tags"])})["listing_id"]; print("brouillon",lid)
for i,p in enumerate(L["images"],1): call(f"shops/{shop}/listings/{lid}/images",{"rank":i},{"image":(os.path.basename(p),open(f"{D}/{p}","rb").read(),"image/jpeg")})
print(len(L["images"]),"photos")
if L.get("video"): call(f"shops/{shop}/listings/{lid}/videos",{"name":"video.mp4"},{"video":("video.mp4",open(f"{D}/{L['video']}","rb").read(),"video/mp4")}); print("vidéo")
fs=L.get("files") or [L["file"]]
for i,f in enumerate(fs,1): call(f"shops/{shop}/listings/{lid}/files",{"name":os.path.basename(f),"rank":i},{"file":(os.path.basename(f),open(f"{D}/{f}","rb").read(),"application/octet-stream")})
print(len(fs),"fichier(s)")
if not DRAFT: r=call(f"shops/{shop}/listings/{lid}",{"state":"active"},method="PATCH"); print("EN LIGNE",r["url"])
