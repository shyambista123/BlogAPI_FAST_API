from fastapi import FastAPI, Depends
from api.routes import auth, posts
from db.database import engine
from models.base import Base
from models.user import User
from models.post import Post
from models.like import Like
from models.comment import Comment
from services.auth import get_current_user, get_db
from api.middlewares import setup_middlewares
from sqlalchemy.orm import Session

app = FastAPI()

setup_middlewares(app)

'''
Create database tables if they don't exist
'''
Base.metadata.create_all(bind=engine)

'''
Including auth routes
'''
app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/posts")
def get_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    all_posts = db.query(Post).all()
    return all_posts