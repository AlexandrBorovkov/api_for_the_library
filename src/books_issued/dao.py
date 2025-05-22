from datetime import datetime

from sqlalchemy import func, insert, select
from sqlalchemy.orm import selectinload

from src.books.models import Book
from src.books_issued.models import BorrowedBook
from src.database import async_session_maker
from src.exceptions.book_exceptions import (
    ActiveIssueWasNotFoundException,
    BookNotAvailableException,
    LimitationNumberBooksException,
    LimitPerInstanceException,
    TheBookWasNotFoundException,
)
from src.exceptions.user_exceptions import TheReaderWasNotFoundException
from src.readers.models import Reader


class BorrowedBookDAO:

    model = BorrowedBook

    @classmethod
    async def get_books_issued(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_reader_books(cls, reader_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                cls.model.reader_id == reader_id,
                cls.model.return_date.is_(None)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def borrow_book(cls, book_id, reader_id):
        async with async_session_maker() as session:
            book_query = select(Book).filter_by(id=book_id)
            book_result = await session.execute(book_query)
            book = book_result.scalar_one_or_none()
            if book is None:
                raise TheBookWasNotFoundException
            reader_query = select(Reader).filter_by(id=reader_id)
            reader = await session.execute(reader_query)
            reader = reader.scalar_one_or_none()
            if reader is None:
                raise TheReaderWasNotFoundException
            if book.books_count < 1:
                raise BookNotAvailableException
            reader_books_query = (
                select(func.count())
                .select_from(BorrowedBook)
                .where(
                    BorrowedBook.reader_id == reader_id,
                    BorrowedBook.return_date.is_(None)
                )
            )
            reader_books_count = await session.scalar(reader_books_query)
            if reader_books_count >= 3:
                raise LimitationNumberBooksException
            active_borrow_query = select(BorrowedBook).filter(
                BorrowedBook.book_id == book_id,
                BorrowedBook.reader_id == reader_id,
                BorrowedBook.return_date.is_(None)
            )
            active_borrow_result = await session.execute(active_borrow_query)
            active_borrow = active_borrow_result.scalar_one_or_none()
            if active_borrow:
                raise LimitPerInstanceException
            query = insert(cls.model).values(
                book_id=book_id,
                reader_id=reader_id,
                borrow_date=datetime.utcnow()
            )
            await session.execute(query)
            book.books_count -= 1
            await session.commit()

    @classmethod
    async def return_book(cls, book_id, reader_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter(
                    cls.model.book_id == book_id,
                    cls.model.reader_id == reader_id,
                    cls.model.return_date.is_(None)
                )
                .options(selectinload(cls.model.book)))
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if not row:
                raise ActiveIssueWasNotFoundException
            row.return_book()
            await session.commit()
