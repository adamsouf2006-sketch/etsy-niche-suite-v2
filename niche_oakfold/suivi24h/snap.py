# Photo vues/favoris/ventes boutique des top annonces ; relancer 24h plus tard puis diff.py
import json,urllib.request,urllib.parse,time,os,sys
H={"x-api-key":os.environ.get("ETSY_KEY","20vtorwavjcwhplpol1mdv44:yrh1fpgnqz")}
def G(u):
    for k in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request("https://openapi.etsy.com/v3/application/"+u,headers=H),timeout=30))
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(2*(k+1)); continue
            return None
D=os.path.dirname(os.path.abspath(__file__)); IDS=os.path.join(D,"ids.json")
KW=["dj contract template","body sculpting consent form","tutoring contract","microblading consent form","brow lamination consent form",
"massage intake form","landscaping invoice","lash tech consent form","event planner contract","dog walking contract","airbnb welcome book","notary forms"]
now=time.time()
if os.path.exists(IDS): ids=json.load(open(IDS))
else:
    ids={}
    for kw in KW:
        d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":50,"sort_on":"score"})) or {}
        L=[l for l in d.get("results",[]) if l.get("is_digital") or l.get("listing_type")=="download"]
        L.sort(key=lambda l:-(l.get("views") or 0)/max((now-l["original_creation_timestamp"])/86400/30.4,1))
        ids[kw]=[l["listing_id"] for l in L[:8]]
    json.dump(ids,open(IDS,"w"))
snap={"t":now,"l":{},"s":{}}
for kw,lst in ids.items():
    for i in lst:
        l=G(f"listings/{i}")
        if not l: continue
        snap["l"][str(i)]={"kw":kw,"v":l.get("views"),"f":l.get("num_favorers"),"sid":l["shop_id"],"t":l["title"][:70],
                           "p":round(l["price"]["amount"]/l["price"]["divisor"],2),"c":l["price"]["currency_code"]}
for sid in {x["sid"] for x in snap["l"].values()}:
    s=G(f"shops/{sid}"); snap["s"][str(sid)]=s and [s["shop_name"],s.get("transaction_sold_count"),s.get("listing_active_count")]
f=os.path.join(D,time.strftime("snap_%Y%m%d_%H%M.json")); json.dump(snap,open(f,"w")); print(f,len(snap["l"]),len(snap["s"]))
