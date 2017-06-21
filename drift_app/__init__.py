from flask import Flask
from drift_app.recommand_page import recommand_bp

import flask_login

app = Flask(__name__)
app.register_blueprint(recommand_bp)
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

import drift_app.main
