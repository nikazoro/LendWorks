# backend/app/crud/item.py
"""
CRUD operations for Item entity.
Handles creation, updates, stock management, and retrieval.
"""

from sqlalchemy.orm import Session
from typing import Optional, List

from ..crud.base import CRUDBase
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemUpdate

from sqlalchemy import func, and_
from ..models.rental import Rental
from datetime import datetime


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_by_owner(self, db: Session, owner_id: str) -> List[Item]:
        return db.query(Item).filter(Item.owner_id == owner_id).all()

    def decrease_stock(self, db: Session, item_id: str, quantity: int) -> Optional[Item]:
        item = self.get(db, id=item_id)
        if item and item.available_stock >= quantity:
            item.available_stock -= quantity
            db.add(item)
            db.commit()
            db.refresh(item)
            return item
        return None

    def increase_stock(self, db: Session, item_id: str, quantity: int) -> Optional[Item]:
        item = self.get(db, id=item_id)
        if item:
            item.available_stock += quantity
            if item.available_stock > item.total_stock:
                item.available_stock = item.total_stock
            db.add(item)
            db.commit()
            db.refresh(item)
            return item
        return None
    
    def get_items_with_availability(
            self,
            db: Session,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            skip: int = 0,
            limit: int = 100,
        ) -> List[Item]:
            """
            Returns items with calculated real-time availability for the requested period.
            """
            # Define base conditions to find active rentals that overlap with the date range
            rental_filter_conditions = [Rental.is_active == True]
            if start_date:
                rental_filter_conditions.append(Rental.end_date >= start_date)
            if end_date:
                rental_filter_conditions.append(Rental.start_date <= end_date)

            # Calculate the quantity of items rented out during the period
            rented_quantity = func.sum(Rental.quantity).filter(and_(*rental_filter_conditions))

            # The main query selects the Item and calculates its available stock
            query = (
                db.query(
                    Item,
                    # Use coalesce to handle items with no rentals (where sum would be NULL)
                    (Item.total_stock - func.coalesce(rented_quantity, 0)).label(
                        "real_available_stock"
                    ),
                )
                .outerjoin(Rental, Rental.item_id == Item.id)
                .group_by(Item.id)
                .offset(skip)
                .limit(limit)
            )

            # The query returns a list of tuples: (Item, available_stock_count)
            query_results = query.all()

            # Process results to match the desired return type: List[Item]
            final_items = []
            for item_obj, available_stock in query_results:
                # Dynamically attach the calculated stock to the item object
                item_obj.real_available_stock = available_stock
                final_items.append(item_obj)

            return final_items

item = CRUDItem(Item)
