from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Integer

from ..core.database import Base


class RSSFeed(Base):
    __tablename__ = "rss_feeds"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    url: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    language: Mapped[str] = mapped_column(String(8), nullable=False, default="uk")
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")  # default status for imported
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    max_items: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    download_images: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_imported_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)


