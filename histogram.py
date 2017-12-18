import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def process(n, p):
    with open("log") as f:
        iter = (n-6) * 4 + p
        for r in range(iter):
            line = f.readline();
            x = []
            for i in range(100):
                line = f.readline();
                data = line.split(" ");
                x.append(data[2])
        num_bins = 8
        n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
        plt.show()

if __name__=="__main__":
    n = input("Which N you want? ")
    p = input("Which P you want? ")
    process(n, p)