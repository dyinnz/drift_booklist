from flask import Blueprint

mine_bp = Blueprint('mine_bp',__name__)

@mine_bp.route('/mine')
def mine():
    return 'mine'
