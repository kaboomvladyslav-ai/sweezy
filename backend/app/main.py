from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
import contextlib
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .core.sentry import init_sentry
from .routers.auth import router as auth_router
from .routers.guides import router as guides_router
from .routers.checklists import router as checklists_router
from .routers.templates import router as templates_router
from .routers.appointments import router as appointments_router
from .routers.remote_config import router as remote_config_router


settings = get_settings()


async def _background_tick() -> None:
    while True:
        await asyncio.sleep(60)
        # Placeholder for periodic background tasks (e.g. cache refresh)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_sentry()
    task = asyncio.create_task(_background_tick())
    try:
        yield
    finally:
        task.cancel()
        # Suppress task cancellation on shutdown to avoid noisy tracebacks
        with contextlib.suppress(asyncio.CancelledError):
            await task


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(guides_router, prefix="/guides", tags=["guides"])
app.include_router(checklists_router, prefix="/checklists", tags=["checklists"])
app.include_router(templates_router, prefix="/templates", tags=["templates"])
app.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
app.include_router(remote_config_router, prefix="/remote-config", tags=["remote-config"])


