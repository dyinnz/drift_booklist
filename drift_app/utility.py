import logging
import os

import flask_login
from flask import Blueprint, jsonify, request,current_app
from werkzeug.utils import secure_filename

from drift_app.db_interface import db_book

UPLOAD_FOLDER = './static/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

utility_bp = Blueprint('utility_bp', __name__)


def allowed_file(filename):
    extensions = ['jpg', 'jpeg', 'png']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@utility_bp.route('/upload', methods=['POST'])
@flask_login.login_required
def upload_file():
    path = ''
    prefix = ''
    # path = request.args.get("path")
    # prefix = request.args.get("prefix")
    logging.info("files: %s", request.files)

    if 'file' not in request.files:
        return jsonify({
            'result': 'No file part',
            'path:': ''
        })

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'result': 'no selected file',
            'path:': ''
        })

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        logging.info("file: %s has been saved.", filename)

        dir = os.path.join(UPLOAD_FOLDER, path)
        if not os.path.exists(dir):
            os.makedirs(dir)

        final_path = os.path.join(dir, prefix + filename)
        file.save(final_path)
        return jsonify({
            'result': 'success in uploading file',
            'path': final_path[1:]
        })

    return jsonify({
        'result': 'failed in uploading file',
        'path:': ''
    })


@utility_bp.route('/search/<keyword>', methods=['POST', 'GET'])
def search(keyword):
    if request.method == 'POST':
        ret = db_book.search_keyword(keyword)
        print(ret)
        return jsonify(ret)
    else:
        return current_app.send_static_file('react/search.html')

