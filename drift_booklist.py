from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login')
def login_or_register():
    return 'login or register'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return 'post'
    else:
        return 'get'


@app.route('/start')
def newbie_start():
    return 'start'


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
