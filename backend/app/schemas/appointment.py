from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from ..models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_at: datetime
    duration_minutes: int = 30
    status: AppointmentStatus = AppointmentStatus.scheduled


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[AppointmentStatus] = None


class AppointmentOut(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


