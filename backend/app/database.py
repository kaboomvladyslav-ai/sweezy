from __future__ import annotations

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def _coerce_async_url(url: str) -> str:
    """Ensure async driver is used when needed.

    - postgresql -> postgresql+asyncpg
    - sqlite (no driver) -> sqlite+aiosqlite
    Otherwise return as-is.
    """
    if url.startswith("postgresql+asyncpg"):
        return url
    if url.startswith("postgresql"):
        return url.replace("postgresql+psycopg2", "postgresql+asyncpg").replace(
            "postgresql://", "postgresql+asyncpg://", 1
        )
    if url.startswith("sqlite+aiosqlite"):
        return url
    if url.startswith("sqlite"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return url


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data.db")
ASYNC_DATABASE_URL = _coerce_async_url(DATABASE_URL)

engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


