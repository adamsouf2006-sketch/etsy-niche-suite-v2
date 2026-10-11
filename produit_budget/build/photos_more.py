import render
from ui import *
O="../img"
def T(t,s=""): return f'<div style="padding:120px 110px 0;text-align:center"><div style="font-family:\'Inter Display\',Inter;font-size:130px;line-height:1;font-weight:900;color:{G};letter-spacing:-.01em">{t}</div><div style="font-size:58px;color:{MUT};margin-top:28px;font-weight:500">{s}</div></div>'
def foot(): return f'<div style="position:absolute;bottom:70px;left:0;right:0">{badges(size=100)}</div>'
def card(w,h,inner,x,y,rot=0): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:24px;overflow:hidden;box-shadow:0 30px 70px rgba(40,50,40,.22);transform:rotate({rot}deg);background:#fff">{inner}</div>'
def setup_tab(f):
    rows="".join(f'<tr><td style="background:{GL}">{c}</td><td style="background:{GL}">{g}</td><td class=n style="background:{GL}">{money(b)}</td></tr>' for c,g,b in data.CATS[:13])
    inc="".join(f'<tr><td style="background:{GL}">{s}</td><td></td><td class=n style="background:{GL}">{money(a)}</td></tr>' for s,a in data.INCOME)
    return f'<div class=dash style="--f:{f}"><div style="padding:1.2em 1.4em"><b style="font-size:1.5em;color:{G}">Setup</b><table class=ct style="margin-top:.8em;font-size:.8em"><tr><th>Income source</th><th></th><th class=n>Monthly</th></tr>{inc}<tr><th>Category</th><th>Group</th><th class=n>Budget</th></tr>{rows}</table></div></div>'
def tx_tab(f):
    t=D["tx"][:16]
    rows="".join(f'<tr><td>Jan {d}, 2027</td><td>{c}</td><td>{desc}</td><td class=n>{money(a,2)}</td><td style="text-align:center">Jan</td></tr>' for d,c,desc,a in t)
    return f'<div class=dash style="--f:{f}"><div style="padding:1.2em 1.4em"><b style="font-size:1.5em;color:{G}">Transactions</b><table class=ct style="margin-top:.8em;font-size:.8em"><tr><th>Date</th><th>Category ▾</th><th>Description</th><th class=n>Amount</th><th>Month</th></tr>{rows}</table></div></div>'
P={}
# 2. Ce que vous recevez
items=[("Start Here","Quick 2-minute instructions"),("Setup","Income + up to 30 categories"),("Transactions","Log expenses, drop-down categories"),("Dashboard","Monthly budget vs actual + chart"),("Annual","Your whole year at a glance"),("Debt Payoff","Snowball tracker, progress bars"),("Savings Goals","Targets and progress bars")]
li="".join(f'<div style="display:flex;align-items:center;gap:40px;background:#fff;border-radius:28px;padding:44px 50px;margin:28px 0;box-shadow:0 10px 30px rgba(40,50,40,.08)"><div style="width:100px;height:100px;border-radius:50%;background:{G if i%2==0 else CO};color:#fff;font-size:54px;font-weight:900;display:grid;place-items:center;flex:none">{i+1}</div><div><div style="font-size:72px;font-weight:800">{a}</div><div style="font-size:42px;color:{MUT}">{b}</div></div></div>' for i,(a,b) in enumerate(items))
P["02_included"]=T("What's included","1 spreadsheet · 7 automated tabs")+f'<div style="padding:40px 150px">{li}</div>'+foot()
# 3. Dashboard zoom
P["03_dashboard"]=T("Monthly Dashboard","Pick a month - everything updates")+card(1800,1180,dashboard("30px"),100,500)+f'<div style="position:absolute;left:110px;right:110px;top:1760px;display:grid;grid-template-columns:repeat(3,1fr);gap:30px">'+"".join(f'<div style="background:#fff;border-radius:28px;padding:40px;text-align:center;font-size:46px;font-weight:700"><div style="font-size:80px">{e}</div>{t}</div>' for e,t in [("📊","Budget vs actual"),("🔴","Overspending in red"),("🍩","Spending chart")])+'</div>'+foot()
# 4. Annual
P["04_annual"]=T("Annual Overview","12 months · every category · totals")+card(1800,1560,annual("27px"),100,500)+foot()
# 5. Debt + savings
P["05_goals"]=T("Debt & Savings","Watch your progress bars fill up")+card(1800,1100,goals("40px"),100,520)+f'<div style="position:absolute;left:0;right:0;top:1720px;text-align:center;font-size:66px;font-weight:700;color:{INK}">Snowball debt payoff · 8 debts · 8 savings goals</div>'+foot()
# 6. Setup + Transactions
P["06_easy"]=T("Easy to use","Fill the green cells - formulas do the rest")+card(900,1500,setup_tab("31px"),90,520,-2)+card(960,1500,tx_tab("27px"),950,580,2)+foot()
# 7. Comment ça marche
steps=[("Download","Get the file instantly after purchase"),("Open","In Google Sheets or Microsoft Excel"),("Set up","Add your income and categories"),("Track","Log expenses, check your dashboard")]
st="".join(f'<div style="display:flex;gap:44px;align-items:center;margin:80px 0"><div style="width:150px;height:150px;border-radius:40px;background:{G};color:#fff;font-size:84px;font-weight:900;display:grid;place-items:center;flex:none">{i+1}</div><div><div style="font-size:76px;font-weight:800">{a}</div><div style="font-size:48px;color:{MUT}">{b}</div></div></div>' for i,(a,b) in enumerate(steps))
P["07_how"]=T("How it works","Start budgeting in 5 minutes")+f'<div style="padding:60px 190px">{st}</div>'+foot()
# 8. Compatibilité
P["08_compat"]=T("Works everywhere","Computer · tablet · phone")+f'<div style="position:absolute;left:90px;top:560px">{laptop(dashboard("17px"),1300)}</div><div style="position:absolute;right:80px;top:720px">{tablet(goals("13px"),560,"3/4")}</div>'+f'<div style="position:absolute;left:110px;right:110px;top:1580px;background:#fff;border-radius:36px;padding:60px;text-align:center"><div style="display:flex;justify-content:center">{badges(size=150)}</div><div style="font-size:48px;color:{MUT};margin-top:40px">Free Google account or Excel 2016 / Microsoft 365</div></div>'
# 9. Bon à savoir
facts=[("⬇️","Instant digital download - nothing shipped"),("💲","Change the currency format in one click"),("🧮","Sample data included to see it working"),("👤","Personal use · not financial advice")]
fa="".join(f'<div style="display:flex;gap:40px;align-items:center;background:#fff;border-radius:30px;padding:70px 60px;margin:44px 0;font-size:62px;font-weight:600"><span style="font-size:90px">{e}</span>{t}</div>' for e,t in facts)
P["09_good"]=T("Good to know","")+f'<div style="padding:40px 150px">{fa}</div>'+foot()
pairs=[]
for k,b in P.items():
    p=f"{O}/html/{k}.html"; open(p,"w").write(page(b)); pairs.append((p,f"{O}/{k}.jpg",2000,2500))
render.run(pairs)
from PIL import Image
ims=[Image.open(f"{O}/{k}.jpg").resize((400,500)) for k in P]
b=Image.new("RGB",(4*410+10,2*510+10),"white")
for i,im in enumerate(ims): b.paste(im,(10+(i%4)*410,10+(i//4)*510))
b.save(f"{O}/planche_secondaires.jpg"); print("ok")
