# Composants HTML partagés : tableau de bord (réplique fidèle du tableur), cadres, icônes.
import figs, data
G="#2F6B4F"; GL="#E4EFE8"; CR="#F3F0EA"; CO="#E07A5F"; INK="#1F2A24"; MUT="#6B7A71"
D=figs.month(1); Y=figs.year()
money=lambda v,d=0: ("-" if v<0 else "")+"$"+f"{abs(v):,.{d}f}"
PAL=["#2F6B4F","#6FAF8B","#A8D5BA","#E07A5F","#F2B880","#8CA6DB","#C7B9E6","#D9CBB0"]
SHEETS_ICON='''<svg viewBox="0 0 48 64" class="ic"><path d="M4 0h28l16 16v44a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4V4a4 4 0 0 1 4-4z" fill="#1E9E5A"/><path d="M32 0l16 16H36a4 4 0 0 1-4-4z" fill="#8ED1AC"/><rect x="10" y="28" width="28" height="22" rx="1.5" fill="#fff"/><path d="M10 35.3h28M10 42.6h28M20 28v22" stroke="#1E9E5A" stroke-width="2.4"/></svg>'''
EXCEL_ICON='''<svg viewBox="0 0 64 64" class="ic"><rect x="18" y="6" width="42" height="52" rx="4" fill="#33A06A"/><path d="M39 6h17a4 4 0 0 1 4 4v14H39z" fill="#5CC08B"/><path d="M39 24h21v16H39z" fill="#2A8A59"/><path d="M39 40h21v14a4 4 0 0 1-4 4H39z" fill="#1F6E46"/><rect x="2" y="16" width="34" height="32" rx="4" fill="#185C3A"/><path d="M11 24l14 16M25 24L11 40" stroke="#fff" stroke-width="4.2" stroke-linecap="round"/></svg>'''
FONT="<style>*{box-sizing:border-box;margin:0}body{font-family:Inter,'DejaVu Sans',sans-serif;color:"+INK+"}</style>"
def donut(size):
    tot=sum(D["groups"].values()); acc=0; stops=[]
    for i,(g,v) in enumerate(D["groups"].items()):
        a=acc/tot*360; acc+=v; b=acc/tot*360; stops.append(f"{PAL[[0,3,1,5][i]]} {a:.1f}deg {b:.1f}deg")
    leg="".join(f'<div style="display:flex;align-items:center;gap:.5em;font-size:.82em;margin:.25em 0"><span style="width:.8em;height:.8em;border-radius:3px;background:{PAL[[0,3,1,5][i]]}"></span>{g}<b style="margin-left:auto">{v/tot:.0%}</b></div>' for i,(g,v) in enumerate(D["groups"].items()))
    return f'''<div style="display:flex;align-items:center;gap:1.2em"><div class=dn style="width:{size}em;height:{size}em;border-radius:50%;background:conic-gradient({",".join(stops)});display:grid;place-items:center;flex:none"><div style="width:62%;height:62%;border-radius:50%;background:#fff;display:grid;place-items:center;text-align:center;font-size:.8em"><div><div style="color:{MUT};font-size:.8em">Spent</div><b style="font-size:1.25em">{money(D["spent"])}</b></div></div></div><div style="flex:1">{leg}</div></div>'''
