from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from hashlib import sha1

from fastapi import APIRouter, Query
from pydantic import BaseModel
import httpx

router = APIRouter()


class PlaceLiveStatus(BaseModel):
    wait_minutes: Optional[int] = None
    busy_level: Optional[str] = None  # low|medium|high
    closes_at: Optional[datetime] = None
    updated_at: datetime
    provider: str = "mock"
    hours_text: Optional[str] = None


# Simple in-memory TTL cache
_cache: Dict[str, Tuple[datetime, PlaceLiveStatus]] = {}
_TTL = timedelta(minutes=5)


def _cache_key(**params: object) -> str:
    payload = "&".join(f"{k}={v}" for k, v in sorted(params.items()) if v is not None)
    return sha1(payload.encode("utf-8")).hexdigest()


async def _mock_provider(category: Optional[str]) -> PlaceLiveStatus:
    # Deterministic heuristic by category
    now = datetime.utcnow()
    defaults = {
        "migration_office": (25, "high"),
        "hospital": (15, "high"),
        "clinic": (10, "medium"),
        "pharmacy": (5, "low"),
        "train_station": (8, "medium"),
        "gemeinde": (12, "medium"),
    }
    minutes, level = defaults.get(category or "", (7, "low"))
    return PlaceLiveStatus(wait_minutes=minutes, busy_level=level, updated_at=now, provider="mock")


async def _overpass_hours(lat: Optional[float], lng: Optional[float], name: Optional[str]) -> Optional[str]:
    if lat is None or lng is None:
        return None
    # Overpass QL query to find nearby element with matching name and opening_hours tag
    radius = 500
    safe_name = (name or "").replace('"', '\\"')
    q = f"""
        [out:json][timeout:12];
        (
          node(around:{radius},{lat},{lng})["name"~"{safe_name}", i];
          way(around:{radius},{lat},{lng})["name"~"{safe_name}", i];
          relation(around:{radius},{lat},{lng})["name"~"{safe_name}", i];
        );
        out tags center 10;
    """
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            r = await client.post("https://overpass-api.de/api/interpreter", data=q)
            if r.status_code >= 400:
                return None
            data = r.json()
            elements = data.get("elements") or []
            for el in elements:
                tags = el.get("tags") or {}
                if "opening_hours" in tags:
                    return tags["opening_hours"]
    except Exception:
        return None
    return None


@router.get("/place-status", response_model=PlaceLiveStatus)
async def place_status(
    name: str,
    category: Optional[str] = Query(None, description="place category, e.g. migration_office"),
    canton: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
) -> PlaceLiveStatus:
    """
    Aggregate live queue/wait information for a place.
    Currently uses a lightweight mock heuristic with 5-minute caching.
    Later we can add real canton/provider adapters here.
    """
    key = _cache_key(name=name, category=category, canton=canton, lat=lat, lng=lng)
    now = datetime.utcnow()
    cached = _cache.get(key)
    if cached and now - cached[0] < _TTL:
        return cached[1]

    # Placeholder for future real providers; currently mock
    status = await _mock_provider(category)
    # Augment with opening hours from OpenStreetMap Overpass if available
    hours = await _overpass_hours(lat, lng, name)
    if hours:
        status.hours_text = hours
        status.provider = status.provider + "+overpass"

    _cache[key] = (now, status)
    return status


