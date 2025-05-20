from sqlalchemy import insert, select

from src.books.models import Book
from src.database import async_session_maker


class BookDAO:

    model = Book

    @classmethod
    async def get_books(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_book(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_book(cls, book_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == book_id)
            row = await session.execute(query)
            row = row.scalar_one()
            await session.delete(row)
            await session.commit()

    @classmethod
    async def update_book(cls, book_id, **data):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == book_id)
            row = await session.execute(query)
            row = row.scalar_one()
            for key, value in data.items():
                setattr(row, key, value)
            await session.commit()
