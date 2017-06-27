import logging
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from drift_app.db_interface import db_user

explore_bp = Blueprint('explore_bp', __name__)


@explore_bp.route('/explore')
def friends():
    return current_app.send_static_file('react/explore.html')


@explore_bp.route('/test_explore')
def test_explore():
    return current_app.send_static_file('explore.html')
