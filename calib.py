import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TABLE data (id integer primary key, src text, mac text, uuid text, timestamp BIGINT, rssi integer)

databases = ['tmp/1m.db','tmp/2m.db','tmp/3m.db','tmp/4m.db','tmp/5m.db']
gateway = 'E0E2E6700FFC'
target_uuid = '35aa7c1f-a03d-5384-b824-b1e9998fb9c8'

rssi_list = []

for database in databases:
    con = sqlite3.connect(database)
    cmd = 'select rssi from data where uuid = \'' + target_uuid + '\' and src = \'' + gateway + '\''
    rssi_list.append(pd.read_sql_query(cmd, con).values)
    con.close()

rssi = [np.mean(i) for i in rssi_list]
