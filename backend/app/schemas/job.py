from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class JobItem(BaseModel):
    id: str
    source: str = Field(description="indeed or rav")
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    canton: Optional[str] = None
    url: str
    posted_at: Optional[datetime] = None
    employment_type: Optional[str] = None
    salary: Optional[str] = None
    snippet: Optional[str] = None


class JobSearchResponse(BaseModel):
    items: List[JobItem]
    total: int
    sources: Dict[str, int] = {}


class JobFavoriteIn(BaseModel):
    job_id: str
    source: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    canton: Optional[str] = None
    url: str


class JobFavoriteOut(BaseModel):
    id: str
    job_id: str
    source: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    canton: Optional[str] = None
    url: str
    created_at: datetime


class JobSearchEventOut(BaseModel):
    keyword: str
    canton: Optional[str] = None
    count: int


