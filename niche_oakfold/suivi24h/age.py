# Ancienneté vs vues/avis des annonces suivies (ids.json)
import json,urllib.request,time,os
H={"x-api-key":os.environ.get("ETSY_KEY","20vtorwavjcwhplpol1mdv44:yrh1fpgnqz")}
def G(u):
    for k in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request("https://openapi.etsy.com/v3/application/"+u,headers=H),timeout=30))
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(2*(k+1)); continue
            return None
ids=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"ids.json"))); now=time.time(); R=[]
for kw,lst in ids.items():
    for i in lst:
        l=G(f"listings/{i}")
        if not l: continue
        age=max((now-l["original_creation_timestamp"])/86400,1); rv=(G(f"listings/{i}/reviews?limit=1") or {}).get("count",0)
        R.append(dict(kw=kw,id=i,age=round(age),v=l.get("views") or 0,vj=round((l.get("views") or 0)/age,1),av=rv,
                      vm=round(rv*10/age*30,1),p=round(l["price"]["amount"]/l["price"]["divisor"],2),c=l["price"]["currency_code"],t=l["title"][:60]))
json.dump(R,open("age.json","w"))
