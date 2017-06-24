import logging
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from drift_app.db_interface import db_user

friends_bp = Blueprint('friends_bp', __name__)


@friends_bp.route('/friends')
def friends():
    return current_app.send_static_file('react/friends.html')
