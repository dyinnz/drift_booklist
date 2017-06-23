from drift_app.db_interface import db
from drift_app.db_interface.db_user import get_account_by_id
import json
import logging


class DB_Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    ISBN = db.Column(db.String(32))
    author = db.Column(db.String(64))
    publisher = db.Column(db.String(45))
    introductionn = db.Column(db.String(256))

    def __repr__(self):
        return "Book:%s\nIntroduction:%s" % (self.name, self.introductionn)


class DB_book_tag(db.Model):
    __tablename__ = 'book_tag'
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), primary_key=True)
    tag_name = db.Column(db.String(16), db.ForeignKey("tags.name"), primary_key=True)


def get_book(book_id):
    """
    get book by book_id.
    :param book_id: book_id, int type.
    :return: If success, return book information in json format, else None.
    """
    try:
        book = DB_Book.query.filter_by(id=book_id).first()
        if book is None:
            return None
        return json.dumps({
            'id': book.id,
            'name': book.name,
            'ISBN': book.ISBN,
            'author': book.author,
            'publisher': book.publisher,
            'introduction': book.introduction
        })
    except Exception as e:
        logging.error('Exception while executing get_book()')
        logging.info(book_id)
        logging.error(e)
        return None


def get_book_by_ISBN(ISBN):
    """
    get book by book ISBN.
    :param ISBN: ISBN.
    :return: If success, return book information in json format, else None.
    """
    try:
        book = DB_Book.query.filter_by(ISBN=ISBN).first()
        if book is None:
            return None
        return json.dumps({
            'id': book.id,
            'name': book.name,
            'ISBN': book.ISBN,
            'author': book.author,
            'publisher': book.publisher,
            'introduction': book.introduction
        })
    except Exception as e:
        logging.error('Exception while executing get_book_by_ISBN()')
        logging.info(ISBN)
        logging.error(e)
        return None


def get_book_tags(book_id):
    """
    get all tags of a book.
    :param book_id: book id.
    :return: If success, return all tags of the book in json format(all tags in a single list), else None.
    """
    try:
        book_tags = DB_book_tag.query.filter_by(book_id=book_id).all()
        tags = json.dumps([b_t.tag_name for b_t in book_tags])
    except Exception as e:
        logging.error('Exception while executing get_book_tags()')
        logging.info(book_id)
        logging.error(e)
        return None

    return tags
