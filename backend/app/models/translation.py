from __future__ import annotations

from datetime import datetime
from uuid import uuid4
from typing import Optional

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base


class Translation(Base):
    __tablename__ = "translations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    entity: Mapped[str] = mapped_column(String(50), nullable=False)  # guides|templates|checklists|news
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    language: Mapped[str] = mapped_column(String(8), nullable=False)  # uk|ru|en
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")  # pending|approved|rejected
    title: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    content: Mapped[Optional[str]] = mapped_column(Text)
    author_email: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


