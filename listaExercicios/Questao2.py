y = 0
i = 0
while i<6:
    n = float(input())
    i +=1
    if n>0:
        y +=1
    if n==0:
        y = y+0
print("%d valores positivos" %(y))
