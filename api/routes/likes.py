from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.like import CreateLike
from services.like import toggle_like, count_likes
from db.database import get_db
from services.auth import get_current_user
from models.user import User

router = APIRouter(tags=["Likes"])

@router.post("/likes", response_model=dict)
def like_unlike_post(like_data: CreateLike, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Likes or unlikes a post depending on its current state."""
    return toggle_like(like_data, db, current_user)

@router.get("/likes/{post_id}/count", response_model=dict)
def get_like_count(post_id: str, db: Session = Depends(get_db)):
    """Returns the total number of likes for a post."""
    return count_likes(post_id, db)
