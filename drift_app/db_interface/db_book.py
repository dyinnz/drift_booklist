from drift_app.db_interface import db
from .db_user import get_account_by_id
from drift_app.db_interface import db_user as db_user
import json
import logging
from flask import jsonify


_booklist_book_table = db.Table(
    'booklist_book',
    db.Column('booklist_id', db.Integer, db.ForeignKey('booklist.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

_book_tag_table = db.Table(
    'book_tag',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('tag_name', db.String(16), db.ForeignKey('tags.name'), primary_key=True)
)

_booklist_tag_table = db.Table(
    'booklist_tag',
    db.Column('booklist_id', db.Integer, db.ForeignKey('booklist.id'), primary_key=True),
    db.Column('tag_name', db.String(16), db.ForeignKey('tags.name'), primary_key=True)
)

# class DB_booklist_tag(db.Model):
#     __tablename__ = 'booklist_tag'
#     booklist_id = db.Column(db.Integer, db.ForeignKey("booklist.id"), primary_key=True)
#     tag_name = db.Column(db.String(16), db.ForeignKey("tags.name"), primary_key=True)

class DB_Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    ISBN = db.Column(db.String(32))
    author = db.Column(db.String(64))
    publisher = db.Column(db.String(45))
    introduction = db.Column(db.String(256))
    cover = db.Column(db.String(40))
    tags = db.relationship('DB_tags', secondary=_book_tag_table, backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return "Book:%s\nIntroduction:%s" % (self.name, self.introduction)

# class DB_book_tag(db.Model):
#     __tablename__ = 'book_tag'
#     book_id = db.Column(db.Integer, db.ForeignKey("book.id"), primary_key=True)
#     tag_name = db.Column(db.String(16), db.ForeignKey("tags.name"), primary_key=True)


class DB_booklist(db.Model):
    __tablename__ = 'booklist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    introduction = db.Column(db.String(256))
    cover = db.Column(db.String(40))
    books = db.relationship('DB_Book', secondary=_booklist_book_table, backref=db.backref('booklists', lazy='dynamic'))
    tags = db.relationship('DB_tags', secondary=_booklist_tag_table, backref=db.backref('booklists', lazy='dynamic'))

    def __repr__(self):
        return 'Booklist %s created by user %s:%s' % (self.name, self.user_id, self.introduction)



# class DB_booklist_book(db.Model):
#     __tablename__ = 'booklist_book'
#     booklist_id = db.Column(db.Integer, db.ForeignKey("booklist.id"), primary_key=True)
#     book_id = db.Column(db.Integer, db.ForeignKey("book.id"), primary_key=True)
#
#     def __repr__(self):
#         return 'Book %s in booklist %s' % (self.book_id, self.booklist_id)



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
            'book_id': book.id,
            'book_name': book.name,
            'book_cover': book.cover,
            'ISBN': book.ISBN,
            'author': book.author,
            'publisher': book.publisher,
            'introduction': book.introduction
        })
    except Exception as e:
        logging.error(book_id)
        logging.error(e)
        return None


def get_book_name(book_id):
    try:
        book = DB_Book.query.filter_by(id=book_id).first()
        if book is None:
            return None
        return book.name
    except Exception as e:
        logging.error(book_id)
        logging.error(e)
        return None


def get_booklist_name(booklist_id):
    try:
        booklist = DB_booklist.query.filter_by(id=booklist_id).first()
        if booklist is None:
            return None
        return booklist.name
    except Exception as e:
        logging.error(booklist_id)
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
            'book_id': book.id,
            'book_name': book.name,
            'book_cover': book.cover,
            'ISBN': book.ISBN,
            'author': book.author,
            'publisher': book.publisher,
            'introduction': book.introduction
        })
    except Exception as e:
        logging.error(ISBN)
        logging.error(e)
        return None


