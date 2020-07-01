"""REST API for index page."""
from flask import session, jsonify, request
import jidp2


@jidp2.app.route('/api/v1/', methods=["GET"])
def get_anomaly():
    """Update warning data."""
    connection = jidp2.model.get_db()
    cur = connection.execute(
        "SELECT * FROM anomaly "
    )
    anomaly = cur.fetchall()
    results = []
    for data_pt in anomaly:
        results.append({
            "date": data_pt["dateuse"],
            "value": data_pt["consumption"],
            "detect_time": data_pt["created"]
        })
    to_json = {
        "results": results,
        "url": "/api/v1/"
    }
    # we need ** in the beginning of the jsonify function
    return jsonify(**to_json)


@jidp2.app.route('/api/v1/', methods=["POST"])
def post_anomaly():
    data = request.get_json()
    date_consuming = data['date_consuming']
    consumption = int(data['consumption'])
    connection = jidp2.model.get_db()
    connection.execute(
        "INSERT INTO anomaly(dateuse, consumption) "
        "VALUES (?, ?)",
        (date_consuming, consumption,)
    )
    context = {
        'date_consuming': date_consuming,
        'consumption': consumption
    }
    return jsonify(**context), 201
