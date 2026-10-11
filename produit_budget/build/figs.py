# Chiffres du mois de janvier, calculés comme dans le tableur (même source).
import data
def month(m=1):
    t=data.transactions(m); inc=sum(a for _,a in data.INCOME)
    act={c:0 for c,_,_ in data.CATS}
    for _,c,_,a in t: act[c]+=a
    rows=[(c,g,b,round(act[c],2)) for c,g,b in data.CATS]
    spent=sum(r[3] for r in rows); bud=sum(r[2] for r in rows)
    sav=sum(r[3] for r in rows if r[1]=="Savings")
    grp={}
    for c,g,b,a in rows: grp[g]=grp.get(g,0)+a
    return dict(rows=rows,income=inc,spent=spent,budget=bud,left=inc-spent,rate=sav/inc,groups=grp,tx=t)
def year():
    return [round(sum(x[3] for x in data.transactions(m)),2) for m in range(1,7)]
if __name__=="__main__":
    d=month(); print({k:v for k,v in d.items() if k not in('rows','tx')}); print(year())
