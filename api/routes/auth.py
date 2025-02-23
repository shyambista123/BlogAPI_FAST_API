from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user import UserCreate, LoginRequest
from models.user import User
from services.auth import create_user, authenticate_user, create_access_token, get_current_user
from config.settings import settings
from datetime import timedelta
from schemas.token import Token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserCreate)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user if email is unique."""
    try:
        new_user = create_user(db, user_data)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# @router.get("/users")
# def get_user(db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: LoginRequest, db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response):
    """Logs out the user by clearing the session cookie"""
    # Clear the session cookie by setting it to an empty value and making it expire
    response.delete_cookie("access_token")  # Or whatever cookie you're using

    return JSONResponse(content={"message": "Logout successful"}, status_code=200)