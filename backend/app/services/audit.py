from __future__ import annotations

import json
from typing import Any, Optional
from sqlalchemy.orm import Session
from ..models.audit_log import AuditLog


def log_audit(db: Session, *, user_email: str, action: str, entity: str, entity_id: str, before: Optional[Any] = None, after: Optional[Any] = None) -> None:
    try:
        change = {"before": _serialize(before), "after": _serialize(after)}
        entry = AuditLog(
            user_email=user_email,
            action=action,
            entity=entity,
            entity_id=str(entity_id),
            changes=json.dumps(change, ensure_ascii=False),
        )
        db.add(entry)
        db.commit()
    except Exception:
        db.rollback()


def _serialize(obj: Any) -> Any:
    if obj is None:
        return None
    if hasattr(obj, "__dict__"):
        # SQLAlchemy model: only simple attrs
        data = {}
        for k, v in vars(obj).items():
            if k.startswith("_"):
                continue
            try:
                json.dumps(v)
                data[k] = v
            except Exception:
                data[k] = str(v)
        return data
    try:
        return obj if isinstance(obj, (str, int, float, dict, list)) else str(obj)
    except Exception:
        return str(obj)


