from __future__ import annotations

from typing import Dict

from pydantic import BaseModel


class RemoteConfigOut(BaseModel):
    app_version: str
    flags: Dict[str, bool]