def get_book_tags(book_id):
    """
    get all tags of a book.
    :param book_id: book id.
    :return: If success, return all tags of the book in json format(all tags in a single list), else None.
    """
    try:
        # book_tags = DB_book_tag.query.filter_by(book_id=book_id).all()
        book = DB_Book.query.filter_by(id=book_id).one()
        return json.dumps([t.name for t in book.tags])
    except Exception as e:
        logging.error(book_id)
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
        # booklist_tags = DB_booklist_tag.query.filter_by(booklist_id=booklist_id).all()
        booklist = DB_booklist.query.filter_by(id=booklist_id).one()
        return json.dumps([t.name for t in booklist.tags])
        # tags = json.dumps([b_t.tag_name for b_t in booklist_tags])
    except Exception as e:
        logging.error(booklist_id)
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
        booklist = DB_booklist.query.filter_by(id=booklist_id).one()
        if booklist is None:
            return None
        return json.dumps([b.id for b in booklist.books])

        # booklist_books = DB_booklist_book.query.filter_by(booklist_id=booklist_id).all()
        # book_ids = [item.book_id for item in booklist_books]
        # return json.dumps(book_ids)
    except Exception as e:
        logging.error(booklist_id)
        logging.error(e)


def upload_book(name, ISBN, author, publisher, introduction):
    """
    add a new book to database.
    :param name: book name.
    :param ISBN: ISBN number.
    :param author: author.
    :param publisher: publisher.
    :param introduction: book introduction.
    :return: If success, return new book id, else return None.
    """
    try:
        if get_book_by_ISBN(ISBN) is not None:
            return False
        book = DB_Book(name=name, ISBN=ISBN, author=author, publisher=publisher, introduction=introduction)
        db.session.add(book)
        return book.id
    except Exception as e:
        logging.error(','.join([str(x) for x in [name, ISBN, author, publisher, introduction]]))
        logging.error(e)
        db.session.rollback()
        return None


def add_booklist(user_id, booklist_name, introduction, cover):
    """
    user create a new booklist.
    :param user_id: user id.
    :param booklist_name: booklist name.
    :param introduction: introduction.
    :return: If successs, return new booklist id, else return None.
    """
    try:
        booklist = DB_booklist(user_id=user_id, name=booklist_name, introduction=introduction, cover=cover)
        db.session.add(booklist)
        db.session.commit()
        return booklist.id
    except Exception as e:
        logging.error('%s,%s,%s,%s' % (user_id, booklist_name, introduction, cover))
        logging.error(e)
        db.session.rollback()
        return None


def add_my_favorite_booklist(user_id, booklist_name, introduction, cover):
    """
    user create a new booklist.
    :param user_id: user id.
    :param booklist_name: booklist name.
    :param introduction: introduction.
    :return: If successs, return new booklist id, else return None.
    """
    try:
        booklist = DB_booklist(user_id=user_id, name=booklist_name, introduction=introduction,
                               cover=cover)
        db.session.add(booklist)
        db.session.commit()
        return booklist.id
    except Exception as e:
        logging.error('%s,%s,%s,%s' % (user_id, booklist_name, introduction, cover))
        logging.error(e)
        db.session.rollback()
        return None


def add_book_to_booklist(booklist_id, book_id):
    """
    add a book to a booklist.
    :param booklist_id: booklist id.
    :param book_id: book id.
    :return: If success, return True else False.
    """
    try:
        booklist = DB_booklist.query.filter_by(id=booklist_id).one()
        if booklist is None:
            return False
        booklist.books.append(DB_Book.query.filter_by(id=book_id).one())
        # booklist_book = DB_booklist_book(booklist_id=booklist_id, book_id=book_id)
        # db.session.add(booklist_book)
        db.session.commit()
        return True
    except Exception as e:
        logging.error('%s, %s' % (booklist_id, book_id))
        logging.error(e)
        db.session.rollback()
        return False


def move_book_from_booklist(booklist_id, book_id):
    """

    :param booklist_id:
    :param book_id:
    :return:
    """
    try:
        booklist = DB_booklist.query.filter_by(id=booklist_id).first_or_404()
        if booklist is None:
            return False
        booklist.books.remove(DB_Book.query.filter_by(id=book_id).first_or_404())
        # booklist_book = DB_booklist_book.query.filter_by(booklist_id=booklist_id, book_id=book_id).first()
        # if booklist_book is None:
        #     return False
        # db.session.delete(booklist_book)
        db.session.commit()
        return True
    except Exception as e:
        logging.error("move book false at %s %s " % (booklist_id, book_id))
        logging.error(e)
        db.session.rollback()
        return None


