import random
random.seed(11)
YEAR=2027; BIZ="Bright Home Services LLC"; TAX=0.25; MILE=0.70
INC_CATS=["Services","Products","Subscriptions","Other income"]
EXP_CATS=["Advertising","Car & truck","Contract labor","Insurance","Legal & professional","Office supplies","Rent","Repairs","Supplies","Software","Phone & internet","Travel","Meals (50%)","Bank & payment fees","Education","Other"]
CLIENTS=["Miller family","Oak Street Dental","Sunrise Realty","J. Patel","Greenway Offices","L. Thompson","Harbor Cafe","R. Nguyen"]
VEND={"Advertising":["Facebook Ads","Local paper"],"Car & truck":["Gas station","Auto repair"],"Insurance":["Liability insurance"],"Legal & professional":["CPA quarterly"],
 "Office supplies":["Office store"],"Supplies":["Cleaning supply co","Wholesale club"],"Software":["Scheduling app","Accounting app"],"Phone & internet":["Mobile carrier"],
 "Bank & payment fees":["Card processor"],"Meals (50%)":["Client lunch"],"Contract labor":["Helper - weekend"],"Education":["Online course"]}
def income(m):
    out=[]
    for _ in range(random.randint(14,18)):
        out.append((random.randint(1,28),random.choice(CLIENTS),random.choices(INC_CATS,[8,2,2,0.5])[0],"Invoice #"+str(1000+m*40+len(out)),round(random.choice([120,150,180,220,260,340,480])*random.uniform(.95,1.15),2),random.choice(["Bank transfer","Card","Check","Cash"])))
    return sorted(out)
def expenses(m):
    out=[]
    fixed=[("Insurance",145),("Software",39),("Phone & internet",85),("Legal & professional",120 if m%3==0 else 0)]
    for c,a in fixed:
        if a: out.append((1,VEND[c][0],c,"Monthly",a))
    for c,(n,lo,hi) in {"Supplies":(3,40,160),"Car & truck":(4,35,70),"Advertising":(2,30,90),"Bank & payment fees":(1,40,75),"Office supplies":(1,15,45),"Meals (50%)":(1,25,60),"Contract labor":(1,150,320)}.items():
        for _ in range(n): out.append((random.randint(1,28),random.choice(VEND[c]),c,"",round(random.uniform(lo,hi),2)))
    return sorted(out)
def mileage(m):
    return sorted((random.randint(1,28),random.choice(["Client job","Supply run","Estimate visit"]),random.choice(CLIENTS),round(random.uniform(6,38),1)) for _ in range(8))
