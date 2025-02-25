from pydantic import BaseModel
from uuid import UUID

class CreateLike(BaseModel):
    user_id: UUID
    post_id: UUID

    class Config:
        orm_mode = True
