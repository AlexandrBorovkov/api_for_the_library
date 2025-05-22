from fastapi import APIRouter, Depends

from src.books_issued.dao import BorrowedBookDAO
from src.books_issued.schemas import SBorrowedBook
from src.librarians.dependencies import get_current_user
from src.librarians.models import Librarian

router = APIRouter(prefix="/borrowedbooks", tags=["Borrowedbooks"])

@router.get("/all_books_issued")
async def get_books_issued(librarian: Librarian = Depends(get_current_user)):
    result = await BorrowedBookDAO.get_books_issued()
    return result

@router.get("/reader_books")
async def get_reader_books(
    reader_id: int,
    librarian: Librarian = Depends(get_current_user)
):
    result = await BorrowedBookDAO.get_reader_books(reader_id)
    return result

@router.post("/borrow_book")
async def borrow_book(
    borrowedbook: SBorrowedBook,
    librarian: Librarian = Depends(get_current_user)
):
    await BorrowedBookDAO.borrow_book(
        book_id=borrowedbook.book_id,
        reader_id=borrowedbook.reader_id
    )

@router.patch("/return_book")
async def return_book(
    borrowedbook: SBorrowedBook,
    librarian: Librarian = Depends(get_current_user)
):
    await BorrowedBookDAO.return_book(
        book_id=borrowedbook.book_id,
        reader_id=borrowedbook.reader_id
    )
