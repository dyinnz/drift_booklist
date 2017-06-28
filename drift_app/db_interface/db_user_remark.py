from drift_app.db_interface import db
from .db_user import get_account_by_id, get_user_infos
import logging
from datetime import datetime
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
    last_vote_time = db.Column(db.DateTime)
    last_follow_time = db.Column(db.DateTime)

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
    last_vote_time = db.Column(db.DateTime)
    last_follow_time = db.Column(db.DateTime)

    def __repr__(self):
        return 'User %s %svoted booklist %s' % (self.user_id, self.vote, self.booklist_id) if self.vote in ['up',
                                                                                                            'down'] \
            else "User %s didn't vote booklist %s" % (self.user_id, self.booklist_id)


class DB_user_book_remark_opinion(db.Model):
    __tablename__ = 'user_book_remark_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_remark_id = db.Column(db.Integer, db.ForeignKey('user_book_remark.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')
    last_vote_time = db.Column(db.DateTime)

    def __repr__(self):
        return 'User %s %svoted book remark %s' % (self.user_id, self.vote, self.book_remark_id) if self.vote in ['up',
                                                                                                                  'down'] \
            else "User %s didn't vote book remark %s" % (self.user_id, self.book_remark_id)


class DB_user_booklist_remark_opinion(db.Model):
    __tablename__ = 'user_booklist_remark_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    booklist_remark_id = db.Column(db.Integer, db.ForeignKey('user_booklist_remark.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')
    last_vote_time = db.Column(db.DateTime)

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
        up_num = DB_user_book_opinion.query.filter_by(book_id=book_id, vote='up').count()
        down_num = DB_user_book_opinion.query.filter_by(book_id=book_id, vote='down').count()

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
            return json.dumps(['neutral', False])
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
            return json.dumps(['neutral', False])
        return json.dumps([opinion.vote, opinion.is_follow])
    except Exception as e:
        logging.error('get booklist opinion %s, %s' % (user_id, booklist_id))
        logging.error(e)
        return None


def get_booklist_vote(booklist_id):
    """
    get vote result of a booklist.
    :param booklist_id: booklist id.
    :return: If success, return json format dict(keys: 'up', 'down'), else None.
    """
    try:
        up_num = DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, vote='up').count()
        down_num = DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, vote='down').count()

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
        user_books = DB_user_book_remark.query.filter_by(book_id=book_id).order_by('-remark_time').paginate(page,
                                                                                                            per_page).query
        return json.dumps(
            [{'id': user_book.id, 'avatar': json.loads(get_user_infos(get_account_by_id(user_book.user_id)))['pic_src'],
              'account': get_account_by_id(user_book.user_id), 'remark': user_book.remark,
              'remark_time': user_book.remark_time} for user_book in user_books]
        )
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
        user_booklists = DB_user_booklist_remark.query.filter_by(booklist_id=booklist_id).order_by(
            '-remark_time').paginate(page, per_page).query
        return json.dumps(
            [{'id': user_booklist.id,
              'avatar': json.loads(get_user_infos(get_account_by_id(user_booklist.user_id)))['pic_src'],
              'account': get_account_by_id(user_booklist.user_id), 'remark': user_booklist.remark,
              'remark_time': user_booklist.remark_time} for user_booklist in user_booklists]
        )
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
        return DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, is_follow=1).count()
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
    :param attitude: string type, 'up', 'down', or 'netural'.
    :return: If success, return True, else False.
    """
    try:
        user_vote = DB_user_book_opinion.query.filter_by(book_id=book_id, user_id=user_id)
        if user_vote is not None:
            user_vote = user_vote.first()
            user_vote.vote = attitude
            user_vote.last_vote_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            db.session.commit()
            return True
        else:
            current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_vote = DB_user_book_opinion(user_id=user_id, book_id=book_id, vote=attitude, is_follow=False,
                                             last_vote_time=current_time)
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
    :param attitude: string type, 'up', 'down', or 'netural'.
    :return: If success, return True, else False.
    """
    try:
        user_vote = DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, user_id=user_id)
        if user_vote is not None:
            user_vote = user_vote.first()
            user_vote.vote = attitude
            user_vote.last_vote_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            db.session.commit()
            return True
        else:
            current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_vote = DB_user_booklist_opinion(user_id=user_id, booklist_id=booklist_id, vote=attitude,
                                                 is_follow=False, last_vote_time=current_time)
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
            user_book_remark.remark_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            db.session.commit()
        else:
            current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_book_remark = DB_user_book_remark(user_id=user_id, book_id=book_id, remark=remark,
                                                   remark_time=current_time)
            db.session.add(user_book_remark)
            db.session.commit()
        return True
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
            user_booklist_remark.remark_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            db.session.commit()
        else:
            current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_booklist_remark = DB_user_booklist_remark(user_id=user_id, booklist_id=booklist_id, remark=remark,
                                                           remark_time=current_time)
            db.session.add(user_booklist_remark)
            db.session.commit()
        return True
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
        booklists = DB_user_booklist_opinion.query.filter_by(user_id=user_id, is_follow=1).all()
        booklist_ids = [item.booklist_id for item in booklists]
        return json.dumps(booklist_ids)
    except Exception as e:
        logging.error('%s' % (user_id))
        logging.error(e)
        return None


