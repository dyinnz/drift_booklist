from flask import request

from drift_app import app
from drift_app import users
from drift_app import User

import flask_login

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
