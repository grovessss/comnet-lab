import sqlite3
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# TABLE data (id integer primary key, src text, mac text, uuid text, timestamp BIGINT, rssi integer)

databases = ['tmp/1m.db','tmp/2m.db','tmp/3m.db','tmp/4m.db','tmp/5m.db']
gateway = 'E0E2E6700FFC'
target_uuid = '35aa7c1f-a03d-5384-b824-b1e9998fb9c8'

rssi_list = []

# l = [1,3,4,5]
# for i in l:
#     con = sqlite3.connect('tmp/%dm.db' % i)
#     cmd = 'select rssi from data where uuid = \'' + target_uuid + '\' and src = \'' + gateway + '\''
#     d = pd.read_sql_query(cmd, con).values
#     np.save('tmp/%dm_rssi.npy' % i, d)
#     con.close()

l = [1,2,3,4,5]
for i in l:
    rssi_list.append(np.load('tmp/%dm_rssi.npy' % i))

xxs = []
yys = []

for i in range(5):
    x = np.log(i+1) / np.log(10) * 10
    y = np.mean(rssi_list[i])
    # y = np.median(rssi_list[i].flatten())
    # y = stats.mode(rssi_list[i].flatten())[0]
    xxs.append(x)
    yys.append(y)

# (log 10 d) * 10 * n + A = abs(rssi)

xxs = np.array(xxs)
yys = np.array(yys)
cnt = len(xxs)

n = ((cnt * (xxs.dot(yys))) - np.sum(xxs) * np.sum(yys)) / (cnt * np.sum(xxs ** 2) - np.sum(xxs) ** 2)
A = np.mean(yys) - n * np.mean(xxs)

print("n=%.3lf, A=%.3lf\n" % (n, A))

def f(x, n, A):
    return np.log(x) / np.log(10) * 10 * n + A

xs = np.arange(0.8, 5.5, step=0.1)
ys = [f(x, n, A) for x in xs]
plt.plot(xs, ys, label="fitting curve")

# scatter 1
# xs1 = []
# ys1 = []
# for i in range(5):
#     for j in rssi_list[i].flatten():
#         xs1.append(i+1)
#         ys1.append(j)
# plt.scatter(xs1, ys1, alpha=0.05, s=8, label="data points")

# scatter 2
xs1 = []
ys1 = []
s1 = []

for i in range(5):
    yy, cnt = np.unique(rssi_list[i].flatten(), return_counts=True)
    m = np.sum(cnt)
    n_cnt = (cnt / m * 120) ** 1.5
    for j in range(len(n_cnt)):
        xs1.append(i+1)
        ys1.append(yy[j])
        s1.append(n_cnt[j])
plt.scatter(xs1, ys1, s=s1, label="data points", linewidth=0.5, alpha=0.7, ec='black')
# plt.scatter(xs1, ys1, s=s1, label="data points")

# labels and legends
plt.xlabel("Distance (m)")
plt.ylabel("RSSI")
plt.legend()
plt.savefig("calib.pdf")
plt.show()
