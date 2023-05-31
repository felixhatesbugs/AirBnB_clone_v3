#!/usr/bin/python3
"""View for user objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """returns all user objects in json
    """
    users = storage.all('User')
    dict_users = [v.to_dict() for v in users.values()]
    return jsonify(dict_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_by_id(user_id):
    """returns a user object
    by its ID in json
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
        '/users/<user_id>',
        methods=['DELETE'],
        strict_slashes=False)
def del_user(user_id):
    """deletes specified user instance
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates new user instance
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'email' not in request.get_json():
        return jsonify({'error': 'Missing email'}), 400
    elif 'password' not in request.get_json():
        return jsonify({'error': 'Missing password'}), 400
    else:
        payload = request.get_json()
        user = User(**payload)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates user instances
    except the id , created_at and
    updated_at keys
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    payload = request.get_json()
    for k in payload:
        if not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, payload[k])
    user.save()
    return jsonify(user.to_dict()), 200
