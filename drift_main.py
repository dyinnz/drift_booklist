from flask import Flask
from drift_app.recommand_page import recommand_bp
from drift_app.login_page import login_bp
from drift_app.login_page import init_login_manager

import flask_login

# setup app
app = Flask(__name__)
app.secret_key = \
b'\x12\x89C\xda\xab\xcbD\xd4\x91@\x9b\xde\xbf?Y\x13\xe8Y\xcf\xbc\xaa\x9c"\x93'

app.register_blueprint(recommand_bp)
app.register_blueprint(login_bp)


init_login_manager(app)


if __name__ == '__main__':
    app.run()
