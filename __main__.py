import numpy as np
from scipy.optimize import linprog

def create_cycle(n):
    g = np.zeros((n,n))
    for i in range(n-1):
        g[i][i+1] = 1
        g[i+1][i] = 1
    g[n-1][0]=1
    g[0][n-1] = 1
    create_all_cut(n, g)

def create_all_cut(n, g):
    m = n-1
    a = np.zeros(m)
    all_cut = list()
    map = dict()
    for i in range(1, n/2):
        map[i]=i
    for i in range(n/2+1,n):
        map[i-1]=i
    while (a[0] == 0):
        cur = set()
        cur.add(0)
        for i in range(1, m):
            if (a[i] != 0):
                cur.add(map[i])
        all_cut.append(cur)
        temp = m-1
        while (a[temp]==1):
            a[temp] = 0
            temp-=1
        a[temp]+=1
    create_LP(n, g, all_cut)

def create_LP(n, g, all_cut):
    mat = []
    print all_cut
    for i in range(n):
        coeff = []
        for cut in all_cut:
            sum = 0
            left = i - 1
            right = i + 1
            if (right >= n):
                right = 0
            if (left < 0):
                left = n - 1
            if (i in cut):
                if (not left in cut):
                    sum = sum + 1.0
                if (not right in cut):
                    sum = sum + 1.0
            else:
                for v in cut:
                    sum+=g[i][v]
            coeff.append(sum)
        coeff.append(-1.0)
        mat.append(coeff)
    coeff = []
    for i in range(len(all_cut)):
        coeff.append(1.0)
    coeff.append(0.0)
    mat.append(coeff)

    coeff = []
    for i in range(len(all_cut)):
        coeff.append(-1.0)
    coeff.append(0.0)
    mat.append(coeff)


    b=[]
    for i in range(n):
        b.append(0)
    b.append(1)
    b.append(-1)

    c=[]
    for i in range(len(all_cut)):
        c.append(0)
    c.append(1)
    print len(mat)
    print mat, b, c
    solveLP(mat,b,c, all_cut, n)

def solveLP(mat,b,c, all_cut, n):
    bounds = [];
    for i in range(pow(2,n-2)+1):
        if (i==0):
            bounds.append( (2/n, 2/n) )
        else:
            bounds.append( (None, None))
        #bounds.append(bound)
    res=linprog(c, A_ub=mat, b_ub=b, bounds=tuple(bounds), options={"disp": True})
    for i in range(len(all_cut)):
        if (res["x"][i]!=0):
            print all_cut[i], res["x"][i];
    print res["fun"]





