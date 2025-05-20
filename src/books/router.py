from fastapi import APIRouter, Depends

from src.books.dao import BookDAO
from src.books.schemas import SBook
from src.librarians.dependencies import get_current_user
from src.librarians.models import Librarian

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/all_books")
async def get_books(librarian: Librarian = Depends(get_current_user)):
    result = await BookDAO.get_books()
    return result

@router.post("/add_book")
async def add_book(
    book: SBook,
    librarian: Librarian = Depends(get_current_user)
):
    await BookDAO.add_book(
        title=book.title,
        author=book.author,
        publication_year=book.publication_year,
        isbn=book.isbn,
        books_count=book.books_count
    )

@router.delete("/delete_book")
async def delete_book(
    book_id: int,
    librarian: Librarian = Depends(get_current_user)
):
    await BookDAO.delete_book(book_id)

@router.patch("/update_book")
async def update_book(
    book_id: int,
    book: SBook,
    librarian: Librarian = Depends(get_current_user)
):
    await BookDAO.update_book(
        book_id,
        title=book.title,
        author=book.author,
        publication_year=book.publication_year,
        isbn=book.isbn,
        books_count=book.books_count
    )
