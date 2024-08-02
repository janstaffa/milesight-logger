from flask import Flask
from flask import request

from decode import decodeHelper
import json

from flask import g


from constants import *

from db import *
from utils import *
import json

import datetime
from dotenv import dotenv_values


config = dotenv_values(".env")

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


# _LAST_RECORD_TIMESTAMP = 1721317738631


@app.route("/api/week", methods=["GET"])
def api_week():
    device = request.args.get("device")
    if device == None:
        response = ResponseMessage(
            ResponseStatus.ERROR, err_message="Device not specified"
        )
        return response.jsonify()

    # now = _LAST_RECORD_TIMESTAMP # Replace for current time

    now = round(time.time() * 1000)
    time_start = now - WEEK_MILLIS

    week_data = get_data_in_range(device, time_start, now)

    response_struct = dict(
        {
            "device_eui": device,
            "from": time_start,
            "to": now,
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
    now = datetime.datetime.now()

    print(f"{now} > logged data for device: {dev_eui}")

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


DEBUG = False
# Run the app
if __name__ == "__main__":
    # Disable logging of Flask messages
    if DEBUG == False:
        import logging

        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)

    app.run(host=config["SERVER_IP"], port=1111, debug=DEBUG)
