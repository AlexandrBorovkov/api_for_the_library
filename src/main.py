from fastapi import FastAPI

from src.books.router import router as router_books
from src.books_issued.router import router as router_books_issued
from src.librarians.router import router as router_librarians
from src.readers.router import router as router_readers

app = FastAPI()

app.include_router(router_librarians)
app.include_router(router_books)
app.include_router(router_readers)
app.include_router(router_books_issued)
