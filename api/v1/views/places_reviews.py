#!/usr/bin/python3
"""View for Review objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/reviews/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """returns all review objects of a place in json
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    dict_reviews = [v.to_dict() for v in place.reviews]
    return jsonify(dict_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_by_id(review_id):
    """returns a review object
    by its ID in json
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """deletes specified review instance
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates new review instance
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'text' not in request.get_json():
        return jsonify({'error': 'Missing test'}), 400
    elif 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400
    else:
        payload = request.get_json()

        place = storage.get('Place', place_id)
        user = storage.get('User', payload['user_id'])

        if user is None or place is None:
            abort(404)

        payload['place_id'] = place.id
        payload['user_id'] = user.id
        review = Review(**payload)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates review instances
    except the id , created_at and
    updated_at keys
    """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    payload = request.get_json()
    for k in payload:
        if k not in ['id', 'user_id', 'created_at', 'place_id', 'updated_at']:
            setattr(review, k, payload[k])
    review.save()
    return jsonify(review.to_dict()), 200
