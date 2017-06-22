from drift_app.db_interface import db

class DB_User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    account = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))
    birthday = db.Column(db.Date)
    introduction = db.Column(db.String(45), nullable=True)
    gender = db.Column(db.Enum('male', 'female'))
    pic_src = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return 'User:%s\nAccount name:%s' % (self.name, self.account)



class DB_tags(db.Model):
    __tablename__ = 'tags'
    name = db.Column(db.String(16), primary_key=True)


class DB_user_interest(db.Model):
    __tablename__ = 'user_interest'
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    tag_name = db.Column(db.String(16), db.ForeignKey("tags.name"), primary_key=True)


class DB_friend(db.Model):
    __tablename__ = 'friend'
    user_id1 = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    user_id2 = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

def authenticate(account, password):
    """
    authenticate user identity.
    :param account: account name, like xlm, not real name.
    :param password: password.
    :return: True if authenticate passes, else False.
    """
    try:
        user = DB_User.query.filter_by(account=account, password=password).first()
    except Exception as e:
        print("Exception while authenticate.")
        print(account, password)
        print(e)
        return False

    print(user)
    return user is not None


def check_duplicate_account(account):
    """
    check account name is duplicate or not when someone wants to register.
    :param account: account name, liek xlm, not real name.
    :return: True if duplicate acccount name, else False.
    """
    user = DB_User.query.filter_by(account=account).first()
    return user is not None

def register_user(name, account, password, birthday, gender, introduction='No Introduction yet', pic_src='resource/pic/default.png'):
    """
    register user.
    :param name: real name.
    :param account: account name.
    :param password: password.
    :param birthday: birthday, string type.
    :param gender: gender, string type, 'male' or 'female'.
    :param introduction: introduction, string type.
    :param pic_src:
    :return:
    """
    user = DB_User(name=name, account=account, password=password, birthday=birthday, introduction=introduction,
                   gender=gender, pic_src=pic_src)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print("Excetpion while registering user.")
        print(name, account, password, birthday, gender, introduction, pic_src)
        print(e)
        return False
    return True


def update_user_password(account, new_password):
    """
    
    :param account:
    :param new_password:
    :return:
    """
    user = DB_User.query.filter_by(account=account)
    user.password = new_password
    try:
        db.session.commit()
    except Exception as e:
        print("Exception while updating user password.")
        print(account, new_password)
        print(e)
        return False
    return True


def add_user_interest(account, tag):
    user = DB_User.query.filter_by(account=account)
    id = user.get_id()
    user_interest = DB_user_interest(user_id=id, tag_name=tag)
    try:
        db.session.add(user_interest)
        db.session.commit()
    except Exception as e:
        print("Exception while adding user interest.")
        print(account, tag)
        print(e)
        return False

    return True
