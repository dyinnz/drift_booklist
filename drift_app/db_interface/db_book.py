from drift_app.db_interface import db

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
