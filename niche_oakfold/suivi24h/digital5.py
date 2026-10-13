# Produits 100 % numériques >= 5 € : >= 3 boutiques avec annonces <= 120 j vendues dans les 30 j
import json,time,urllib.parse,re
from api2 import G,N,save
EUR={'EUR':1,'USD':0.86,'GBP':1.15,'CAD':0.62,'AUD':0.57,'NZD':0.52,'INR':0.0103,'TRY':0.021,'MAD':0.093,'PHP':0.015,'MYR':0.2,'SGD':0.66,'CHF':1.07}
REL=r"christmas|xmas|noel|santa|easter|halloween|spooky|witch|tarot|zodiac|bible|christian|church|faith|jesus|god|prayer|ramadan|islamic|muslim|quran|eid|hanukkah|diwali|lds|angel|saint|holy|advent|thanksgiving|valentine|plr|mrr|resell"
now=time.time(); OUT={}
KW=["printable journal bundle","2027 printable planner","2027 digital planner","goodnotes planner","journal pages printable","digital journal bundle",
"wedding website template","canva wedding invitation","instagram templates canva","social media kit canva","notion template","budget spreadsheet",
"homeschool curriculum printable","reading journal printable","printable workbook"]
for kw in KW:
    d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"sort_on":"score"})) or {}
    R=[]
    for l in d.get("results",[]):
        if not(l.get("is_digital") or l.get("listing_type")=="download") or re.search(REL,l["title"].lower()): continue
        l["eur"]=l["price"]["amount"]/l["price"]["divisor"]*EUR.get(l["price"]["currency_code"],0.86)
        l["age"]=max((now-l["original_creation_timestamp"])/86400,1); l["vj"]=(l.get("views") or 0)/l["age"]
        if l["eur"]>=5 and l["age"]<=120: R.append(l)
    rows=[];shops=set()
    for l in sorted(R,key=lambda l:-l["vj"])[:10]:
        r=G(f"listings/{l['listing_id']}/reviews?limit=100") or {}
        c30=sum(now-x["create_timestamp"]<30*86400 for x in r.get("results",[]))
        if c30: shops.add(l["shop_id"])
        rows.append(dict(age=round(l["age"]),vj=round(l["vj"],1),av=r.get("count",0),av30=c30,eur=round(l["eur"],2),sid=l["shop_id"],t=l["title"][:75]))
    OUT[kw]=dict(n=d.get("count"),shops=len(shops),av30=sum(r["av30"] for r in rows),rows=rows)
    print(f"{kw:32}| boutiques recentes >=5€ qui vendent {len(shops)} | avis30j {OUT[kw]['av30']:>3} | {'VALIDE' if len(shops)>=3 else '-'}",flush=True)
json.dump(OUT,open("digital5.json","w"),indent=1); save(); print("req",N[0])
