from drift_app.db_interface import db
from drift_app.db_interface.db_user import get_account_by_id, get_user_infos, DB_user, get_following, DB_tags, DB_user
from drift_app.db_interface.db_book import get_book_name, get_booklist_name, DB_booklist, DB_Book
from drift_app.recommender import fm_recommender, tag_recommender
import logging
import numpy as np
from datetime import datetime
from flask import json


class DB_user_book_remark(db.Model):
    __tablename__ = 'user_book_remark'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    remark = db.Column(db.String(1024))
    remark_time = db.Column(db.DateTime)

    def remark_info(self):
        account = get_account_by_id(self.user_id)
        avatar = json.loads(get_user_infos(account))['pic_src']
        timestamp = str(self.remark_time)
        book_name = get_book_name(self.book_id)
        content = '评论了书: %s : %s' % (book_name, self.remark)
        href = 'book/%s' % self.book_id
        return dict({
            'avatar': avatar,
            'account': account,
            'timestamp': timestamp,
            'content': content,
            'href': href
        })


class DB_user_book_opinion(db.Model):
    __tablename__ = 'user_book_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')
    is_follow = db.Column(db.Boolean, default=False)
    last_vote_time = db.Column(db.DateTime)
    last_follow_time = db.Column(db.DateTime)
    click_time = db.Column(db.Integer, default=0)

    def vote_info(self):
        account = get_account_by_id(self.user_id)
        avatar = json.loads(get_user_infos(account))['pic_src']
        timestamp = str(self.last_vote_time)
        book_name = get_book_name(self.book_id)
        content = '顶了书: %s' % book_name if self.vote == 'up' else '踩了书 %s' % book_name
        href = 'book/%s' % self.book_id
        return dict({
            'avatar': avatar,
            'account': account,
            'timestamp': timestamp,
            'content': content,
            'href': href
        })

    def follow_info(self):
        account = get_account_by_id(self.user_id)
        avatar = json.loads(get_user_infos(account))['pic_src']
        timestamp = str(self.last_vote_time)
        book_name = get_book_name(self.book_id)
        content = '关注了书: %s' % book_name if self.is_follow else '取关了书 %s' % book_name
        href = 'book/%s' % self.book_id
        return dict({
            'avatar': avatar,
            'account': account,
            'timestamp': timestamp,
            'content': content,
            'href': href
        })


class DB_user_booklist_remark(db.Model):
    __tablename__ = 'user_booklist_remark'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    booklist_id = db.Column(db.Integer, db.ForeignKey('booklist.id'))
    remark = db.Column(db.String(1024))
    remark_time = db.Column(db.DateTime)

    def remark_info(self):
        account = get_account_by_id(self.user_id)
        avatar = json.loads(get_user_infos(account))['pic_src']
        timestamp = str(self.remark_time)
        booklist_name = get_booklist_name(self.booklist_id)
        content = '评论了书单: %s : %s' % (booklist_name, self.remark)
        href = 'booklist/%s' % self.booklist_id
        return dict({
            'avatar': avatar,
            'account': account,
            'timestamp': timestamp,
            'content': content,
            'href': href
        })


class DB_user_booklist_opinion(db.Model):
    __tablename__ = 'user_booklist_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    booklist_id = db.Column(db.Integer, db.ForeignKey('booklist.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')
    is_follow = db.Column(db.Boolean, default=False)
    last_vote_time = db.Column(db.DateTime)
    last_follow_time = db.Column(db.DateTime)

    def vote_info(self):
        account = get_account_by_id(self.user_id)
        avatar = json.loads(get_user_infos(account))['pic_src']
        timestamp = str(self.last_vote_time)
        booklist_name = get_booklist_name(self.booklist_id)
        content = '顶了书单: %s' % booklist_name if self.vote == 'up' else '踩了书单 %s' % booklist_name
        href = 'booklist/%s' % self.booklist_id
        return dict({
            'avatar': avatar,
            'account': account,
            'timestamp': timestamp,
            'content': content,
            'href': href
        })

    def follow_info(self):
        account = get_account_by_id(self.user_id)
        avatar = json.loads(get_user_infos(account))['pic_src']
        timestamp = str(self.last_vote_time)
        booklist_name = get_booklist_name(self.booklist_id)
        content = '关注了书单: %s' % booklist_name if self.is_follow else '取关了书单 %s' % booklist_name
        href = 'booklist/%s' % self.booklist_id
        return dict({
            'avatar': avatar,
            'account': account,
            'timestamp': timestamp,
            'content': content,
            'href': href
        })


