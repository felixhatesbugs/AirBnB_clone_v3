#!/usr/bin/python3
"""flask with index routes
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status')
def status():
    """returns OK status
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """returns stats of models in api
    """
    stats = {"amenities": storage.count('Amenity'),
             "cities": storage.count('City'),
             "places": storage.count('Place'),
             "reviews": storage.count('Review'),
             "states": storage.count('State'),
             "users": storage.count('User')}

    return jsonify(stats)
