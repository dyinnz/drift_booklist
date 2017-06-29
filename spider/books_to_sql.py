from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    ISBN = Column(String)
    author = Column(String)
    publisher = Column(String)
    introduction = Column(String)
    cover = Column(String)


db_uri = input("Input db_uri:\nExample:mysql+pymysql://user:password@localhost:3306/database?charset=utf8\n")
engine = create_engine(db_uri, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

books = json.load(open('books.json'), encoding='utf8')
for b in books:
    book = Book(name=b['bookname'], ISBN=b['ISBN'], author=b['author'], publisher=b['publisher'], introduction=b['introduction'], cover=b['pic_src'])
    session.add(book)

try:
    session.commit()
except Exception as e:
    print(e)
    session.rollback()
