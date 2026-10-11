# Données d'exemple partagées par le tableur et les images (une seule source).
import random
random.seed(7)
YEAR = 2027
INCOME = [("Paycheck - Main job", 3200.0), ("Paycheck - Partner", 2450.0), ("Side hustle", 380.0)]
# (catégorie, groupe, budget mensuel)
CATS = [
 ("Rent / Mortgage","Bills",1650),("Utilities","Bills",210),("Phone & Internet","Bills",120),
 ("Insurance","Bills",185),("Subscriptions","Bills",48),
 ("Groceries","Living",620),("Dining Out","Living",180),("Transportation","Living",260),
 ("Health","Living",90),("Personal Care","Living",70),("Shopping","Living",150),
 ("Entertainment","Living",110),("Gifts","Living",60),
 ("Emergency Fund","Savings",400),("Vacation Fund","Savings",200),("Retirement","Savings",350),
 ("Credit Card","Debt",300),("Car Loan","Debt",285),
]
MERCH = {"Groceries":["Fresh Market","Green Grocer","Corner Store"],"Dining Out":["Pizza night","Coffee shop","Taco place"],
 "Transportation":["Gas station","Bus pass","Parking"],"Shopping":["Clothing store","Home goods"],"Entertainment":["Movie tickets","Concert"],
 "Health":["Pharmacy"],"Personal Care":["Haircut"],"Gifts":["Birthday gift"]}
def transactions(month):
    """Transactions réalistes pour un mois (dépenses)."""
    out=[]
    fixed={"Rent / Mortgage":1650,"Utilities":196.4,"Phone & Internet":120,"Insurance":185,"Subscriptions":45.97,
           "Emergency Fund":400,"Vacation Fund":200,"Retirement":350,"Credit Card":300,"Car Loan":285}
    day=1
    for c,a in fixed.items():
        out.append((day, c, c if c not in ("Utilities",) else "Electric & water", round(a*random.uniform(0.97,1.03),2) if c=="Utilities" else a)); day=min(28,day+2)
    var={"Groceries":(5,95,140),"Dining Out":(4,22,48),"Transportation":(4,38,70),"Shopping":(2,35,80),"Entertainment":(2,25,55),
         "Health":(1,25,60),"Personal Care":(1,35,45),"Gifts":(1,30,55)}
    for c,(n,lo,hi) in var.items():
        for _ in range(n):
            out.append((random.randint(1,28), c, random.choice(MERCH[c]), round(random.uniform(lo,hi)*(1+0.04*(month%3)),2)))
    return sorted(out)
