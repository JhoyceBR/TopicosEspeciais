som = 0
cont = 0
i = 0
while (i<6):
    n = float(input())
    if n>0:
        som+=n
        cont+=1
    i+=1
        
print("%d valores positivos" %cont)
print("%.1f" %(som/cont))
