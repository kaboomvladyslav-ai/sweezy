from __future__ import annotations

from pathlib import Path
from fastapi import APIRouter, File, UploadFile

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()


@router.post("/upload")
async def upload_media(file: UploadFile = File(...)) -> dict:
  suffix = Path(file.filename).suffix
  safe_name = file.filename.replace(' ', '_')
  target = UPLOAD_DIR / safe_name
  i = 1
  while target.exists():
    target = UPLOAD_DIR / f"{target.stem}_{i}{suffix}"
    i += 1
  content = await file.read()
  target.write_bytes(content)
  return {"url": f"/media/{target.name}", "filename": target.name}


