import sys,os; sys.path.insert(0,os.path.abspath("../../commun"))
from mockups import laptop, tablet, badges, FONT, money
import cfigs as figs, data
N="#1E3A5F"; NL="#E6EEF7"; GO="#C9A227"; INK="#1B2430"; MUT="#667085"; BG="#F4F1EA"
MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
CSS=f'''<style>*{{box-sizing:border-box;margin:0}}body{{font-family:Inter,sans-serif;color:{INK}}}.ic{{width:100%;height:100%}}
.dash{{background:#fff;font-size:var(--f);height:100%;display:flex;flex-direction:column}}
.tb{{height:2.4em;background:#F5F7FA;border-bottom:1px solid #E4E8EE;display:flex;align-items:center;gap:.5em;padding:0 1em;font-size:.8em;color:{MUT}}} .tb i{{width:.7em;height:.7em;border-radius:50%;display:inline-block}}
.k{{background:{NL};border-radius:.6em;padding:.6em .8em}} .k small{{display:block;font-size:.64em;color:{MUT};font-weight:700;letter-spacing:.06em}} .k b{{font-size:1.3em;color:{N}}}
.card{{border:1px solid #E6EAF0;border-radius:.6em;padding:.8em .9em;overflow:hidden}} .card h4{{font-size:.76em;color:{MUT};margin-bottom:.6em;letter-spacing:.04em}}
.ct{{width:100%;border-collapse:collapse;font-size:.74em}} .ct td,.ct th{{padding:.32em .3em;border-bottom:1px solid #EEF1F5;text-align:left;white-space:nowrap}} .ct th{{color:{MUT};font-weight:600}} .n{{text-align:right!important}}
.tabs{{height:2.2em;border-top:1px solid #E4E8EE;background:#F5F7FA;display:flex;font-size:.68em;align-items:stretch;padding-left:1em}} .tabs div{{padding:0 .9em;display:flex;align-items:center;color:{MUT}}} .tabs .on{{background:#fff;color:{N};font-weight:700;border-bottom:3px solid {N}}}
.mb,.me{{transform-origin:bottom}} .cb{{transform-origin:left}}</style>'''
TABS=["Start Here","Setup","Income","Expenses","Mileage","Profit & Loss","Dashboard","Quarterly Tax"]
def tabs(on): return "".join(f'<div class="{"on" if t==on else ""}">{t}</div>' for t in TABS)
def shell(inner,on,f): return f'<div class=dash style="--f:{f}"><div class=tb><i style="background:#F28B82"></i><i style="background:#FDD663"></i><i style="background:#81C995"></i><span style="margin-left:1em">Small_Business_Bookkeeping_2027</span></div><div style="flex:1;padding:1.1em 1.3em;overflow:hidden">{inner}</div><div class=tabs>{tabs(on)}</div></div>'
def bars(h):
    mx=max(figs.MI)
    c="".join(f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:.3em"><div style="display:flex;gap:2px;align-items:flex-end;height:100%;width:80%"><div class=mb style="flex:1;height:{(figs.MI[i]/mx*92 if i<9 else 2):.0f}%;background:{N};border-radius:.2em .2em 0 0"></div><div class=me style="flex:1;height:{(figs.ME[i]/mx*92 if i<9 else 2):.0f}%;background:{GO};border-radius:.2em .2em 0 0"></div></div><span style="font-size:.6em;color:{MUT}">{MON[i]}</span></div>' for i in range(12))
    return f'<div style="display:flex;height:{h}em;gap:.15em">{c}</div><div style="display:flex;gap:1.2em;font-size:.7em;margin-top:.5em;color:{MUT}"><span><b style="color:{N}">■</b> Income</span><span><b style="color:{GO}">■</b> Expenses</span></div>'
def catlist(n=8):
    mx=figs.CAT[0][1]
    return "".join(f'<div style="display:flex;align-items:center;gap:.6em;font-size:.74em;margin:.42em 0"><span style="width:9em">{c}</span><div style="flex:1;height:.6em;background:#EEF1F5;border-radius:1em;overflow:hidden"><div class=cb style="width:{v/mx*100:.0f}%;height:100%;background:#7FA7D9"></div></div><b style="width:4.5em;text-align:right">{money(v)}</b></div>' for c,v in figs.CAT[:n])
def dashboard(f="14px"):
    k=[("INCOME",figs.TI),("EXPENSES",figs.TE),("NET PROFIT",figs.NP),("TAX TO SET ASIDE",figs.NP*data.TAX)]
    kp="".join(f'<div class=k><small>{a}</small><b class=kv data-v="{v:.0f}">{money(v)}</b></div>' for a,v in k)
    inner=f'''<div style="display:flex;align-items:baseline;gap:1em"><b style="font-size:1.5em;color:{N}">Business Dashboard</b><span style="color:{MUT};font-size:.85em">{data.BIZ} · Year to date</span><span style="margin-left:auto;background:#FFF4D6;padding:.2em .7em;border-radius:.4em;font-weight:700;font-size:.82em">Margin {figs.NP/figs.TI:.0%}</span></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.7em;margin:.9em 0">{kp}</div>
<div style="display:grid;grid-template-columns:1.3fr 1fr;gap:.9em"><div class=card><h4>INCOME VS EXPENSES</h4>{bars(17)}</div><div class=card><h4>TOP EXPENSE CATEGORIES</h4>{catlist(12)}</div></div>'''
    return shell(inner,"Dashboard",f)
def pl(f="12px"):
    rows=[("Services",[sum(x[4] for x in figs.INC[m] if x[2]=="Services") for m in range(1,10)]),("Products",[sum(x[4] for x in figs.INC[m] if x[2]=="Products") for m in range(1,10)]),("Subscriptions",[sum(x[4] for x in figs.INC[m] if x[2]=="Subscriptions") for m in range(1,10)])]
    cell=lambda v: f'<td class=n>{v:,.0f}</td>'
    h="".join(f"<th class=n>{m}</th>" for m in MON)+"<th class=n>Total</th>"
    def row(name,vals,b=False,bg=""):
        return f'<tr style="{"font-weight:700;" if b else ""}{bg}"><td>{name}</td>'+"".join(cell(v) for v in vals)+"".join('<td class=n style="color:#C5CCD6">-</td>' for _ in range(12-len(vals)))+f'<td class=n><b>{sum(vals):,.0f}</b></td></tr>'
    ex={}
    for m in range(1,10):
        for x in figs.EXP[m]: ex.setdefault(x[2],[0]*9)[m-1]+=x[4]
    er="".join(row(c,v) for c,v in sorted(ex.items(),key=lambda x:-sum(x[1]))[:8])
    inner=f'''<b style="font-size:1.45em;color:{N}">Profit &amp; Loss Statement</b><table class=ct style="margin-top:.7em;font-size:.68em"><tr><th>Category</th>{h}</tr>
<tr><td colspan=14 style="color:{N};font-weight:800">INCOME</td></tr>{"".join(row(n,v) for n,v in rows)}{row("Total income",figs.MI,True,"background:"+NL)}
<tr><td colspan=14 style="color:{N};font-weight:800">EXPENSES</td></tr>{er}{row("Total expenses",figs.ME,True,"background:"+NL)}
{row("NET PROFIT",[a-b for a,b in zip(figs.MI,figs.ME)],True,"background:#FFF4D6;color:"+N)}</table>'''
    return shell(inner,"Profit & Loss",f)
def ledger(kind="Income",f="13px",n=14):
    if kind=="Income":
        rows="".join(f'<tr><td>{MON[0]} {d}, 2027</td><td>{c}</td><td><span style="background:{NL};padding:.1em .5em;border-radius:.3em">{cat}</span></td><td>{ref}</td><td class=n>{money(a,2)}</td><td>{pm}</td></tr>' for d,c,cat,ref,a,pm in figs.INC[1][:n])
        hd="<th>Date</th><th>Client</th><th>Category ▾</th><th>Reference</th><th class=n>Amount</th><th>Payment ▾</th>"
    else:
        rows="".join(f'<tr><td>{MON[0]} {d}, 2027</td><td>{v}</td><td><span style="background:{NL};padding:.1em .5em;border-radius:.3em">{cat}</span></td><td class=n>{money(a,2)}</td><td style="text-align:center">Y</td></tr>' for d,v,cat,_,a in figs.EXP[1][:n])
        hd="<th>Date</th><th>Vendor</th><th>Category ▾</th><th class=n>Amount</th><th>Deductible</th>"
    return shell(f'<b style="font-size:1.45em;color:{N}">{kind}</b><table class=ct style="margin-top:.7em;font-size:.8em"><tr>{hd}</tr>{rows}</table>',kind,f)
def quarterly(f="14px"):
    q=[("Q1","Jan-Mar",7887.12,1971.78,"Apr 15",1200,"Partly paid"),("Q2","Apr-May",6026.84,1506.71,"Jun 15",1450,"Partly paid"),("Q3","Jun-Aug",8153.52,2038.38,"Sep 15",0,"To pay"),("Q4","Sep-Dec",3337.49,834.37,"Jan 15",0,"To pay")]
    col={"Partly paid":"#B54708","To pay":"#B42318","Covered":"#067647"}
    rows="".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td class=n>{money(c)}</td><td class=n><b>{money(d)}</b></td><td>{e}</td><td class=n>{money(g)}</td><td style="color:{col[h]};font-weight:700">{h}</td></tr>' for a,b,c,d,e,g,h in q)
    mil=sum(x[3] for m in figs.MIL for x in figs.MIL[m])
    inner=f'''<b style="font-size:1.45em;color:{N}">Quarterly Estimated Tax</b><table class=ct style="margin-top:.8em;font-size:.82em"><tr><th>Quarter</th><th>Months</th><th class=n>Net profit</th><th class=n>Set aside 25%</th><th>Due</th><th class=n>Paid</th><th>Status</th></tr>{rows}</table>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:.8em;margin-top:1em"><div class=k><small>MILES DRIVEN</small><b>{mil:,.0f} mi</b></div><div class=k><small>MILEAGE DEDUCTION</small><b>{money(mil*data.MILE)}</b></div></div>'''
    return shell(inner,"Quarterly Tax",f)
def page(body,w=2000,h=2500,bg=BG): return f"<!doctype html><html><head><meta charset=utf-8>{FONT}{CSS}<style>html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{bg}}}</style></head><body>{body}</body></html>"
