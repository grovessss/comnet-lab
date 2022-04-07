import db

import os
from flask import Flask, render_template, request
import json

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
    tmp_filename = os.path.join('tmp', '1.tmp')
    f.save(tmp_filename)

    data = {}
    with open(tmp_filename) as f:
        data = json.loads(f.read())
    raw_beacons_data = data['raw_beacons_data']

    src = 'receiver1'
    mac = raw_beacons_data[:12]
    timestamp = 12345
    rssi = int(raw_beacons_data[56:58]) # TODO: find out whether it is hex
    db.insert(src, mac, timestamp, rssi)

    return "uploaded"

@app.route("/time")
def timer():
    pass


def main() -> None:
    if not os.path.exists("tmp/"):
        os.mkdir("tmp/")
    db.init()
    app.run()

if __name__ == "__main__":
    main()