from drift_app.db_interface import db
from .db_user import get_account_by_id
import logging
from flask import json


class DB_user_book_remark(db.Model):
    __tablename__ = 'user_book_remark'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    remark = db.Column(db.String(1024))
    remark_time = db.Column(db.DateTime)

    def __repr__(self):
        return 'User %s remark book %s: %s at %s' % (self.user_id, self.book_id, self.remark, self.remark_time)


class DB_user_book_opinion(db.Model):
    __tablename__ = 'user_book_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')
    is_follow = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return 'User %s %svoted book %s' % (self.user_id, self.vote, self.book_id) if self.vote in ['up', 'down'] \
            else "User %s didn't vote book %s" % (self.user_id, self.book_id)


class DB_user_booklist_remark(db.Model):
    __tablename__ = 'user_booklist_remark'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    booklist_id = db.Column(db.Integer, db.ForeignKey('booklist.id'))
    remark = db.Column(db.String(1024))
    remark_time = db.Column(db.DateTime)

    def __repr__(self):
        return 'User %s remark booklist %s: %s at %s' % (self.user_id, self.booklist_id, self.remark, self.remark_time)


class DB_user_booklist_opinion(db.Model):
    __tablename__ = 'user_booklist_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    booklist_id = db.Column(db.Integer, db.ForeignKey('booklist.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')
    is_follow = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return 'User %s %svoted booklist %s' % (self.user_id, self.vote, self.booklist_id) if self.vote in ['up',
                                                                                                            'down'] \
            else "User %s didn't vote booklist %s" % (self.user_id, self.booklist_id)


class DB_user_book_remark_opinion(db.Model):
    __tablename__ = 'user_book_remark_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_remark_id = db.Column(db.Integer, db.ForeignKey('user_book_remark.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')

    def __repr__(self):
        return 'User %s %svoted book remark %s' % (self.user_id, self.vote, self.book_remark_id) if self.vote in ['up',
                                                                                                                  'down'] \
            else "User %s didn't vote book remark %s" % (self.user_id, self.book_remark_id)


class DB_user_booklist_remark_opinion(db.Model):
    __tablename__ = 'user_booklist_remark_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    booklist_remark_id = db.Column(db.Integer, db.ForeignKey('user_booklist_remark.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')

    def __repr__(self):
        return 'User %s %svoted booklist remark %s' % (
            self.user_id, self.vote, self.booklist_remark_id) if self.vote in ['up', 'down'] \
            else "User %s didn't vote booklist remark %s" % (self.user_id, self.booklist_remark_id)


def get_book_vote_num(book_id):
    """
    get vote result of a book.
    :param book_id: book id.
    :return: If success, return json format dict(keys: 'up', 'down'), else None.
    """
    try:
        up_num = DB_user_book_opinion.query.filter_by(book_id=book_id, up_or_down='up').count()
        down_num = DB_user_book_opinion.query.filter_by(book_id=book_id, up_or_down='down').count()

        return json.dumps({
            'up': up_num,
            'down': down_num
        })
    except Exception as e:
        logging.error(book_id)
        logging.error(e)
        return None

def get_user_book_opinion(user_id, book_id):
    """
    get user up/down and is_follow of a book.
    :param user_id: user id.
    :param book_id: book id.
    :return: If success, return json list [vote, is_follow], vote is in ['up', 'down', 'neutral'] and is_follow is Boolean, else None.
    """
    try:
        opinion = DB_user_book_opinion.query.filter_by(user_id=user_id, book_id=book_id).first()
        if opinion is None:
            return 'neutral'
        return json.dumps([opinion.vote, opinion.is_follow])
    except Exception as e:
        logging.error('%s, %s' % (user_id, book_id))
        logging.error(e)
        return None

def get_user_booklist_opinion(user_id, booklist_id):
    """
    get user up/down and is_follow of a booklist.
    :param user_id: user id.
    :param booklist_id: booklist id.
    :return: If success, return json list [vote, is_follow], vote is in ['up', 'down', 'neutral'] and is_follow is Boolean, else None.
    """
    try:
        opinion = DB_user_booklist_opinion.query.filter_by(user_id=user_id, booklist_id=booklist_id).first()
        if opinion is None:
            return 'neutral'
        return json.dumps([opinion.vote, opinion.is_follow])
    except Exception as e:
        logging.error('%s, %s' % (user_id, booklist_id))
        logging.error(e)
        return None

