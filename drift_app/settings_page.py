import logging
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify

settings_bp = Blueprint('settings_bp', __name__)


@settings_bp.route("/settings")
def settings():
    return current_app.send_static_file('settings.html')


@settings_bp.route("/settings/get")
@flask_login.login_required
def get_account_settings():
    logging.info("Get settings of %s", current_user.account)
    return jsonify({
        "name": "aaa",
        "birthday": "2017/01/01",
        "introduction": "hehehe",
        "gender": "male"
    })


@settings_bp.route("/settings/update", methods=["POST"])
@flask_login.login_required
def update_account_settings():
    logging.info("Update settings of %s", current_user.account)
