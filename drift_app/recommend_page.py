from flask import Blueprint
import flask_login

recommend_bp = Blueprint('recommend_bp', __name__)


@recommend_bp.route('/index')
@recommend_bp.route('/recommend')
def recommend():
    if not flask_login.current_user.is_anonymous:
        return 'recommend page for' + flask_login.current_user.get_id()
    else:
        return 'recommend page for guest'


@recommend_bp.route('/recommend/fetch')
def recommend_fetch():
    return 'TODO: add some json data'
