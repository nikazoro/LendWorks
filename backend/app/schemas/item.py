# backend/app/schemas/item.py
"""
Pydantic schemas for Item entity.
Used for request validation and response serialization.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- Shared properties ---
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_day: float
    total_stock: int
    available_stock: int
    is_active: Optional[bool] = True


# --- Create ---
class ItemCreate(ItemBase):
    pass


# --- Update ---
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_per_day: Optional[float] = None
    total_stock: Optional[int] = None
    available_stock: Optional[int] = None
    is_active: Optional[bool] = None


# --- Database object ---
class ItemInDBBase(ItemBase):
    id: str
    owner_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Response model ---
class ItemResponse(ItemInDBBase):
    real_available_stock: Optional[int] = None
