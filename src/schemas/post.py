from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from src.schemas.user import UserResponse

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    author: UserResponse

    class Config:
        orm_mode = True
