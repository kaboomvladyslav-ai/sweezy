from __future__ import annotations

from typing import Annotated, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .core.database import get_db
from .core.security import decode_token


security_scheme = HTTPBearer(auto_error=True)


def get_current_admin(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
) -> Dict:
    try:
        payload = decode_token(credentials.credentials)
        if not payload.get("is_admin"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return payload
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")


CurrentAdmin = Annotated[Dict, Depends(get_current_admin)]
DBSession = Annotated[Session, Depends(get_db)]


