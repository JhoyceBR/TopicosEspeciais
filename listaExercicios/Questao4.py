posicao = 0
maior = 0
for i in range(15):
    n = int(input())
    
    if n > maior:
        maior = n
        posicao = i+1
        
print("%d\n%d"%(maior,posicao))
