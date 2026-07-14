from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

try:
    from .database import get_db
    from .auth import get_current_admin
    from .models import Author, BookAuthor, Book
    from .schemas import AuthorCreate, AuthorUpdate
except ImportError:
    from database import get_db
    from auth import get_current_admin
    from models import Author, BookAuthor, Book
    from schemas import AuthorCreate, AuthorUpdate

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

#endpoint 1 Create Author 
@router.post("/")
def create_author(
    author: AuthorCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    existing_author = (
        db.query(Author)
        .filter(Author.author_name == author.AuthorName)
        .first()
    )

    if existing_author:
        return {
            "Message": " Error 400 Author already exists."
        }

    new_author = Author(
        author_name=author.AuthorName
    )

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return {
        "message": "Author created successfully.",
        "author": {
            "AuthorID": new_author.authorid,
            "AuthorName": new_author.author_name
        }
    }

# endpoint 2 Get all authors
@router.get("/")
def get_all_authors(
    db: Session = Depends(get_db)
):

    authors = db.query(Author).all()

    return [
        {
            "AuthorID": author.authorid,
            "AuthorName": author.author_name
        }
        for author in authors
    ]

# endpoint 3 Get author by ID
@router.get("/{author_id}")
def get_author(
    author_id: int,
    db: Session = Depends(get_db)
):

    author = (
        db.query(Author)
        .filter(Author.authorid == author_id)
        .first()
    )

    if not author:
        return {
            "Message": " Error 404 Author not found."
        }

    return {
        "AuthorID": author.authorid,
        "AuthorName": author.author_name
    }

# endpoint 4 Update Author
@router.patch("/{author_id}")
def update_author(
    author_id: int,
    updated_author: AuthorUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    author = (
        db.query(Author)
        .filter(Author.authorid == author_id)
        .first()
    )

    if not author:
        return {
            "Message": " Error 404 Author not found."
        }

    if updated_author.AuthorName is not None:

        duplicate = (
            db.query(Author)
            .filter(Author.author_name == updated_author.AuthorName)
            .first()
        )

        if duplicate and duplicate.authorid != author_id:
            return {
                "Message": " Error 400 Author already exists."
            }

        author.author_name = updated_author.AuthorName

    db.commit()
    db.refresh(author)

    return {
        "message": "Author updated successfully.",
        "author": {
            "AuthorID": author.authorid,
            "AuthorName": author.author_name
        }
    }

# endpoint 5 Delete Author
@router.delete("/{author_id}")
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    author = (
        db.query(Author)
        .filter(Author.authorid == author_id)
        .first()
    )

    if not author:
        return {
            "Message": " Error 404 Author not found."
        }

    linked_books = (
        db.query(BookAuthor)
        .filter(BookAuthor.authorid == author_id)
        .first()
    )

    if linked_books:
        return {
            "Message": " Error 400 Author is linked to one or more books."
        }

    db.delete(author)
    db.commit()

    return {
        "message": "Author deleted successfully."
    }

# endpoint 6 Get all Books by an author
@router.get("/{author_id}/books")
def get_books_by_author(
    author_id: int,
    db: Session = Depends(get_db)
):

    author = (
        db.query(Author)
        .filter(Author.authorid == author_id)
        .first()
    )

    if not author:
        return {
            "Message": " Error 404 Author not found."
        }

    books = (
        db.query(Book)
        .join(BookAuthor, Book.bookid == BookAuthor.bookid)
        .filter(BookAuthor.authorid == author_id)
        .all()
    )

    return [
        {
            "BookID": book.bookid,
            "BookName": book.book_name,
            "Year": book.year
        }
        for book in books
    ]
