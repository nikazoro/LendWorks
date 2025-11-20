# backend/app/crud/user.py
"""
CRUD operations for User entity.
Handles user creation, retrieval, update, and authentication.
"""

from sqlalchemy.orm import Session
from typing import Optional

from ..crud.base import CRUDBase
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_owner=obj_in.is_owner or False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, getattr(user, "hashed_password", "")):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return bool(user.is_active)

    def is_owner(self, user: User) -> bool:
        return bool(user.is_owner)


user = CRUDUser(User)