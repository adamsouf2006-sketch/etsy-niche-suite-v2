import datetime as dt, data
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import DoughnutChart, BarChart, Reference
G="2F6B4F"; GL="E4EFE8"; CR="FBF7F0"; CO="E07A5F"; INK="1F2A24"; MUT="6B7A71"
F=lambda **k: Font(name="Arial", color=k.pop("color",INK), **k)
fill=lambda c: PatternFill("solid", fgColor=c)
thin=Side(style="thin", color="D9E2DC"); B=Border(bottom=thin)
MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONEY='$#,##0.00;[Red]-$#,##0.00'
wb=Workbook()
def sheet(name, widths, title, sub, tab=G):
    ws=wb.create_sheet(name); ws.sheet_properties.tabColor=tab; ws.sheet_view.showGridLines=False
    for i,w in enumerate(widths): ws.column_dimensions[chr(66+i)].width=w
    ws.column_dimensions["A"].width=3
    ws["B2"]=title; ws["B2"].font=F(size=20,bold=True,color=G)
    ws["B3"]=sub; ws["B3"].font=F(size=10,color=MUT); ws.row_dimensions[2].height=30
    return ws
def head(ws,row,cols,c0=2):
    for i,h in enumerate(cols):
        c=ws.cell(row,c0+i,h); c.font=F(bold=True,color="FFFFFF",size=10); c.fill=fill(G); c.alignment=Alignment(horizontal="center",vertical="center")
    ws.row_dimensions[row].height=22
wb.remove(wb.active)
# ---------- Start Here
ws=sheet("Start Here",[90],"Annual Budget Planner "+str(data.YEAR),"Read me first - 2 minutes")
steps=["1. SETUP tab: type your income sources and your budget categories (green cells). Categories feed every other tab.",
 "2. TRANSACTIONS tab: log each expense - date, category (drop-down), description, amount. The month fills in by itself.",
 "3. DASHBOARD tab: pick a month in the yellow cell. Totals, budget vs actual and the chart update automatically.",
 "4. ANNUAL tab: your whole year at a glance, month by month and category by category.",
 "5. DEBT PAYOFF and SAVINGS GOALS: enter balances and targets, progress bars fill in as you go.",
 "","Only type in green-shaded cells. White cells contain formulas - leave them as they are.",
 "Works in Google Sheets (File > Import, or open from Drive) and Microsoft Excel 2016 or newer.",
 "Sample data is included so you can see it working. Clear it from the green cells when you are ready.",
 "","This is a personal budgeting tool, not financial advice."]
for i,s in enumerate(steps): c=ws.cell(5+i,2,s); c.font=F(size=11,bold=s[:1].isdigit()); c.alignment=Alignment(wrap_text=True,vertical="top"); ws.row_dimensions[5+i].height=30 if s else 10
# ---------- Setup
ws=sheet("Setup",[28,14,16,4,26,16],"Setup","Your income and budget categories")
ws["B5"]="INCOME (monthly)"; ws["B5"].font=F(bold=True,color=G)
head(ws,6,["Source","","Amount"])
for i,(s,a) in enumerate(data.INCOME):
    r=7+i; ws.cell(r,2,s).fill=fill(GL); c=ws.cell(r,4,a); c.fill=fill(GL); c.number_format=MONEY
for r in range(7+len(data.INCOME),12): ws.cell(r,2).fill=fill(GL); ws.cell(r,4).fill=fill(GL); ws.cell(r,4).number_format=MONEY
ws["B12"]="Total income"; ws["B12"].font=F(bold=True); ws["D12"]="=SUM(D7:D11)"; ws["D12"].number_format=MONEY; ws["D12"].font=F(bold=True)
ws["B14"]="BUDGET CATEGORIES"; ws["B14"].font=F(bold=True,color=G)
head(ws,15,["Category","Group","Monthly budget"])
CAT0=16; NCAT=30; CATN=CAT0+NCAT-1
dvg=DataValidation(type="list",formula1='"Bills,Living,Savings,Debt"'); ws.add_data_validation(dvg)
for i in range(NCAT):
    r=CAT0+i
    for col in (2,3,4): ws.cell(r,col).fill=fill(GL)
    ws.cell(r,4).number_format=MONEY; dvg.add(ws.cell(r,3))
    if i<len(data.CATS): n,g,b=data.CATS[i]; ws.cell(r,2,n); ws.cell(r,3,g); ws.cell(r,4,b)
