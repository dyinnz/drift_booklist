from flask import Blueprint
import flask_login

recommand_bp = Blueprint('recommand_bp', __name__)

@recommand_bp.route('/index')
@recommand_bp.route('/recommand')
def recommand():
    if not flask_login.current_user.is_anonymous:
        return 'recommand page for' + flask_login.current_user.get_id()
    else:
        return 'recommand page for guest'


@recommand_bp.route('/recommand/fetch')
def recommand_fetch():
    return 'TODO: add some json data'

