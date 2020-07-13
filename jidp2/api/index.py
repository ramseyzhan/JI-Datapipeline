"""REST API for index page."""
from flask import session, jsonify, request
import jidp2


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
def increase_anomaly():
    """Get one more anomaly each time."""
    size = request.args.get("size", default=1, type=int)
    page = request.args.get("page", default=0, type=int)
    # ERROR HANDLING, if page or size is negative we return 400 status
    if size < 0 or page < 0:
        to_json_error = {
            "message": "Bad Request",
            "status_code": "400"
        }
        return jsonify(**to_json_error)
    connection = jidp2.model.get_db()
    cur = connection.execute(
        "SELECT * FROM anomaly "
        "ORDER BY anomalyid "
        "LIMIT ? OFFSET ?", (size + 1, size * page,)
    )
    anomalies = cur.fetchall()
    num_anomalies = len(anomalies)
    results = []
    to_json = format_to_json(num_anomalies, page, anomalies, results, size)
    return jsonify(**to_json)


def format_to_json(num_anomalies, page, anomalies, results, size):
    to_json = {}
    need_next_page = False
    for anomaly in anomalies:
        anomaly_id = anomaly["anomalyid"]
        results.append({
            "anomalyid": int(anomaly["anomalyid"]),
            "url": '/api/v1/m/' + str(anomaly_id) + '/'
        })
    if num_anomalies >= size + 1:
        need_next_page = True
        results.pop()
    else:
        need_next_page = False
    to_json["results"] = results
    to_json["url"] = '/api/v1/m/'
    if not need_next_page:
        next_str = ''
    else:
        next_str = '/api/v1/m/?size=' + str(size) + \
                   '&' + 'page=' + str(page + 1)
    to_json["next"] = next_str
    return to_json
