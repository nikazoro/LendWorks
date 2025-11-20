# backend/app/db/session.py
"""
Database session and engine setup.
Supports both SQLite and MySQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase 
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

# SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
class Base(DeclarativeBase):
    pass
