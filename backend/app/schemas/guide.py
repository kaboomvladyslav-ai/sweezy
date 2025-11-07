from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class GuideBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_published: bool = True
    version: int = 1


class GuideCreate(GuideBase):
    pass


class GuideUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_published: Optional[bool] = None
    version: Optional[int] = None


class GuideOut(GuideBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


