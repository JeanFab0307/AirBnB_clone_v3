#!/usr/bin/python3
"""Add routes"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,
                 methods=["GET"])
def amenities():
    amenitiesList = []
    for k, v in storage.all(Amenity).items():
        amenitiesList.append(v.to_dict())
    return jsonify(amenitiesList)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["GET"])
def get_amenity(amenity_id):
    if storage.get(Amenity, amenity_id) is None:
        abort(404)
    return jsonify(storage.get(Amenity, amenity_id).to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    if storage.get(Amenity, amenity_id) is None:
        abort(404)
    storage.delete(storage.get(Amenity, amenity_id))
    storage.save()
    return {}, 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def new_amenity():
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    obj = Amenity(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    """update amenity"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
