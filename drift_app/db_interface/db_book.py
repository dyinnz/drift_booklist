from drift_app.db_interface import db
from drift_app.db_interface.db_user import get_account_by_id
import json

class DB_Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ISBN = db.Column(db.String(32))
    author = db.Column(db.String(64))
    publisher = db.Column(db.String(45))
    introductionn = db.Column(db.String(256))

    def __repr__(self):
        return "Book:%s\nIntroduction:%s" % (self.name, self.introductionn)


class DB_user_book(db.Model):
    __tablename__ = 'user_book'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    remark = db.Column(db.String(1024), nullable=True)
    up_or_down = db.Column(db.Enum('up', 'down'), nullable=True)
    is_follow = db.Column(db.Boolean, nullable=True)


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
            return False
        return json.dumps({
                'id':   book.id,
                'name': book.name,
                'ISBN': book.ISBN,
                'author': book.author,
                'publisher': book.publisher,
                'introduction': book.introduction
            })
    except Exception as e:
        print("Exception while getting book by book id.")
        print(book_id)
        print(e)
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
        print("Exception while getting book tags.")
        print(book_id)
        print(e)
        return None

    return tags

def get_book_up_and_down(book_id):
    """
    get up and down numbers of a book.
    :param book_id: book id.
    :return: If success, return json format dict(keys: 'up', 'down'), else None.
    """
    try:
        up_num = len(DB_user_book.query.filter_by(book_id=book_id, up_or_down='up').all())
        down_num = len(DB_user_book.query.filter_by(book_id=book_id, up_or_down='down').all())
        return json.dumps({
            'up': up_num,
            'down': down_num
        })
    except Exception as e:
        print("Exception while getting book up and down.")
        print(book_id)
        print(e)
        return None


def get_book_remark(book_id, page=1, per_page=10):
    """
    get some book remarks of one book, for example, get_book_remark(1, 20, 10) get remark20 to remark30 of book 1.
    :param book_id: book id.
    :param start: start index
    :param count: remark count number.
    :return:
    """
    try:
        user_books = DB_user_book.query.filter_by(book_id=book_id).paginate(page, per_page).query
        return json.dumps(dict(
            [(get_account_by_id(user_book.user_id), user_book.remark) for user_book in user_books]
        ))
    except Exception as e:
        print("Exception while getting book remark.")
        print(book_id)
        print(e)
        return None

