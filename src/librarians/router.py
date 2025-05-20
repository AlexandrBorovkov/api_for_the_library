from fastapi import APIRouter, Response

from src.exceptions import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
)
from src.librarians.auth import (
    authenticate_librarian,
    create_access_token,
    get_password_hash,
)
from src.librarians.dao import LibrarianDAO
from src.librarians.schemas import SLibrarian

router = APIRouter(
    prefix="/auth",
    tags=["Librarians"])

@router.post("/register")
async def register_librarian(librarian_data: SLibrarian):
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

@router.post("/login")
async def login_librarian(response: Response, librarian_data: SLibrarian):
    librarian = await authenticate_librarian(
        librarian_data.email,
        librarian_data.password
    )
    if not librarian:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(librarian.id)})
    response.set_cookie("user_access_token", access_token, httponly=True)
    return access_token

@router.post("/logout")
async def logout_librarian(response: Response):
    response.delete_cookie("user_access_token")
