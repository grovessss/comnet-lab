from flask import Flask, render_template, request

import os
import sqlite3
import json

DATABASE_NAME = '1.db'

def create_db():
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()
    # currently store mac as string
    cur.execute("CREATE TABLE data (id integer primary key, src text, mac text, timestamp BIGINT, rssi integer)")
    con.commit()
    con.close()

# src: String
# mac: String
# timestamp: int
# rssi: int
def insert(src: str, mac: str, timestamp: int, rssi: int):
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()
    cmd = "INSERT INTO data (src, mac, timestamp, rssi) VALUES ('%s', '%s', %d, %d)" % (src, mac, timestamp, rssi)
    cur.execute(cmd)
    con.commit()
    con.close()


if not os.path.exists(DATABASE_NAME):
    create_db()

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Index Page</p>"

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/uploader", methods = ['POST'])
def uploader():
    f = request.files['file']
    print(f)
    f.save("1.tmp")
    data = {}
    with open("1.tmp") as f:
        data = json.loads(f.read())

    raw_beacons_data = data['raw_beacons_data']
    src = 'receiver1'
    mac = raw_beacons_data[:12]
    timestamp = 12345
    rssi = int(raw_beacons_data[56:58]) # TODO: find out whether it is hex
    insert(src, mac, timestamp, rssi)

    return "uploaded"
