#!/usr/bin/python3
"""Add routes"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=["GET"])
def places(city_id):
    placesList = []
    if storage.get(City, city_id) is None:
        abort(404)
    for k, v in storage.all(Place).items():
        if v.city_id == city_id:
            placesList.append(v.to_dict())
    return jsonify(placesList)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=["GET"])
def get_place(place_id):
    if storage.get(Place, place_id) is None:
        abort(404)
    return jsonify(storage.get(Place, place_id).to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    if storage.get(Place, place_id) is None:
        abort(404)
    storage.delete(storage.get(Place, place_id))
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def new_place(city_id):
    data = request.get_json(force=True, silent=True)
    if storage.get(City, city_id) is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if storage.get(User, data['user_id']) is None:
        abort(404)
    data['city_id'] = city_id
    obj = Place(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["PUT"])
def update_place(place_id):
    """update place"""
    ignoredKeys = ['id', 'created_at', 'updated_at',
                   'city_id','user_id']
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    for key in ignoreKeys:
        if key in data.keys():
            data.pop(key)
    obj = Place(**data)
    obj.save()
    return jsonify(obj.to_dict()), 200
