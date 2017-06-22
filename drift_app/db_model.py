from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

class DB_User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    userame = db.Column(db.String(45))
    account = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))
    # birthday = db.Column(db.Date)
    # introduction = db.Column(db.String(45))
    # gender = db.Column(db.Enum)


    def __init__(self, id, username, account, password):
        self.id = id
        self.userame = username
        self.account = account
        self.password = password


    def __repr__(self):
        return 'User:%s\nAccount name:%s' % (self.username, self.account)


def authenticate(account, password):
    print(account, password)
    try:
        user = DB_User.query().filter_by(account=account, password=password).first()
    except Exception as e:
        print(account, password)
        print(e)
        return False

    return user is not None
