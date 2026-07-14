from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from .database import get_db
    from .auth import get_current_user, get_current_admin
    from .models import Borrowing, Book, User
except ImportError:
    from database import get_db
    from auth import get_current_user, get_current_admin
    from models import Borrowing, Book, User

router = APIRouter(prefix="/borrowings", tags=["Borrowings"])

@router.post("/borrow/{book_id}")
def borrow_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Check whether the book exists
    book = db.query(Book).filter(
        Book.bookid == book_id
    ).first()

    if not book:
        return { "Message": " Error 404  Book not found."   }

    # Check if someone currently has the book
    active_borrowing = db.query(Borrowing).filter(
        Borrowing.bookid == book_id,
        Borrowing.returnedon == None
    ).first()

    if active_borrowing:
        return { "Message": " Error 400  Book is already borrowed."   }

    borrowing = Borrowing(
        userid=current_user.userid,
        bookid=book_id,
        borrowedon=datetime.utcnow(),
        returnedon=None
    )

    db.add(borrowing)
    db.commit()
    db.refresh(borrowing)

    return {
        "message": "Book borrowed successfully.",
        "borrowing": {
            "borrowingid": borrowing.borrowingid,
            "userid": borrowing.userid,
            "bookid": borrowing.bookid,
            "borrowedon": borrowing.borrowedon
        }
    }

@router.get("/me")
def my_borrowings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    borrowings = (
        db.query(Borrowing)
        .filter(Borrowing.userid == current_user.userid)
        .all()
    )

    return [
        {
            "borrowingid": borrowing.borrowingid,
            "userid": borrowing.userid,
            "bookid": borrowing.bookid,
            "borrowedon": borrowing.borrowedon,
            "returnedon": borrowing.returnedon
        }
        for borrowing in borrowings
    ]

@router.patch("/return/{book_id}")
def return_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    borrowing = (
        db.query(Borrowing)
        .filter(
            Borrowing.bookid == book_id,
            Borrowing.userid == current_user.userid,
            Borrowing.returnedon == None
        )
        .first()
    )

    if not borrowing:
        return { "Message": " Error 404  No active borrowing found"   }

    borrowing.returnedon = datetime.utcnow()

    db.commit()
    db.refresh(borrowing)

    return {
        "message": "Book returned successfully.",
        "returned_on": borrowing.returnedon
    }


@router.get("/")
def get_all_borrowings(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    borrowings = db.query(Borrowing).all()

    return [
        {
            "borrowingid": borrowing.borrowingid,
            "userid": borrowing.userid,
            "bookid": borrowing.bookid,
            "borrowedon": borrowing.borrowedon,
            "returnedon": borrowing.returnedon
        }
        for borrowing in borrowings
    ]