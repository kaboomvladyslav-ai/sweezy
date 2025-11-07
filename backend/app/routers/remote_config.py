from __future__ import annotations

from fastapi import APIRouter, HTTPException
from ..dependencies import CurrentAdmin

from ..schemas import RemoteConfigOut
from ..services import RemoteConfigService


router = APIRouter()


@router.get("/", response_model=RemoteConfigOut)
def get_remote_config() -> RemoteConfigOut:
    return RemoteConfigOut(**RemoteConfigService.get_config())


@router.post("/")
def update_remote_config(payload: dict, _: CurrentAdmin) -> RemoteConfigOut:
    try:
        return RemoteConfigOut(**RemoteConfigService.update_config(payload))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

