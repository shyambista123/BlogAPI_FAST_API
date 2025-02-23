from models.base import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    posts = relationship("Post", back_populates="user")