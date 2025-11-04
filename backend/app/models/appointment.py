from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base


class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    canceled = "canceled"


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(
        SQLEnum(AppointmentStatus, name="appointment_status", native_enum=False),
        default=AppointmentStatus.scheduled,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


