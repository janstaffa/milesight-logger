import sqlite3
from flask import g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("data.db")

    return g.db


def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource("sql/init.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# Helper functions
def get_latest_data(device_eui: str):
    result = query_db(
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
            WHERE device_eui = ?
            AND parameter = 'temperature'
            ORDER BY timestamp DESC
            LIMIT 1) t
        LEFT JOIN 
        (SELECT device_eui, value
            FROM data
            WHERE device_eui = ?
            AND parameter = 'humidity'
            ORDER BY timestamp DESC
            LIMIT 1) h
        ON t.device_eui = h.device_eui
        LEFT JOIN 
            (SELECT device_eui, value
            FROM data
            WHERE device_eui = ?
            AND parameter = 'battery'
            ORDER BY timestamp DESC
            LIMIT 1) b
        ON t.device_eui = b.device_eui;""",
        args=(device_eui, device_eui, device_eui),
        one=True,
    )
    if result == None:
        raise

    (eui, temp, hum, bat, timestamp) = result

    return dict(
        {"eui": eui, "temp": temp, "hum": hum, "bat": bat, "timestamp": timestamp}
    )




def get_data_in_range(device, t_from, t_to):
    records = query_db(
        """
        SELECT device_eui, timestamp, parameter, value
        FROM data
        WHERE device_eui = ?
        AND timestamp > ?
        AND timestamp < ?
        ORDER BY timestamp DESC
        """,
        (device, t_from, t_to),
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
