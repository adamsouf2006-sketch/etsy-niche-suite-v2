# Balayage large n°2 : nouvelles familles de produits numériques ; annonces <=120 j qui vendent (avis 30 j)
import json,time,urllib.parse,re
exec(open('airbnb.py').read().split('KW=')[0])
now=time.time()
KW=["coloring pages","clipart","printable wall art","crochet pattern","sewing pattern","invitation template","printable bookmarks","printable stickers",
"kids worksheets","planner inserts","lesson plans","christmas printable","advent calendar printable","christmas games printable","gift tags printable",
"recipe card template","menu template","bingo cards printable","party games printable","ebook guide","procreate brushes","lightroom presets",
"embroidery pattern","cross stitch pattern","stl file","laser cut file","digital paper","seamless pattern","quilt pattern","knitting pattern"]
L={}
for kw in KW:
    for off in (0,100):
        d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"offset":off,"sort_on":"score"})) or {}
        for l in d.get("results",[]):
            if l.get("is_digital") or l.get("listing_type")=="download": L[l["listing_id"]]=dict(l,kw=kw)
for l in L.values(): l["age"]=max((now-l["original_creation_timestamp"])/86400,1); l["vj"]=(l.get("views") or 0)/l["age"]
LIC=r"disney|marvel|pokemon|pikachu|frozen|elsa|mario|spider|bluey|paw patrol|barbie|kpop|demon hunter|fortnite|minecraft|roblox|sonic|taylor|swift|nfl|nba|moana|stitch|hello kitty|harry potter|grinch|snoopy|peanuts|sanrio|kuromi|labubu|stanley|starbucks|nike|chanel|lv |gucci|mickey|minnie|toy story|cocomelon|ms rachel|wednesday|stranger things|super bowl|chiefs"
rec=sorted([l for l in L.values() if l["age"]<=120 and not re.search(LIC,l["title"].lower())],key=lambda l:-l["vj"])[:220]
print("numeriques",len(L),"recentes retenues",len(rec),"req",N[0],flush=True)
S=[]
for l in rec:
    r=G(f"listings/{l['listing_id']}/reviews?limit=100") or {}
    c30=sum(now-x["create_timestamp"]<30*86400 for x in r.get("results",[]))
    if c30: S.append(dict(id=l["listing_id"],sid=l["shop_id"],kw=l["kw"],age=round(l["age"]),vj=round(l["vj"],1),av=r.get("count",0),av30=c30,
                          p=round(l['price']['amount']/l['price']['divisor'],2),c=l['price']['currency_code'],t=l["title"]))
json.dump(S,open("large2.json","w"))
print("annonces recentes qui vendent:",len(S),"req",N[0])
for s in sorted(S,key=lambda s:-s["av30"]): print(f"{s['age']}j {s['vj']}v/j {s['av30']}av30 {s['p']}{s['c']} {s['sid']} [{s['kw']}] | {s['t'][:80]}")
