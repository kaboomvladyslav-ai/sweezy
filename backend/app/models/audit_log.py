from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # create|update|delete
    entity: Mapped[str] = mapped_column(String(50), nullable=False)  # guides|templates|checklists|news|...
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    changes: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string or diff

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


