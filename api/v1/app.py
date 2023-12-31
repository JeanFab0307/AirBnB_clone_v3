#!/usr/bin/python3
"""Flask blueprint usage"""

from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close(ctx):
    storage.close()


@app.errorhandler(404)
def not_found(err):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')\
        if getenv('HBNB_API_HOST') is not None else '0,0,0,0'
    HBNB_API_PORT = getenv('HBNB_API_PORT')\
        if getenv('HBNB_API_PORT') is not None else '5000'
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