class DB_user_book_remark_opinion(db.Model):
    __tablename__ = 'user_book_remark_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_remark_id = db.Column(db.Integer, db.ForeignKey('user_book_remark.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')
    last_vote_time = db.Column(db.DateTime)

    def vote_info(self):
        account = get_account_by_id(self.user_id)
        avatar = json.loads(get_user_infos(account))['pic_src']
        timestamp = str(self.last_vote_time)
        remark = json.loads(get_book_remark_by_id(self.book_remark_id))['remark']
        content = '顶了书评: %s' % remark if self.vote == 'up' else '踩了书评 %s' % remark
        href = 'book/%s' % get_book_id_from_remark(self.book_remark_id)
        return dict({
            'avatar': avatar,
            'account': account,
            'timestamp': timestamp,
            'content': content,
            'href': href
        })


class DB_user_booklist_remark_opinion(db.Model):
    __tablename__ = 'user_booklist_remark_opinion'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    booklist_remark_id = db.Column(db.Integer, db.ForeignKey('user_booklist_remark.id'), primary_key=True)
    vote = db.Column(db.Enum('up', 'down', 'netural'), default='netural')
    last_vote_time = db.Column(db.DateTime)

    def vote_info(self):
        account = get_account_by_id(self.user_id)
        avatar = json.loads(get_user_infos(account))['pic_src']
        timestamp = str(self.last_vote_time)
        remark = json.loads(get_booklist_remark_by_id(self.booklist_remark_id))['remark']
        content = '顶了书单评论: %s' % remark if self.vote == 'up' else '踩了书单评论 %s' % remark
        href = 'booklist/%s' % get_booklist_id_from_remark(self.booklist_remark_id)
        return dict({
            'avatar': avatar,
            'account': account,
            'timestamp': timestamp,
            'content': content,
            'href': href
        })


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

def get_book_remark_num(book_id):
    try:
        return DB_user_book_remark.query.filter_by(book_id=book_id).count()
    except Exception as e:
        logging.error(book_id)
        logging.error(e)
        return None

def get_booklist_remark_num(booklist_id):
    try:
        return DB_user_booklist_remark.query.filter_by(booklist_id=booklist_id).count()
    except Exception as e:
        logging.error(booklist_id)
        logging.error(e)
        return None

def get_book_remark_by_id(id):
    try:
        remark = DB_user_book_remark.query.filter_by(id=id).one()
        if remark is not None:
            return json.dumps({
                'id': remark.id,
                'avatar': json.loads(get_user_infos(get_account_by_id(remark.user_id)))['pic_src'],
                'account': get_account_by_id(remark.user_id),
                'remark': remark.remark,
                'remark_time': remark.remark_time,
            }, ensure_ascii=False
            )
        return None
    except Exception as e:
        logging.error(id)
        logging.error(e)
        return None


def get_book_id_from_remark(remark_id):
    try:
        remark = DB_user_book_remark.query.filter_by(id=remark_id).one()
        if remark is None:
            return None
        return remark.book_id
    except Exception as e:
        logging.error(remark_id)
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
                                                                                                           per_page).items
        return json.dumps(
            [{'id': user_book.id,
              'avatar': json.loads(get_user_infos(get_account_by_id(user_book.user_id)))['pic_src'],
              'account': get_account_by_id(user_book.user_id),
              'remark': user_book.remark,
              'remark_time': user_book.remark_time} for user_book in user_books], ensure_ascii=False
        )
    except Exception as e:
        logging.error(book_id)
        logging.error(e)
        return None


def get_booklist_id_from_remark(remark_id):
    try:
        remark = DB_user_booklist_remark.query.filter_by(id=remark_id).one()
        if remark is None:
            return None
        return remark.booklist_id
    except Exception as e:
        logging.error(remark_id)
        logging.error(e)
        return None


