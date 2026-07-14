from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP

try:
    from .database import Base
except ImportError:
    from database import Base

class Author(Base):
    __tablename__ = "authors"

    authorid = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(Text, nullable=False, unique=True)

class BookAuthor(Base):
    __tablename__ = "bookauthors"

    bookid = Column(
        Integer,
        ForeignKey("books.bookid"),
        primary_key=True
    )

    authorid = Column(
        Integer,
        ForeignKey("authors.authorid"),
        primary_key=True
    )


class Book(Base):
    __tablename__ = "books"

    bookid = Column(Integer, primary_key=True, autoincrement=True)
    book_name = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False, unique=True)
    hashed_password = Column(Text, nullable=False)
    role = Column(Text, nullable=False)


class Borrowing(Base):
    __tablename__ = "borrowings"

    borrowingid = Column(Integer, primary_key=True, autoincrement=True)
    bookid = Column(Integer, ForeignKey("books.bookid"), nullable=False)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    borrowedon = Column(TIMESTAMP)
    returnedon = Column(TIMESTAMP)


class Review(Base):
    __tablename__ = "reviews"

    reviewid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    bookid = Column(Integer, ForeignKey("books.bookid"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    createdat = Column(TIMESTAMP)
    