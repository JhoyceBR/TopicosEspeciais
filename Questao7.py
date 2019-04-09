def fatorial(n): 
   if n<=1: 
      return 1
   else: 
      return n*fatorial(n-1)
    
N = int(input())
fatorial(N)
print ("{}".format(fatorial(N)))
