#!/usr/bin/python3
"""Module for actions and handles Apparently needs to be more documented."""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieves the list of all state objects"""
    states = []
    for value in storage.all("State").values():
        states.append(value.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """retrieves a state object"""
    state_dic = storage.get("State", state_id)
    if state_dic is None:
        abort(404)
    return jsonify(state_dic.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object"""
    state_del = storage.get("State", state_id)
    if state_del is None:
        abort(404)
    state_del.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createState():
    """Creates a new State"""
    if request.get_json() is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates a state obj"""
    if not request.get_json():
        make_response(jsonify({'error': 'Not a JSON'}), 400)

    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    obj.save()
    return jsonify(obj.to_dict())
