from fastapi import Depends
from sqlalchemy.orm import Session
from models.like import Like
from models.user import User
from services.auth import get_current_user
from schemas.like import CreateLike

def toggle_like(like_data: CreateLike, db: Session, current_user: User = Depends(get_current_user)):
    """Toggles the like status on a post (like if not liked, unlike if already liked)."""

    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.post_id == like_data.post_id
    ).first()

    if existing_like:
        # If already liked, unlike the post
        db.delete(existing_like)
        db.commit()
        return {"message": "Post unliked successfully"}

    # If not liked, create a new like
    new_like = Like(user_id=current_user.id, post_id=like_data.post_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    return {"message": "Post liked successfully"}

def count_likes(post_id: str, db: Session):
    """Returns the total number of likes for a post."""
    
    total_likes = db.query(Like).filter(Like.post_id == post_id).count()
    return {"post_id": post_id, "likes_count": total_likes}
