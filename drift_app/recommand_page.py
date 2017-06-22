from flask import Blueprint

recommand_bp = Blueprint('recommand_bp', __name__)

@recommand_bp.route('/recommand')
def recommand():
    return 'recommand page'
