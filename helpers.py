from sqlalchemy.orm import Session

try:
    from .models import Author, BookAuthor
except ImportError:
    from models import Author, BookAuthor


def link_authors_to_book(
    db: Session,
    book_id: int,
    authors: list[str]
):

    old_links = (
        db.query(BookAuthor)
        .filter(BookAuthor.bookid == book_id)
        .all()
    )

    for link in old_links:
        db.delete(link)

    db.commit()

    for author_name in set(authors):

        author = (
            db.query(Author)
            .filter(Author.author_name == author_name)
            .first()
        )

        if not author:

            author = Author(
                author_name=author_name
            )

            db.add(author)
            db.commit()
            db.refresh(author)

        db.add(
            BookAuthor(
                bookid=book_id,
                authorid=author.authorid
            )
        )

    db.commit()