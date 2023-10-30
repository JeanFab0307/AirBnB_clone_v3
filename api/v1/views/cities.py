#!/usr/bin/python3
"""Add routes"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/cities',strict_slashes=False,
                 methods=["GET"])
def cities():
    citiesList = []
    for k, v in storage.all(City).items():
        citiesList.append(v.to_dict())
    return jsonify(citiesList)


@app_views.route('/cities/<city_id>',strict_slashes=False,
                 methods=["GET"])
def get_city(city_id):
    if storage.get(City, city_id) == None:
        abort(404)
    return jsonify(storage.get(City, city_id).to_dict())


@app_views.route('/cities/<city_id>',strict_slashes=False,
                 methods=['DELETE'])
def delete(city_id):
    if storage.get(City, city_id) == None:
        abort(404)
    storage.delete(storage.get(City, city_id))
    storage.save()
    return {}, 200


@app_views.route('/cities',strict_slashes=False,
                 methods=['POST'])
def new():
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    obj = City(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["PUT"])
def update(city_id):
    """update city"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
