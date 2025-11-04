from __future__ import annotations

import sentry_sdk

from .config import get_settings


def init_sentry() -> None:
    settings = get_settings()
    if not settings.SENTRY_DSN:
        return
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.APP_ENV,
        release=settings.APP_VERSION,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        profiles_sample_rate=settings.SENTRY_PROFILES_SAMPLE_RATE,
    )


