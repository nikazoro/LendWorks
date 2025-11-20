# backend/app/schemas/rental.py
"""
Pydantic schemas for Rental entity.
Used for request validation and response serialization.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- Shared properties ---
class RentalBase(BaseModel):
    start_date: datetime
    end_date: datetime
    quantity: int


# --- Create ---
class RentalCreate(RentalBase):
    item_id: str


# --- Update ---
class RentalUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None


# --- Database object ---
class RentalInDBBase(RentalBase):
    id: str
    renter_id: str
    item_id: str
    total_price: float
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Response model ---
class RentalResponse(RentalInDBBase):
    pass
