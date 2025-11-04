from __future__ import annotations

from fastapi import APIRouter

from ..schemas import RemoteConfigOut
from ..services import RemoteConfigService


router = APIRouter()


@router.get("/", response_model=RemoteConfigOut)
def get_remote_config() -> RemoteConfigOut:
    return RemoteConfigOut(**RemoteConfigService.get_config())


