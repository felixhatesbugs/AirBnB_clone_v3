#!/usr/bin/python3
"""View for Place objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_place(city_id):
    """returns all place objects of a city in json
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    dict_places = [v.to_dict() for v in city.places]
    return jsonify(dict_cities)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_by_id(place_id):
    """returns a place object
    by its ID in json
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """deletes specified place instance
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates new place instance
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    elif 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400
    else:
        payload = request.get_json()

        city = storage.get('City', state_id)
        if city is None:
            abort(404)
        user = storage.get('User', payload['user_id'])
        if user is None:
            abort(404)

        payload['city_id'] = city.id
        payload['user_id'] = user.id
        place = Place(**payload)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates place instances
    except the id , created_at and
    updated_at keys
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    payload = request.get_json()
    for k in payload:
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, payload[k])
    place.save()
    return jsonify(place.to_dict()), 200
