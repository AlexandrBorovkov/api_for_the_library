from sqlalchemy import insert, select

from src.database import async_session_maker
from src.exceptions.user_exceptions import (
    TheReaderAlreadyExistsException,
    TheReaderWasNotFoundException,
)
from src.readers.models import Reader


class ReaderDAO:

    model = Reader

    @classmethod
    async def get_readers(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_reader(cls, **data):
        async with async_session_maker() as session:
            active_reader_query = select(cls.model).filter(
                cls.model.email == data["email"]
            )
            active_reader = await session.execute(active_reader_query)
            active_reader = active_reader.scalar_one_or_none()
            if active_reader:
                raise TheReaderAlreadyExistsException
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_reader(cls, reader_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == reader_id)
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if row is None:
                raise TheReaderWasNotFoundException
            await session.delete(row)
            await session.commit()

    @classmethod
    async def update_reader(cls, reader_id: int, **data):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == reader_id)
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if row is None:
                raise TheReaderWasNotFoundException
            for key, value in data.items():
                setattr(row, key, value)
            await session.commit()

    @classmethod
    async def show_reader(cls, reader_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=reader_id)
            row = await session.execute(query)
            row = row.scalar_one_or_none()
            if row is None:
                raise TheReaderWasNotFoundException
            return row
