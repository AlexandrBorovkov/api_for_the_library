from pydantic import BaseModel


class SBorrowedBook(BaseModel):
    book_id: int
    reader_id: int