def get_booklist_vote(booklist_id):
    """
    get vote result of a booklist.
    :param booklist_id: booklist id.
    :return: If success, return json format dict(keys: 'up', 'down'), else None.
    """
    try:
        up_num = DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, up_or_down='up').count()
        down_num = DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, up_or_down='down').count()

        return json.dumps({
            'up': up_num,
            'down': down_num
        })
    except Exception as e:
        logging.error(booklist_id)
        logging.error(e)
        return None


def get_book_remark(book_id, page=1, per_page=10):
    """
    get remarks of one book, remarks are organized in pages format for display convinence.
    for example, get_book_remark(1, 2, 10) returns remarks of book 1 in page 2, each page contains 10 remarks.
    :param book_id: book id.
    :param page: page number.
    :param per_page: item number per page.
    :return: If success, return json key-value format user-remark datas, else None.
    """
    try:
        user_books = DB_user_book_remark.query.filter_by(book_id=book_id).paginate(page, per_page).query
        return json.dumps(dict(
            [(get_account_by_id(user_book.user_id), user_book.remark) for user_book in user_books]
        ))
    except Exception as e:
        logging.error(book_id)
        logging.error(e)
        return None


def get_booklist_remark(booklist_id, page=1, per_page=10):
    """
    get remarks of one booklist, remarks are organized in pages format for display convinence.
    for example, get_booklist_remark(1, 2, 10) returns remarks of booklist 1 in page 2, each page contains 10 remarks.
    :param booklist_id: booklist id.
    :param page: page number.
    :param per_page: item number per page.
    :return: If success, return json key-value format user-remark datas, else None.
    """
    try:
        user_booklists = DB_user_booklist_remark.query.filter_by(booklist_id=booklist_id).paginate(page, per_page).query
        return json.dumps(dict(
            [(get_account_by_id(user_booklist.user_id), user_booklist.remark) for user_booklist in user_booklists]
        ))
    except Exception as e:
        logging.error(booklist_id)
        logging.error(e)
        return None

def get_booklist_remark_num(booklist_id):
    """
    get the number of remarks of booklist
    :param booklist_id:
    :return: number
    """
    try:
        return DB_user_booklist_remark.query.filter_by(booklist_id=booklist_id).count()
    except Exception as e:
        logging.error(booklist_id)
        logging.error(e)
        return None

def get_book_follower_num(book_id):
    """
    return number of followers of a book.
    :param book_id: book id.
    :return: If success, return followers' count, else return None.
    """
    try:
        return DB_user_book_opinion.query.filter_by(book_id=book_id, is_follow=1).count()
    except Exception as e:
        logging.error(book_id)
        logging.error(e)
        return None

def get_booklist_follower_num(booklist_id):
    """
    return number of followers of a booklist
    :param booklist_id:
    :return:
    """
    try:
        return DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id,is_follow=1).count()
    except Exception as e:
        logging.error(booklist_id)
        logging.error(e)
        return None


def get_book_followers(book_id, page=1, per_page=10):
    """
    get all users following one book, use page again.
    :param book_id: book id.
    :param page: page number.
    :param per_page: item number per page.
    :return: If success, return json format users' account names, else None.
    """
    try:
        user_books = DB_user_book_opinion.query.filter_by(book_id=book_id, is_follow=1).paginate(page, per_page).query
        return json.dumps(dict(
            [(get_account_by_id(user_book.user_id)) for user_book in user_books]
        ))
    except Exception as e:
        logging.error(book_id)
        logging.error(e)
        return None


