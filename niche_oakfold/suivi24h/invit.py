# Thèmes précis d'invitations enfant (sans licence) : plusieurs annonces récentes qui vendent ?
import json,time,urllib.parse
exec(open('airbnb.py').read().split('KW=')[0])
now=time.time(); OUT={}
KW=["squishy birthday invitation","charm bracelet birthday invitation","backyard movie night invitation","emergency vehicle birthday invitation",
"fort birthday invitation","dino rescue birthday invitation","berry first birthday invitation","kawaii birthday invitation",
"two cool birthday invitation","bluey style","sleepover birthday invitation","pickleball birthday invitation"]
KW=[k for k in KW if k!="bluey style"]
for kw in KW:
    d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"sort_on":"score"})) or {}
    R=[l for l in d.get("results",[]) if l.get("is_digital") or l.get("listing_type")=="download"]
    for l in R: l["age"]=max((now-l["original_creation_timestamp"])/86400,1); l["vj"]=(l.get("views") or 0)/l["age"]
    rec=sorted([l for l in R if l["age"]<=180],key=lambda l:-l["vj"])[:6]
    rows=[];shops=set()
    for l in rec:
        r=G(f"listings/{l['listing_id']}/reviews?limit=100") or {}
        c30=sum(now-x["create_timestamp"]<30*86400 for x in r.get("results",[]))
        if r.get("count",0): shops.add(l["shop_id"])
        rows.append((round(l["age"]),round(l["vj"],1),r.get("count",0),c30,round(l['price']['amount']/l['price']['divisor'],2),l['price']['currency_code'],l["title"][:60]))
    OUT[kw]=dict(n=d.get("count"),num=len(R),rec=sum(l["age"]<=180 for l in R),rows=rows,shops=len(shops))
    print(f"{kw:38}| res {d.get('count')} | recentes {OUT[kw]['rec']}/{len(R)} | boutiques recentes qui vendent {len(shops)} | avis30j {sum(r[3] for r in rows)} | {[(r[0],r[2]) for r in rows]}",flush=True)
json.dump(OUT,open("invit.json","w")); print("req",N[0])
