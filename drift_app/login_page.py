import flask
from flask import Blueprint, request
from drift_app.db_model import authenticate
import flask_login
import logging

login_bp = Blueprint('login_page', __name__)

logging.basicConfig(level=logging.DEBUG)

# fake users data
users = {'xlm': {'password': '1234'}}


# class
class User(flask_login.UserMixin):
    def __init__(self, account):
        self.id = account

    def __str__(self):
        return 'User[' + self.id + ']'


# should be called by app file
login_manager = flask_login.LoginManager()


def init_login_manager(app):
    login_manager.init_app(app)


# callback
@login_manager.user_loader
def user_loader(account):
    if account not in users:
        return
    return User(account)


@login_bp.route('/')
def root():
    logging.debug("%s accesses root", flask_login.current_user)
    if not flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('recommand_bp.recommand'))
    else:
        return flask.redirect(flask.url_for('.login'))


# route
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    logging.debug("%s accesses login", flask_login.current_user)

    if request.method == 'GET':
        if not flask_login.current_user.is_anonymous:
            return flask.redirect(flask.url_for('recommand_bp.recommand'))
        return '''
        <form action='login' method='POST'>
        <input type='text' name='account' id='account' placeholder='account'></input>
        <input type='password' name='password' id='password' placeholder='password'></input>
        <input type='submit' name='submit'></input>
        </form>
        '''

    account = flask.request.form['account']

    if account not in users:
        return 'Login Error'

    if flask.request.form['password'] != users[account]['password']:
        return 'Login Error'

    flask_login.login_user(User(account))
    return flask.redirect(flask.url_for('recommand_bp.recommand'))


@login_bp.route('/start')
@flask_login.login_required
def start():
    return 'start as: ' + flask_login.current_user.id


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return '''
        <form action='register' method='POST'>
        <input type='text' name='account' id='account' placeholder='account'></input>
        <input type='password' name='password' id='password' placeholder='password'></input>
        <input type='submit' name='submit'></input>
        </form>
        '''

    account = flask.request.form['account']
    password = flask.request.password['password']

    if account in users:
        return 'account has been used'

    users[account] = {'password': password}
    flask_login.login_user(User(account))
    return flask.redirect(flask.url_for('.start'))


@login_bp.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('.login'))
