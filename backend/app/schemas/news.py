from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class NewsBase(BaseModel):
    title: str = Field(..., max_length=300)
    summary: str = ""
    url: HttpUrl
    source: str = "Sweezy"
    language: str = "uk"
    published_at: datetime
    image_url: Optional[HttpUrl] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    url: Optional[HttpUrl] = None
    source: Optional[str] = None
    language: Optional[str] = None
    published_at: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None


class NewsOut(NewsBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


