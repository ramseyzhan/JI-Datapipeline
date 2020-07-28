"""REST API for index page."""
from flask import session, jsonify, request
import jidp2
from jidp2.api.helper import format_to_json


@jidp2.app.route('/api/v1/', methods=["GET"])
def get_services():
    """Get all anomalies."""
    to_json = {
        "anomaly": "/api/v1/m/",
        "url": "/api/v1/"
    }
    # we need ** in the beginning of the jsonify function
    return jsonify(**to_json)


@jidp2.app.route('/api/v1/m/', methods=["GET"])
def get_anomaly():
    """Get all the anomalies."""
    connection = jidp2.model.get_db()
    cur = connection.execute(
        "SELECT * FROM anomaly "
        "ORDER BY anomalyid "
    )
    anomalies = cur.fetchall()
    results = []
    to_json = format_to_json(anomalies, results)
    return jsonify(**to_json)
