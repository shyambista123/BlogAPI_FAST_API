from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from services.auth import get_current_user
from schemas.post import PostCreate
from sqlalchemy.orm import Session
from db.database import get_db
from services.post import create_post, get_all_posts, update_post, delete_post
from uuid import UUID

router = APIRouter(prefix="/api", tags=["APIs"])

@router.post("/posts")
def new_post(post_data: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new post."""
    try:
        new_post = create_post(post_data, db, current_user)
        return new_post
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/posts")
def my_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get my all posts"""
    try:
        posts = get_all_posts(db, current_user)
        return posts
    except Exception as e:
        raise Exception(e)


@router.put("/posts/{post_id}")
def update_single_post(
    post_id: UUID, 
    post_update: PostCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Update a post by its ID."""
    try:
        updated_post = update_post(post_id, post_update, db, current_user)
        return updated_post
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/posts/{post_id}")
def delete_single_post(post_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a post by its ID."""
    try:
        delete_post(post_id, db, current_user)
        return {"detail": "Post deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
