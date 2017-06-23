from drift_app.db_interface import db
from .db_user import get_account_by_id
import logging
import json


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
    book_remark_id = db.Column(db.Integer, db.ForeignKey('book_remark.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')

    def __repr__(self):
        return 'User %s %svoted book remark %s' % (self.user_id, self.vote, self.book_remark_id) if self.vote in ['up',
                                                                                                                  'down'] \
            else "User %s didn't vote book remark %s" % (self.user_id, self.book_remark_id)


class DB_user_booklist_remark_opinion(db.Model):
    __tablename__ = 'user_booklist_remark_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    booklist_remark_id = db.Column(db.Integer, db.ForeignKey('booklist_remark.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')

    def __repr__(self):
        return 'User %s %svoted booklist remark %s' % (
        self.user_id, self.vote, self.booklist_remark_id) if self.vote in ['up', 'down'] \
            else "User %s didn't vote booklist remark %s" % (self.user_id, self.booklist_remark_id)


def get_book_vote(book_id):
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
        logging.debug(book_id)
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
        logging.debug(book_id)
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
        logging.info(book_id)
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
        logging.info('%s,%s,%s' % (book_id, user_id, attitude))
        logging.error(e)
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
        logging.info('%s,%s,%s' % (book_id, user_id, remark))
        logging.error(e)
        return False
