from flask import Flask
from drift_app.recommand_page import recommand_bp
from drift_app.login_page import login_bp
from drift_app.mine_page import mine_bp
from drift_app.login_page import init_login_manager
from drift_app.db_model import init_db

import flask_login

# setup app
app = Flask(__name__)
app.secret_key = \
b'\x12\x89C\xda\xab\xcbD\xd4\x91@\x9b\xde\xbf?Y\x13\xe8Y\xcf\xbc\xaa\x9c"\x93'

app.register_blueprint(recommand_bp)
app.register_blueprint(login_bp)
app.register_blueprint(mine_bp)


init_login_manager(app)
init_db(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:flowers@localhost/shixun'


if __name__ == '__main__':
    app.run()
