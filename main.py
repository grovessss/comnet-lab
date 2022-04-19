import db
import os
from flask import Flask, render_template, request
import json, msgpack
from beacontools import parse_packet
from beacontools.packet_types.ibeacon import IBeaconAdvertisement

run_on = '172.20.10.2' # configure gateway to send to this address

app = Flask(__name__)

@app.route("/", methods = ['POST'])
def uploader():
    data = msgpack.loads(request.get_data()) # data keys: dict_keys(['v', 'mid', 'time', 'ip', 'mac', 'devices'])
    devices = data['devices']  # devices is list of bytes
    src = data['mac']          # mac is a str(gateway mac)
    timestamp = 12345

    for device in devices:
        mac = "{:02X}{:02X}{:02X}{:02X}{:02X}{:02X}".format((device[1]), 
            (device[2]), (device[3]), (device[4]), (device[5]), (device[6]))
        rssi = device[7] - 256
        adv = parse_packet(device[8:])
        
        # devices are of various length, parse_packet only parse len(device[8:])==30?
        if type(adv) == IBeaconAdvertisement:
            db.insert(src, mac, adv.uuid, timestamp, rssi)
    return "uploaded"


@app.route("/time")
def timer():
    pass


def main() -> None:
    if not os.path.exists("tmp/"):
        os.mkdir("tmp/")
    db.init()
    app.run(run_on)

if __name__ == "__main__":
    main()

