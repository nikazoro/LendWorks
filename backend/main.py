# backend/app/main.py
"""
FastAPI application entry point.
Includes middleware, routers, and startup/shutdown events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .app.api.app_v1.app import api_router
from .app.db.session import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rental Gears API")

origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include API routes
app.include_router(api_router, prefix="/api/v1")
