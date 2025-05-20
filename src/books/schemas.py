from pydantic import BaseModel


class SBook(BaseModel):
    title: str
    author: str
    publication_year: int
    isbn: str
    books_count: int