ws.cell(CATN+1,2,"Total budget").font=F(bold=True); c=ws.cell(CATN+1,4,f"=SUM(D{CAT0}:D{CATN})"); c.number_format=MONEY; c.font=F(bold=True)
CATR=f"Setup!$B${CAT0}:$B${CATN}"
# ---------- Transactions
ws=sheet("Transactions",[13,24,30,14,9],"Transactions","Log every expense here")
head(ws,5,["Date","Category","Description","Amount","Month"])
dv=DataValidation(type="list",formula1=f"={CATR}",allow_blank=True); ws.add_data_validation(dv)
r=6
for m in range(1,7):
    for d,c,desc,a in data.transactions(m):
        ws.cell(r,2,dt.date(data.YEAR,m,d)); ws.cell(r,3,c); ws.cell(r,4,desc); ws.cell(r,5,a); r+=1
NT=r-1; TMAX=1000
for rr in range(6,TMAX+1):
    for col in (2,3,4,5): ws.cell(rr,col).fill=fill(GL)
    ws.cell(rr,2).number_format="mmm d, yyyy"; ws.cell(rr,5).number_format=MONEY
    ws.cell(rr,6,f'=IF(B{rr}="","",TEXT(B{rr},"mmm"))').alignment=Alignment(horizontal="center")
dv.add(f"C6:C{TMAX}"); ws.freeze_panes="B6"
T=lambda col: f"Transactions!${col}$6:${col}${TMAX}"
# ---------- Dashboard
ws=sheet("Dashboard",[24,15,15,15,12,4,16,16],"Budget Dashboard","Pick a month - everything updates")
ws["B5"]="Month"; ws["B5"].font=F(bold=True); ws["C5"]="Jan"; ws["C5"].fill=fill("FFF2C6"); ws["C5"].font=F(bold=True,size=12)
ws.add_data_validation(dvm:=DataValidation(type="list",formula1='"'+",".join(MON)+'"')); dvm.add("C5")
cards=[("Income","=Setup!D12"),("Spent",f'=SUMIFS({T("E")},{T("F")},C5)'),("Budgeted",f"=Setup!D{CATN+1}"),("Left",'=C7-D7')]
for i,(lab,fm) in enumerate(cards):
    c=ws.cell(6,3+i if i<4 else 0,lab); c.font=F(size=9,bold=True,color=MUT); c.alignment=Alignment(horizontal="center")
    c=ws.cell(7,3+i,fm); c.number_format='$#,##0;[Red]-$#,##0'; c.font=F(size=16,bold=True,color=G); c.alignment=Alignment(horizontal="center"); c.fill=fill(GL)
ws["B7"]="This month"; ws["B7"].font=F(bold=True); ws.row_dimensions[7].height=32
ws["B8"]="Savings rate"; ws["C8"]=f'=IFERROR(SUMIFS({T("E")},{T("F")},C5,{T("C")},"*Fund")+SUMIFS({T("E")},{T("F")},C5,{T("C")},"Retirement"),0)/C7'
ws["C8"].number_format="0.0%"; ws["C8"].font=F(bold=True,color=G)
head(ws,10,["Category","Budget","Actual","Difference","% used"])
for i in range(NCAT):
    r=11+i; s=CAT0+i
    ws.cell(r,2,f'=IF(Setup!B{s}="","",Setup!B{s})')
    ws.cell(r,3,f'=IF(B{r}="","",Setup!D{s})').number_format=MONEY
    ws.cell(r,4,f'=IF(B{r}="","",SUMIFS({T("E")},{T("C")},B{r},{T("F")},$C$5))').number_format=MONEY
    ws.cell(r,5,f'=IF(B{r}="","",C{r}-D{r})').number_format=MONEY
    ws.cell(r,6,f'=IF(OR(B{r}="",C{r}=0),"",D{r}/C{r})').number_format="0%"
    for col in range(2,7): ws.cell(r,col).border=B
DE=11+NCAT-1
ws.conditional_formatting.add(f"F11:F{DE}",CellIsRule(operator="greaterThan",formula=["1"],fill=fill("F9D9D0"),font=Font(color="B23A1E",bold=True)))
ws.conditional_formatting.add(f"F11:F{DE}",CellIsRule(operator="between",formula=["0.9","1"],fill=fill("FFF2C6")))
ws.conditional_formatting.add(f"E11:E{DE}",CellIsRule(operator="lessThan",formula=["0"],font=Font(color="B23A1E",bold=True)))
ch=DoughnutChart(); ch.title="Spending by category"; ch.holeSize=55
ch.add_data(Reference(ws,min_col=4,min_row=10,max_row=10+len(data.CATS)),titles_from_data=True)
ch.set_categories(Reference(ws,min_col=2,min_row=11,max_row=10+len(data.CATS))); ch.height=9; ch.width=13
ws.add_chart(ch,"H10")
# ---------- Annual
ws=sheet("Annual",[22]+[11]*12+[13],"Annual Overview",str(data.YEAR)+" month by month")
head(ws,5,["Category"]+MON+["Total"])
for i in range(NCAT):
    r=6+i; s=CAT0+i; ws.cell(r,2,f'=IF(Setup!B{s}="","",Setup!B{s})')
    for m in range(12):
        col=3+m; L=ws.cell(5,col).column_letter
        ws.cell(r,col,f'=IF($B{r}="","",SUMIFS({T("E")},{T("C")},$B{r},{T("F")},{L}$5))').number_format='#,##0;-#,##0;"-"'
    ws.cell(r,15,f'=IF(B{r}="","",SUM(C{r}:N{r}))').number_format='$#,##0'