def get_books_user_followed(user_id):
    """

    :param user_id:
    :return:
    """
    try:
        book_ids = DB_user_book_opinion.query.filter_by(user_id=user_id, is_follow=1).all()
        return json.dumps([item.book_id for item in book_ids])
    except Exception as e:
        logging.error('%s' % (user_id))
        logging.error(e)
        return None


def set_booklist_follow(user_id, booklist_id, is_follow):
    """

    :return:
    """
    try:
        user_vote = DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, user_id=user_id).first()
        if user_vote is None:
            current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_booklist_follow = DB_user_booklist_opinion(user_id=user_id, booklist_id=booklist_id,
                                                            is_follow=is_follow, last_follow_time=current_time)
            db.session.add(user_booklist_follow)
            db.session.commit()
        else:
            user_vote.is_follow = is_follow
            user_vote.last_follow_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            db.session.commit()
        return True
    except Exception as e:
        logging.error('set follow %s' % (booklist_id))
        logging.error(e)
        return None


def set_book_follow(user_id, book_id, is_follow):
    """

    :return:
    """
    try:
        user_vote = DB_user_book_opinion.query.filter_by(book_id=book_id, user_id=user_id).first()
        if user_vote is None:
            current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            user_book_follow = DB_user_book_opinion(user_id=user_id, book_id=book_id, is_follow=is_follow,
                                                    last_follow_time=current_time)
            db.session.add(user_book_follow)
            db.session.commit()
        else:
            user_vote.is_follow = is_follow
            user_vote.last_follow_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            db.session.commit()
        return True
    except Exception as e:
        logging.error('set follow %s' % (book_id))
        logging.error(e)
        return None


def get_book_remark_vote_num(book_remark_id):
    """

    :param book_remark_id:
    :return:
    """
    try:
        return json.dumps({
            'up': DB_user_book_remark_opinion.query.filter_by(book_remark_id=book_remark_id, vote='up').count(),
            'down': DB_user_book_remark_opinion.query.filter_by(book_remark_id=book_remark_id, vote='down').count()
        })
    except Exception as e:
        logging.error("get vote num false at %s" % (book_remark_id))
        logging.error(e)
        return None


def get_booklist_remark_vote_num(booklist_remark_id):
    """

    :return:
    """
    try:
        return json.dumps({
            'up': DB_user_booklist_remark_opinion.query.filter_by(booklist_remark_id=booklist_remark_id,
                                                                  vote='up').count(),
            'down': DB_user_booklist_remark_opinion.query.filter_by(booklist_remark_id=booklist_remark_id,
                                                                    vote='down').count()
        })
    except Exception as e:
        logging.error("get vote num false at %s" % (booklist_remark_id))
        logging.error(e)
        return None


def get_user_book_remark_opinion(user_id, book_remark_id):
    """"""
    try:
        user_book_remark_opinion = DB_user_book_remark_opinion.query.filter_by(user_id=user_id,
                                                                               book_remark_id=book_remark_id).first()
        if user_book_remark_opinion is None:
            return 'netural'
        else:
            return user_book_remark_opinion.vote
    except Exception as e:
        logging.error("get opinion false at %s" % (book_remark_id))
        logging.error(e)
        return None


def get_user_booklist_remark_opinion(user_id, booklist_remark_id):
    """"""
    try:
        user_booklist_remark_opinion = DB_user_booklist_remark_opinion.query.filter_by(user_id=user_id,
                                                                                       booklist_remark_id=booklist_remark_id).first();
        if user_booklist_remark_opinion is None:
            return 'netural'
        else:
            return user_booklist_remark_opinion.vote
    except Exception as e:
        logging.error("get opinion false at %s" % (booklist_remark_id))
        logging.error(e)
        return None


def user_vote_book_remark(user_id, book_remark_id, attitude):
    """"""
    try:
        user_book_remark_vote = DB_user_book_remark_opinion.query.filter_by(user_id=user_id,
                                                                            book_remark_id=book_remark_id).first()
        current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        if user_book_remark_vote is None:
            user_book_remark_vote = DB_user_book_remark_opinion(user_id=user_id, book_remark_id=book_remark_id,
                                                                vote=attitude, last_vote_time=current_time)
            user_book_remark_vote.last_vote_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            db.session.add(user_book_remark_vote)
            db.session.commit()
            return True
        else:
            user_book_remark_vote.vote = attitude
            user_book_remark_vote.last_vote_time = current_time
            db.session.commit()
            return True
    except Exception as e:
        logging.error("vote book remark false at %s" % (book_remark_id))
        logging.error(e)
        db.session.rollback()
        return None


def user_vote_booklist_remark(user_id, booklist_remark_id, attitude):
    """"""
    try:
        user_booklist_remark_vote = DB_user_booklist_remark_opinion.query.filter_by(user_id=user_id,
                                                                                    booklist_remark_id=booklist_remark_id).first()
        current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        if user_booklist_remark_vote is None:
            user_booklist_remark_vote = DB_user_booklist_remark_opinion(user_id=user_id,
                                                                        booklist_remark_id=booklist_remark_id,
                                                                        vote=attitude, last_vote_time=current_time)
            db.session.add(user_booklist_remark_vote)
            db.session.commit()
            return True
        else:
            user_booklist_remark_vote.vote = attitude
            user_booklist_remark_vote.last_vote_time = current_time
            db.session.commit()
            return True
    except Exception as e:
        logging.error("vote book remark false at %s" % (booklist_remark_id))
        logging.error(e)
        db.session.rollback()
        return None

