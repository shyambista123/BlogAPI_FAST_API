from pydantic import BaseModel, EmailStr, field_validator
import re

class UserBase(BaseModel):
    name : str
    email : EmailStr

    class Config:
        orm_mode = True
        
class UserCreate(UserBase):
    password : str

    @field_validator("password")
    def validate_password(cls, password: str):
        """Validates that the password meets the required criteria."""
        if not re.search(r"[A-Za-z]", password):
            raise ValueError("Password must contain at least one letter.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[@$!%*?&]", password):
            raise ValueError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return password

class LoginRequest(BaseModel):
    email : str
    password : str