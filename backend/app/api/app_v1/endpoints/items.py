# backend/app/api/api_v1/endpoints/items.py
"""
Item endpoints: CRUD operations for rental items.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ....schemas.item import ItemCreate, ItemUpdate, ItemResponse
from ....api.deps import get_db, get_current_user
from backend.app import crud
from ....models.user import User
from datetime import datetime

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemResponse)
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can create items",
        )
    db_item = crud.item.create(db, obj_in=item_in)
    # Associate with owner
    db_item.owner_id = current_user.id
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[ItemResponse])
def list_items(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    # Fetch items with real_available_stock attached
    items_with_stock = crud.item.get_items_with_availability(
        db, start_date=start_date, end_date=end_date, skip=skip, limit=limit
    )

    # Convert to response schema using model_validate
    result = []
    for item_obj in items_with_stock:
        item_data = ItemResponse.model_validate(item_obj).model_dump()
        result.append(item_data)

    return result



@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    item = crud.item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: str,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = crud.item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
    updated_item = crud.item.update(db, db_obj=item, obj_in=item_in)
    return updated_item


@router.delete("/{item_id}", response_model=ItemResponse)
def delete_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = crud.item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")
    deleted_item = crud.item.remove(db, id=item_id)
    return deleted_item
