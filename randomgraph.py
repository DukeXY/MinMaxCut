import numpy as np
import random
from scipy.optimize import linprog


def create_graph(n, prob):
    global g
    g = np.zeros((n, n))
    prob /= 2
    for i in range(0, n/2):
        g[i][i+n/2] = 1
        g[i+n/2][i] = 1
    for i in range(0, n/2):
        for j in range(0, n/2):
            if (random.uniform(0,1) < prob):
                g[i][j] = 1
                g[j][i] = 1

    for i in range(n/2, n):
        for j in range(n/2, n):
            if (random.uniform(0,1) < prob):
                g[i][j] = 1
                g[j][i] = 1

def create_LP(n):
    cnt = 0
    a = []
    b = []
    for u in range(0, n):
        for v in range(u+1, n):
            for w in range(0, n):
                if (u == v or v == w or u == w):
                    continue
                line = []
                for cnt in range(0, n*n):
                    uu = cnt / n
                    vv = cnt % n
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
    for cnt in range(0, n*n):
        uu = cnt / n
        vv = cnt % n
        if (uu == 0 and vv == n/2):
            line.append(-1)
            continue
        line.append(0)
    line.append(0)
    a.append(line)
    b.append(-1)

    line = []
    for cnt in range(0, n*n):
        uu = cnt / n
        vv = cnt % n
        if (uu == n/2 and vv == 0):
            line.append(-1)
            continue
        line.append(0)
    line.append(0)
    a.append(line)
    b.append(-1)

    for v in range(0, n):
        line = []
        for cnt in range(0, n*n):
            uu = cnt / n
            vv = cnt % n
            if (vv == v and g[uu][vv] == 1):
                line.append(1)
                continue
            line.append(0)
        line.append(-1)
        a.append(line)
        b.append(0)

    c = []
    for cnt in range(0, n*n):
        c.append(0)
    c.append(1)
    #print a
    #print b
    #print c
    res = linprog(c, A_ub=a, b_ub=b, options={"disp": True, "maxiter": 10000})
    print res

if __name__=="__main__":
    n = input("Enter your N: ")
    p = input("Enter your probability: ")
    create_graph(n, p)
    create_LP(n)