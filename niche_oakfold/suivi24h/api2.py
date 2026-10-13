# Accès API Etsy en lecture avec cache léger dédié (évite les écritures concurrentes sur airbnb_cache.json)
import json,os,time,urllib.request
H={"x-api-key":os.environ.get("ETSY_KEY","20vtorwavjcwhplpol1mdv44:yrh1fpgnqz")}
CF=os.environ.get("CACHE","api2_cache.json"); C=json.load(open(CF)) if os.path.exists(CF) else {}; N=[0]
def save(): json.dump(C,open(CF+".tmp","w")); os.replace(CF+".tmp",CF)
def G(u):
    if u in C: return C[u]
    r=None
    for k in range(5):
        try: r=json.load(urllib.request.urlopen(urllib.request.Request("https://openapi.etsy.com/v3/application/"+u,headers=H),timeout=30)); break
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(2*(k+1)); continue
            break
        except Exception: time.sleep(2)
    N[0]+=1; C[u]=r
    if N[0]%50==0: save()
    return r
