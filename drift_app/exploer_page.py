import logging
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from drift_app.db_interface import db_user
from drift_app.db_interface import db_user_remark

explore_bp = Blueprint('explore_bp', __name__)


@explore_bp.route('/explore')
def explore():
    if flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('login_bp.login'))
    else:
        return flask.current_app.send_static_file('react/explore.html')


@explore_bp.route('/test_explore')
def test_explore():
    # result = db_user_remark.get_recommend_booklists(flask_login.current_user.db_id)
    result = db_user_remark.get_user_moments(flask_login.current_user.db_id)
    logging.debug('test explore: %s' % result)
    return flask.current_app.send_static_file('react/login.html')


@explore_bp.route('/get_moment', methods=['GET', 'POST'])
def get_moment():
    data = request.get_json()
    jsondata = db_user_remark.get_user_moments(flask_login.current_user.db_id, data['page'])
    logging.debug(jsondata)
    return jsondata
