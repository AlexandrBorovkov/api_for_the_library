from pydantic import BaseModel, conint


class SBook(BaseModel):
    title: str
    author: str
    publication_year: int
    isbn: str
    books_count: conint(ge=0)
