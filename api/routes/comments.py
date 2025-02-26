from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.comment import CommentCreate
from services.comment import (
    create_new_comment,
    get_comment_by_id,
    update_comment,
    delete_comment,
)
from db.database import get_db
from services.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=dict)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Creates a new comment."""
    return create_new_comment(comment, db, current_user)

@router.get("/{comment_id}", response_model=dict)
def get_comment(comment_id: str, db: Session = Depends(get_db)):
    """Fetches a comment by ID."""
    return get_comment_by_id(comment_id, db)

@router.put("/{comment_id}", response_model=dict)
def update_existing_comment(comment_id: str, comment_data: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Updates a comment (Only the owner can update)."""
    return update_comment(comment_id, comment_data, db, current_user)

@router.delete("/{comment_id}", response_model=dict)
def remove_comment(comment_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Deletes a comment (Only the owner can delete)."""
    return delete_comment(comment_id, db, current_user)
