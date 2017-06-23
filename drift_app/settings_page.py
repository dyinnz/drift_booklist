import logging
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from drift_app.db_interface import db_user

settings_bp = Blueprint('settings_bp', __name__)


@settings_bp.route('/settings')
def settings():
    return current_app.send_static_file('settings.html')


@settings_bp.route('/settings/get')
@flask_login.login_required
def get_account_settings():
    logging.info('Get settings of %s', current_user.account)
    return db_user.get_user_infos(current_user.account)


@settings_bp.route('/settings/update', methods=['POST'])
@flask_login.login_required
def update_account_settings():
    new_settings = request.get_json()
    if db_user.update_user_infos(current_user.account, new_settings):
        return 'Succeed!'
    else:
        return 'Failed!'


@settings_bp.route('/settings/update_ps', methods=['POST'])
@flask_login.login_required
def update_account_password():
    json_data = request.get_json()

    if not db_user.authenticate(current_user.account, json_data['old_ps']):
        return "Old password is not correct!"

    if db_user.update_user_password(current_user.account, json_data['new_ps']):
        return 'Succeed!'
    else:
        return 'Failed'
