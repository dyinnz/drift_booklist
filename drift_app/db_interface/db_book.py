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


class DB_booklist(db.Model):
    __tablename__ = 'booklist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    introduction = db.Column(db.String(256))

    def __repr__(self):
        return 'Booklist %s created by user %s:%s' % (self.name, self.user_id, self.introduction)


class DB_booklist_tag(db.Model):
    __tablename__ = 'booklist_tag'
    booklist_id = db.Column(db.Integer, db.ForeignKey("booklist.id"), primary_key=True)
    tag_name = db.Column(db.String(16), db.ForeignKey("tags.name"), primary_key=True)


class DB_booklist_book(db.Model):
    __tablename__ = 'booklist_book'
    booklist_id = db.Column(db.Integer, db.ForeignKey("booklist.id"), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), primary_key=True)

    def __repr__(self):
        return 'Book %s in booklist %s' % (self.book_id, self.booklist_id)


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
        logging.debug(book_id)
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
        logging.debug(ISBN)
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
        logging.debug(book_id)
        logging.error(e)
        return None

    return tags


def get_booklist_tag(booklist_id):
    """
    get all tags of a booklist.
    :param book_id: booklist id.
    :return: If success, return all tags of the booklist in json format(all tags in a single list), else None.
    """
    try:
        booklist_tags = DB_book_tag.query.filter_by(booklist_id=booklist_id).all()
        tags = json.dumps([b_t.tag_name for b_t in booklist_tags])
    except Exception as e:
        logging.debug(booklist_id)
        logging.error(e)
        return None

    return tags


def get_books_in_booklist(booklist_id):
    """
    get all books in a booklist.
    :param booklist_id: booklist id.
    :return: If success, return book objects list in json format, else None.
    """
    try:
        booklist_books = DB_booklist_book.query.filter_by(booklist_id=booklist_id).all()
        book_ids = [item.book_id for item in booklist_books]
        return json.dumps(
            [get_book(id) for id in book_ids]
        )
    except Exception as e:
        logging.debug(booklist_id)
        logging.error(e)


def add_book_to_booklist(booklist_id, book_id):
    """
    add a book to a booklist.
    :param booklist_id: booklist id.
    :param book_id: book id.
    :return: If success, return True else False.
    """
    try:
        booklist_book = DB_booklist_book(booklist_id=booklist_id, book_id=book_id)
        db.session.add(booklist_book)
        db.session.commit()
        return True
    except Exception as e:
        logging.debug('%s, %s' % (booklist_id, book_id))
        logging.error(e)
        db.session.rollback()
        return False
