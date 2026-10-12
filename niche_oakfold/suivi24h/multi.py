# Niche validée si plusieurs annonces récentes (<=180 j) ont des vues et des avis
import json,urllib.request,urllib.parse,time,os
H={"x-api-key":os.environ.get("ETSY_KEY","20vtorwavjcwhplpol1mdv44:yrh1fpgnqz")}
def G(u):
    for k in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request("https://openapi.etsy.com/v3/application/"+u,headers=H),timeout=30))
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(2*(k+1)); continue
            return None
KW=["airbnb welcome book","airbnb host bundle","house manual template","annual finance planner spreadsheet","paycheck budget spreadsheet",
"sinking funds spreadsheet","debt snowball spreadsheet","couples budget spreadsheet","net worth tracker spreadsheet","savings challenge tracker",
"wedding budget spreadsheet","rental property spreadsheet","landlord forms","lease agreement template","rental application form",
"etsy seller spreadsheet","inventory spreadsheet","profit and loss template","mileage log spreadsheet","small business tax spreadsheet",
"real estate buyer packet","realtor open house sign in","cleaning business bundle","notary forms","massage intake form",
"esthetician forms bundle","daycare forms bundle","photography contract","event planner contract","dog walking contract"]
now=time.time();out={}
for kw in KW:
    d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"sort_on":"score"})) or {}
    R=[]
    for l in d.get("results",[]):
        if not(l.get("is_digital") or l.get("listing_type")=="download"): continue
        age=max((now-l["original_creation_timestamp"])/86400,1)
        if age>180: continue
        vj=(l.get("views") or 0)/age
        if vj<3: continue
        R.append(dict(id=l["listing_id"],age=round(age),vj=round(vj,1),t=l["title"][:70],
                      p=round(l["price"]["amount"]/l["price"]["divisor"],2),c=l["price"]["currency_code"]))
    R.sort(key=lambda r:-r["vj"])
    for r in R[:6]:
        r["av"]=(G(f"listings/{r['id']}/reviews?limit=1") or {}).get("count",0); r["vm"]=round(r["av"]*10/r["age"]*30,1)
    out[kw]=dict(n=d.get("count",0),rec=R)
    ok=[r for r in R[:6] if r.get("av",0)>=1]
    print(f"{kw:36}| {len(R)} recentes >=3 vues/j | {len(ok)} avec avis | ventes/mois: {[r['vm'] for r in ok]}",flush=True)
json.dump(out,open("multi.json","w"))
