from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class SignupRequest(BaseModel):
    username: str
    password: str


class BookCreate(BaseModel):
    BookName: str
    Authors: list[str]
    Year: int


class BookResponse(BaseModel):
    BookID: int
    BookName: str
    Authors: list[str]
    Year: int

class BookUpdate(BaseModel):
    BookName: str | None = None
    Authors: list[str] | None = None
    Year: int | None = None

class ReviewCreate(BaseModel):
    rating: int
    comment: str


class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None


class AuthorCreate(BaseModel):
    AuthorName: str


class AuthorUpdate(BaseModel):
    AuthorName: str | None = None