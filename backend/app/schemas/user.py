# backend/app/schemas/user.py
"""
Pydantic schemas for User entity.
Used for request validation and response serialization.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- Shared properties ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_owner: Optional[bool] = False


# --- Create ---
class UserCreate(UserBase):
    password: str


# --- Update ---
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_owner: Optional[bool] = None


# --- Database object ---
class UserInDBBase(UserBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Response models ---
class UserResponse(UserInDBBase):
    pass


# --- Internal model with hashed password ---
class UserInDB(UserInDBBase):
    hashed_password: str
