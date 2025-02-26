from pydantic import BaseModel
from uuid import UUID

class CreateLike(BaseModel):
    post_id: UUID

    class Config:
        orm_mode = True
