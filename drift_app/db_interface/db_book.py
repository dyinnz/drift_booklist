from drift_app.db_interface import db
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
    try:
        book = DB_Book.query.filter_by(id=book_id).first()
        if book is None:
            return False
        return json.dump({
                'id':   book.id,
                'name': book.name,
                'ISBN': book.ISBN,
                'author': book.author,
                'publisher': book.publisher,
                'introduction': book.introduction
            })
    except Exception as e:
        print(book_id)
        print(e)
        return None


def get_book_tags(book_id):
    try:
        book_tags = DB_book_tag.query.filter_by(book_id=book_id).all()
        tags = (b_t.tag_name for b_t in book_tags)
    except Exception as e:
        print(book_id)
        print(e)
        return None

    return tags

def get_book_up_and_down(book_id):
    try:
        up_num = DB_user_book.query.filter_by(book_id=book_id, up_or_down='up').first()
        down_num = DB_user_book.query.filter_by(book_id=book_id, up_or_down='down').first()
        return json.dump({
            'up': up_num,
            'down': down_num
        })
    except Exception as e:
        print(book_id)
        print(e)
        return None
