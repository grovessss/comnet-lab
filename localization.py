import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geometry

# TABLE data (id integer primary key, src text, mac text, uuid text, timestamp BIGINT, rssi integer)

no = 1  # which position

database = 'tmp/pos%d.db' % no
gateways = ['E0E2E6701830', 'E0E2E6700FFC', 'E0E2E670175C']
target_uuid = '35aa7c1f-a03d-5384-b824-b1e9998fb9c8'

gateway_coord = np.array([[0, 0], [2.5, 0], [0, 3]])
target_coords = np.array([[1, 1.1], [0.7, 0.1], [2.5, 2]])
target_coord = target_coords[no-1]

n_calib = 2.001
A_calib = 51.345

# read in RSSIs

con = sqlite3.connect(database)
rssi_list = []

for gateway in gateways:
    cmd = 'select rssi from data where uuid = \'' + target_uuid + '\' and src = \'' + gateway + '\''
    rssi_list.append(pd.read_sql_query(cmd, con).values)

con.close()

# localization

def rssi2dist(rssi,n=n_calib,A=A_calib):
    return 10**((abs(rssi) - A) / (10 * n))

n_rssi = [len(i) for i in rssi_list]

error = []
for j in range(200,np.min(n_rssi),200):
    rssi = np.array([np.mean(i[:j]) for i in rssi_list])
    dist = rssi2dist(rssi)
    x, y = geometry.localize(gateway_coord[0],gateway_coord[1],gateway_coord[2],*dist)
    error.append(np.linalg.norm(np.array([x,y])-target_coord))

rssi = np.array([np.mean(i) for i in rssi_list])
dist = rssi2dist(rssi)
x, y = geometry.localize(gateway_coord[0],gateway_coord[1],gateway_coord[2],*dist)
error_single = np.linalg.norm(np.array([x,y])-target_coord)
print(error_single)

geometry.plot(gateway_coord[0],gateway_coord[1],gateway_coord[2],*dist)
plt.scatter(target_coord[0], target_coord[1], c='green')
plt.savefig('pos%d.png' % no)
plt.show()
