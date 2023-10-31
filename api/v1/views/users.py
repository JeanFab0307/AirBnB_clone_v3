#!/usr/bin/python3
"""Add routes"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False,
                 methods=["GET"])
def users():
    usersList = []
    for k, v in storage.all(User).items():
        usersList.append(v.to_dict())
    return jsonify(usersList)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=["GET"])
def get_user(user_id):
    if storage.get(User, user_id) is None:
        abort(404)
    return jsonify(storage.get(User, user_id).to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    if storage.get(User, user_id) is None:
        abort(404)
    storage.delete(storage.get(User, user_id))
    storage.save()
    return {}, 200


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def new_user():
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    obj = User(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id):
    """update user"""
    ignoredKeys = ['id', 'created_at', 'updated_at', 'email']
    obj = storage.get(User, user_id)
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
