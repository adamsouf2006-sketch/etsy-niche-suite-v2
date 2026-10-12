# Validation stricte par produit précis : >=3 boutiques distinctes, annonces <=120 j vendues dans les 30 j, hors religion/fêtes
import json,time,urllib.parse,re
exec(open('airbnb.py').read().split('KW=')[0])
REL=r"christmas|xmas|noel|santa|nativity|easter|halloween|spooky|witch|pagan|occult|tarot|zodiac|bible|christian|church|faith|jesus|god|prayer|ramadan|eid|hanukkah|diwali|angel|saint|holy|advent|gnome|thanksgiving|skull|ghost|haunted|reindeer|snowman|ornament|wise ?men|tree skirt|blessed|everything beautiful|valentine|patriotic|4th of july|st patrick"
now=time.time(); OUT={}
KW=["memory bear sewing pattern","patchwork quilt pattern","crossbody bag sewing pattern","zipper pouch sewing pattern","tote bag sewing pattern","felt food sewing pattern","coffee cup sleeve pattern","teddy bear sewing pattern"]
for kw in KW:
    d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"sort_on":"score"})) or {}
    R=[l for l in d.get("results",[]) if (l.get("is_digital") or l.get("listing_type")=="download") and not re.search(REL,l["title"].lower())]
    for l in R: l["age"]=max((now-l["original_creation_timestamp"])/86400,1); l["vj"]=(l.get("views") or 0)/l["age"]
    rec=sorted([l for l in R if l["age"]<=120],key=lambda l:-l["vj"])[:10]; rows=[]; shops=set()
    for l in rec:
        r=G(f"listings/{l['listing_id']}/reviews?limit=100") or {}
        c30=sum(now-x["create_timestamp"]<30*86400 for x in r.get("results",[]))
        if c30: shops.add(l["shop_id"])
        rows.append(dict(id=l["listing_id"],sid=l["shop_id"],age=round(l["age"]),vj=round(l["vj"],1),av=r.get("count",0),av30=c30,
                         p=round(l['price']['amount']/l['price']['divisor'],2),c=l['price']['currency_code'],t=l["title"][:75]))
    OUT[kw]=dict(n=d.get("count"),rec=len([l for l in R if l["age"]<=120]),shops=len(shops),av30=sum(r["av30"] for r in rows),rows=rows)
    ok="VALIDE" if len(shops)>=3 else "-"
    print(f"{kw:34}| res {d.get('count'):>6} | boutiques recentes qui vendent {len(shops)} | avis30j {OUT[kw]['av30']:>3} | {ok}",flush=True)
json.dump(OUT,open("couture.json","w")); print("req",N[0])
