#!/usr/bin/python3
"""Add routes"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states',strict_slashes=False,
                 methods=["GET"])
def states():
    statesList = []
    for k, v in storage.all(State).items():
        statesList.append(v.to_dict())
    return jsonify(statesList)


@app_views.route('/states/<state_id>',strict_slashes=False,
                 methods=["GET"])
def get_state(state_id):
    if storage.get(State, state_id) == None:
        abort(404)
    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route('/states/<state_id>',strict_slashes=False,
                 methods=['DELETE'])
def delete(state_id):
    if storage.get(State, state_id) == None:
        abort(404)
    storage.delete(storage.get(State, state_id))
    storage.save()
    return {}, 200


@app_views.route('/states',strict_slashes=False,
                 methods=['POST'])
def new():
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    obj = State(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["PUT"])
def update(state_id):
    """update state"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
