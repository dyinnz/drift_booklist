from drift_app.db_interface import db
import logging


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

    def __repr__(self):
        return 'User Id:%s\nUser Name:%s\nAccount name:%s' % (self.id, self.name, self.account)


class DB_tags(db.Model):
    __tablename__ = 'tags'
    name = db.Column(db.String(16), primary_key=True, unique=True)

    def __repr__(self):
        return 'tag:%s' % self.name


class DB_user_interest(db.Model):
    __tablename__ = 'user_interest'
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    tag_name = db.Column(db.String(16), db.ForeignKey("tags.name"), primary_key=True)

    def __repr__(self):
        return 'User:%s is interested in %s' % (self.user_id, self.tag_name)


class DB_friend(db.Model):
    __tablename__ = 'friend'
    user_id1 = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    user_id2 = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    def __repr__(self):
        return 'User %s and User %s are friends' % (self.user_id1, self.user_id2)


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
        print("Excepiton while getting account by user id.")
        print(user_id)
        print(e)
        return None


def authenticate(account, password):
    """
    authenticate user identity.
    :param account: account name, like xlm, not real name.
    :param password: password.
    :return: If authentication passes return True, else False.
    """
    try:
        user = DB_user.query.filter_by(account=account, password=password).first()
        if user is None:
            return False
    except Exception as e:
        logging.debug('%s, %s' % (account, password))
        logging.error(e)
        return False

    logging.info(user)
    return True


def check_duplicate_account(account):
    """
    check account name is duplicate or not when someone wants to register.
    :param account: account name, liek xlm, not real name.
    :return: True if duplicate acccount name, else False.
    """
    try:
        user = DB_user.query.filter_by(account=account).first()
    except Exception as e:
        logging.debug(account)
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
        logging.debug(','.join([str(x) for x in [name, account, password, birthday, gender, introduction, pic_src]]))
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
        logging.debug(account, new_password)
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
        id = user.id
        user_interest = DB_user_interest(user_id=id, tag_name=tag)
        db.session.add(user_interest)
        db.session.commit()
    except Exception as e:
        logging.debug(account, tag)
        logging.error(e)
        db.session.rollback()
        return False

    return True