def bars(h):
    mx=max(Y); m=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    cols="".join(f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:.3em;height:100%"><div class=mb style="width:62%;height:{(Y[i]/mx*88 if i<6 else 3):.0f}%;background:{G if i==0 else "#A8D5BA" if i<6 else "#E6EBE7"};border-radius:.25em .25em 0 0"></div><span style="font-size:.62em;color:{MUT}">{m[i]}</span></div>' for i in range(12))
    return f'<div style="display:flex;height:{h}em;gap:.2em;align-items:flex-end">{cols}</div>'
def cat_table(n=16):
    r=""
    for c,g,b,a in sorted(D["rows"],key=lambda x:-x[3])[:n]:
        p=a/b if b else 0; col=CO if p>1 else G
        r+=f'<tr><td>{c}</td><td class=n>{money(b)}</td><td class=n>{money(a,0)}</td><td style="width:32%"><div class=tbar style="height:.55em;background:#EEF1EE;border-radius:1em;overflow:hidden"><div style="width:{min(p,1)*100:.0f}%;height:100%;background:{col}"></div></div></td><td class=n style="color:{col};font-weight:700">{p:.0%}</td></tr>'
    return f'<table class=ct><tr><th>Category</th><th class=n>Budget</th><th class=n>Actual</th><th></th><th class=n>Used</th></tr>{r}</table>'
CSS=f'''<style>.dash{{background:#fff;font-size:var(--f);height:100%;display:flex;flex-direction:column}}
.tb{{height:2.4em;background:#F6F8F6;border-bottom:1px solid #E3E8E4;display:flex;align-items:center;gap:.5em;padding:0 1em;font-size:.8em;color:{MUT}}}
.tb i{{width:.7em;height:.7em;border-radius:50%;display:inline-block}}
.body{{flex:1;padding:1.1em 1.3em;display:grid;grid-template-columns:1.25fr 1fr;grid-template-rows:auto auto 1fr;gap:.9em}}
.h1{{grid-column:1/3;display:flex;align-items:baseline;gap:1em}} .h1 b{{font-size:1.55em;color:{G}}} .h1 span{{margin-left:auto;background:#FFF2C6;padding:.2em .7em;border-radius:.4em;font-weight:700;font-size:.85em}}
.kpis{{grid-column:1/3;display:grid;grid-template-columns:repeat(4,1fr);gap:.7em}}
.k{{background:{GL};border-radius:.6em;padding:.6em .8em}} .k small{{display:block;font-size:.66em;color:{MUT};font-weight:700;letter-spacing:.06em}} .k b{{font-size:1.3em;color:{G}}}
.card{{border:1px solid #E6EBE7;border-radius:.6em;padding:.8em .9em;overflow:hidden}} .card h4{{font-size:.78em;color:{MUT};margin-bottom:.6em;letter-spacing:.04em}}
.ct{{width:100%;border-collapse:collapse;font-size:.74em}} .ct td,.ct th{{padding:.32em .3em;border-bottom:1px solid #EEF1EE;text-align:left}} .ct th{{color:{MUT};font-weight:600}} .n{{text-align:right!important;white-space:nowrap}}
.tabs{{height:2.2em;border-top:1px solid #E3E8E4;background:#F6F8F6;display:flex;font-size:.7em;align-items:stretch;padding-left:1em}}
.tabs div{{padding:0 1em;display:flex;align-items:center;color:{MUT}}} .tabs .on{{background:#fff;color:{G};font-weight:700;border-bottom:3px solid {G}}}</style>'''
TABS=["Start Here","Setup","Transactions","Dashboard","Annual","Debt Payoff","Savings Goals"]
def dashboard(f="14px",n=16):
    tabs="".join(f'<div class="{"on" if t=="Dashboard" else ""}">{t}</div>' for t in TABS)
    return f'''<div class=dash style="--f:{f}"><div class=tb><i style="background:#F28B82"></i><i style="background:#FDD663"></i><i style="background:#81C995"></i><span style="margin-left:1em">Annual_Budget_Planner_2027</span></div>
<div class=body><div class=h1><b>Budget Dashboard</b><span>Month: Jan ▾</span></div>
<div class=kpis><div class=k><small>INCOME</small><b>{money(D["income"])}</b></div><div class=k><small>SPENT</small><b>{money(D["spent"])}</b></div><div class=k><small>BUDGETED</small><b>{money(D["budget"])}</b></div><div class=k><small>LEFT</small><b>{money(D["left"])}</b></div></div>
<div class=card style="grid-row:3/4">{"<h4>BUDGET VS ACTUAL</h4>"+cat_table(n)}</div>
<div style="display:grid;gap:.9em;grid-template-rows:auto 1fr"><div class=card><h4>SPENDING BY GROUP</h4>{donut(7)}</div><div class=card><h4>SPENT PER MONTH</h4>{bars(6)}</div></div></div>
<div class=tabs>{tabs}</div></div>'''
def annual(f="12px"):
    m=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    import data as dd
    per={}
    for mm in range(1,7):
        for _,c,_,a in dd.transactions(mm): per[(c,mm)]=per.get((c,mm),0)+a
    rows="".join("<tr><td>"+c+"</td>"+"".join(f'<td class=n>{per.get((c,mm),0):,.0f}</td>' if mm<=6 else '<td class=n style="color:#C9D1CB">-</td>' for mm in range(1,13))+"</tr>" for c,_,_ in dd.CATS[:14])
    tot="<tr style='font-weight:700;background:"+GL+"'><td>Total spent</td>"+"".join(f'<td class=n>{Y[i]:,.0f}</td>' if i<6 else '<td class=n>-</td>' for i in range(12))+"</tr>"
    tabs="".join(f'<div class="{"on" if t=="Annual" else ""}">{t}</div>' for t in TABS)
    return f'''<div class=dash style="--f:{f}"><div class=tb><i style="background:#F28B82"></i><i style="background:#FDD663"></i><i style="background:#81C995"></i></div><div style="flex:1;padding:1em 1.2em"><b style="font-size:1.5em;color:{G}">Annual Overview 2027</b>
<table class=ct style="margin-top:.8em;font-size:.72em"><tr><th>Category</th>{"".join(f"<th class=n>{x}</th>" for x in m)}</tr>{rows}{tot}</table></div><div class=tabs>{tabs}</div></div>'''
def goals(f="14px"):
    gl=[("Emergency Fund",10000,6400),("Vacation",3000,1200),("New Laptop",1500,950),("Holiday Gifts",800,240)]
    db=[("Credit Card",4200,1800),("Car Loan",11400,1710),("Student Loan",8600,660)]
    row=lambda n,t,s,c: f'<div style="margin:.75em 0"><div style="display:flex;font-size:.85em"><b>{n}</b><span style="margin-left:auto;color:{MUT}">{money(s)} / {money(t)}</span></div><div style="height:.9em;background:#EEF1EE;border-radius:1em;margin-top:.3em;overflow:hidden"><div style="width:{s/t*100:.0f}%;height:100%;background:{c};border-radius:1em"></div></div></div>'
    return f'''<div class=dash style="--f:{f}"><div class=tb><i style="background:#F28B82"></i><i style="background:#FDD663"></i><i style="background:#81C995"></i></div><div style="flex:1;padding:1.2em 1.4em;display:grid;grid-template-columns:1fr 1fr;gap:1.4em">
<div class=card><h4>SAVINGS GOALS</h4>{"".join(row(n,t,s,"#6FAF8B") for n,t,s in gl)}</div><div class=card><h4>DEBT PAYOFF · SNOWBALL</h4>{"".join(row(n,t,s,CO) for n,t,s in db)}<div style="margin-top:1em;font-size:.85em">Total paid: <b style="color:{G}">{money(sum(x[2] for x in db))}</b> · {sum(x[2] for x in db)/sum(x[1] for x in db):.0%} done</div></div></div></div>'''
def laptop(inner,w):
    return f'''<div style="width:{w}px"><div style="background:#1E2421;border-radius:{w*.03}px {w*.03}px 0 0;padding:{w*.022}px {w*.022}px {w*.03}px;box-shadow:0 {w*.04}px {w*.08}px rgba(40,50,40,.28)"><div style="aspect-ratio:16/10;overflow:hidden;border-radius:4px">{inner}</div></div>
<div style="height:{w*.035}px;background:linear-gradient(#D6D9D7,#A9AEAB);margin:0 -{w*.07}px;border-radius:0 0 {w*.06}px {w*.06}px;position:relative"><div style="position:absolute;left:42%;width:16%;top:0;height:35%;background:#9CA19E;border-radius:0 0 8px 8px"></div></div></div>'''
def tablet(inner,w,ratio="4/3"):
    return f'''<div style="width:{w}px;background:#1E2421;border-radius:{w*.05}px;padding:{w*.035}px;box-shadow:0 {w*.05}px {w*.1}px rgba(40,50,40,.32)"><div style="aspect-ratio:{ratio};overflow:hidden;border-radius:{w*.015}px">{inner}</div></div>'''
def page(body,bg=CR,w=2000,h=2500):
    return f"<!doctype html><html><head><meta charset=utf-8>{FONT}{CSS}<style>html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{bg}}}</style></head><body>{body}</body></html>"
def badges(color=INK,size=92):
    return f'''<div style="display:flex;gap:56px;justify-content:center;align-items:center;font-weight:700;font-size:{size*.5}px;color:{color}"><div style="display:flex;align-items:center;gap:20px"><div style="height:{size}px;width:{size*.75}px">{SHEETS_ICON}</div>Google Sheets</div><div style="display:flex;align-items:center;gap:20px"><div style="height:{size}px;width:{size}px">{EXCEL_ICON}</div>Excel</div></div><style>.ic{{width:100%;height:100%}}</style>'''
