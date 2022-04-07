import os
import sqlite3

DATABASE_PATH = ""

def create_db():
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    # currently store mac as string
    cur.execute("CREATE TABLE data (id integer primary key, src text, mac text, timestamp BIGINT, rssi integer)")
    con.commit()
    con.close()

def insert(src: str, mac: str, timestamp: int, rssi: int):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cmd = "INSERT INTO data (src, mac, timestamp, rssi) VALUES ('%s', '%s', %d, %d)" % (src, mac, timestamp, rssi)
    cur.execute(cmd)
    con.commit()
    con.close()

def init():
    global DATABASE_PATH
    i = 1
    DATABASE_PATH = os.path.join('tmp', '%d.db' % i)
    while os.path.exists(DATABASE_PATH):
        i += 1
        DATABASE_PATH = os.path.join('tmp', '%d.db' % i)
    create_db()