def get_user_created_booklist(user_id):
    """
    get my booklist
    :param user_id:
    :return: list of booklist_id
    """
    try:
        booklists = DB_booklist.query.filter_by(user_id=user_id).order_by('id').all()
        booklist_ids = [item.id for item in booklists]
        return json.dumps(booklist_ids)
    except Exception as e:
        logging.error('get booklist created by %s' % (user_id))
        logging.error(e)
        return None


def get_booklist_by_id(booklist_id):
    """
    get booklist by id
    :param booklist_id:
    :return: the infomation of booklist
    """
    try:
        booklist = DB_booklist.query.filter_by(id=booklist_id).first()
        #logging.debug(booklist_id)
        #logging.debug(booklist)
        if booklist is None:
            return None
        return json.dumps({
            'booklist_id': booklist.id,
            'booklist_name': booklist.name,
            'booklist_cover': booklist.cover,
            'create_user': get_account_by_id(booklist.user_id),
            'introduction': booklist.introduction
        })
    except Exception as e:
        logging.error("%s" % booklist_id)
        logging.error(e)
        return None


def delete_booklist(booklist_id):
    """
    delete booklist by booklist_id
    :param booklist_id: booklist_id
    :return: if success return true else return false
    """
    try:
        booklist = DB_booklist.query.filter_by(id=booklist_id).first()
        if booklist is None:
            return False
        db.session.delete(booklist)
        db.session.commit()
        return True
    except Exception as e:
        logging.error(e)
        return None


def change_booklist(booklist_id, booklist_name, booklist_cover, introduction):
    """
    uppdate the info of booklist
    :param booklist_id:
    :param booklist_name:
    :param booklist_cover:
    :param introduction:
    :return: if success return true else return false
    """
    try:
        booklist = DB_booklist.query.filter_by(id=booklist_id).first()
        if booklist is None:
            return False

        booklist.cover = booklist_cover
        booklist.introduction = introduction
        booklist.name = booklist_name
        db.session.commit()
        return True
    except Exception as e:
        logging.error("change booklist info false at %s" % (booklist_id))
        logging.error(e)
        return None


def change_booklist_tags(booklist_id, tags):
    """

    :return:
    """
    try:
        booklist = DB_booklist.query.filter_by(id=booklist_id).first_or_404()
        if len(booklist.tags)!=0:
            del booklist.tags[:]
        for tag_name in tags:
            # booklist_tag = DB_booklist_tag(booklist_id=booklist_id, tag_name=tag)
            tag = db_user.DB_tags.query.filter_by(name=tag_name).first_or_404()
            booklist.tags.append(tag)
            # db.session.add(booklist_tag)
        db.session.commit()
        return True
    except Exception as e:
        logging.error("change tags false at %s" % (booklist_id))
        logging.error(e)
        return None


def book_to_dict(book):
    return dict(
        id=book.id,
        name=book.name,
        ISBN=book.ISBN,
        author=book.author,
        publisher=book.publisher,
        introduction=book.introduction,
        cover=book.cover,
        tags=[t.name for t in book.tags]
    )


def booklist_to_dict(booklist):
    return dict(
        id=booklist.id,
        name=booklist.name,
        author=db_user.get_account_by_id(booklist.user_id),
        introduction=booklist.introduction,
        cover=booklist.cover,
        books=[book_to_dict(b) for b in booklist.books],
        tags=[t.name for t in booklist.tags],
    )


def search_keyword(keyword):
    try:
        books = DB_Book.query.filter(DB_Book.name.like('%%%s%%' % keyword)).all()
        lists = DB_booklist.query.filter(DB_booklist.name.like('%%%s%%' % keyword)).all()
        return {
            'books': [book_to_dict(b) for b in books],
            'lists': [booklist_to_dict(l) for l in lists],
        }
    except Exception as e:
        logging.error("search_book() error: %s", e)