def get_booklist_remark_by_id(id):
    try:
        remark = DB_user_booklist_remark.query.filter_by(id=id).one()
        if remark is not None:
            return json.dumps({
                'id': remark.id,
                'avatar': json.loads(get_user_infos(get_account_by_id(remark.user_id)))['pic_src'],
                'account': get_account_by_id(remark.user_id),
                'remark': remark.remark,
                'remark_time': remark.remark_time,
            }, ensure_ascii=False
            )
    except Exception as e:
        logging.error(id)
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
            'remark_time').paginate(page, per_page).items
        return json.dumps(
            [{'id': user_booklist.id,
              'avatar': json.loads(get_user_infos(get_account_by_id(user_booklist.user_id)))['pic_src'],
              'account': get_account_by_id(user_booklist.user_id),
              'remark': user_booklist.remark,
              'remark_time': user_booklist.remark_time} for user_booklist in user_booklists], ensure_ascii=False
        )
    except Exception as e:
        logging.error("get_booklist_remark(): %s", booklist_id)
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
        user_books = DB_user_book_opinion.query.filter_by(book_id=book_id, is_follow=1).paginate(page, per_page).items
        return json.dumps(dict(
            [(get_account_by_id(user_book.user_id)) for user_book in user_books], ensure_ascii=False
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
                                                                                                                 per_page).items
        return json.dumps(dict(
            [(get_account_by_id(user_booklist.user_id)) for user_booklist in user_booklists], ensure_ascii=False
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
        user_vote = DB_user_book_opinion.query.filter_by(book_id=book_id, user_id=user_id).first()
        if user_vote is not None:
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
        user_vote = DB_user_booklist_opinion.query.filter_by(booklist_id=booklist_id, user_id=user_id).first()
        if user_vote is not None:
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
        """user_book_remark = DB_user_book_remark.query.filter_by(book_id=book_id, user_id=user_id)
        if user_book_remark is not None:
            user_book_remark = user_book_remark.first()
            user_book_remark.remark = remark
            user_book_remark.remark_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            db.session.commit()
        else:"""
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
        """user_booklist_remark = DB_user_booklist_remark.query.filter_by(booklist_id=booklist_id, user_id=user_id)
        if user_booklist_remark is not None:
            user_booklist_remark = user_booklist_remark.first()
            user_booklist_remark.remark = remark
            user_booklist_remark.remark_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            db.session.commit()
        else:"""
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
                                                                                       booklist_remark_id=booklist_remark_id).first()
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


def get_user_moments(user_id, page=1, per_page=10):
    try:
        following = [f[0] for f in json.loads(get_following(user_id))]
        if len(following) == 0:
            return json.dumps([])
        # logging.debug(following)
        # sql = r"(SELECT 'u_b_r' as type, remark_time as thetime from user_book_remark WHERE remark_time IS NOT NULL UNION) " \
        #       r"(SELECT 'u_bl_r' as type, remark_time as thetime from user_booklist_remark WHERE remark_time IS NOT NULL) UNION " \
        #       r"(SELECT 'u_b_v' as type, last_vote_time as thetime from user_book_opinion WHERE remark_time IS NOT NULL) UNION " \
        #       r"(SELECT 'u_b_f' as type, last_follow_time as thetime from user_book_opinion WHERE remark_time IS NOT NULL) UNION " \
        #       r"(SELECT 'u_bl_v ' as type, last_vote_time as thetime from user_booklist_opinion WHERE remark_time IS NOT NULL) UNION " \
        #       r"(SELECT 'u_bl_f' as type, last_follow_time as thetime from user_booklist_opinion WHERE remark_time IS NOT NULL) " \
        #       r"ORDER BY thetime"
        # results = db.engine.execute(sql)
        # logging.info("raw sql results:")
        # for r in results:
        #     logging.info(r)
        # return None
        logging.debug("following: %s" % following)
        results = []
        for u_id in following:
            book_remark = DB_user_book_remark.query.filter_by(user_id=u_id).order_by(
                DB_user_book_remark.remark_time.desc()).paginate(page, per_page).items
            results.extend([(x.remark_info(), x.remark_time) for x in book_remark if x is not None])
            logging.info("fuck1")

            booklist_remark = DB_user_booklist_remark.query.filter_by(user_id=u_id).order_by(
                DB_user_booklist_remark.remark_time.desc()).paginate(page, per_page).items
            results.extend([(x.remark_info(), x.remark_time) for x in booklist_remark if x is not None])
            logging.info("fuck2")

            book_vote = DB_user_book_opinion.query.filter_by(user_id=u_id).order_by(
                DB_user_book_opinion.last_vote_time.desc()).paginate(page, per_page).items
            results.extend([(x.vote_info(), x.last_vote_time) for x in book_vote if x is not None])
            logging.info("fuck3")

            booklist_vote = DB_user_booklist_opinion.query.filter_by(user_id=u_id).order_by(
                DB_user_booklist_opinion.last_vote_time.desc()).paginate(page, per_page).items
            results.extend([(x.vote_info(), x.last_vote_time) for x in booklist_vote if x is not None])
            logging.info("fuck4")

            book_follow = DB_user_book_opinion.query.filter_by(user_id=u_id, is_follow=1).order_by(
                DB_user_book_opinion.last_follow_time.desc()).paginate(page, per_page).items
            results.extend([(x.follow_info(), x.last_follow_time) for x in book_follow if x is not None])
            logging.info("fuck5")

            booklist_follow = DB_user_booklist_opinion.query.filter_by(user_id=u_id, is_follow=1).order_by(
                DB_user_booklist_opinion.last_follow_time.desc()).paginate(page, per_page).items
            results.extend([(x.follow_info(), x.last_follow_time) for x in booklist_follow if x is not None])
            logging.info("fuck6")

            book_remark_vote = DB_user_book_remark_opinion.query.filter_by(user_id=u_id).order_by(
                DB_user_book_remark_opinion.last_vote_time.desc()).paginate(page, per_page).items
            results.extend([(x.vote_info(), x.last_vote_time) for x in book_remark_vote if x is not None])
            logging.info("fuck7")

            booklist_remark_vote = DB_user_booklist_remark_opinion.query.filter_by(user_id=u_id).order_by(
                DB_user_booklist_remark_opinion.last_vote_time.desc()).paginate(page, per_page).items
            results.extend([(x.vote_info(), x.last_vote_time) for x in booklist_remark_vote if x is not None])
            logging.info("fuck8")

        results = [x[0] for x in
                   sorted(results, key=lambda x: x[1], reverse=True)[(page - 1) * per_page:page * per_page]]
        return json.dumps(results, ensure_ascii=False)

    except Exception as e:
        logging.error('error in get_user_moments')
        logging.error('%s %s %s', user_id, page, per_page)
        logging.error(e)
        return None


def get_recommend_booklists(user_id, K=10):
    try:
        user = DB_user.query.filter_by(id=user_id).one()
        tmp = DB_user_book_opinion.query.filter_by(user_id=user_id, is_follow=1).count()
        tmp += DB_user_book_opinion.query.filter(DB_user_book_opinion.user_id == user_id).filter(DB_user_book_opinion.vote != 'neutral').count()

        booklists = DB_booklist.query.order_by(DB_booklist.id)
        n_booklists = booklists.count()
        booklists = booklists.all()
        booklist_dic = dict(zip([t.id for t in booklists], range(n_booklists)))
        books = DB_Book.query.order_by(DB_Book.id)
        n_books = books.count()
        books = books.all()
        book_dic = dict(zip([t.id for t in books], range(n_books)))

        booklist_book = np.zeros((n_booklists, n_books))
        for i, bl in enumerate(booklists):
            for b in bl.books:
                booklist_book[booklist_dic[bl.id], book_dic[b.id]] = 1
        del booklists

        if tmp < 5:
            logging.info("Using tag recommender")
            # tags
            tags = DB_tags.query.all()
            tag_dic = dict(zip((t.name for t in tags), range(len(tags))))

            book_tags = np.zeros((n_books, len(tags)))
            user_tags = np.zeros(len(tags))
            del tags

            for i, b in enumerate(books):
                for t in b.tags:
                    book_tags[i, tag_dic[t.name]] = 1
            for t in user.interests:
                user_tags[tag_dic[t.name]] = 1

            recommend_booklists = list(tag_recommender.topK_booklists(book_tags, user_tags, booklist_book, k=K))
            logging.info(type(recommend_booklists))
            return recommend_booklists
        else:
            logging.info("Using fm recommender")
            users = [t.id for t in DB_user.query.order_by(DB_user.id).all()]
            n_users = len(users)
            user_books = np.zeros((n_users, n_books))
            user_dic = dict(zip(users, range(n_users)))
            for i, u in enumerate(users):
                u_books = DB_user_book_opinion.query.filter_by(user_id=u)
                for ub in u_books:
                    if ub.is_follow:
                        user_books[i, book_dic[ub.book_id]] += 5
                    if ub.vote == 'up':
                        user_books[i, book_dic[ub.book_id]] += 10
                    elif ub.vote == 'down':
                        user_books[i, book_dic[ub.book_id]] -= 10
                    user_books[i, book_dic[ub.book_id]] += ub.click_time

            user_books += np.min(user_books)
            user_books = 1.0 / (1 + np.exp(-0.1 * user_books))

            fm_recommender.fit(user_books)
            return fm_recommender.topK_booklists(user_dic[user_id], booklist_book, 2, exclude=[1])
    except Exception as e:
        logging.error(e)
        return None



def get_recommend_booklist_by_tags(user_id, K=10):
    try:
        user = DB_user.query.filter_by(id=user_id).one()
        interests = user.interests
        d = {}
        candidates = []
        for tag in interests:
            for bl in tag.booklists:
                candidates.append(bl.id)
                up_num = DB_user_booklist_opinion.query.filter_by(booklist_id=bl.id, vote='up').count()
                d[bl.id] = get_booklist_follower_num(bl.id) + up_num
        return sorted(candidates, key=lambda x: d[x], reverse=True)[:K]
    except Exception as e:
        logging.error("error in get_recommend_booklist_by_tags()")
        logging.error(user_id)
        logging.error(e)
        return None

