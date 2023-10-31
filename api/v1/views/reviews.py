#!/usr/bin/python3
"""Add routes"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=["GET"])
def reviews(place_id):
    reviewsList = []
    if storage.get(Place, place_id) is None:
        abort(404)
    for k, v in storage.all(Review).items():
        if v.place_id == place_id:
            reviewsList.append(v.to_dict())
    return jsonify(reviewsList)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=["GET"])
def get_review(review_id):
    if storage.get(Review, review_id) is None:
        abort(404)
    return jsonify(storage.get(Review, review_id).to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    if storage.get(Review, review_id) is None:
        abort(404)
    storage.delete(storage.get(Review, review_id))
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def new_review(place_id):
    data = request.get_json(force=True, silent=True)
    if storage.get(Place, place_id) is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    if 'text' not in data:
        abort(400, 'Missing text')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if storage.get(User, data['user_id']) is None:
        abort(404)
    data['place_id'] = place_id
    obj = Review(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["PUT"])
def update_review(review_id):
    """update review"""
    ignoredKeys = ['id', 'created_at', 'updated_at',
                   'place_id','user_id']
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    for key in ignoreKeys:
        if key in data.keys():
            data.pop(key)
    obj = Review(**data)
    obj.save()
    return jsonify(obj.to_dict()), 200
