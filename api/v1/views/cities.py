#!/usr/bin/python3
"""View for State objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """returns all city objects of a state in json
    """
    state = storage.get('State', state_id)
    dict_cities = [v.to_dict() for v in state.cities]
    return jsonify(dict_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city_by_id(city_id):
    """returns a city object
    by its ID in json
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """deletes specified city instance
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/state_id/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """creates new state instance
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    else:
        state = storage.get('State', state_id)
        if state is None:
            abort(404)
        payload = request.get_json()
        payload['state_id'] = state.id
        city = City(**payload)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates state instances
    except the id , created_at and
    updated_at keys
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    payload = request.get_json()
    # for k in payload:
    #     if k not in ['id', 'created_at', 'updated_at']:
    #         state.__dict__[k] = payload[k]
    city.name = payload['name']
    state.save()
    return jsonify(state.to_dict()), 200
