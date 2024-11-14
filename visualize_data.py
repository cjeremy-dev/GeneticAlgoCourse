from matplotlib import pyplot as plt
import math
def f(x):
    return  math.sin(math.cos(math.tan(x)))
a=0.0001
C=[]
b=2
eps = 0.0000001
while(abs(b-a)>eps):
    c = (a+b)/2
    if(f(a)*f(c)<0):
        b=c
    else:
        a=c
    C.append(c)
# X = [x/100+1 for x in range(1000)]
# Y = [f(x) for x in X]
# plt.plot(X,Y, 'r')
# plt.show()
plt.plot(C,'r')
plt.plot([c]*len(C),'b--')
plt.show()