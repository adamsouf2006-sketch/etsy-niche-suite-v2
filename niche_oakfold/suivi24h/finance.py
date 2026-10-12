# Test strict niche finances : >=3 boutiques distinctes avec annonce <=120 j et avis dans les 30 derniers jours
import json,time,urllib.parse
exec(open('airbnb.py').read().split('KW=')[0])
now=time.time(); OUT={}
KW=["annual finance planner spreadsheet","paycheck budget spreadsheet","biweekly budget spreadsheet","monthly budget spreadsheet",
"budget planner google sheets","zero based budget spreadsheet","debt payoff tracker spreadsheet","savings tracker spreadsheet",
"expense tracker spreadsheet","bookkeeping spreadsheet","finance tracker spreadsheet","couples budget spreadsheet"]
for kw in KW:
    R={}
    for off in (0,100):
        d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"offset":off,"sort_on":"score"})) or {}
        if off==0: n=d.get("count")
        for l in d.get("results",[]):
            if l.get("is_digital") or l.get("listing_type")=="download": R[l["listing_id"]]=l
    R=list(R.values())
    for l in R: l["age"]=max((now-l["original_creation_timestamp"])/86400,1); l["vj"]=(l.get("views") or 0)/l["age"]
    rec=sorted([l for l in R if l["age"]<=120],key=lambda l:-l["vj"])[:10]
    rows=[];shops=set()
    for l in rec:
        r=G(f"listings/{l['listing_id']}/reviews?limit=100") or {}
        c30=sum(now-x["create_timestamp"]<30*86400 for x in r.get("results",[]))
        if c30>=1: shops.add(l["shop_id"])
        rows.append(dict(age=round(l["age"]),vj=round(l["vj"],1),av=r.get("count",0),av30=c30,p=round(l['price']['amount']/l['price']['divisor'],2),c=l['price']['currency_code'],sid=l["shop_id"],t=l["title"][:80]))
    OUT[kw]=dict(n=n,num=len(R),rec=sum(l["age"]<=120 for l in R),shops=len(shops),av30=sum(r["av30"] for r in rows),rows=rows)
    print(f"{kw:36}| res {n} | recentes {OUT[kw]['rec']}/{len(R)} | boutiques recentes qui vendent {len(shops)} | avis30j {OUT[kw]['av30']}",flush=True)
json.dump(OUT,open("finance.json","w")); print("req",N[0])
