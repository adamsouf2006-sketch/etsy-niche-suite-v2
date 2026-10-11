# Crée la fiche en BROUILLON sur Etsy (photos + fichier). Usage: ETSY_TOKEN=... python3 publish.py
import json,os,urllib.request,urllib.parse,uuid
K=os.environ["ETSY_KEY"]  # "keystring:secret"
T=os.environ["ETSY_TOKEN"]; A="https://openapi.etsy.com/v3/application/"
H={"x-api-key":K,"Authorization":"Bearer "+T}
def call(path,data=None,files=None,method=None):
    h=dict(H); body=None
    if files:
        b=uuid.uuid4().hex; parts=[]
        for k,v in (data or {}).items(): parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
        for k,(fn,content,ct) in files.items(): parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{fn}"\r\nContent-Type: {ct}\r\n\r\n'.encode()+content+b"\r\n")
        body=b"".join(parts)+f"--{b}--\r\n".encode(); h["Content-Type"]="multipart/form-data; boundary="+b
    elif data is not None:
        body=urllib.parse.urlencode(data,doseq=True).encode(); h["Content-Type"]="application/x-www-form-urlencoded"
    return json.load(urllib.request.urlopen(urllib.request.Request(A+path,data=body,headers=h,method=method)))
uid=T.split(".")[0]; shop=call(f"users/{uid}/shops")["shop_id"]
L=json.load(open("listing.json"))
tax=int(os.environ.get("ETSY_TAXONOMY","12487"))  # Personal Finance Templates
d=call(f"shops/{shop}/listings",{"quantity":999,"title":L["title"],"description":L["description"],"price":L["price"],
  "who_made":"i_did","when_made":"made_to_order","taxonomy_id":tax,"type":"download","is_supply":"false","tags":",".join(L["tags"]),"state":"draft"})
lid=d["listing_id"]; print("brouillon créé",lid)
for i,p in enumerate(["img/main_A.jpg","img/main_C.jpg","img/main_B.jpg"],1):
    call(f"shops/{shop}/listings/{lid}/images",{"rank":i},{"image":(os.path.basename(p),open(p,"rb").read(),"image/jpeg")}); print("photo",i)
call(f"shops/{shop}/listings/{lid}/files",{"name":"Annual_Budget_Planner_2027.xlsx","rank":1},{"file":("Annual_Budget_Planner_2027.xlsx",open("out/Annual_Budget_Planner_2027.xlsx","rb").read(),"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")})
print("fichier ajouté. Fiche: https://www.etsy.com/your/shops/me/listing-editor/edit/"+str(lid))
