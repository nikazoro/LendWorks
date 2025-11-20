# backend/app/api/api_v1/endpoints/auth.py
"""
Authentication routes: signup, login, JWT token issuance.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from ....schemas.user import UserCreate, UserResponse
from ....core.security import create_access_token
from ....api.deps import get_db
from backend.app import crud
from ....core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.post("/login")
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = crud.user.authenticate(db, email=user_in.email, password=user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.id, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
