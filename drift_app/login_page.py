import flask
from flask import Blueprint, request
import flask_login

login_bp = Blueprint('login_page', __name__)


# fake users data
users = {'xlm': {'password': '1234'}}


# class
class User(flask_login.UserMixin):
    pass


login_manager = flask_login.LoginManager()
def init_login_manager(app):
    login_manager.init_app(app)

# callback
@login_manager.user_loader
def uesr_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return
    user = User()
    user.id = username

    user.is_authenticated = (
            request.form['password'] == users[username]['password']
            )

    return user


# route
@login_bp.route('/login', methods=['GET', 'POST'])
def login_or_register():
    if request.method == 'GET':
        return '''
        <form action='login' method='POST'>
        <input type='text' name='username' id='username' placeholder='username'></input>
        <input type='password' name='password' id='password' placeholder='password'></input>
        <input type='submit' name='submit'></input>
        </form>
        '''

    username = flask.request.form['username']
    if flask.request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('start'))

    return 'Login Error!'


@login_bp.route('/start')
@flask_login.login_required
def start():
    return 'start as: ' + flask_login.current_user.id


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    return 'register'


@login_bp.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


