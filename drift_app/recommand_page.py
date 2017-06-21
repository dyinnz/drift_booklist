from flask import Blueprint

recommand_bp = Blueprint('recommand', __name__)

@recommand_bp.route('/recommand_page')
def recommand_page():
    return 'recommand page'
