from __future__ import annotations

from datetime import datetime
from uuid import uuid4
from typing import Optional

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base


class GlossaryTerm(Base):
    __tablename__ = "glossary_terms"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    term: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    uk: Mapped[Optional[str]] = mapped_column(String(255))
    ru: Mapped[Optional[str]] = mapped_column(String(255))
    en: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


