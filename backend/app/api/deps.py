# backend/app/api/deps.py
"""
Shared dependencies for API routes.
Handles database session and current user retrieval.
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.session import SessionLocal
from ..core.security import get_current_user_id
from ...app import crud, models


# --- DB Session Dependency ---
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Current User Dependency ---
def get_current_user(
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)
) -> models.User:
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
