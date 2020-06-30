"""REST API for index page."""
from flask import session, jsonify, request
import jidp2


@jidp2.app.route('/api/v1/', methods=["GET"])
def get_services():
    """Get all posts."""
    to_json = {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }
    # we need ** in the beginning of the jsonify function
    return jsonify(**to_json)