#!/usr/bin/python3
"""Add routes"""


from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False, methods=["GET"])
def status():
    return jsonify({'status': 'OK'})