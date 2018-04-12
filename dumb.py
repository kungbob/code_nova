array=[];
n=int(input());
max=0
winner = 1;
s = 0
t = 0;
for i in range(0,n):
    x,y=input().split();
    s+=int(x)
    t+=int(y)
    k=s-t
    if(max<k):
        winner=1
        max=k;
    if(k<0):
        k*=-1
        if(max<k):
            winner=2
            max=k;
print (winner, max);