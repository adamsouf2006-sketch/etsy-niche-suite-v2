# Validation approfondie niche Airbnb (cache dans airbnb_cache.json pour ne pas refaire les requêtes)
import json,urllib.request,urllib.parse,time,os,collections
H={"x-api-key":os.environ.get("ETSY_KEY","20vtorwavjcwhplpol1mdv44:yrh1fpgnqz")}
CF="airbnb_cache.json"; C=json.load(open(CF)) if os.path.exists(CF) else {}; N=[0]
def G(u):
    if u in C: return C[u]
    for k in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request("https://openapi.etsy.com/v3/application/"+u,headers=H),timeout=30)); break
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(2*(k+1)); continue
            r=None; break
    N[0]+=1; C[u]=r; json.dump(C,open(CF,"w")); return r
KW=["airbnb welcome book","vacation rental welcome book","airbnb guidebook","airbnb house rules sign","airbnb wifi sign","airbnb host bundle","airbnb checkout sign"]
now=time.time(); L={}
for kw in KW:
    for off in ((0,100,200) if kw=="airbnb welcome book" else (0,)):
        d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"offset":off,"sort_on":"score"})) or {}
        if off==0: print(f"{kw:32} resultats {d.get('count')}")
        for l in d.get("results",[]):
            if l.get("is_digital") or l.get("listing_type")=="download": L.setdefault(l["listing_id"],dict(l,kw=kw))
for l in L.values(): l["age"]=max((now-l["original_creation_timestamp"])/86400,1); l["vj"]=(l.get("views") or 0)/l["age"]
rec=sorted([l for l in L.values() if l["age"]<=180],key=lambda l:-l["vj"])
print("annonces numeriques",len(L),"| <=180j",len(rec),"| <=180j et >=5 vues/j",sum(l["vj"]>=5 for l in rec))
# avis des 30 meilleures recentes + dates des avis
rows=[]
for l in rec[:30]:
    r=G(f"listings/{l['listing_id']}/reviews?limit=100") or {}
    ts=[x["create_timestamp"] for x in r.get("results",[])]
    rows.append((l,r.get("count",0),sum(now-t<30*86400 for t in ts)))
shops=collections.Counter(); 
print("\nage | vues/j | avis total | avis 30j | prix | boutique | titre")
for l,c,c30 in rows:
    if c: shops[l["shop_id"]]+=1
    print(f"{round(l['age'])}j | {l['vj']:.1f} | {c} | {c30} | {l['price']['amount']/l['price']['divisor']:.2f} {l['price']['currency_code']} | {l['shop_id']} | {l['title'][:60]}")
print("\nboutiques differentes avec ventes recentes:",len(shops))
for sid in list(shops)[:12]:
    s=G(f"shops/{sid}") or {}
    print(" ",s.get("shop_name"),"ventes",s.get("transaction_sold_count"),"age",round((now-s.get("create_date",now))/86400),"j fiches",s.get("listing_active_count"))
print("requetes reseau:",N[0])
