from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ChecklistBase(BaseModel):
    title: str
    description: Optional[str] = None
    items: List[str] = []
    is_published: bool = True


class ChecklistCreate(ChecklistBase):
    pass


class ChecklistUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    items: Optional[List[str]] = None
    is_published: Optional[bool] = None


class ChecklistOut(ChecklistBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


