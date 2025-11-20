# backend/app/api/api_v1/endpoints/rentals.py
"""
Rental endpoints: create rental, list active rentals, end rental.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....schemas.rental import RentalCreate, RentalResponse
from ....api.deps import get_db, get_current_user
from backend.app import crud
from ....models.user import User

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.post("/", response_model=RentalResponse)
def create_rental(
    rental_in: RentalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rental_obj = crud.rental.create_with_availability_check(
        db, obj_in=rental_in, renter_id=current_user.id
    )
    if not rental_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item not available for requested quantity/dates",
        )
    return rental_obj


@router.get("/active", response_model=List[RentalResponse])
def list_active_rentals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rentals = crud.rental.get_active_rentals(db, renter_id=current_user.id)
    return rentals


@router.post("/{rental_id}/end", response_model=RentalResponse)
def end_rental(
    rental_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rental_obj = crud.rental.get(db, id=rental_id)
    if not rental_obj or rental_obj.renter_id != current_user.id:
        raise HTTPException(status_code=404, detail="Rental not found")
    ended_rental = crud.rental.end_rental(db, rental_id=rental_id)
    return ended_rental

@router.post("/{rental_id}/confirm", response_model=RentalResponse)
def confirm_received(
    rental_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rental_obj = crud.rental.get(db, id=rental_id)
    if not rental_obj:
        raise HTTPException(status_code=404, detail="Rental not found")
    if rental_obj.item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can confirm receipt")
    
    confirmed_rental = crud.rental.confirm_owner_received(db, rental_id=rental_id)
    return confirmed_rental