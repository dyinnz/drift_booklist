from drift_app.db_interface import db

class DB_booklist(db.Model):
    __tablename__ = 'booklist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)


class booklist_book(db.Model):
    __tablename__ = 'booklist_book'
    booklist_id = db.Column(db.Integer, db.ForeignKey("booklist.id"), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), primary_key=True)



class DB_user_booklist(db.Model):
    __tablename__ = 'user_booklist'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    booklist_id = db.Column(db.Integer, db.ForeignKey('booklist.id'), primary_key=True)
    remark = db.Column(db.String(1024), nullable=True)
    up_or_down = db.Column(db.Enum('up', 'down'), nullable=True)
    is_follow = db.Column(db.Boolean, nullable=True)


class DB_booklist_tag(db.Model):
    __tablename__ = 'booklist_tag'
    booklist_id = db.Column(db.Integer, db.ForeignKey("booklist.id"), primary_key=True)
    tag_name = db.Column(db.Integer, db.ForeignKey("tags.name"), primary_key=True)
