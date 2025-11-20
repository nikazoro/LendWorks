# backend/app/api/api_v1/api.py
"""
Main API v1 router that includes all endpoints.
"""

from fastapi import APIRouter

from .endpoints import auth, items, rentals

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(items.router)
api_router.include_router(rentals.router)
