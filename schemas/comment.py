from pydantic import BaseModel
from uuid import UUID

class CommentCreate(BaseModel):
    content : str
    post_id : UUID
    user_id : UUID

    class Config:
        orm_mode = True