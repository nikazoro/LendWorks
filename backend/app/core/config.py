"""
Application configuration using Pydantic-Settings.

Designed for production-ready deployments:
- Reads from environment variables and .env files.
- Provides sensible defaults for local development.
- Validates critical settings early to prevent runtime errors.
"""
from __future__ import annotations

from datetime import timedelta
from typing import List

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Manages all application settings.
    Reads settings from environment variables, case-insensitively.
    """

    # Define model config. This replaces the old inner `Config` class.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Environment variables are case-insensitive
    )

    # App
    APP_NAME: str = "rental-gears"
    DEBUG: bool = False
    ENV: str = "production"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    # Accepts a comma-separated string from env vars, converted to a list.
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        """Converts a comma-separated string of origins into a list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    # Database
    # A full SQLAlchemy URL is expected. E.g., for async postgres:
    # postgresql+asyncpg://user:pass@host:5432/dbname
    DATABASE_URL: str = "sqlite:///./rental_gears.db"

    # JWT / Auth
    # In Pydantic V2, fields without a default value are required.
    SECRET_KEY: str = "your-secret-key-here-change-in-production-must-be-at-least-32-chars"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    ALGORITHM: str = "HS256"

    @field_validator("SECRET_KEY")
    @classmethod
    def _validate_secret_key(cls, v: str) -> str:
        """Ensures the secret key is sufficiently long."""
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long.")
        return v

    # Password hashing
    BCRYPT_ROUNDS: int = 12

    # S3 / Object storage (S3-compatible)
    S3_ENABLED: bool = False
    S3_ENDPOINT: str | None = None
    S3_ACCESS_KEY: str | None = None
    S3_SECRET_KEY: str | None = None
    S3_BUCKET: str | None = None
    S3_REGION: str | None = None
    S3_FORCE_PATH_STYLE: bool = False  # useful for MinIO

    # Use a model_validator to check consistency between multiple fields.
    @model_validator(mode="after")
    def _validate_s3_config(self) -> "Settings":
        """If S3 is enabled, ensures all required S3 settings are present."""
        if self.S3_ENABLED:
            required = [
                "S3_ENDPOINT",
                "S3_ACCESS_KEY",
                "S3_SECRET_KEY",
                "S3_BUCKET",
            ]
            missing = [
                field for field in required if not getattr(self, field)
            ]
            if missing:
                raise ValueError(
                    f"S3 is enabled but missing required settings: {', '.join(missing)}"
                )
        return self

    # Pagination / limits
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 200

    # Security
    RATE_LIMIT_PER_MINUTE: int = 600

    # Properties to provide computed values
    @property
    def access_token_expiry(self) -> timedelta:
        """Returns the access token expiry as a timedelta object."""
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)


# Create a single, reusable instance of the settings for the application.
settings = Settings()
