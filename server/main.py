from flask import Flask
from flask import request, render_template, jsonify

from decode import decodeHelper
import json

from flask import g

import pandas as pd
import sqlite3

from constants import *

from db import *
from utils import *
import json


# Initialize the app
app = Flask(__name__)

# Connect to db
init_db(app)


@app.route("/", methods=["GET"])
def home():
    return "<h3>Welcome to Milesight logger server</h3>"
    # latest = get_latest_data()
    # return render_template(
    #     "home.html",
    #     args=(
    #         latest["eui"],
    #         latest["temp"],
    #         latest["hum"],
    #         round(latest["bat"] / 255 * 100, 1),
    #     ),
    # )


@app.route("/api/devices", methods=["GET"])
def api_devices():
    devices = query_db("SELECT DISTINCT device_eui FROM data")
    device_euis = list(map(lambda d: str(d[0]), devices))

    response = ResponseMessage(ResponseStatus.OK, data=device_euis)

    return response.jsonify()


@app.route("/api/latest", methods=["GET"])
def api_latest():
    device = request.args.get("device")
    if device == None:
        response = ResponseMessage(
            ResponseStatus.ERROR, err_message="Device not specified"
        )
        return response.jsonify()

    try:
        latest = get_latest_data(device)
        response = ResponseMessage(ResponseStatus.OK, data=latest)
        return response.jsonify()
    except:
        return ResponseMessage(
            ResponseStatus.ERROR, err_message="Failed to fetch data from db"
        ).jsonify()


_LAST_RECORD_TIMESTAMP = 1721317738631 # Replace for current time 

@app.route("/api/week", methods=["GET"])
def api_week():
    device = request.args.get("device")
    if device == None:
        response = ResponseMessage(
            ResponseStatus.ERROR, err_message="Device not specified"
        )
        return response.jsonify()

    time_start = _LAST_RECORD_TIMESTAMP - WEEK_MILLIS

    week_data = get_data_in_range(device, time_start, _LAST_RECORD_TIMESTAMP)

    response_struct = dict(
        {
            "device_eui": device,
            "from": time_start,
            "to": _LAST_RECORD_TIMESTAMP,
            "data": week_data,
        }
    )
    return ResponseMessage(ResponseStatus.OK, data=response_struct).jsonify()


# Handle incoming data
@app.route("/", methods=["POST"])
def data():
    data = request.get_json()
    data_obj = json.loads(data["data"])

    dev_eui = data_obj["EUI"]
    msg_ts = data_obj["ts"]
    dev_data_enc = data_obj["data"]
    dev_bat = int(data_obj["bat"])

    dev_decoded_data = decodeHelper(dev_data_enc)

    db_data = []

    for key in [TEMPERATURE_KEY, HUMIDITY_KEY]:
        if key in dev_decoded_data:
            new_record = (dev_eui, msg_ts, key, dev_decoded_data[key])
            db_data.append(new_record)

    db_data.append((dev_eui, msg_ts, BATTERY_KEY, dev_bat))

    cur = get_db().cursor()
    cur.executemany(
        "INSERT INTO data (device_eui, timestamp, parameter, value) VALUES (?, ?, ?, ?)",
        db_data,
    )
    get_db().commit()

    return ("", 204)


# Handle shutdown
@app.teardown_appcontext
def teardown_db(_):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# Run the app
if __name__ == "__main__":
    app.run(host="localhost", port=1111, debug=True)
