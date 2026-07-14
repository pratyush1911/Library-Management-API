from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

try:
    from .schemas import BookCreate, BookUpdate
    from .auth import get_current_admin
    from .database import get_db
    from .models import (Book as BookModel, Author, BookAuthor)
    from .helpers import link_authors_to_book
except ImportError:
    from schemas import BookCreate, BookUpdate
    from auth import get_current_admin
    from database import get_db
    from models import (Book as BookModel, Author, BookAuthor)
    from helpers import link_authors_to_book


router = APIRouter()


# Endpoint 1 - Create a Book
@router.post("/books")
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    new_book = BookModel(
        book_name=book.BookName,
        year=book.Year
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    link_authors_to_book(
    db,
    new_book.bookid,
    book.Authors
    ) 

    return {
        "message": "Book added successfully",
        "book": {
            "BookID": new_book.bookid,
            "BookName": new_book.book_name,
            "Authors": book.Authors,
            "Year": new_book.year
        }
    }


# Endpoint 2 - Get all books by an author
@router.get("/books")
def display_books(db: Session = Depends(get_db)):

    books = db.query(BookModel).all()

    results = []

    for book in books:

        authors = (
            db.query(Author.author_name)
            .join(BookAuthor, Author.authorid == BookAuthor.authorid)
            .filter(BookAuthor.bookid == book.bookid)
            .all()
        )

        results.append(
            {
                "BookID": book.bookid,
                "BookName": book.book_name,
                "Authors": [a.author_name for a in authors],
                "Year": book.year
            }
        )

    return results


# Endpoint 3 - Get a specific book by ID
@router.get("/books/{book_id}")
def specific_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = (
        db.query(BookModel)
        .filter(BookModel.bookid == book_id)
        .first()
    )

    if not book:
        return {
            "Message": " Error 404 Book ID does not exist."
        }

    authors = (
        db.query(Author.author_name)
        .join(BookAuthor, Author.authorid == BookAuthor.authorid)
        .filter(BookAuthor.bookid == book.bookid)
        .all()
    )

    return {
        "BookID": book.bookid,
        "BookName": book.book_name,
        "Authors": [a.author_name for a in authors],
        "Year": book.year
    }


# Endpoint 4 - Update an entire book
@router.put("/books/{book_id}")
def update_book(
    book_id: int,
    book: BookCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    existing_book = (
        db.query(BookModel)
        .filter(BookModel.bookid == book_id)
        .first()
    )

    if not existing_book:
        return {
            "Message": " Error 404 Book ID does not exist."
        }

    existing_book.book_name = book.BookName
    existing_book.year = book.Year

    db.commit()
    db.refresh(existing_book)

    link_authors_to_book(
        db,
        book_id,
        book.Authors
    )

    return {
        "message": "Book updated successfully",
        "book": {
            "BookID": existing_book.bookid,
            "BookName": existing_book.book_name,
            "Authors": book.Authors,
            "Year": existing_book.year
        }
    }


# Endpoint 5 - Partial book updation
@router.patch("/books/{book_id}")
def update_book_partial(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    existing_book = (
        db.query(BookModel)
        .filter(BookModel.bookid == book_id)
        .first()
    )

    if not existing_book:
        return {
            "Message": " Error 404 Book ID does not exist."
        }

    if book.BookName is not None:
        existing_book.book_name = book.BookName

    if book.Year is not None:
        existing_book.year = book.Year

    db.commit()
    db.refresh(existing_book)

    if book.Authors is not None:
        link_authors_to_book(
            db,
            book_id,
            book.Authors
        )

    authors = (
        db.query(Author.author_name)
        .join(BookAuthor, Author.authorid == BookAuthor.authorid)
        .filter(BookAuthor.bookid == book_id)
        .all()
    )

    return {
        "message": "Book updated successfully",
        "book": {
            "BookID": existing_book.bookid,
            "BookName": existing_book.book_name,
            "Authors": [a.author_name for a in authors],
            "Year": existing_book.year
        }
    }


# Endpoint 6 - Delete a book
@router.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    existing_book = (
        db.query(BookModel)
        .filter(BookModel.bookid == book_id)
        .first()
    )

    if not existing_book:
        return {
            "Message": " Error 404 Book ID does not exist."
        }

    book_authors = (
        db.query(BookAuthor)
        .filter(BookAuthor.bookid == book_id)
        .all()
    )

    for link in book_authors:
        db.delete(link)

    db.commit()

    db.delete(existing_book)
    db.commit()

    return {
        "message": "Deletion successful"
    }