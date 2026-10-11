import random
import data as data
random.seed(11)
INC={m:data.income(m) for m in range(1,10)}; EXP={m:data.expenses(m) for m in range(1,10)}; MIL={m:data.mileage(m) for m in range(1,10)}
mi=lambda m: sum(x[3] for x in MIL[m])*data.MILE
MI=[round(sum(x[4] for x in INC[m]),2) for m in range(1,10)]
ME=[round(sum(x[4] for x in EXP[m])+mi(m),2) for m in range(1,10)]
TI,TE=sum(MI),sum(ME); NP=TI-TE
CAT={}
for m in EXP:
    for x in EXP[m]: CAT[x[2]]=CAT.get(x[2],0)+x[4]
CAT["Mileage"]=sum(mi(m) for m in MIL)
CAT=sorted(CAT.items(),key=lambda x:-x[1])
