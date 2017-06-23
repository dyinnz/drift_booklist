import os
import logging
import flask
import flask_login
import drift_app.db_interface.db_user as db_user

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

login_bp = Blueprint('login_bp', __name__)

logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = './uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ------------------------------------------------------------------------------
# utility class and function for login

class User(flask_login.UserMixin):
    def __init__(self, account):
        self.id = account
        self.db_id = db_user.get_id_by_account(account)

    def __str__(self):
        return 'User[' + self.account + ']'

    @property
    def account(self):
        return self.id


# should be called by app file
login_manager = flask_login.LoginManager()


def init_login_manager(app):
    login_manager.init_app(app)


# callback
@login_manager.user_loader
def user_loader(account):
    if not db_user.check_duplicate_account(account):
        return
    return User(account)


# ------------------------------------------------------------------------------

def allowed_avatar_file(filename):
    extensions = ['jpg', 'jpeg', 'png']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@login_bp.route('/upload/avatar', methods=['GET', 'POST'])
def upload_avatar():
    if request.method == 'GET':
        return '''
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''

    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'no selected file'

    if file and allowed_avatar_file(file.filename):
        filename = secure_filename(file.filename)
        logging.info("file: %s has been saved.", filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return 'success in uploading file'

    return 'fail in uploading file'


# ------------------------------------------------------------------------------

@login_bp.route('/')
def root():
    logging.debug("%s accesses root", flask_login.current_user)
    if not flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('recommend_bp.recommend'))
    else:
        return flask.redirect(flask.url_for('.login'))


# route
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    logging.debug("%s accesses login", flask_login.current_user)

    if request.method == 'GET':
        if not flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('recommend_bp.recommend'))

        return flask.current_app.send_static_file('login.html')

    account = flask.request.form['account']
    password = flask.request.form['password']

    auth_result, user_id = db_user.authenticate(account, password)
    if not auth_result:
        return jsonify({"ok": False,
                        "brief": "Authenticate failed!"})

    flask_login.login_user(User(account))
    return flask.redirect(flask.url_for('recommend_bp.recommend'))


@login_bp.route('/start', methods=['GET', 'POST'])
@flask_login.login_required
def start():
    if request.method == 'GET':
        return '''
        <form action='start' method='POST'>
        <input type='text' name='tags'></input>
        <input type='submit' name='submit'></input>
        </form>
        '''

    tags = request.form['tags']
    for tag in tags.split(' '):
        db_user.add_user_interest(flask_login.current_user.account, tag)

    return 'start as: ' + flask_login.current_user.account


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return '''
        <form action='register' method='POST'>
        <input type='text' name='account' id='account' placeholder='account'></input>
        <input type='password' name='password' id='password' placeholder='password'></input>
        <input type='text' name='name' id='name' placeholder='name'></input>
        <input type='text' name='birthday' id='birthday' placeholder='birthday'></input>
        <input type='text' name='introduction' id='introduction' placeholder='introduction'></input>
        <input type='text' name='gender' id='gender' placeholder='gender'></input>
        <input type='text' name='pic_src' id='pic_src' placeholder='pic_src'></input>
        <input type='submit' name='submit'></input>
        </form>
        '''

    form = request.form

    account = form['account']
    password = form['password']
    name = form['name']
    birthday = form['birthday']
    introduction = form['introduction']
    gender = form['gender']
    pic_src = form['pic_src']

    if db_user.check_duplicate_account(account):
        return jsonify({"ok": False,
                        "brief": "Account has been registered!"})

    db_user.register_user(name, account, password, birthday, gender, introduction, pic_src)

    flask_login.login_user(User(account))
    return flask.redirect(flask.url_for('.start'))


@login_bp.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('.login'))
