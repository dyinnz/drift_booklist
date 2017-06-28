from drift_app.db_interface import db
import logging
from flask import json

_user_interest_table = db.Table(
    'user_interest',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('tag_name', db.String, db.ForeignKey('tags.name'), primary_key=True)
)

_friend_table = db.Table(
    'friend',
    db.Column('user_id1', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('user_id2', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class DB_user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    account = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))
    birthday = db.Column(db.Date)
    introduction = db.Column(db.String(45), nullable=True, default='No Introduction yet.')
    gender = db.Column(db.Enum('male', 'female'))
    pic_src = db.Column(db.String(128), nullable=True, default='resource/pic/default.png')
    interests = db.relationship('DB_tags', secondary=_user_interest_table, backref=db.backref('users', lazy='dynamic'))
    friends = db.relationship('DB_user', secondary=_friend_table, primaryjoin=id == _friend_table.c.user_id1,
                              secondaryjoin=id == _friend_table.c.user_id2,
                              backref=db.backref('friends2'))

    def __repr__(self):
        return 'User Id:%s\nUser Name:%s\nAccount name:%s' % (self.id, self.name, self.account)


class DB_tags(db.Model):
    __tablename__ = 'tags'
    name = db.Column(db.String(16), primary_key=True, unique=True)

    def __repr__(self):
        return '%s' % self.name


def get_user_interests(user_id):
    try:
        user = DB_user.query.filter_by(id=user_id).first()
        if user is None:
            return None
        return json.dumps([x.name for x in user.interests])
    except Exception as e:
        logging.error(user_id)
        logging.error(e)
        return None


def get_friends(user_id):
    try:
        user = DB_user.query.filter_by(id=user_id).first()
        if user is None:
            return None
        return json.dumps([x.account for x in user.friends])
    except Exception as e:
        logging.error(user_id)
        logging.error(e)
        return None

def get_account_by_id(user_id):
    """
    get user account name by user id.
    :param user_id: user id.
    :return: account name, string type.
    """
    try:
        user = DB_user.query.filter_by(id=user_id).first()
        if user is None:
            return None
        return user.account
    except Exception as e:
        logging.error(user_id)
        logging.error(e)
        return None


def get_id_by_account(account):
    """
    get user id by account.
    :param account: account.
    :return: If success, return user id, else None.
    """
    try:
        user = DB_user.query.filter_by(account=account).first()
        if user is None:
            return None
        return user.id
    except Exception as e:
        logging.error(account)
        logging.error(e)
        return None


def get_user_infos(account):
    """
    get user informations by account.
    :param account: account
    :return: If success, return user information in json format, else None.
    """
    try:
        user = DB_user.query.filter_by(account=account).first_or_404()
        if user is None:
            return None
        return json.dumps({
            'name': user.name,
            'birthday': user.birthday,
            'introduction': user.introduction,
            'gender': user.gender,
            'pic_src': user.pic_src
        })
    except Exception as e:
        logging.error(account)
        logging.error(e)
        return None


def update_user_infos(account, infos):
    try:
        user = DB_user.query.filter_by(account=account).first_or_404()
        if not user:
            return None

        user.name = infos['name']
        user.introduction = infos['introduction']
        user.birthday = infos['birthday']
        user.gender = infos['gender']
        user.pic_src = infos['pic_src']
        print(infos['pic_src'])
        db.session.commit()

        return True

    except Exception as e:
        logging.error("update %s error: %s", account, e)
        db.session.rollback()
        return None


def authenticate(account, password):
    """
    authenticate user identity.
    :param account: account name, like xlm, not real name.
    :param password: password.
    :return: If authentication passes return tuple (id, account), else None.
    """
    try:
        user = DB_user.query.filter_by(account=account, password=password).first()
        if user is None:
            return None
        logging.info(user)
        return user.id, user.account
    except Exception as e:
        logging.error('%s, %s' % (account, password))
        logging.error(e)
        return None


def check_duplicate_account(account):
    """
    check account name is duplicate or not when someone wants to register.
    :param account: account name, liek xlm, not real name.
    :return: True if duplicate acccount name, else False.
    """
    try:
        user = DB_user.query.filter_by(account=account).first()
    except Exception as e:
        logging.error(account)
        logging.error(e)
        return True

    return user is not None


def register_user(name, account, password, birthday, gender, introduction='No Introduction yet.',
                  pic_src='resource/pic/default.png'):
    """
    register user with A LOT OF parameters.
    :param name: real name.
    :param account: account name.
    :param password: password.
    :param birthday: birthday, string type.
    :param gender: gender, string type, 'male' or 'female'.
    :param introduction: introduction, string type.
    :param pic_src: user picture source path, string type.
    :return: True if register is success, else False.
    """
    user = DB_user(name=name, account=account, password=password, birthday=birthday, introduction=introduction,
                   gender=gender, pic_src=pic_src)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.error(','.join([str(x) for x in [name, account, password, birthday, gender, introduction, pic_src]]))
        logging.error(e)
        db.session.rollback()
        return False
    return True


def update_user_password(account, new_password):
    """
    update user password.
    :param account: account name.
    :param new_password: password.
    :return: True if change is done, else False.
    """
    try:
        user = DB_user.query.filter_by(account=account).first_or_404()
        if user is None:
            return False
        user.password = new_password
        db.session.commit()
    except Exception as e:
        logging.error(account, new_password)
        logging.error(e)
        db.session.rollback()
        return False
    return True


def add_user_interest(account, tag):
    """
    add user interest tag.
    :param account: account name.
    :param tag: tag, string type.
    :return: True if interest is added, else False.
    """
    try:
        user = DB_user.query.filter_by(account=account).first_or_404()
        tag = DB_tags.query.filter_by(name=tag).first_or_404()
        user.interests.append(tag)
        db.session().commit()
    except Exception as e:
        logging.error(account, tag)
        logging.error(e)
        db.session.rollback()
        return False

    return True
