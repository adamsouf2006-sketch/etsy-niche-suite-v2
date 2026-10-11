import ui, render, os
from ui import *
O="../img"; os.makedirs(O+"/html",exist_ok=True)
def pill(t,bg=CO,fg="#fff",fs=54): return f'<div style="background:{bg};color:{fg};font-weight:800;font-size:{fs}px;padding:20px 46px;border-radius:999px;letter-spacing:.02em;display:inline-block">{t}</div>'
V={}
# A — crème, titre en haut, ordinateur + tablette
V["A"]=f'''<div style="padding:120px 110px 0;text-align:center"><div style="font-size:64px;font-weight:700;color:{CO};letter-spacing:.14em">GOOGLE SHEETS + EXCEL · 2027</div>
<div style="font-family:'Inter Display',Inter;font-size:188px;line-height:.98;font-weight:900;color:{G};letter-spacing:-.02em;margin-top:24px">ANNUAL BUDGET<br>SPREADSHEET</div>
<div style="font-size:64px;color:{INK};margin-top:30px;font-weight:500">Monthly budget · Debt · Savings · Bills</div></div>
<div style="position:absolute;left:110px;top:900px">{laptop(dashboard("19px"),1500)}</div>
<div style="position:absolute;right:60px;top:1380px">{tablet(goals("13px"),700,"4/3")}</div>
<div style="position:absolute;left:90px;top:800px;transform:rotate(-6deg)">{pill("7 AUTO TABS",CO,"#fff",72)}</div>
<div style="position:absolute;bottom:70px;left:0;right:0">{badges(size=130)}</div>'''
# B — fond vert sauge, titre blanc
V["B"]=f'''<div style="position:absolute;inset:0;background:{G}"></div><div style="position:relative;padding:130px 110px 0">
<div style="font-family:'Inter Display',Inter;font-size:200px;line-height:.95;font-weight:900;color:#fff;letter-spacing:-.02em">Budget<br>Spreadsheet</div>
<div style="font-size:70px;color:#CFE6D8;margin-top:36px;font-weight:600">Take control of every paycheck</div></div>
<div style="position:absolute;right:130px;top:150px;width:330px;height:330px;border-radius:50%;background:{CO};color:#fff;display:grid;place-items:center;text-align:center;transform:rotate(8deg)"><div><div style="font-size:120px;font-weight:900;line-height:1">7</div><div style="font-size:44px;font-weight:800">AUTO TABS</div></div></div>
<div style="position:absolute;left:-60px;top:1000px;transform:rotate(-3deg)">{tablet(annual("15px"),1250,"4/3")}</div>
<div style="position:absolute;right:70px;top:1180px;transform:rotate(3deg)">{tablet(dashboard("12px"),1180,"16/11")}</div>
<div style="position:absolute;bottom:0;left:0;right:0;height:230px;background:{CR};display:grid;place-items:center">{badges()}</div>'''
# C — crème, grand écran plein cadre, titre en bandeau
V["C"]=f'''<div style="position:absolute;left:-80px;top:1000px;transform:rotate(-4deg)">{laptop(dashboard("21px"),1900)}</div>
<div style="position:absolute;left:0;right:0;top:0;padding:110px 110px 0;text-align:left">
<div style="display:inline-block;background:{GL};color:{G};font-weight:800;font-size:56px;padding:14px 34px;border-radius:14px">GOOGLE SHEETS + EXCEL</div>
<div style="font-family:'Inter Display',Inter;font-size:176px;line-height:.98;font-weight:900;color:{INK};margin-top:30px;letter-spacing:-.02em">The Budget<br>Planner <span style="color:{CO}">that<br>does the math</span></div></div>
<div style="position:absolute;right:110px;top:250px;text-align:right">{pill("DASHBOARD",G,"#fff",56)}<br><br>{pill("DEBT + SAVINGS",CO,"#fff",56)}</div>
<div style="position:absolute;bottom:80px;left:0;right:0">{badges()}</div>'''
pairs=[]
for k,b in V.items():
    p=f"{O}/html/main_{k}.html"; open(p,"w").write(page(b)); pairs.append((p,f"{O}/main_{k}.jpg",2000,2500))
render.run(pairs); print("ok")
