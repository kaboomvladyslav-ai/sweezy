from __future__ import annotations

from datetime import timedelta

from ..core.config import get_settings
from ..core.security import create_access_token, get_password_hash, verify_password


class AuthService:
    @staticmethod
    def authenticate_admin(email: str, password: str) -> str | None:
        settings = get_settings()

        # Hash on first use to avoid storing plain admin password anywhere else
        hashed = get_password_hash(settings.ADMIN_PASSWORD)
        if email.lower() != settings.ADMIN_EMAIL.lower():
            return None
        if not verify_password(password, hashed):
            return None

        token = create_access_token(
            subject=email,
            is_admin=True,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return token


