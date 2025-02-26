from fastapi import Depends, HTTPException, status
from models.user import User
from models.comment import Comment
from services.auth import get_current_user
from schemas.comment import CommentCreate
from sqlalchemy.orm import Session

def create_new_comment(comment: CommentCreate, db: Session, current_user: User = Depends(get_current_user)):
    """Creates a new comment."""
    new_comment = Comment(
        content=comment.content, 
        user_id=current_user.id, 
        post_id=comment.post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_comment_by_id(comment_id: str, db: Session):
    """Fetches a comment by ID."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment

def update_comment(comment_id: str, comment_data: CommentCreate, db: Session, current_user: User = Depends(get_current_user)):
    """Updates a comment (Only the owner can update)."""
    comment = get_comment_by_id(comment_id, db)
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")

    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(comment_id: str, db: Session, current_user: User = Depends(get_current_user)):
    """Deletes a comment (Only the owner can delete)."""
    comment = get_comment_by_id(comment_id, db)
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
