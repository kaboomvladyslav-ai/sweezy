from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="backend/.env", env_file_encoding="utf-8", extra="ignore")

    # App
    APP_NAME: str = "SWEEEZY Backend"
    APP_ENV: str = Field(default="development", description="environment: development|staging|production")
    APP_VERSION: str = Field(default="1.0.0")

    # CORS
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/sweeezy",
        description="SQLAlchemy database URL",
    )

    # Security
    JWT_SECRET_KEY: str = Field(default="change-me-in-production")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)

    # Demo admin (for issuing JWT tokens). In production, replace with real user store.
    ADMIN_EMAIL: str = Field(default="admin@sweeezy.app")
    ADMIN_PASSWORD: str = Field(default="admin123")

    # Sentry
    SENTRY_DSN: Optional[str] = None
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    SENTRY_PROFILES_SAMPLE_RATE: float = 0.0

    # Remote config
    REMOTE_FLAGS: dict = Field(default_factory=lambda: {"enableNewOnboarding": True})


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


