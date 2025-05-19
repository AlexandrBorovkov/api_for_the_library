from fastapi import APIRouter

from src.exceptions import UserAlreadyExistsException
from src.librarians.auth import get_password_hash
from src.librarians.dao import LibrarianDAO
from src.librarians.schemas import SLibrarian

router = APIRouter(
    prefix="/auth",
    tags=["Библиотекари"])

@router.post("/register")
async def register_librarians(librarian_data: SLibrarian):
    existing_librarian = await LibrarianDAO.find_one_or_none(
        email=librarian_data.email
    )
    if existing_librarian:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(librarian_data.password)
    await LibrarianDAO.add(
        email=librarian_data.email,
        hashed_password=hashed_password
    )
