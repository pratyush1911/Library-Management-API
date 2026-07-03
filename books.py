from fastapi import APIRouter, HTTPException, Depends
from .models import Book
from .auth import get_current_admin

router=APIRouter()

Books = []

# Endpoint 1 - Create a Book
@router.post("/books")
def create_book(book: Book, current_admin = Depends(get_current_admin)):
    for existing_book in Books:
        if book.BookID == existing_book.BookID:
            raise HTTPException(status_code=409, detail="Book ID already exists")

    Books.append(book)

    return {
        "message": "Book added successfully",
        "book": book
    }


# Endpoint 2 - Get all books by an author
@router.get("/books")
def display_books(author: str):
    author_books = []

    for book in Books:
        if book.Author == author:
            author_books.append(book)

    if not author_books:
        raise HTTPException(status_code=404, detail="Author not found")

    return author_books


# Endpoint 3 - Get a specific book by ID
@router.get("/books/{book_id}")
def specific_book(book_id: int):
    for existing_book in Books:
        if existing_book.BookID == book_id:
            return existing_book

    raise HTTPException(status_code=404, detail="Book ID does not exist")


# Endpoint 4 - Update an entire book
@router.put("/books/{book_id}")
def update_book(book_id: int, book: Book, current_admin = Depends(get_current_admin)):
    for existing_book in Books:
        if existing_book.BookID == book_id:
            existing_book.BookName = book.BookName
            existing_book.Author = book.Author
            existing_book.Year = book.Year
            return {
                "message": "Book updated successfully",
                "book": existing_book
            }

    raise HTTPException(status_code=404, detail="Book ID does not exist")


# Endpoint 5 - Update only the book name
@router.patch("/books/{book_id}")
def name_change(book_id: int, bookname: str, current_admin = Depends(get_current_admin)):
    for existing_book in Books:
        if existing_book.BookID == book_id:
            existing_book.BookName = bookname
            return {
                "message": "Book name updated successfully",
                "book": existing_book
            }

    raise HTTPException(status_code=404, detail="Book ID does not exist")


# Endpoint 6 - Delete a book
@router.delete("/books/{book_id}")
def delete_book(book_id: int, current_admin = Depends(get_current_admin)):
    for existing_book in Books:
        if existing_book.BookID == book_id:
            Books.remove(existing_book)
            return {"message": "Deletion successful"}

    raise HTTPException(status_code=404, detail="Book ID does not exist")
