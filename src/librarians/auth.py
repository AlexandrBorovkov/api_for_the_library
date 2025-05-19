from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta
from jose import jwt
from src.config import settings

from src.librarians.dao import LibrarianDAO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

async def authenticate_librarian(email: EmailStr, password: str):
    librarian = await LibrarianDAO.find_one_or_none(email=email)
    if not librarian and not verify_password(password, librarian.password):
        return None
    return librarian