
import logging
import os
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename

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

