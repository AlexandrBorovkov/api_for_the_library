from sqlalchemy import Column, Integer, String

from src.database import Base


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
