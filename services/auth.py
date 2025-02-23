from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from passlib.context import CryptContext
import re
from sqlalchemy.exc import IntegrityError
from db.database import get_db
from datetime import timedelta, timezone, datetime
from config.settings import settings
from fastapi.security import OAuth2PasswordBearer
import jwt
from schemas.token import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(password: str) -> str:
    """Hashes a plain text password."""
    return pwd_context.hash(password)


def validate_name(name: str):
    """Ensures the name only contains alphabets and spaces."""
    if not re.match("^[A-Za-z ]+$", name):
        raise ValueError("Name can only contain alphabets and spaces.")
    return name


def create_user(db: Session, user_data: UserCreate):
    """Registers a new user in the database."""
    validate_name(user_data.name)
    
    try:
        hashed_password = get_password_hash(user_data.password)
        
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user

    except IntegrityError:
        db.rollback()
        raise ValueError("Email is already registered.")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user