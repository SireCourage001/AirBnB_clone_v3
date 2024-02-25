#!/usr/bin/python3

"""Views for Airbnb Api."""
from flask import jsonify
from api.v1.views import app_views
from models import storage


# Create route /status on the object app_views
@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON response for RESTful Api."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Retrieves the number of each objects by type.
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)


if __name__ == "__main__":
    pass
