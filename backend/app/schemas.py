# schemas.py
from pydantic import BaseModel



class UserBase(BaseModel):
    id: int | None = None
    name: str
    age: int
    gender: str
    email: str
    password: str
    
        
class UserCreate(UserBase):
    password: str

class User(BaseModel):
    email: str