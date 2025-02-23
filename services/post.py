from fastapi import Depends, HTTPException, status
from models.user import User
from models.post import Post
from services.auth import get_current_user
from schemas.post import PostCreate
from sqlalchemy.orm import Session

def create_post(post: PostCreate, db: Session, current_user: User = Depends(get_current_user)):
    new_post = Post(title=post.title, content=post.content, user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_post(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

def update_post(post_id: int, post_update: PostCreate, db: Session, current_user: User = Depends(get_current_user)):
    post = get_post(post_id, db)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    post.title = post_update.title
    post.content = post_update.content
    db.commit()
    db.refresh(post)
    return post

def delete_post(post_id: int, db: Session, current_user: User = Depends(get_current_user)):
    post = get_post(post_id, db)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted successfully"}

def get_all_posts(db: Session, current_user: User = Depends(get_current_user)):
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()
    return posts