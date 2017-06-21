import flask
from flask import Flask
from flask import request

import flask_login

app = Flask(__name__)
app.secret_key = b'\x12\x89C\xda\xab\xcbD\xd4\x91@\x9b\xde\xbf?Y\x13\xe8Y\xcf\xbc\xaa\x9c"\x93'


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'xlm': {'password': '1234'}}


class User(flask_login.UserMixin):
    pass


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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    return 'register'

@app.route('/start')
@flask_login.login_required
def start():
    return 'start as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@app.route('/explore')
def explore():
    return 'explore'


@app.route('/mine')
def mine():
    return 'mine'


@app.route('/friends')
def friends():
    return 'friends'


@app.route('/booklist')
def booklist():
    return 'booklist'


@app.route('/book')
def book():
    return 'book'


@app.route('/profile')
def profile():
    return 'profile'


@app.route('/settings')
def settings():
    return 'settings'


@app.route('/search')
def search():
    return 'search'


if __name__ == '__main__':
    app.run()
