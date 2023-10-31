#!/usr/bin/python3
"""Add routes"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=["GET"])
def cities(state_id):
    citiesList = []
    if storage.get(State, state_id) is None:
        abort(404)
    for k, v in storage.all(City).items():
        if v.state_id == state_id:
            citiesList.append(v.to_dict())
    return jsonify(citiesList)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=["GET"])
def get_city(city_id):
    if storage.get(City, city_id) is None:
        abort(404)
    return jsonify(storage.get(City, city_id).to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    if storage.get(City, city_id) is None:
        abort(404)
    storage.delete(storage.get(City, city_id))
    storage.save()
    return {}, 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def new_city(state_id):
    data = request.get_json(force=True, silent=True)
    if storage.get(State, state_id) is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    obj = City(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["PUT"])
def update_city(city_id):
    """update city"""
    ignoredKeys = ['id', 'created_at', 'updated_at', 'state_id']
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    for key in ignoreKeys:
        if key in data.keys():
            data.pop(key)
    obj = City(**data)
    obj.save()
    return jsonify(obj.to_dict()), 200
