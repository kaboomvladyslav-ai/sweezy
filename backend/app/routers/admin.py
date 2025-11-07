from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..dependencies import DBSession, CurrentAdmin
from ..models import User, Guide, Template, Checklist, Appointment
from ..schemas import GuideCreate, TemplateCreate, ChecklistCreate
from ..core.config import get_settings


router = APIRouter()


@router.get("/stats")
def stats(_: CurrentAdmin, db: DBSession) -> Dict[str, Any]:
    settings = get_settings()
    counts = {
        "users": db.scalar(select(func.count()).select_from(User)) or 0,
        "guides": db.scalar(select(func.count()).select_from(Guide)) or 0,
        "templates": db.scalar(select(func.count()).select_from(Template)) or 0,
        "checklists": db.scalar(select(func.count()).select_from(Checklist)) or 0,
        "appointments": db.scalar(select(func.count()).select_from(Appointment)) or 0,
    }
    return {
        "app_version": settings.APP_VERSION,
        "counts": counts,
    }


@router.get("/users")
def list_users(_: CurrentAdmin, db: DBSession) -> List[Dict[str, Any]]:
    rows = (
        db.query(User.id, User.email, User.is_superuser, User.created_at)
        .order_by(User.created_at.desc())
        .limit(100)
        .all()
    )
    return [
        {
            "id": r.id,
            "email": r.email,
            "is_superuser": bool(r.is_superuser),
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


@router.get("/activity")
def activity(_: CurrentAdmin, db: DBSession) -> Dict[str, Any]:
    def recent_simple(model):
        created = getattr(model, "created_at")
        rows = db.query(model.id, created).order_by(created.desc()).limit(5).all()
        return [
            {"id": r.id, "created_at": r.created_at.isoformat() if r.created_at else None}
            for r in rows
        ]

    recent_users = (
        db.query(User.id, User.email, User.created_at)
        .order_by(User.created_at.desc())
        .limit(5)
        .all()
    )
    return {
        "users": [
            {
                "id": r.id,
                "email": r.email,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in recent_users
        ],
        "guides": recent_simple(Guide),
        "templates": recent_simple(Template),
        "checklists": recent_simple(Checklist),
        "appointments": recent_simple(Appointment),
    }


@router.get("/categories/guides")
def guide_categories(_: CurrentAdmin) -> Dict[str, Any]:
    # Keep in sync with Swift enum GuideCategory
    categories = [
        "documents", "housing", "insurance", "work", "finance", "education",
        "healthcare", "legal", "emergency", "integration", "transport", "banking",
    ]
    return {"categories": categories}


@router.post("/import/guides")
def import_guides(payload: Dict[str, Any], db: DBSession, _: CurrentAdmin) -> Dict[str, Any]:
    items = payload.get("items") or []
    created = 0
    for raw in items:
        try:
            data = GuideCreate(**raw)
            obj = Guide(
                title=data.title,
                slug=data.slug,
                description=data.description,
                content=data.content,
                category=data.category,
                image_url=getattr(data, "image_url", None),
                is_published=data.is_published,
                version=data.version,
            )
            db.add(obj)
            created += 1
        except Exception:
            continue
    db.commit()
    return {"created": created}


@router.post("/import/templates")
def import_templates(payload: Dict[str, Any], db: DBSession, _: CurrentAdmin) -> Dict[str, Any]:
    items = payload.get("items") or []
    created = 0
    for raw in items:
        try:
            data = TemplateCreate(**raw)
            obj = Template(**data.model_dump())
            db.add(obj)
            created += 1
        except Exception:
            continue
    db.commit()
    return {"created": created}


@router.post("/import/checklists")
def import_checklists(payload: Dict[str, Any], db: DBSession, _: CurrentAdmin) -> Dict[str, Any]:
    items = payload.get("items") or []
    created = 0
    for raw in items:
        try:
            data = ChecklistCreate(**raw)
            obj = Checklist(**data.model_dump())
            db.add(obj)
            created += 1
        except Exception:
            continue
    db.commit()
    return {"created": created}


