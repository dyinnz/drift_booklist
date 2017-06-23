
import logging
import os
import flask
import flask_login
from flask_login import current_user
from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

utility_bp = Blueprint('utility_bp', __name__)


def allowed_file(filename):
    extensions = ['jpg', 'jpeg', 'png']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@utility_bp.route('/upload', methods=['POST'])
def upload_file():
    path = request.args.get("path")
    prefix = request.args.get("prefix")

    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'no selected file'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        logging.info("file: %s has been saved.", filename)

        dir = os.path.join(UPLOAD_FOLDER, path)
        if not os.path.exists(dir):
            os.makedirs(dir)

        file.save(os.path.join(dir, prefix + filename))
        return 'success in uploading file'

    return 'fail in uploading file'

