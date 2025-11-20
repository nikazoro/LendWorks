# backend/app/core/security.py
"""
Security utilities:
- Password hashing/verification
- JWT token creation/verification
- Current user dependency for FastAPI routes
"""

from datetime import datetime, timedelta
from typing import Optional, Any

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# --- Password Hashing ---
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT Handling ---
def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    if isinstance(subject, (dict, list)):
        raise ValueError("JWT subject must be a string, not dict/list")
    expire = datetime.utcnow() + (expires_delta or settings.access_token_expiry)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


# --- Dependencies ---
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
