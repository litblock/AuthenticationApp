import uuid

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime



# noinspection PyMethodParameters
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator("username")
    def username_must_be_longer_than_three_characters(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be longer than 3 characters")
        return v

    @validator("password")
    def password_must_be_longer_than_three_characters(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be longer than 8 characters")
        return v


class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    date_created: datetime

    class Config:
        orm_mode = True
