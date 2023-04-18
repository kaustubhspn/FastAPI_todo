from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    due_at: Optional[datetime] = None

class Post(PostBase):
    id: int
    created_at: datetime
    due_at: Optional[datetime] = None
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


    