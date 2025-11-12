from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Template
from ..schemas import TemplateCreate, TemplateUpdate


class TemplateService:
    @staticmethod
    def list(db: Session, *, offset: int = 0, limit: int = 100, status: str | None = None, include_drafts: bool = False) -> List[Template]:
        stmt = select(Template)
        if status:
            stmt = stmt.where(getattr(Template, "status", None) == status)  # type: ignore[attr-defined]
        elif not include_drafts and hasattr(Template, "status"):
            stmt = stmt.where(Template.status == "published")  # type: ignore[attr-defined]
        stmt = stmt.offset(offset).limit(limit)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get(db: Session, template_id: str) -> Optional[Template]:
        return db.get(Template, template_id)

    @staticmethod
    def create(db: Session, data: TemplateCreate) -> Template:
        obj = Template(**data.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def update(db: Session, template: Template, data: TemplateUpdate) -> Template:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(template, key, value)
        db.add(template)
        db.commit()
        db.refresh(template)
        return template

    @staticmethod
    def delete(db: Session, template: Template) -> None:
        db.delete(template)
        db.commit()


