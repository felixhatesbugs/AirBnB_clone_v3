#!/usr/bin/python3
"""View for State objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """returns all state objects in json
    """
    states = storage.all('State')
    dict_states = [v.to_dict() for v in states.values()]
    return jsonify(dict_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """returns a state object
    by its ID in json
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'],
        strict_slashes=False)
def del_state(state_id):
    """deletes specified state instance
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates new state instance
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    else:
        payload = request.get_json()
        state = State(**payload)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates state instances
    except the id , created_at and
    updated_at keys
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    payload = request.get_json()
    # for k in payload:
    #     if k not in ['id', 'created_at', 'updated_at']:
    #         state.__dict__[k] = payload[k]
    state.name = payload['name']
    state.save()
    return jsonify(state.to_dict()), 200
