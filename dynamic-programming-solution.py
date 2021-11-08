import sys
import math
import numpy as np
import matplotlib.pyplot as plt

granularity = 0.01
sys.setrecursionlimit(15000)


class Curve:
    def __init__(self, x, y, k, mkt):
        self.x = x
        self.y = y
        self.k = k
        self.mkt = mkt
        self.a = x-(y/mkt)
        self.w = k*mkt/y**2
        self.next = []

    def get_y(self, x):
        return self.k/self.w/(x-self.a)

    def print(self):
        print("w is: ", self.w, "a is: ", self.a)

    def plot(self, xf, color):
        x = np.linspace(self.x, xf, 1000)
        y = self.k/self.w/(x-self.a)
        plt.plot(x, y, color)
        plt.grid()

    def tangent(self, xf):
        return (self.y-self.mkt*(xf-self.x))


def OPT(curve, xf, n):
    class Struct:
        def __init__(self, x, y, prev):
            self.x = x
            self.y = y
            self.prev = prev
    set = {}
    count = 1
    while(len(set.keys()) < n):
        temp = {}
        u = curve.x
        if count == 1:
            while(u <= xf):
                pac = Struct(u, curve.y-curve.get_y(u), None)
                temp[u] = pac
                u += granularity
        else:
            while(u <= xf):
                storage = []
                for i in set[count-1]:
                    prev = Curve(i, curve.y-set[count - 1][i].y, curve.k, curve.mkt)
                    storage.append((curve.y-prev.get_y(u), i))
                index = 0
                for i in range(len(storage)):
                    if storage[index][0] >= storage[i][0]:
                        pass
                    else:
                        index = i
                pac = Struct(u,storage[index][0],set[count-1][storage[index][1]])
                temp[u] = pac
                u += granularity
        set[count] = temp
        count += 1
    ptr = set[n][curve.x]
    for i in set[n]:
        if ptr.y >= set[n][i].y:
            pass
        else:
            ptr = set[n][i]
    yf=ptr.y
    policy=[]
    while (ptr != None):
        policy.insert(0,ptr.x)
        ptr = ptr.prev
    return curve.y-yf, policy

def exhaustive(curve, xf, storage, count, params):
    curve.plot(xf, "g")
    storage.append(curve.y)
    count += 1
    if params["policy"] == "greedy":
        intercept = (math.sqrt(xf**2-2*curve.a*xf+3*curve.k /
                     curve.mkt/curve.w+curve.a**2)+xf+2*curve.a)/3
    elif params["policy"] == "arithmetic":
        intercept = curve.x+params["params"]
    elif params["policy"] == "geometric":
        intercept = curve.x+count**params["params"]
    elif params["policy"] == "exponential":
        intercept = curve.x+2**params["params"]
    if((intercept) >= xf):
        curve.next = None
        plt.figure()
        x = list(range(0, len(storage)))
        plt.plot(x, storage, 'g')
        return count, curve.get_y(xf)
    else:
        curve.next.append(Curve(intercept, curve.get_y(intercept), k, mkt))
        return exhaustive(curve.next[0], xf, storage, count, params)


if __name__ == "__main__":
    x0 = 100
    y0 = 100
    xf = 110
    mkt = 5
    k = 10000
    trade_limit = 5
    params = [
        {"policy": "greedy", "params": None},
        {"policy": "arithmetic", "params": granularity},
        {"policy": "geometric", "params": 0.0001},
        {"policy": "exponential", "params": 0.0001},
    ]
    curve = Curve(x0, y0, k, mkt)
    print("Optimal yf:", curve.tangent(xf))

    print("Optimal yf and its corresponding trading policy under", trade_limit,
          "trades:", OPT(curve, xf, trade_limit))

    plt.figure()
    print("yf with", int((xf-x0)/granularity), "trades:",
          exhaustive(curve, xf, [], 0, params[1])[1])
    plt.grid()
    plt.show()
