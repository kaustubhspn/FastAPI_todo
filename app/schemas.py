from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    """
    Pydantic model for returning user data to the client
    """
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    """
    Pydantic model for post data received from the client
    """
    title: str
    content: str


class PostCreate(PostBase):
    """
    Pydantic model for creating a new post
    """
    due_at: Optional[datetime] = None


class Post(PostBase):
    """
    Pydantic model for returning post data to the client
    """
    id: int
    created_at: datetime
    due_at: Optional[datetime] = None
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user
    """
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    """
    Pydantic model for user login
    """
    email: EmailStr
    password: str


class Token(BaseModel):
    """
    Pydantic model for returning the access token to the client
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Pydantic model for storing the data contained in the access token
    """
    id: Optional[str] = None
