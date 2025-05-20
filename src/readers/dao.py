from sqlalchemy import insert, select

from src.database import async_session_maker
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
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_reader(cls, reader_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == reader_id)
            row = await session.execute(query)
            row = row.scalar_one()
            await session.delete(row)
            await session.commit()

    @classmethod
    async def update_reader(cls, reader_id, **data):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == reader_id)
            row = await session.execute(query)
            row = row.scalar_one()
            for key, value in data.items():
                setattr(row, key, value)
            await session.commit()

    @classmethod
    async def find_by_id(cls, reader_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=reader_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
