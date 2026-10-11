import sys,os; sys.path.insert(0,os.path.abspath("../../commun")); import render
from ui2 import *
O="../img"
def pill(t,bg=GO,fg=INK,fs=60): return f'<div style="background:{bg};color:{fg};font-weight:900;font-size:{fs}px;padding:20px 46px;border-radius:999px;display:inline-block">{t}</div>'
def T(t,s=""): return f'<div style="padding:120px 110px 0;text-align:center"><div style="font-family:\'Inter Display\',Inter;font-size:128px;line-height:1;font-weight:900;color:{N}">{t}</div><div style="font-size:58px;color:{MUT};margin-top:26px;font-weight:500">{s}</div></div>'
foot=lambda: f'<div style="position:absolute;bottom:70px;left:0;right:0">{badges(size=100)}</div>'
def card(w,h,inner,x,y,rot=0): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:24px;overflow:hidden;box-shadow:0 30px 70px rgba(20,35,60,.22);transform:rotate({rot}deg);background:#fff">{inner}</div>'
P={}
P["01_main_A"]=f'''<div style="padding:110px 100px 0;text-align:center"><div style="font-size:60px;font-weight:800;color:{GO};letter-spacing:.14em">GOOGLE SHEETS + EXCEL</div>
<div style="font-family:'Inter Display',Inter;font-size:170px;line-height:.98;font-weight:900;color:{N};letter-spacing:-.02em;margin-top:22px">SMALL BUSINESS<br>BOOKKEEPING</div>
<div style="font-size:64px;margin-top:28px;font-weight:500">Income · Expenses · Profit &amp; Loss · Tax</div></div>
<div style="position:absolute;left:100px;top:900px">{laptop(dashboard("19px"),1500)}</div>
<div style="position:absolute;right:60px;top:1380px">{tablet(quarterly("12.5px"),700,"4/3")}</div>
<div style="position:absolute;left:80px;top:800px;transform:rotate(-6deg)">{pill("8 AUTO TABS",GO,INK,72)}</div>
<div style="position:absolute;bottom:70px;left:0;right:0">{badges(size=130)}</div>'''
P["01_main_B"]=f'''<div style="position:absolute;inset:0;background:{N}"></div><div style="position:relative;padding:130px 110px 0"><div style="font-family:'Inter Display',Inter;font-size:190px;line-height:.95;font-weight:900;color:#fff">Bookkeeping<br>Spreadsheet</div><div style="font-size:70px;color:{GO};margin-top:34px;font-weight:700">Know your profit in seconds</div></div>
<div style="position:absolute;left:90px;top:1000px">{laptop(dashboard("19px"),1500)}</div>
<div style="position:absolute;right:120px;top:140px;width:320px;height:320px;border-radius:50%;background:{GO};display:grid;place-items:center;text-align:center;transform:rotate(8deg)"><div><div style="font-size:110px;font-weight:900;line-height:1;color:{N}">P&amp;L</div><div style="font-size:42px;font-weight:800;color:{N}">AUTOMATIC</div></div></div>
<div style="position:absolute;bottom:0;left:0;right:0;height:230px;background:{BG};display:grid;place-items:center">{badges(size=110)}</div>'''
P["01_main_C"]=f'''<div style="position:absolute;left:-60px;top:980px;transform:rotate(-4deg)">{laptop(pl("17px"),1900)}</div>
<div style="padding:110px 110px 0"><div style="display:inline-block;background:{NL};color:{N};font-weight:800;font-size:54px;padding:14px 34px;border-radius:14px">FOR SMALL BUSINESS OWNERS</div>
<div style="font-family:'Inter Display',Inter;font-size:170px;line-height:.98;font-weight:900;margin-top:30px">Bookkeeping<br><span style="color:{GO}">made easy</span></div></div>
<div style="position:absolute;right:110px;top:300px;text-align:right">{pill("PROFIT &amp; LOSS",N,"#fff",54)}<br><br>{pill("TAX SET-ASIDE",GO,INK,54)}</div><div style="position:absolute;bottom:70px;left:0;right:0">{badges(size=120)}</div>'''
items=[("Start Here","Quick setup guide"),("Setup","Business info + your categories"),("Income","Log every payment"),("Expenses","Log purchases, deductible Y/N"),("Mileage","Trips + automatic deduction"),("Profit & Loss","Monthly + yearly statement"),("Dashboard","KPIs, charts, top expenses"),("Quarterly Tax","Set-aside per quarter")]
li="".join(f'<div style="display:flex;align-items:center;gap:36px;background:#fff;border-radius:26px;padding:30px 42px;margin:20px 0;box-shadow:0 10px 30px rgba(20,35,60,.08)"><div style="width:92px;height:92px;border-radius:50%;background:{N if i%2==0 else GO};color:{"#fff" if i%2==0 else INK};font-size:50px;font-weight:900;display:grid;place-items:center;flex:none">{i+1}</div><div><div style="font-size:64px;font-weight:800">{a}</div><div style="font-size:40px;color:{MUT}">{b}</div></div></div>' for i,(a,b) in enumerate(items))
P["02_included"]=T("What's included","1 spreadsheet · 8 automated tabs")+f'<div style="padding:30px 150px">{li}</div>'+foot()
feat=lambda xs: f'<div style="position:absolute;left:110px;right:110px;top:1760px;display:grid;grid-template-columns:repeat(3,1fr);gap:30px">'+"".join(f'<div style="background:#fff;border-radius:28px;padding:40px;text-align:center;font-size:46px;font-weight:700"><div style="font-size:80px">{e}</div>{t}</div>' for e,t in xs)+'</div>'
P["03_dashboard"]=T("Business Dashboard","Your numbers at a glance")+card(1800,1180,dashboard("30px"),100,500)+feat([("💰","Net profit"),("📈","Income vs expenses"),("🧾","Tax to set aside")])+foot()
P["04_pl"]=T("Profit &amp; Loss","Monthly + year to date, automatic")+card(1800,1180,pl("33px"),100,560)+feat([("📊","By category"),("📆","Month by month"),("🏁","Net profit + margin")])+foot()
P["05_income"]=T("Log in seconds","Drop-down categories · month auto-fills")+card(920,1450,ledger("Income","25px",22),80,540,-2)+card(920,1450,ledger("Expenses","25px",22),1000,600,2)+foot()
P["06_tax"]=T("Quarterly Tax","Never be surprised at tax time")+card(1800,760,quarterly("36px"),100,600)+feat([("📅","Due dates"),("✅","Paid / to pay"),("🚗","Mileage deduction")])+foot()
steps=[("Download","Get the file right after purchase"),("Open","In Google Sheets or Excel"),("Set up","Business name + categories"),("Track","Log income &amp; expenses, see profit")]
st="".join(f'<div style="display:flex;gap:44px;align-items:center;margin:80px 0"><div style="width:150px;height:150px;border-radius:40px;background:{N};color:#fff;font-size:84px;font-weight:900;display:grid;place-items:center;flex:none">{i+1}</div><div><div style="font-size:76px;font-weight:800">{a}</div><div style="font-size:48px;color:{MUT}">{b}</div></div></div>' for i,(a,b) in enumerate(steps))
P["07_how"]=T("How it works","Start in 5 minutes")+f'<div style="padding:40px 190px">{st}</div>'+foot()
P["08_compat"]=T("Works everywhere","Computer · tablet · phone")+f'<div style="position:absolute;left:90px;top:560px">{laptop(dashboard("17px"),1300)}</div><div style="position:absolute;right:80px;top:720px">{tablet(quarterly("11px"),560,"3/4")}</div><div style="position:absolute;left:110px;right:110px;top:1580px;background:#fff;border-radius:36px;padding:60px;text-align:center"><div style="display:flex;justify-content:center">{badges(size=150)}</div><div style="font-size:48px;color:{MUT};margin-top:40px">Free Google account or Excel 2016 / Microsoft 365</div></div>'
who=[("🧹","Cleaning businesses"),("🔧","Handymen &amp; contractors"),("💇","Salons &amp; beauty pros"),("📸","Photographers &amp; creatives"),("🛍️","Etsy &amp; online sellers"),("💼","Freelancers &amp; consultants")]
P["09_who"]=T("Made for","Self-employed and small business owners")+f'<div style="padding:60px 130px;display:grid;grid-template-columns:1fr 1fr;gap:36px">'+"".join(f'<div style="background:#fff;border-radius:30px;padding:56px 40px;text-align:center"><div style="font-size:120px">{e}</div><div style="font-size:54px;font-weight:800;margin-top:16px">{t}</div></div>' for e,t in who)+'</div>'+foot()
facts=[("⬇️","Instant digital download - nothing shipped"),("💲","Change the currency format in one click"),("🧮","Sample data included to see it working"),("⚖️","Bookkeeping tool, not tax advice")]
P["10_good"]=T("Good to know","")+f'<div style="padding:40px 150px">'+"".join(f'<div style="display:flex;gap:40px;align-items:center;background:#fff;border-radius:30px;padding:70px 60px;margin:44px 0;font-size:62px;font-weight:600"><span style="font-size:90px">{e}</span>{t}</div>' for e,t in facts)+'</div>'+foot()
pairs=[]
for k,b in P.items():
    p=f"{O}/html/{k}.html"; open(p,"w").write(page(b)); pairs.append((p,f"{O}/{k}.jpg",2000,2500))
render.run(pairs)
from PIL import Image
ks=list(P); b=Image.new("RGB",(4*410+10,3*510+10),"white")
for i,k in enumerate(ks): b.paste(Image.open(f"{O}/{k}.jpg").resize((400,500)),(10+(i%4)*410,10+(i//4)*510))
b.save(f"{O}/planche.jpg"); print("ok")
