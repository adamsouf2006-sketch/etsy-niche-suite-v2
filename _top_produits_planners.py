# -*- coding: utf-8 -*-
"""Produits planners/templates/tableurs qui vendent le plus (toutes boutiques). Avis listing = proxy ventes (~x10). Cache."""
import sys, json, os, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import etsy_core
if os.environ.get('ETSY_KEY'): etsy_core.API_KEY = os.environ['ETSY_KEY']
TO_EUR = {'EUR':1,'USD':0.86,'GBP':1.15,'CAD':0.62,'AUD':0.57,'INR':0.0103,'TRY':0.021,'PKR':0.0031}
KWS = ['digital planner','goodnotes planner','budget spreadsheet','budget planner','google sheets template','excel template','notion template',
 'canva template','life planner spreadsheet','finance tracker spreadsheet','debt payoff tracker','savings tracker','expense tracker',
 'wedding planner spreadsheet','wedding budget spreadsheet','adhd planner','cleaning planner','meal planner','habit tracker','fitness planner',
 'teacher planner','student planner','small business spreadsheet','inventory spreadsheet','etsy seller spreadsheet','social media template',
 'instagram template canva','content calendar','resume template','business plan template','travel planner','baby planner','pregnancy planner',
 'home binder printable','printable planner','2027 planner','paycheck budget','couples budget','bill tracker','sinking funds tracker']
EXCL = ['christmas','halloween','thanksgiving','bible','christian','faith','lds','disney','marvel','pokemon','plr','mrr','resell']
CACHE = '_top_prod_planners_cache.json'
C = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {'kw': {}, 'rev': {}, 'shop': {}}
sv = lambda: json.dump(C, open(CACHE, 'w', encoding='utf-8'))
for kw in KWS:
    for off in (0, 100):
        k = f'{kw}|{off}'
        if k in C['kw']: continue
        r = etsy_core._get(f'/listings/active?limit=100&offset={off}&keywords={kw.replace(" ","+")}&sort_on=score')['results']
        C['kw'][k] = [{'id': l['listing_id'], 'sid': l['shop_id'], 't': l['title'], 'v': l.get('views') or 0, 'f': l.get('num_favorers') or 0,
                       'c': l['original_creation_timestamp'], 'd': bool(l.get('is_digital') or l.get('listing_type') == 'download'),
                       'p': round(l['price']['amount'] / l['price']['divisor'] * TO_EUR.get(l['price']['currency_code'], 0.86), 2)} for l in r]
        sv()
    print('ok', kw, flush=True)
now = time.time(); L = {}
for k, rows in C['kw'].items():
    for l in rows:
        if l['d'] and not any(e in l['t'].lower() for e in EXCL): L.setdefault(l['id'], l | {'kw': k.split('|')[0]})
L = list(L.values())
for l in L: l['vm'] = l['v'] / max((now - l['c']) / 86400 / 30.4, 1)
L.sort(key=lambda l: -l['vm'])
top = L[:350]
for l in top:
    i = str(l['id'])
    if i not in C['rev']:
        C['rev'][i] = etsy_core._get(f'/listings/{i}/reviews?limit=1').get('count', 0); sv()
    l['avis'] = C['rev'][i]
top.sort(key=lambda l: -l['avis'])
for l in top[:100]:
    s = str(l['sid'])
    if s not in C['shop']:
        d = etsy_core._get(f'/shops/{s}'); C['shop'][s] = [d.get('shop_name'), d.get('transaction_sold_count')]; sv()
json.dump([l | {'shop': C['shop'][str(l['sid'])]} for l in top[:100]], open('_top_produits_planners.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('listings numeriques uniques', len(L))
for n, l in enumerate(top[:100], 1):
    s = C['shop'][str(l['sid'])]
    print(f"{n}|{l['avis']}|{l['p']}|{round(l['vm'])}|{s[0]}|{s[1]}|{l['t'][:95]}|{l['id']}")
