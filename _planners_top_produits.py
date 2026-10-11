# -*- coding: utf-8 -*-
"""20 boutiques planners/templates jeunes: leurs listings les plus vus/favorisés. 1 req/boutique + avis top listings."""
import sys, json, os, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import etsy_core
if os.environ.get('ETSY_KEY'): etsy_core.API_KEY = os.environ['ETSY_KEY']
TO_EUR = {'EUR':1,'USD':0.86,'GBP':1.15,'CAD':0.62,'AUD':0.57,'INR':0.0103,'TRY':0.021,'PKR':0.0031}
WS = ['planner','template','spreadsheet','sheets','notion','canva','website','tracker']
C = json.load(open('_num_jeunes_cache.json', encoding='utf-8'))['shop']
now = time.time(); shops = []
for sid, s in C.items():
    age = (now - (s['create_date'] or 0)) / 86400; vm = (s['transaction_sold_count'] or 0) / max(age, 1) * 30
    if age <= 61 and vm >= 50 and any(w in (s['ex'] or '').lower() for w in WS): shops.append((sid, s, vm))
print('boutiques', len(shops))
OUT = '_planners_top_produits.json'
D = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
for sid, s, vm in shops:
    if sid in D: continue
    r = etsy_core._get(f'/shops/{sid}/listings/active?limit=100&sort_on=score')['results']
    D[sid] = [{'id': l['listing_id'], 't': l['title'], 'v': l.get('views') or 0, 'f': l.get('num_favorers') or 0, 'c': l['original_creation_timestamp'],
               'p': round(l['price']['amount'] / l['price']['divisor'] * TO_EUR.get(l['price']['currency_code'], 0.86), 2)} for l in r]
    json.dump(D, open(OUT, 'w', encoding='utf-8'))
rows = []
for sid, s, vm in shops:
    for l in D.get(sid, []):
        m = max((now - l['c']) / 86400 / 30.4, 0.3)
        rows.append((l['f'] / m + l['v'] / m / 20, s['shop_name'], round(vm), l))
rows.sort(key=lambda x: -x[0])
for sc, shop, vm, l in rows[:40]:
    k = f"rev{l['id']}"
    if k not in D: D[k] = etsy_core._get(f"/listings/{l['id']}/reviews?limit=1").get('count', 0); json.dump(D, open(OUT, 'w', encoding='utf-8'))
    print(f"{shop} ({vm}/m) | {l['t'][:85]} | {l['p']}€ | vues {l['v']} | fav {l['f']} | avis {D[k]} | https://www.etsy.com/listing/{l['id']}")
