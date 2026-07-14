from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from .database import get_db
    from .auth import get_current_user
    from .models import Review, Book, User
    from .schemas import ReviewCreate, ReviewUpdate
except ImportError:
    from database import get_db
    from auth import get_current_user
    from models import Review, Book, User
    from schemas import ReviewCreate, ReviewUpdate

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.post("/{book_id}")
def create_review(
    book_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    book = (
        db.query(Book)
        .filter(Book.bookid == book_id)
        .first()
    )

    if not book:
        return { "Message": " Error 404  Book not found."   }
    
    existing_review = (
             db.query(Review)
            .filter(
                 Review.userid == current_user.userid,
                 Review.bookid == book_id
                )
                .first()
            )

    if existing_review:
       return {
        "Message": " Error 400 You have already reviewed this book."
    }

    new_review = Review(
        userid=current_user.userid,
        bookid=book_id,
        rating=review.rating,
        comment=review.comment,
        createdat=datetime.utcnow()
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return {
        "message": "Review added successfully.",
        "review": {
            "reviewid": new_review.reviewid,
            "rating": new_review.rating,
            "comment": new_review.comment,
            "createdat": new_review.createdat
        }
    }

@router.get("/{book_id}")
def get_reviews(
    book_id: int,
    db: Session = Depends(get_db)
):

    reviews = (
        db.query(Review)
        .filter(Review.bookid == book_id)
        .all()
    )

    results = []

    for review in reviews:

        user = (
            db.query(User)
            .filter(User.userid == review.userid)
            .first()
        )

        results.append(
            {
                "reviewid": review.reviewid,
                "username": user.username if user else None,
                "rating": review.rating,
                "comment": review.comment,
                "createdat": review.createdat
            }
        )

    return results

@router.patch("/{review_id}")
def update_review(
    review_id: int,
    updated_review: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    review = (
        db.query(Review)
        .filter(Review.reviewid == review_id)
        .first()
    )

    if not review:
        return { "Message": " Error 404  Review not found."   }
    
    if review.userid != current_user.userid:
        return { "Message": " Error 403 You can only edit your own reviews." }

    if updated_review.rating is not None:
        review.rating = updated_review.rating

    if updated_review.comment is not None:
        review.comment = updated_review.comment

    db.commit()
    db.refresh(review)

    return {
        "message": "Review updated successfully.",
        "review": {
            "reviewid": review.reviewid,
            "rating": review.rating,
            "comment": review.comment,
            "createdat": review.createdat
        }
    }

@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    review = (
        db.query(Review)
        .filter(Review.reviewid == review_id)
        .first()
    )

    if not review:
        return { "Message": " Error 404  Review not found."   }
    
    if review.userid != current_user.userid:
        return { "Message": " Error 403 You can only delete your own reviews." }

    db.delete(review)
    db.commit()

    return {
        "message": "Review deleted successfully."
    }