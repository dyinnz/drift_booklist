import logging
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from drift_app.db_interface import db_user

book_bp = Blueprint('book_bp', __name__)


@book_bp.route('/book/<book_id>')
@flask_login.login_required
def book(book_id):
    return current_app.send_static_file('react/book.html')
