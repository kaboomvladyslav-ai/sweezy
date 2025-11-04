from __future__ import annotations

from ..core.config import get_settings


class RemoteConfigService:
    @staticmethod
    def get_config() -> dict:
        settings = get_settings()
        return {
            "app_version": settings.APP_VERSION,
            "flags": settings.REMOTE_FLAGS,
        }


