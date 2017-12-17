import random
import numpy as np
from scipy.optimize import linprog
from cvxpy import *
import time

global filename

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
    a = findOptimum(n, g)
    b = create_LP(n, g)
    if a == 0:
        return
    with open(filename, 'a') as f:
        f.write(str(a) + " " + str(b) + " " + str(float(a)/b)+ "\n")
    f.close()
    #print float(a)/b
    if (b == 0):
        return -1
    return float(a)/b

def create_graph(n, prob):
    global g
    g = np.zeros((n, n))
    prob /= 2
    for i in range(0, n):
        for j in range(0, n):
            if (random.uniform(0,1) < prob):
                g[i][j] = 1
                g[j][i] = 1
    a = findOptimum(n, g)

    start = time.time()
    b = create_LP(n, g)
    end = time.time()
    timenew = end - start
    #print "New " + str(end - start)

    #start = time.time()
    #c = create_LP2(n, g)
    #end = time.time()
    timeold = end - start
    #print "Old " + str(end - start)
    if (b == 0):
        return -1
    #if (c == 0):
    #    return -1
    #print a, b, c
    with open(filename, 'a') as f:
        f.write(str(a) + " " + str(b) + " " + str(float(a)/b)+ "\n")
    f.close()
    #print float(a)/b
    return float(a)/b


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
    #print minx,
    return minx

def create_LP(n, g):
    x = Variable(n*(n-1)/2+1)
    constraints = []

    for u in range(0, n):
        for v in range(u+1, n):
            for w in range(v+1, n):
                aa = transfer(u ,v)
                bb = transfer(v, w)
                cc = transfer(u, w)

                constraints.append(x[aa] + x[bb] >= x[cc])
                constraints.append(x[aa] + x[cc] >= x[bb])
                constraints.append(x[bb] + x[cc] >= x[aa])
    constraints.append(x[transfer(0, n-1)] >= 1)
    for v in range(0, n):
        indices = []
        for u in range(0, n):
            if (u == v):
                continue
            if g[u][v]==1:
                if (u < v):
                    indices.append(transfer(u, v))
                else:
                    indices.append(transfer(v, u))

        constraints.append(sum([x[i] for i in indices]) <= x[n*(n-1)/2])
    constraints.append(x >= 0)

    obj = Minimize(x[n*(n-1)/2])

    prob = Problem(obj, constraints)
    prob.solve()  # Returns the optimal value.
    return prob.value


def create_LP2(n, g):
    cnt = 0
    a = []
    b = []
    for u in range(0, n):
        for v in range(u+1, n):
            for w in range(v+1, n):
                line1 = []
                line2 = []
                line3 = []
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
                        line1.append(-1)
                        line2.append(-1)
                        line3.append(1)
                        continue
                    if (uu == v and vv == w):
                        line1.append(-1)
                        line2.append(1)
                        line3.append(-1)
                        continue
                    if (uu == u and vv == w):
                        line1.append(1)
                        line2.append(-1)
                        line3.append(-1)
                        continue
                    line1.append(0)
                    line2.append(0)
                    line3.append(0)
                line1.append(0)
                line2.append(0)
                line3.append(0)
                a.append(line1)
                a.append(line2)
                a.append(line3)
                b.append(0)
                b.append(0)
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
    res = linprog(c, A_ub=a, b_ub=b, options={"disp": False, "maxiter": 10000})
    #print res["fun"],
    if res["fun"] < 1.0/n:
        with open("log", "a") as f:
            f.write(str(res))
        f.close()
        return 0
    return res["fun"]

def transfer(u,v):
    s = 0
    for i in range(n - u, n):
        s = s + i
    aa = s + v - u - 1
    return aa

if  __name__=="__main__":
    global n, filename
    filename = "test"
    n = 10
    iter = 100
    prob = [1.0 / 2.0, 2.0 / 3.0, 3.0 / 4.0, 4.0 / 5.0]
    for n in range(11, 22):
        filename = "workfile" + str(n)
        for p in prob:
            mean = 0
            min = n
            max = 0
            res = []
            for i in range(iter):
                ans = create_graph(n, p)
                if (ans == -1):
                    continue
                res.append(ans)
                mean += ans
                if (ans < min):
                    min = ans
                if (ans > max):
                    max = ans
            with open(filename, "a") as f:
                f.write("For n and d " + str(n) + " " + str(p) + "\n")
                f.write("Mean: " + str(mean / iter) + "\n")
                f.write("Min: " + str(min) + "\n")
                f.write("Max: " + str(max) + "\n")
                variance = np.var(np.array(res))
                f.write("Variance: " + str(variance) + "\n")
            f.close()
            print "Finish Case with " + str(n) + " " + str(p) + "\n"

