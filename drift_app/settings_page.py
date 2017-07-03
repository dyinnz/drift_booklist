import logging
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from drift_app.db_interface import db_user
import json

settings_bp = Blueprint('settings_bp', __name__)


@settings_bp.route('/settings')
@flask_login.login_required
def settings():
    return current_app.send_static_file('react/settings.html')


@settings_bp.route('/settings/get')
@flask_login.login_required
def get_account_settings():
    logging.info('Get settings of %s', current_user.account)
    ret = json.loads(db_user.get_user_infos(current_user.account))
    ret['tags'] = json.loads(db_user.get_user_interests(current_user.account))
    if not ret['tags']:
        ret['tags'] = []
    return json.dumps(ret)


@settings_bp.route('/settings/update', methods=['POST'])
@flask_login.login_required
def update_account_settings():
    new_settings = request.get_json()
    logging.info("new_settings: %s", new_settings)

    true= db_user.update_user_tags(current_user.account,new_settings['tags'])

    if db_user.update_user_infos(current_user.account, new_settings) and true:
        return 'Succeed!'
    else:
        return 'Failed!'


@settings_bp.route('/settings/update_ps', methods=['POST'])
@flask_login.login_required
def update_account_password():
    old_ps = request.form['old_ps']
    new_ps = request.form['new_ps']

    if not db_user.authenticate(current_user.account, old_ps):
        return "Old password is not correct!"

    if db_user.update_user_password(current_user.account, new_ps):
        return 'Succeed!'
    else:
        return 'Failed'