def get_booklist_followers(booklist_id, page=1, per_page=10):
    """
    get all users following one booklist, use page again.
    :param booklist_id: booklist id.
    :param page: page number.
    :param per_page: item number per page.
    :return: If success, return json format users' account names, else None.
    """
    try:
        user_booklists = DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, is_follow=1).paginate(page,
                                                                                                                 per_page).query
        return json.dumps(dict(
            [(get_account_by_id(user_booklist.user_id)) for user_booklist in user_booklists]
        ))
    except Exception as e:
        logging.error(booklist_id)
        logging.error(e)
        return None


def user_vote_book(book_id, user_id, attitude):
    """
    user votes a book.
    :param book_id: book id.
    :param user_id: user id.
    :param attitude: string type, 'up', 'down', or 'neutral'.
    :return: If success, return True, else False.
    """
    try:
        user_vote = DB_user_book_opinion.query.filter_by(book_id=book_id, user_id=user_id)
        if user_vote is not None:
            user_vote = user_vote.first()
            user_vote.vote = attitude
            db.session.commit()
            return True
        else:
            user_vote = DB_user_book_remark(user_id=user_id, book_id=book_id, vote=attitude, is_follow=True)
            db.session.add(user_vote)
            db.session.commit()
            return True
    except Exception as e:
        logging.error('%s,%s,%s' % (book_id, user_id, attitude))
        logging.error(e)
        db.session.rollback()
        return False


def user_vote_booklist(booklist_id, user_id, attitude):
    """
    user votes a booklist.
    :param booklist_id: booklist id.
    :param user_id: user id.
    :param attitude: string type, 'up', 'down', or 'neutral'.
    :return: If success, return True, else False.
    """
    try:
        user_vote = DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, user_id=user_id)
        if user_vote is not None:
            user_vote = user_vote.first()
            user_vote.vote = attitude
            db.session.commit()
            return True
        else:
            user_vote = DB_user_booklist_remark(user_id=user_id, booklist_id=booklist_id, vote=attitude, is_follow=True)
            db.session.add(user_vote)
            db.session.commit()
            return True
    except Exception as e:
        logging.error('%s,%s,%s' % (booklist_id, user_id, attitude))
        logging.error(e)
        db.session.rollback()
        return False


def user_remark_book(book_id, user_id, remark):
    """
    user remarks a book.
    :param book_id: book id.
    :param user_id: user id.
    :param remark: remark content.
    :return: If success, return True, else False.
    """
    try:
        user_book_remark = DB_user_book_remark.query.filter_by(book_id=book_id, user_id=user_id)
        if user_book_remark is not None:
            user_book_remark = user_book_remark.first()
            user_book_remark.remark = remark
            db.session.commit()
        else:
            user_book_remark = DB_user_book_remark(user_id=user_id, book_id=book_id, remark=remark)
            db.session.add(user_book_remark)
            db.session.commit()
    except Exception as e:
        logging.error('%s,%s,%s' % (book_id, user_id, remark))
        logging.error(e)
        db.session.rollback()
        return False


def user_remark_booklist(booklist_id, user_id, remark):
    """
    user remarks a booklist.
    :param booklist_id: booklist id.
    :param user_id: user id.
    :param remark: remark content.
    :return: If success, return True, else False.
    """
    try:
        user_booklist_remark = DB_user_booklist_remark.query.filter_by(booklist_id=booklist_id, user_id=user_id)
        if user_booklist_remark is not None:
            user_booklist_remark = user_booklist_remark.first()
            user_booklist_remark.remark = remark
            db.session.commit()
        else:
            user_booklist_remark = DB_user_booklist_remark(user_id=user_id, booklist_id=booklist_id, remark=remark)
            db.session.add(user_booklist_remark)
            db.session.commit()
    except Exception as e:
        logging.error('%s,%s,%s' % (booklist_id, user_id, remark))
        logging.error(e)
        db.session.rollback()
        return False

def get_booklist_user_followed(user_id):
    """
    get booklist user followed
    :param user_id:
    :return: list of booklist_id
    """
    try:
        booklists=DB_user_booklist_opinion.query.filter_by(user_id=user_id, is_follow=1).all()
        booklist_ids=[item.booklist_id for item in booklists]
        return json.dumps(booklist_ids)
    except Exception as e:
        logging.error('%s' % (user_id))
        logging.error(e)
        return None