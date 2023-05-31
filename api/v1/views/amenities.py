#!/usr/bin/python3
"""View for amenity objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """returns all amenity objects in json
    """
    amenities = storage.all('Amenity')
    dict_amenities = [v.to_dict() for v in amenities.values()]
    return jsonify(dict_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id):
    """returns a amenity object
    by its ID in json
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False)
def del_amenity(amenity):
    """deletes specified amenity instance
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates new amenity instance
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    else:
        payload = request.get_json()
        amenity = Amenity(**payload)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates amenity instances
    except the id , created_at and
    updated_at keys
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    payload = request.get_json()
    # for k in payload:
    #     if k not in ['id', 'created_at', 'updated_at']:
    #         amenity.__dict__[k] = payload[k]
    amenity.name = payload['name']
    amenity.save()
    return jsonify(amenity.to_dict()), 200
