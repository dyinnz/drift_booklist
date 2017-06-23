import json

from flask import Flask

from drift_app.db_interface import init_db
from drift_app.login_page import init_login_manager
from drift_app.login_page import login_bp
from drift_app.mine_page import mine_bp
from drift_app.recommend_page import recommend_bp



json_config = None
with open('config.json') as f:
    json_config = json.load(f)

# setup app
app = Flask(__name__)

app.secret_key = \
b'\x12\x89C\xda\xab\xcbD\xd4\x91@\x9b\xde\xbf?Y\x13\xe8Y\xcf\xbc\xaa\x9c"\x93'

app.config['SQLALCHEMY_DATABASE_URI'] = json_config['db_uri']


# blueprint
app.register_blueprint(recommend_bp)
app.register_blueprint(login_bp)
app.register_blueprint(mine_bp)

# init other model
init_login_manager(app)
init_db(app)


if __name__ == '__main__':
    app.run()
