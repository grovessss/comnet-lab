import numpy as np
import math
import matplotlib.pyplot as plt

def plot(p1, p2, p3, r1, r2, r3, c):
    plt.figure(figsize=(8,8))
    if c is None:
        c = localize(p1,p2,p3,r1,r2,r3)
    plt.scatter(*list(zip(*[p1, p2, p3, c])))
    plt.gcf().gca().add_artist(plt.Circle(p1, r1, fill=False))
    plt.gcf().gca().add_artist(plt.Circle(p2, r2, fill=False))
    plt.gcf().gca().add_artist(plt.Circle(p3, r3, fill=False))
    xmin = min(p1[0]-r1, p2[0]-r2, p3[0]-r3)
    xmax = max(p1[0]+r1, p2[0]+r2, p3[0]+r3)
    ymin = min(p1[1]-r1, p2[1]-r2, p3[1]-r3)
    ymax = max(p1[1]+r1, p2[1]+r2, p3[1]+r3)
    d = max(xmax-xmin,ymax-ymin)
    plt.xlim(xmin-1,xmin+d+1)
    plt.ylim(ymin-1,ymin+d+1)
    plt.show()


def get_inter(p1, p2, r1, r2, p3, r3):
    d = np.linalg.norm(p1-p2)
    if d > r1+r2:
        return r2/(r1+r2)*p1+r1/(r1+r2)*p2
    a = (r1**2-r2**2+d**2)/(2*d)
    h = math.sqrt(r1**2-a**2)
    c0 = p1 + a/d * (p2-p1)
    delta = h/d * np.array([p2[1]-p1[1],p1[0]-p2[0]])
    c1 = c0 - delta
    c2 = c0 + delta
    if abs(np.linalg.norm(c1-p3)-r3) < abs(np.linalg.norm(c2-p3)-r3):
        return c1
    else:
        return c2

def localize(p1, p2, p3, r1, r2, r3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    x1 = get_inter(p1, p2, r1, r2, p3, r3)
    x2 = get_inter(p2, p3, r2, r3, p1, r1)
    x3 = get_inter(p3, p1, r3, r1, p2, r2)
    # plt.scatter(*list(zip(*[x1, x2, x3])))
    return ((x1+x2+x3)/3).tolist()


if __name__ == '__main__':
    p1 = [0,0]
    r1 = 2
    p2 = [2.5,0]
    r2 = 2
    p3 = [0,3]
    r3 = 2.5
    plot(p1,p2,p3,r1,r2,r3,None)
