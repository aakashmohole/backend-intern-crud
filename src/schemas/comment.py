from pydantic import BaseModel
from datetime import datetime
from src.schemas.user import UserResponse

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    user: UserResponse

    class Config:
        orm_mode = True
