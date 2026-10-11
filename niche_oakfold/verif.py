import json,urllib.request,urllib.parse,time,re,concurrent.futures as cf
H={"x-api-key":"20vtorwavjcwhplpol1mdv44:yrh1fpgnqz"}
def G(u):
    for k in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request("https://openapi.etsy.com/v3/application/"+u,headers=H),timeout=30))
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(2+k*2); continue
            return None
P={"bookkeeping":(["bookkeeping spreadsheet","small business bookkeeping","profit and loss spreadsheet","income expense tracker business","bookkeeping template"],r"bookkeep|profit.{0,5}loss|income.{0,10}expense|accounting"),
 "cleaning":(["cleaning business bundle","cleaning business forms","cleaning service contract","cleaning proposal template","cleaning business starter kit"],r"clean|janitor|housekeep|maid"),
 "esthetician":(["esthetician forms","lash consent form","facial consultation form","salon client intake form","spa forms bundle"],r"esthetic|lash|brow|facial|salon|spa |consent|wax|skin"),
 "daycare":(["daycare forms","home daycare contract","childcare forms bundle","daycare starter kit","nanny contract"],r"daycare|childcare|child care|nanny|preschool|babysit")}
now=time.time(); res={}
for k,(kws,rx) in P.items():
    shops={}
    for kw in kws:
        for off in (0,100):
            d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"offset":off,"sort_on":"score"}))
            for l in (d or {}).get("results",[]): shops.setdefault(l["shop_id"],[]).append(l)
    def info(sid):
        s=G(f"shops/{sid}")
        if not s: return None
        age=(now-s["create_date"])/86400
        if age>365 or s["transaction_sold_count"]<30: return None
        ls=(G(f"shops/{sid}/listings/active?limit=100") or {}).get("results",[])
        share=sum(bool(re.search(rx,l["title"].lower())) for l in ls)/max(len(ls),1)
        best=max(shops[sid],key=lambda l:l["num_favorers"])
        return dict(shop=s["shop_name"],sales=s["transaction_sold_count"],age=round(age),vm=round(s["transaction_sold_count"]/max(age,1)*30),listings=s["listing_active_count"],share=round(share,2),
            price=best["price"]["amount"]/best["price"]["divisor"],cur=best["price"]["currency_code"],fav=best["num_favorers"],title=best["title"][:85])
    with cf.ThreadPoolExecutor(8) as ex: r=[x for x in ex.map(info,list(shops)) if x]
    res[k]=sorted(r,key=lambda x:-x["vm"]); json.dump(res,open("verif.json","w")); print(k,len(shops),"boutiques,",len(r),"récentes ≥30 ventes",flush=True)

