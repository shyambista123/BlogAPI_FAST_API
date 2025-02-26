import uuid
from models.base import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")