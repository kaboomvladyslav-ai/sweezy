from __future__ import annotations

from typing import Annotated, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .core.database import get_db
from .core.security import decode_token
from .services.users import UserService


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


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    db: DBSession,
):
    try:
        payload = decode_token(credentials.credentials)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = UserService.get_by_email(db, email)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")

CurrentUser = Annotated[object, Depends(get_current_user)]


def require_roles(*roles: str):
    def dependency(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)]):
        payload = decode_token(credentials.credentials)
        role = payload.get("role")
        is_admin = payload.get("is_admin")
        if is_admin:
            return payload
        if role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return payload
    return Depends(dependency)


