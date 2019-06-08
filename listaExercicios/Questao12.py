def valorPagamento(VPrestacao, DAtraso):
    if(DAtraso == 0):
        return(VPrestacao)
    else:
        NPreco = VPrestacao+(VPrestacao*3/100) + (DAtraso*0.1/100)
        return(NPreco)

qtd = 0
totalP = 0
while(True):
    VPrestacao = int(input())
    if(VPrestacao==0):
        print(qtd)
        print(totalP)
        break
    DAtraso = int(input())
    qtd += 1
    totalP += valorPagamento(VPrestacao, DAtraso)
    print(valorPagamento(VPrestacao, DAtraso))
    
    
