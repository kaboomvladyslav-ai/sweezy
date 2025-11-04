from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class TemplateBase(BaseModel):
    name: str
    category: Optional[str] = None
    content: str


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None


class TemplateOut(TemplateBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


