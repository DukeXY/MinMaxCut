import random
import numpy as np
from scipy.optimize import linprog

def createConstantDegreeGraph(n, degree):
    g = np.zeros((n, n))

    for i in range(0, n):
        cnt = 0
        v = set()
        v.add(i)
        for j in range(0, n):
            if (i==j):
                continue
            cnt += g[i][j]
            if (g[i][j]==1):
                v.add(j)
        while (cnt < degree):
            r = int(random.uniform(0, n))
            if (not r in v):
                v.add(r)
                cnt += 1
                g[i][r] = 1
                g[r][i] = 1
            #print g
    #print g
    findOptimum(n, g)
    create_LP(n, g)

def findOptimum(n, g):
    b = np.zeros((n,))
    maxx = 0
    minx = n
    while (b[0] == 0):
        left = set()
        right = set()
        left.add(0)
        right.add(n-1)
        for i in range(1, n-1):
            #print b[i],
            if (b[i] == 0):
                left.add(i)
            else:
                right.add(i)
        #print
        maxx = 0
        for u in left:
            cnt = 0
            for v in right:
                cnt += g[u][v]
            if  (cnt > maxx):
                maxx = cnt

        for u in right:
            cnt = 0
            for v in left:
                cnt += g[u][v]
            if  (cnt > maxx):
                maxx = cnt
        p = n - 2
        while (b[p] == 1):
            b[p] = 0
            p -= 1
        b[p] += 1
        if (maxx < minx):
            #print maxx
            minx = maxx
    print minx,

def create_LP(n, g):
    cnt = 0
    a = []
    b = []
    for u in range(0, n):
        for v in range(u+1, n):
            for w in range(v+1, n):
                line = []
                modul = n
                uu = 0
                vv = 0
                for cnt in range(0, n*(n-1)/2):
                    vv += 1
                    if (vv >= modul):
                        uu += 1
                        vv = uu + 1
                    #print uu, vv
                    if (uu == u and vv == v):
                        line.append(-1)
                        continue
                    if (uu == v and vv == w):
                        line.append(-1)
                        continue
                    if (uu == u and vv == w):
                        line.append(1)
                        continue
                    line.append(0)
                line.append(0)
                a.append(line)
                b.append(0)

    line = []
    uu = 0
    vv = 0
    for cnt in range(0, n*(n-1) /2):
        vv += 1
        if (vv >= modul):
            uu += 1
            vv = uu + 1
        if (uu == 0 and vv == n-1):
            line.append(-1)
            continue
        line.append(0)
    line.append(0)
    a.append(line)
    b.append(-1)

    for v in range(0, n):
        line = []
        uu = 0
        vv = 0
        for cnt in range(0, n*(n-1)/2):
            vv += 1
            if (vv >= modul):
                uu += 1
                vv = uu + 1
            if ((vv == v or uu == v)  and g[uu][vv] == 1):
                line.append(1)
                continue
            line.append(0)
        line.append(-1)
        a.append(line)
        b.append(0)
    #print a
    c = []
    for cnt in range(0, n*(n-1)/2):
        c.append(0)
    c.append(1)
    #print a.__sizeof__()
    #print b.__sizeof__()
    #print c.__sizeof__()
    res = linprog(c, A_ub=a, b_ub=b, options={"disp": False, "maxiter": 10000})
    print res["fun"]

if  __name__=="__main__":
    n = input("Enter Number of vertices: ")
    degree = input("Enter Degrees: ")
    iter = input("Enter Iterations: ")
    for i in range(iter):
        createConstantDegreeGraph(n, degree)


