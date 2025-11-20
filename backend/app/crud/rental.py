# backend/app/crud/rental.py
"""
CRUD operations for Rental entity.
Handles rental creation, validation, and returns.
"""

from sqlalchemy.orm import Session
from typing import List, Optional

from ..crud.base import CRUDBase
from ..models.rental import Rental
from ..schemas.rental import RentalCreate, RentalUpdate
from ..crud.item import item as crud_item
from sqlalchemy import and_, func

class CRUDRental(CRUDBase[Rental, RentalCreate, RentalUpdate]):
    def create_with_renter(
        self, db: Session, obj_in: RentalCreate, renter_id: str
    ) -> Optional[Rental]:
        # Check if item exists and has enough stock
        db_item = crud_item.get(db, id=obj_in.item_id)
        if not db_item or db_item.available_stock < obj_in.quantity:
            return None

        # Calculate rental price
        rental_days = (obj_in.end_date - obj_in.start_date).days
        if rental_days <= 0:
            return None

        total_price = rental_days * db_item.price_per_day * obj_in.quantity

        # Create rental
        db_obj = Rental(
            renter_id=renter_id,
            item_id=obj_in.item_id,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            quantity=obj_in.quantity,
            total_price=total_price,
            is_active=True,
        )
        db.add(db_obj)

        # Decrease stock
        crud_item.decrease_stock(db, db_item.id, obj_in.quantity)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def end_rental(self, db: Session, rental_id: str) -> Optional[Rental]:
        rental = self.get(db, id=rental_id)
        if not rental or not rental.is_active:
            return None

        rental.is_active = False
        crud_item.increase_stock(db, rental.item_id, rental.quantity)

        db.add(rental)
        db.commit()
        db.refresh(rental)
        return rental

    def get_active_rentals(self, db: Session, renter_id: str) -> List[Rental]:
        return (
            db.query(Rental)
            .filter(Rental.renter_id == renter_id, Rental.is_active == True)  # noqa: E712
            .all()
        )
        
    def confirm_owner_received(self, db: Session, rental_id: str) -> Optional[Rental]:
        rental = self.get(db, id=rental_id)
        if not rental or rental.owner_received:
            return None
        rental.owner_received = True
        rental.is_active = False

        # increase stock
        crud_item.increase_stock(db, rental.item_id, rental.quantity)

        db.add(rental)
        db.commit()
        db.refresh(rental)
        return rental
    
    def create_with_availability_check(
        self,
        db: Session,
        *,
        obj_in: RentalCreate,
        renter_id: str
    ) -> Rental:
        """
        Create a rental only if enough real-time stock is available for the requested period.
        """
        # 1. Fetch the item
        item_obj = crud_item.get(db, id=obj_in.item_id)
        if not item_obj or not item_obj.is_active:
            raise ValueError("Item not found or inactive.")

        # 2. Calculate real-time available stock for requested dates
        rental_filter_conditions = [Rental.is_active == True, Rental.item_id == obj_in.item_id]
        if obj_in.start_date:
            rental_filter_conditions.append(Rental.end_date >= obj_in.start_date)
        if obj_in.end_date:
            rental_filter_conditions.append(Rental.start_date <= obj_in.end_date)

        rented_quantity = db.query(
            func.coalesce(func.sum(Rental.quantity), 0)
        ).filter(and_(*rental_filter_conditions)).scalar()

        real_available_stock = item_obj.total_stock - rented_quantity

        if obj_in.quantity > real_available_stock:
            raise ValueError("Not enough stock available for the selected period.")

        # 3. Calculate total price
        days = (obj_in.end_date - obj_in.start_date).days + 1
        total_price = days * item_obj.price_per_day * obj_in.quantity

        # 4. Create rental
        db_obj = Rental(
            renter_id=renter_id,
            item_id=obj_in.item_id,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            quantity=obj_in.quantity,
            total_price=total_price
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # 5. Reduce available_stock (optional, for faster frontend queries)
        item_obj.available_stock -= obj_in.quantity
        db.add(item_obj)
        db.commit()

        return db_obj


rental = CRUDRental(Rental)
