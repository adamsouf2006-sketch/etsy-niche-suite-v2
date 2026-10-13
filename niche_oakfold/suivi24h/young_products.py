# Produits des jeunes boutiques à fort volume : ventes estimées par annonce, prix >= 5 €, hors religion/fêtes/licences
import json,time,urllib.parse,re,collections,os
from api2 import G,N,save
now=time.time()
EUR={'EUR':1,'USD':0.86,'GBP':1.15,'CAD':0.62,'AUD':0.57,'NZD':0.52,'INR':0.0103,'TRY':0.021,'PKR':0.0031,'MAD':0.093,'PHP':0.015,'IDR':0.000053,'MYR':0.2,'BRL':0.16,'MXN':0.047,'SGD':0.66,'CHF':1.07,'SEK':0.088,'NOK':0.085,'DKK':0.134,'PLN':0.23,'ILS':0.24,'ZAR':0.05,'HKD':0.11,'JPY':0.0058,'VND':0.000034}
REL=r"christmas|xmas|noel|santa|nativity|easter|halloween|spooky|witch|pagan|occult|tarot|zodiac|bible|christian|church|faith|jesus|god|prayer|ramadan|eid|hanukkah|diwali|lds|angel|saint|holy|advent|gnome|thanksgiving|skull|ghost|haunted|reindeer|snowman|ornament|valentine|krampus|grinch|jack o lantern|trick or treat"
LIC=r"disney|marvel|pokemon|frozen|mario|spider|bluey|paw patrol|barbie|kpop|demon hunter|fortnite|fort game|minecraft|roblox|sonic|taylor swift|nfl|nba|ncaa|university|college|moana|stitch|hello kitty|harry potter|snoopy|sanrio|kuromi|labubu|deadpool|tintin|starbucks|stanley|nike|cola|sprite|fanta|yoshi|squishy|needoh|costco|walgreens|monopoly|hot wheels|plr|mrr|resell rights"
# boutiques : fichier du 10/10 + scans d'hier
names=[re.sub(r'\[(.*?)\].*',r'\1',l.split('|')[2].strip()) for l in open('../../BOUTIQUES_NUMERIQUES_2MOIS.md') if re.match(r'\| \d',l) and not re.search(REL+"|"+LIC,l.lower())]
for f in ("young.json","young_niche.json"):
    if os.path.exists(f): names+=[x["shop"] for x in json.load(open(f))]
names=list(dict.fromkeys(names)); print("boutiques",len(names),flush=True)
P=[]
for n in names:
    s=((G("shops?"+urllib.parse.urlencode({"shop_name":n})) or {}).get("results") or [None])[0]
    if not s: continue
    sage=max((now-s["create_date"])/86400,1)
    d=G(f"shops/{s['shop_id']}/listings/active?limit=100") or {}
    for l in d.get("results",[]):
        t=l["title"]
        if re.search(REL+"|"+LIC,t.lower()): continue
        eur=l["price"]["amount"]/l["price"]["divisor"]*EUR.get(l["price"]["currency_code"],0.86)
        age=max((now-l["original_creation_timestamp"])/86400,1)
        P.append(dict(id=l["listing_id"],shop=n,sage=round(sage),ssold=s.get("transaction_sold_count"),eur=round(eur,2),age=round(age),
                      vj=round((l.get("views") or 0)/age,1),fav=l.get("num_favorers") or 0,t=t[:90]))
print("annonces",len(P),"req",N[0],flush=True)
top=sorted([p for p in P if p["eur"]>=5],key=lambda p:-p["vj"])[:300]
for p in top:
    r=G(f"listings/{p['id']}/reviews?limit=100") or {}
    p["av"]=r.get("count",0); p["av30"]=sum(now-x["create_timestamp"]<30*86400 for x in r.get("results",[]))
json.dump(top,open("young_products.json","w"),indent=1)
print("annonces >=5 EUR analysees",len(top),"req",N[0])
for p in sorted(top,key=lambda p:-p["av30"])[:80]:
    print("%3d av30 %4d av %6.2f€ %3dj %6.1fv/j %-22s | %s"%(p["av30"],p["av"],p["eur"],p["age"],p["vj"],p["shop"],p["t"]))
save()
