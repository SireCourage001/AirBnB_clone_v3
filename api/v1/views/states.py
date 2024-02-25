#!/usr/bin/python3

"""State objects that handles all default RESTFul API actions."""

from flask import abort, jsonify, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Get all states objects from the storage."""
    states = storage.all(State).values()
    """Convert object to dict and JSON."""
    state_list = [state.to_dict() for state in states]

    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """"Get state object with the given id from storage."""
    state = storage.get(State, state_id)
    """Return state object in JSON otherwise 404 error."""
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state:
        """Delete state object from storege and save changes
           and return empty JSON with status code 200
           otherwise return 404 error.
        """
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """If the request data is not in JSON format
       and if 'name' key is missing in the JSON
       data return error 400.Otherwise add new State
       object with the JSON data
    """
    data = requset.get_json()
    if not data or 'name' not in data:
        abort(404)

    state = State(** data)
    state.save()
    """ Return the newly created State object
        in JSON format with 201 status code.
    """
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates State object.
       Get State object with
       the given ID from the storage.
     """

    state = storage.get(State, state_id)
    if not state:
        """Return 404 if state is not found."""
        abort(404)

    data = request.get_json()
    if not data:
        """Return 400 if request data is not JSON."""
        abort(400, 'Not a JSON')

    """Update attributes of the State object with the JSON data."""
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    """Save updated State object to the storage.
       Return updated State object in JSON format
       with 200 status code.
    """
    state.save()
    return jsonify(state.to_dict()), 200


"""Error Handlers."""


@app_views.errorhandler(404)
def not_found(error):
    """
    Returns a JSON response for 404 error (Not Found).
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Returns a JSON response for 400 error (Bad Request).
    """
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
