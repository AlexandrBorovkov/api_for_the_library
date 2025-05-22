from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, and_
from sqlalchemy.orm import relationship

from src.database import Base


class BorrowedBook(Base):
    __tablename__ = "borrowedbooks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="borrowedbooks")
    reader = relationship("Reader", back_populates="borrowedbooks")

    __table_args__ = (
        Index(
            'uix_book_reader_active',
            'book_id',
            'reader_id',
            unique=True,
            postgresql_where=and_(return_date.is_(None))
        ),
    )

    def return_book(self):
        self.return_date = datetime.utcnow()
        self.book.books_count += 1
