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


    @staticmethod
    def update_config(data: dict) -> dict:
        settings = get_settings()
        flags = data.get("flags")
        if flags is None or not isinstance(flags, dict):
            raise ValueError("'flags' must be an object")
        # mutate in-memory settings (ephemeral across restarts)
        settings.REMOTE_FLAGS = flags  # type: ignore[attr-defined]
        return {
            "app_version": settings.APP_VERSION,
            "flags": settings.REMOTE_FLAGS,
        }


