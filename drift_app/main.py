from flask import request

import flask_login

@app.route('/')
def hello_world():
    return 'Hello World!'


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