AE=6+NCAT-1
for lab,k in (("Total spent",0),("Income",1),("Left over",2)):
    r=AE+1+k; ws.cell(r,2,lab).font=F(bold=True)
    for m in range(13):
        col=3+m; L=ws.cell(5,col).column_letter
        f={0:f"=SUM({L}6:{L}{AE})",1:"=Setup!$D$12" if m<12 else "=Setup!$D$12*12",2:f"={L}{AE+2}-{L}{AE+1}"}[k]
        c=ws.cell(r,col,f); c.number_format='$#,##0;[Red]-$#,##0'; c.font=F(bold=True,color=G if k==2 else INK); c.fill=fill(GL)
bc=BarChart(); bc.title="Spent per month"; bc.add_data(Reference(ws,min_col=3,max_col=14,min_row=AE+1),from_rows=True,titles_from_data=False)
bc.set_categories(Reference(ws,min_col=3,max_col=14,min_row=5)); bc.legend=None; bc.height=7; bc.width=22; ws.add_chart(bc,f"B{AE+6}")
# ---------- Debt payoff
ws=sheet("Debt Payoff",[22,14,10,14,14,14,14],"Debt Payoff Tracker","Snowball: smallest balance first")
head(ws,5,["Debt","Starting balance","APR","Min payment","Paid so far","Remaining","Progress"])
debts=[("Credit Card",4200,0.229,120,1800),("Car Loan",11400,0.069,285,1710),("Student Loan",8600,0.045,110,660)]
for i in range(8):
    r=6+i
    for col in range(2,7): ws.cell(r,col).fill=fill(GL)
    if i<len(debts):
        for j,v in enumerate(debts[i]): ws.cell(r,2+j,v)
    ws.cell(r,3).number_format=MONEY; ws.cell(r,4).number_format="0.0%"; ws.cell(r,5).number_format=MONEY; ws.cell(r,6).number_format=MONEY
    ws.cell(r,7,f'=IF(C{r}="","",C{r}-F{r})').number_format=MONEY; ws.cell(r,7).fill=PatternFill()
    ws.cell(r,8,f'=IF(C{r}="","",F{r}/C{r})').number_format="0%"
ws["B15"]="Total"; ws["B15"].font=F(bold=True)
for col in "CFG": ws[f"{col}15"]=f"=SUM({col}6:{col}13)"; ws[f"{col}15"].number_format=MONEY; ws[f"{col}15"].font=F(bold=True)
ws["H15"]="=IFERROR(F15/C15,0)"; ws["H15"].number_format="0%"; ws["H15"].font=F(bold=True,color=G)
from openpyxl.formatting.rule import DataBarRule
ws.conditional_formatting.add("H6:H13",DataBarRule(start_type="num",start_value=0,end_type="num",end_value=1,color="6FAF8B"))
# ---------- Savings goals
ws=sheet("Savings Goals",[22,14,14,14,12,14],"Savings Goals","Watch every goal fill up")
head(ws,5,["Goal","Target","Saved","Still needed","Progress","Target date"])
goals=[("Emergency Fund",10000,6400,"Dec 2027"),("Vacation",3000,1200,"Jul 2027"),("New Laptop",1500,950,"Sep 2027"),("Holiday Gifts",800,240,"Nov 2027")]
for i in range(8):
    r=6+i
    for col in (2,3,4,7): ws.cell(r,col).fill=fill(GL)
    if i<len(goals): g=goals[i]; ws.cell(r,2,g[0]); ws.cell(r,3,g[1]); ws.cell(r,4,g[2]); ws.cell(r,7,g[3])
    ws.cell(r,3).number_format=MONEY; ws.cell(r,4).number_format=MONEY
    ws.cell(r,5,f'=IF(C{r}="","",MAX(0,C{r}-D{r}))').number_format=MONEY
    ws.cell(r,6,f'=IF(C{r}="","",MIN(1,D{r}/C{r}))').number_format="0%"
ws.conditional_formatting.add("F6:F13",DataBarRule(start_type="num",start_value=0,end_type="num",end_value=1,color="6FAF8B"))
wb.active=wb.sheetnames.index("Dashboard")
wb.save("../out/Annual_Budget_Planner_2027.xlsx"); print("saved",NT,"transactions")
