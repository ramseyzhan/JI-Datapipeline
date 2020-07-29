"""REST API for index page."""
from flask import session, jsonify, request
from os import path, mkdir
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


@jidp2.app.route('/api/v1/', methods=["POST"])
def get_parameters():
    data = request.get_json()
    email = data['text']
    threshold = data['number']
    
    newstock = data['newstock']



    tmp_dir = 'tmp'
    mkdir(tmp_dir)
    tmp_para = path.join(tmp_dir, 'parameters.txt')
    with open(tmp_para, 'w+') as f:
        f.write(email + '\n' + threshold)
    f.close()
    context = {
        'email': email,
        'threshold': threshold
    }
    return jsonify(**context), 201


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
