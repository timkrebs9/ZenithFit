import datetime
from pydantic import BaseModel, EmailStr

# User schemas
class UserBase(BaseModel):
    user_id: int | None = None
    name: str
    age: int
    gender: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime.datetime
    
    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr

class UserUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    gender: str | None = None


# Post schemas
class PostBase(BaseModel):
    post_id: int | None = None
    title: str
    content: str
    published: bool

class PostCreate(PostBase):
    pass  

class Post(PostBase):
    created_at: datetime.datetime

    class Config:
        orm_mode = True
