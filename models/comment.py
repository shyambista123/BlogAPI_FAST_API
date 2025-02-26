import uuid
from .base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, index=True)
    post_id = Column(UUID, ForeignKey("posts.id"))
    user_id = Column(UUID, ForeignKey("users.id"))
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
