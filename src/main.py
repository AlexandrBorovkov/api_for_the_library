from fastapi import FastAPI

from src.librarians.router import router as router_librarians

app = FastAPI()

app.include_router(router_librarians)
