#!/usr/bin/python3
"""flask with index routes
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """returns OK status
    """
    return jsonify({'status': 'OK'})
