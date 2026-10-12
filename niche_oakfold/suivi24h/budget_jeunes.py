# Produits gagnants des jeunes boutiques de tableurs budget (BOUTIQUES_NUMERIQUES_2MOIS.md)
import json,time,urllib.parse
exec(open('airbnb.py').read().split('KW=')[0])
now=time.time()
for name in ["BudgetwithRozCanada","XclusivetemplatesArt","Smarbudget"]:
    s=((G("shops?"+urllib.parse.urlencode({"shop_name":name})) or {}).get("results") or [{}])[0]
    sid=s.get("shop_id"); print(f"\n== {name} ventes {s.get('transaction_sold_count')} age {round((now-s.get('create_date',now))/86400)}j")
    d=G(f"shops/{sid}/listings/active?limit=100") or {}
    L=d.get("results",[])
    for l in L: l["age"]=max((now-l["original_creation_timestamp"])/86400,1)
    for l in sorted(L,key=lambda l:-(l.get("views") or 0))[:5]:
        r=G(f"listings/{l['listing_id']}/reviews?limit=100") or {}
        c30=sum(now-x["create_timestamp"]<30*86400 for x in r.get("results",[]))
        print(f"  {round(l['age'])}j {(l.get('views') or 0)/l['age']:.1f}v/j {r.get('count',0)}av {c30}av30j {l['price']['amount']/l['price']['divisor']:.2f}{l['price']['currency_code']} | {l['title'][:90]}")
print("req",N[0])
