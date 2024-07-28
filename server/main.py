from flask import Flask
from flask import request, render_template, jsonify

from decode import decodeHelper
import json

from flask import g

import pandas as pd
import sqlite3

from constants import *


app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("data.db")

    return g.db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("sql/init.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


init_db()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_latest_data():
    (eui, temp, hum, bat, timestamp) = query_db(
        """
        SELECT 
            t.device_eui,
            t.value AS latest_temperature,
            h.value AS latest_humidity,
            b.value AS latest_battery,
            t.timestamp
        FROM 
        (SELECT device_eui, value, timestamp
            FROM data
            WHERE parameter = 'temperature'
            ORDER BY timestamp DESC
            LIMIT 1) t
        LEFT JOIN 
        (SELECT device_eui, value
            FROM data
            WHERE parameter = 'humidity'
            ORDER BY timestamp DESC
            LIMIT 1) h
        ON t.device_eui = h.device_eui
        LEFT JOIN 
            (SELECT device_eui, value
            FROM data
            WHERE parameter = 'battery'
            ORDER BY timestamp DESC
            LIMIT 1) b
        ON t.device_eui = b.device_eui;""",
        one=True,
    )
    return dict(
        {"eui": eui, "temp": temp, "hum": hum, "bat": bat, "timestamp": timestamp}
    )


_LAST_RECORD_TIMESTAMP = 1721317738631
WEEK_MILLIS = 7 * 24 * 60 * 60 * 1000


def get_data_in_range(t_from, t_to):
    records = query_db(
        """
        SELECT device_eui, timestamp, parameter, value
        FROM data
        WHERE timestamp > ?
        AND timestamp < ?
        ORDER BY timestamp DESC
        """,
        (t_from, t_to),
    )

    result = dict(
        {
            "temperature": dict(
                {
                    "vals": list(),
                    "timestamps": list(),
                }
            ),
            "humidity": dict(
                {
                    "vals": list(),
                    "timestamps": list(),
                }
            ),
            "battery": dict(
                {
                    "vals": list(),
                    "timestamps": list(),
                }
            ),
        }
    )

    for r in records:
        result[r[2]]["vals"].append(r[3])
        result[r[2]]["timestamps"].append(r[1])

    return result


@app.route("/", methods=["GET"])
def home():
    latest = get_latest_data()
    return render_template(
        "home.html",
        args=(
            latest["eui"],
            latest["temp"],
            latest["hum"],
            round(latest["bat"] / 255 * 100, 1),
        ),
    )


@app.route("/api/latest", methods=["GET"])
def api_latest():
    latest = get_latest_data()
    return jsonify(latest)


@app.route("/api/week", methods=["GET"])
def api_week():
    time_start = _LAST_RECORD_TIMESTAMP - WEEK_MILLIS

    week_data = get_data_in_range(time_start, _LAST_RECORD_TIMESTAMP)

    response_struct = dict(
        {"from": time_start, "to": _LAST_RECORD_TIMESTAMP, "data": week_data}
    )
    return jsonify(response_struct)


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

    # print(db_data)
    cur = get_db().cursor()
    cur.executemany(
        "INSERT INTO data (device_eui, timestamp, parameter, value) VALUES (?, ?, ?, ?)",
        db_data,
    )
    get_db().commit()

    return ("", 204)


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop("db", None)

    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host="localhost", port=1111, debug=True)
