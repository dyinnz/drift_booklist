from flask import Blueprint, current_app
import flask_login
import logging

recommend_bp = Blueprint('recommend_bp', __name__)


@recommend_bp.route('/index')
@recommend_bp.route('/recommend')
def recommend():
    if not flask_login.current_user.is_anonymous:
        logging.info('recommend page for %s', flask_login.current_user.get_id())
    else:
        logging.info('recomemnd page for anonymous')

    return current_app.send_static_file('index.html')


@recommend_bp.route('/recommend/fetch')
def recommend_fetch():
    return 'TODO: add some json data'
