# schemas.py
from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: int | None = None
    name: str
    age: int
    gender: str
    email: str
    password: str
    
    class Config:
        orm_mode = True
        
class UserCreate(UserBase):
    pass


