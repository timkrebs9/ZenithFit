from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    user_id: int | None = None
    name: str
    age: int
    gender: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass  # Inherits all attributes from UserBase


class User(BaseModel):
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    gender: str | None = None
