from pydantic import BaseModel

class PostCreate(BaseModel):
    title : str
    content : str

    class Config:
        orm_mode = True