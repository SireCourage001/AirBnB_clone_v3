#!/usr/bin/python3
''' a new view for Review object that handles all
default RESTFul API actions'''

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET']
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    ''' Return a list of reviews for the given place_id.'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<string:review_id>', methods=['GET']
                 strict_slashes=False)
def get_single_review(review_id):
    ''' Get a review for a given review id '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    ''' Delete a review from the database'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST']
                 strict_slashes=False)
def create_review(place_id):
    ''' Create a new review'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get('User', data['user_id'])

    if user is not None:
        abort(404)

    if 'text' not in data:
        abort(400, 'Missing text')

    data['place_id'] = place_id
    review = Review(**data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT']
                 strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()

    return jsonify(review.to_dict()), 200


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
