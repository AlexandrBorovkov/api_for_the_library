from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from src.config import settings
from src.exceptions.user_exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from src.librarians.dao import LibrarianDAO


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        print(token)
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    librarian_id: str = payload.get("sub")
    if not librarian_id:
        raise UserIsNotPresentException
    librarian = await LibrarianDAO.find_by_id(int(librarian_id))
    if not librarian:
        raise UserIsNotPresentException
    return librarian
