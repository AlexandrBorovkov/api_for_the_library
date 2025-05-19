from pydantic import BaseModel, EmailStr


class SLibrarian(BaseModel):
    email: EmailStr
    password: str
