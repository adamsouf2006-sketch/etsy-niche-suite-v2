# Memory bear : toutes les annonces récentes, ventes par annonce, tendance hebdomadaire, boutiques
import json,time,urllib.parse,collections
exec(open('airbnb.py').read().split('KW=')[0])
now=time.time(); L={}
for kw,offs in [("memory bear sewing pattern",(0,100,200)),("keepsake bear pattern",(0,)),("memorial bear sewing pattern",(0,)),("patchwork bear sewing pattern",(0,))]:
    for off in offs:
        d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"offset":off,"sort_on":"score"})) or {}
        for l in d.get("results",[]):
            if (l.get("is_digital") or l.get("listing_type")=="download") and "bear" in l["title"].lower(): L[l["listing_id"]]=l
for l in L.values(): l["age"]=max((now-l["original_creation_timestamp"])/86400,1); l["vj"]=(l.get("views") or 0)/l["age"]
rec=[l for l in L.values() if l["age"]<=120]
print("annonces numeriques 'bear' trouvees",len(L),"| <=120 j",len(rec),"req",N[0],flush=True)
rows=[]; week=collections.Counter(); shops=collections.defaultdict(lambda:[0,0])
for l in sorted(rec,key=lambda l:-l["vj"])[:60]:
    r=G(f"listings/{l['listing_id']}/reviews?limit=100") or {}
    ts=[x["create_timestamp"] for x in r.get("results",[])]
    c30=sum(now-t<30*86400 for t in ts)
    for t in ts:
        w=int((now-t)//(7*86400))
        if w<8: week[w]+=1
    rows.append((round(l["age"]),round(l["vj"],1),r.get("count",0),c30,round(l['price']['amount']/l['price']['divisor'],2),l['price']['currency_code'],l["shop_id"],l["title"][:60]))
    shops[l["shop_id"]][0]+=1; shops[l["shop_id"]][1]+=c30
sell=[r for r in rows if r[3]>0]
print("annonces recentes analysees",len(rows),"| qui vendent (avis 30 j)",len(sell),"| boutiques distinctes qui vendent",len({r[6] for r in sell}))
print("avis par semaine (0 = cette semaine):",[week[w] for w in range(8)])
for r in sorted(rows,key=lambda r:-r[3])[:25]: print("  %3dj %6.1fv/j %3d av (%2d en 30j) %6.2f %s sid=%d | %s"%r)
sh=[s for s,v in shops.items() if v[1]>0]
for s in sh[:12]:
    d=G(f"shops/{s}") or {}
    print("  boutique",d.get("shop_name"),"age",round((now-d.get("create_date",now))/86400),"j ventes",d.get("transaction_sold_count"),"fiches",d.get("listing_active_count"))
json.dump(rows,open("bear.json","w")); print("req",N[0])
