from sqlalchemy import Column, Integer, String

from src.database import Base


class Librarian(Base):
    __tablename__ = "librarians"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
