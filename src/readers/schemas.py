from pydantic import BaseModel, EmailStr


class SReader(BaseModel):
    name: str
    email: EmailStr
