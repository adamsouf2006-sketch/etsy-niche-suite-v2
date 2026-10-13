# Nouvelles boutiques <= 60 j qui vendent >= 50 ventes/mois (hors religion, fêtes, licences), budget ~600 requêtes
import json,time,urllib.parse,re,collections
exec(open('airbnb.py').read().split('KW=')[0])
now=time.time()
KNOWN={re.sub(r'\[(.*?)\].*',r'\1',l.split('|')[2].strip()) for l in open('../../BOUTIQUES_NUMERIQUES_2MOIS.md') if re.match(r'\| \d',l)}
KW=["contract template","invoice template","client intake form","business forms bundle","service agreement template","estimate template",
"bookkeeping spreadsheet","budget spreadsheet","google sheets template","excel template","small business planner","business plan template",
"cleaning business forms","esthetician forms","daycare forms","photography contract","real estate template","realtor forms","lash tech forms",
"salon forms","consent form template","order form template","price list template","receipt template","inventory spreadsheet",
"etsy seller spreadsheet","financial planner spreadsheet","debt payoff tracker","wedding planner spreadsheet","adhd planner"]
REL=r"christmas|xmas|noel|santa|nativity|easter|halloween|spooky|witch|pagan|occult|tarot|zodiac|bible|christian|church|faith|jesus|god|prayer|ramadan|eid|hanukkah|diwali|lds|angel|saint|holy|advent|gnome|thanksgiving|skull|ghost|haunted|reindeer|snowman|ornament|valentine|krampus|grinch"
LIC=r"disney|marvel|pokemon|frozen|mario|spider|bluey|paw patrol|barbie|kpop|demon hunter|fortnite|minecraft|roblox|sonic|taylor swift|nfl|nba|ncaa|university|college|moana|stitch|hello kitty|harry potter|snoopy|sanrio|kuromi|labubu|deadpool|tintin|starbucks|stanley|nike|cola|sprite|fanta|team"
cand=collections.defaultdict(lambda:{"vj":0,"t":""})
for kw in KW:
    for off in (0,100):
        d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"offset":off,"sort_on":"score"})) or {}
        for l in d.get("results",[]):
            if not(l.get("is_digital") or l.get("listing_type")=="download"): continue
            age=max((now-l["original_creation_timestamp"])/86400,1)
            if age>60 or re.search(REL+"|"+LIC,l["title"].lower()): continue
            c=cand[l["shop_id"]]; vj=(l.get("views") or 0)/age
            if vj>c["vj"]: c.update(vj=vj,t=l["title"][:80],kw=kw)
print("boutiques candidates",len(cand),"req",N[0],flush=True)
res=[]
for sid,c in sorted(cand.items(),key=lambda kv:-kv[1]["vj"])[:450]:
    s=G(f"shops/{sid}") or {}
    if not s: continue
    age=max((now-s.get("create_date",now))/86400,1); sold=s.get("transaction_sold_count") or 0
    if age<=60 and sold/age*30>=50 and s.get("shop_name") not in KNOWN:
        res.append(dict(shop=s["shop_name"],spm=round(sold/age*30),sold=sold,age=round(age),n=s.get("listing_active_count"),kw=c["kw"],t=c["t"]))
res.sort(key=lambda r:-r["spm"])
json.dump(res,open("young_niche.json","w"),indent=1)
print("NOUVELLES boutiques <=60 j, >=50 ventes/mois :",len(res),"req",N[0])
for r in res: print("%5d/mois %5d ventes %3dj %4s fiches %-24s [%s] %s"%(r["spm"],r["sold"],r["age"],r["n"],r["shop"],r["kw"],r["t"]))
