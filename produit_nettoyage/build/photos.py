import sys,os,base64; sys.path.insert(0,os.path.abspath("../../commun"))
import render
from mockups import badges, FONT
from content import DOCS, ACC
ACC2="#F59E0B"; INK="#1F2937"; MUT="#6B7280"; BG="#EEF5F3"; SOFT="#D5ECE7"
img=lambda n: "data:image/png;base64,"+base64.b64encode(open(f"../img/pages/{n}.png","rb").read()).decode()
def pg(n,w,x,y,rot=0,z=1,sh=.25): return f'<img src="{img(n)}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);box-shadow:0 {w*.03:.0f}px {w*.08:.0f}px rgba(15,60,55,{sh});border-radius:6px;z-index:{z}">'
def page(b): return f"<!doctype html><html><head><meta charset=utf-8>{FONT}<style>*{{box-sizing:border-box;margin:0}}body{{font-family:Inter,sans-serif;color:{INK}}}.ic{{width:100%;height:100%}}html,body{{width:2000px;height:2500px;overflow:hidden;background:{BG}}}</style></head><body>{b}</body></html>"
def T(t,s=""): return f'<div style="padding:110px 100px 0;text-align:center;position:relative;z-index:9"><div style="font-family:\'Inter Display\',Inter;font-size:124px;line-height:1;font-weight:900;color:{ACC}">{t}</div><div style="font-size:56px;color:{MUT};margin-top:24px;font-weight:500">{s}</div></div>'
def pill(t,bg=ACC2,fg=INK,fs=60): return f'<div style="background:{bg};color:{fg};font-weight:900;font-size:{fs}px;padding:20px 46px;border-radius:999px;display:inline-block">{t}</div>'
FMT=f'<div style="display:flex;gap:26px;justify-content:center;flex-wrap:wrap">'+"".join(f'<div style="background:#fff;border:3px solid {ACC};color:{ACC};font-weight:800;font-size:50px;padding:18px 36px;border-radius:20px">{t}</div>' for t in ["Fillable PDF","Word","Google Docs","US Letter + A4"])+'</div>'
foot=lambda: f'<div style="position:absolute;bottom:80px;left:0;right:0;z-index:9">{FMT}</div>'
P={}
fan=lambda y=820: "".join(pg(n,780,x,y+dy,r,z) for n,x,dy,r,z in [("p05",140,170,-11,1),("p03",380,60,-5,2),("p06",840,60,5,2),("p02",1080,170,11,1),("p01",610,0,0,5)])
P["01_main_A"]=f'''<div style="padding:110px 100px 0;text-align:center"><div style="font-size:58px;font-weight:800;color:{ACC2};letter-spacing:.12em">EDITABLE + FILLABLE</div>
<div style="font-family:'Inter Display',Inter;font-size:176px;line-height:.96;font-weight:900;color:{ACC};margin-top:20px">CLEANING<br>BUSINESS KIT</div>
<div style="font-size:62px;margin-top:26px;font-weight:500">Contract · Estimate · Invoice · Checklist</div></div>{fan()}
<div style="position:absolute;right:90px;top:760px;width:330px;height:330px;border-radius:50%;background:{ACC2};display:grid;place-items:center;text-align:center;transform:rotate(10deg);z-index:9;box-shadow:0 20px 50px rgba(0,0,0,.18)"><div><div style="font-size:130px;font-weight:900;line-height:1">7</div><div style="font-size:44px;font-weight:800">DOCUMENTS</div></div></div>{foot()}'''
P["01_main_B"]=f'''<div style="position:absolute;inset:0;background:{ACC}"></div><div style="position:relative;padding:120px 110px 0;z-index:9"><div style="font-family:'Inter Display',Inter;font-size:180px;line-height:.95;font-weight:900;color:#fff">Cleaning<br>Business<br>Forms</div><div style="font-size:66px;color:#A7F3D0;margin-top:30px;font-weight:700">Look professional from day one</div></div>
{pg("p01",820,1080,560,6,3,.4)}{pg("p03",800,110,1260,-6,2,.4)}{pg("p05",800,1080,1440,5,2,.4)}
<div style="position:absolute;bottom:0;left:0;right:0;height:220px;background:{BG};display:grid;place-items:center;z-index:9">{FMT}</div>'''
P["01_main_C"]=f'''<div style="padding:110px 110px 0;position:relative;z-index:9"><div style="display:inline-block;background:{SOFT};color:{ACC};font-weight:800;font-size:52px;padding:14px 32px;border-radius:14px">FOR CLEANING BUSINESSES</div>
<div style="font-family:'Inter Display',Inter;font-size:164px;line-height:.98;font-weight:900;margin-top:28px">Every form<br><span style="color:{ACC}">you need</span></div></div>
<div style="position:absolute;right:100px;top:300px;text-align:right;z-index:9">{pill("7 DOCS")}<br><br>{pill("PDF + WORD",ACC,"#fff")}</div>
{"".join(pg(f"p0{i+1}",560,90+(i%4)*455,880+(i//4)*700,(-4,3,-2,4,3,-3,2)[i],i) for i in range(7))}{foot()}'''
li="".join(f'<div style="display:flex;align-items:center;gap:34px;background:#fff;border-radius:26px;padding:26px 40px;margin:18px 0"><img src="{img("p"+n)}" style="width:110px;border-radius:4px;box-shadow:0 4px 12px rgba(0,0,0,.15)"><div><div style="font-size:58px;font-weight:800">{t}</div><div style="font-size:38px;color:{MUT}">{s}</div></div></div>' for n,t,s,_ in DOCS)
P["02_included"]=T("What's included","7 documents · fillable PDF + Word · Letter + A4")+f'<div style="padding:24px 150px">{li}</div>'
P["03_agreement"]=T("Service Agreement","9 clear terms that protect your business")+pg("p01",1500,250,480,0,2)+f'<div style="position:absolute;left:120px;top:1300px;z-index:9">{pill("Cancellation",ACC,"#fff",48)}</div><div style="position:absolute;right:120px;top:1650px;z-index:9">{pill("Lockout fee",ACC2,INK,48)}</div><div style="position:absolute;left:150px;top:2050px;z-index:9">{pill("Satisfaction policy",ACC,"#fff",48)}</div>'
P["04_fillable"]=T("Type right in the PDF","Free Adobe Reader · computer, tablet, phone")+pg("f03",1480,260,480,0,2)+f'<div style="position:absolute;left:300px;top:905px;width:1400px;height:110px;border:8px solid {ACC2};border-radius:18px;z-index:9"></div><div style="position:absolute;right:120px;top:1050px;z-index:9">{pill("✍ Fillable fields")}</div>'
P["05_word"]=T("Edit everything in Word","Add your logo, wording and prices")+pg("w01",1450,275,480,0,2)+f'<div style="position:absolute;left:960px;top:575px;width:330px;height:130px;border:8px solid {ACC2};border-radius:18px;z-index:9"></div><div style="position:absolute;left:1000px;top:730px;z-index:9">{pill("Your logo here",ACC2,INK,46)}</div><div style="position:absolute;left:100px;top:2200px;right:100px;text-align:center;z-index:9;font-size:54px;font-weight:700;color:{ACC}">Microsoft Word · Google Docs · Pages</div>'
steps=[("02","Walkthrough","Intake Form"),("03","Quote","Estimate"),("01","Sign","Service Agreement"),("07","Access","Key Authorization"),("05","Clean","Checklist"),("06","Get paid","Invoice")]
st="".join(f'<div style="display:flex;align-items:center;gap:40px;margin:30px 0"><div style="width:110px;height:110px;border-radius:50%;background:{ACC};color:#fff;font-size:60px;font-weight:900;display:grid;place-items:center;flex:none">{i+1}</div><img src="{img("p"+n)}" style="width:150px;box-shadow:0 6px 16px rgba(0,0,0,.15);border-radius:4px"><div><div style="font-size:64px;font-weight:800">{a}</div><div style="font-size:44px;color:{MUT}">{b}</div></div></div>' for i,(n,a,b) in enumerate(steps))
P["06_workflow"]=T("From first call to payment","A document for every step")+f'<div style="padding:30px 220px">{st}</div>'
P["07_sizes"]=T("US Letter + A4","Both sizes included, ready to print")+pg("p06",820,170,560,-3,2)+pg("a06",800,1030,540,3,2)+f'<div style="position:absolute;left:170px;top:1720px;width:820px;text-align:center;font-size:64px;font-weight:800;color:{ACC}">US Letter</div><div style="position:absolute;left:1030px;top:1720px;width:800px;text-align:center;font-size:64px;font-weight:800;color:{ACC}">A4</div>'+foot()
P["08_checklist"]=T("Room-by-room checklist","41 tasks · tick as you go")+pg("p05",1450,275,480,0,2)
how=[("Download","Get the ZIP right after purchase"),("Pick your size","US Letter or A4 folder"),("Customize","Logo, prices, details in Word"),("Use","Fill, print, sign, send")]
P["09_how"]=T("How it works","Ready in 10 minutes")+f'<div style="padding:60px 190px">'+"".join(f'<div style="display:flex;gap:44px;align-items:center;margin:80px 0"><div style="width:150px;height:150px;border-radius:40px;background:{ACC};color:#fff;font-size:84px;font-weight:900;display:grid;place-items:center;flex:none">{i+1}</div><div><div style="font-size:76px;font-weight:800">{a}</div><div style="font-size:48px;color:{MUT}">{b}</div></div></div>' for i,(a,b) in enumerate(how))+'</div>'+foot()
facts=[("⬇️","Instant digital download - nothing shipped"),("📄","Adobe Reader (free) for fillable PDFs"),("✏️","Word, Google Docs or Pages to edit"),("⚖️","Templates, not legal advice")]
P["10_good"]=T("Good to know","")+f'<div style="padding:40px 150px">'+"".join(f'<div style="display:flex;gap:40px;align-items:center;background:#fff;border-radius:30px;padding:70px 60px;margin:44px 0;font-size:60px;font-weight:600"><span style="font-size:90px">{e}</span>{t}</div>' for e,t in facts)+'</div>'
pairs=[]
for k,b in P.items():
    p=f"../img/html/{k}.html"; open(p,"w").write(page(b)); pairs.append((p,f"../img/{k}.jpg",2000,2500))
render.run(pairs)
from PIL import Image
ks=list(P); b=Image.new("RGB",(4*410+10,3*510+10),"white")
for i,k in enumerate(ks): b.paste(Image.open(f"../img/{k}.jpg").resize((400,500)),(10+(i%4)*410,10+(i//4)*510))
b.save("../img/planche.jpg"); print("ok")
