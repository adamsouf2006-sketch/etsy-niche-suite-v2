# Balayage large : annonces numériques <=120 j qui vendent (avis 30 j), regroupées par type de produit
import json,time,urllib.parse,collections,re
exec(open('airbnb.py').read().split('KW=')[0])
now=time.time()
KW=["editable template","printable","spreadsheet","canva template","digital download","notion template","worksheets","pdf guide",
"digital planner","printable planner","google sheets template","excel template","workbook pdf","checklist printable","tracker printable",
"business template","social media template","resume template","wedding template","baby shower template","kids printable","teacher printable",
"homeschool printable","journal printable","ebook","course workbook","forms bundle","contract template","guide printable","binder printable"]
L={}
for kw in KW:
    for off in (0,100):
        d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"offset":off,"sort_on":"score"})) or {}
        for l in d.get("results",[]):
            if l.get("is_digital") or l.get("listing_type")=="download": L[l["listing_id"]]=l
for l in L.values(): l["age"]=max((now-l["original_creation_timestamp"])/86400,1); l["vj"]=(l.get("views") or 0)/l["age"]
LIC=r"disney|marvel|pokemon|pikachu|frozen|elsa|mario|spider|bluey|paw|barbie|kpop|demon hunter|fort|minecraft|roblox|sonic|taylor|swift|nfl|nba|bulldogs|moana|stitch|hello kitty|harry potter|lds|costco|walgreens|bible|church"
rec=sorted([l for l in L.values() if l["age"]<=120 and not re.search(LIC,l["title"].lower())],key=lambda l:-l["vj"])[:170]
print("numeriques",len(L),"recentes retenues",len(rec),"req",N[0],flush=True)
S=[]
for l in rec:
    r=G(f"listings/{l['listing_id']}/reviews?limit=100") or {}
    c30=sum(now-x["create_timestamp"]<30*86400 for x in r.get("results",[]))
    if c30: S.append(dict(id=l["listing_id"],sid=l["shop_id"],age=round(l["age"]),vj=round(l["vj"],1),av=r.get("count",0),av30=c30,
                          p=round(l['price']['amount']/l['price']['divisor'],2),c=l['price']['currency_code'],t=l["title"]))
json.dump(S,open("large.json","w"))
print("annonces recentes qui vendent:",len(S),"req",N[0])
for s in sorted(S,key=lambda s:-s["av30"]): print(f"{s['age']}j {s['vj']}v/j {s['av30']}av30 {s['p']}{s['c']} {s['sid']} | {s['t'][:85]}")
