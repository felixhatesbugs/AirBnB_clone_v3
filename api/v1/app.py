#!/usr/bin/python3
"""
App instance of
flask application
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='0.0.0.0')
app.register_blueprint(app_views)


@app.teardown_appcontext
def refresh_storage(self):
    """closes query after each request
    making new request start with a new query
    to a possibly updated database"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns
    a JSON-formatted 404 status code response
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'),
            threaded=True)
