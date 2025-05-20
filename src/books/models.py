from sqlalchemy import CheckConstraint, Column, Integer, String

from src.database import Base


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint('books_count >= 0', name='check_books_count_positive'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    books_count = Column(Integer, default=1, nullable=False)
