import json,urllib.request,urllib.parse,time,collections,concurrent.futures as cf
H={"x-api-key":"20vtorwavjcwhplpol1mdv44:yrh1fpgnqz"}
def G(u):
    for k in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request("https://openapi.etsy.com/v3/application/"+u,headers=H),timeout=30))
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(2*(k+1)); continue
            if e.code==404: return None
            raise
KW=["cleaning business contract","cleaning service forms","contractor estimate template","handyman invoice template","service agreement template",
"client intake form","invoice template","quote template","small business contract","daycare forms","childcare contract","photography contract",
"lawn care business forms","cleaning checklist business","business forms bundle","contractor forms","home daycare forms","pet sitting forms",
"house cleaning contract","consulting agreement template","independent contractor agreement","event planner contract","bookkeeping spreadsheet",
"small business planner","estimate and invoice template","work order form","client onboarding template","hair salon forms","esthetician forms","dog grooming forms"]
lst={}
for kw in KW:
    for off in (0,100):
        d=G("listings/active?"+urllib.parse.urlencode({"keywords":kw,"limit":100,"offset":off,"sort_on":"score"}))
        for l in (d or {}).get("results",[]):
            if l.get("is_digital") or l.get("listing_type")=="download":
                l["kw"]=kw; lst.setdefault(l["listing_id"],l)
print("listings",len(lst))
shops=collections.defaultdict(list)
for l in lst.values(): shops[l["shop_id"]].append(l)
def shop(i): return G(f"shops/{i}")
with cf.ThreadPoolExecutor(6) as ex: info=dict(zip(shops,ex.map(shop,list(shops))))
now=time.time(); out=[]
for sid,s in info.items():
    if not s: continue
    age=(now-s["create_date"])/86400; ls=shops[sid]
    out.append({"shop":s["shop_name"],"sales":s["transaction_sold_count"],"age_days":round(age),"listings":s["listing_active_count"],
      "reviews":s.get("review_count"),"rating":s.get("review_average"),"title":s.get("title"),"n_in_niche":len(ls),
      "top":sorted(ls,key=lambda x:-x["num_favorers"])[0]["title"][:90],"kws":sorted({x["kw"] for x in ls})[:4],
      "price_med":sorted(x["price"]["amount"]/x["price"]["divisor"] for x in ls)[len(ls)//2],"cur":ls[0]["price"]["currency_code"]})
json.dump(out,open("shops.json","w")); print("shops",len(out))
