from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import os

from ..dependencies import get_db, CurrentAdmin
from sqlalchemy.orm import Session

router = APIRouter()


class CVPersonal(BaseModel):
    fullName: str = ""
    title: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    summary: str = ""


class CVEducation(BaseModel):
    id: Optional[str] = None
    school: str = ""
    degree: str = ""
    period: str = ""
    details: str = ""


class CVExperience(BaseModel):
    id: Optional[str] = None
    role: str = ""
    company: str = ""
    period: str = ""
    location: str = ""
    achievements: str = ""


class CVLanguage(BaseModel):
    id: Optional[str] = None
    name: str = ""
    level: str = ""


class CVSuggestRequest(BaseModel):
    personal: CVPersonal
    education: List[CVEducation] = []
    experience: List[CVExperience] = []
    languages: List[CVLanguage] = []
    skills: List[str] = []
    hobbies: List[str] = []
    target: str = Field(..., description="summary or experience:<uuid>")


class CVSuggestResponse(BaseModel):
    text: str


def _fallback_generate(payload: CVSuggestRequest) -> str:
    # Deterministic, simple Swiss-style phrasing (no external AI required)
    if payload.target.startswith("experience"):
        # pick first relevant exp
        target_id = payload.target.split(":", 1)[1] if ":" in payload.target else None
        exp = payload.experience[0] if not target_id else next((e for e in payload.experience if str(e.id) == target_id), None)
        if not exp:
            return ""
        parts = []
        if exp.role:
            parts.append(f"{exp.role} у {exp.company}".strip())
        if exp.period:
            parts.append(f"({exp.period})")
        header = " ".join(p for p in parts if p)
        bullets = [
            "Відповідав(-ла) за якісне та своєчасне виконання задач.",
            "Покращив(-ла) процеси та взаємодію в команді, дотримуючись принципів прозорої комунікації.",
            "Досяг(-ла) вимірюваних результатів і регулярно звітував(-ла) перед стейкхолдерами."
        ]
        return header + "\n• " + "\n• ".join(bullets)
    else:
        # summary
        name = payload.personal.fullName or "Фахівець"
        title = payload.personal.title or "Спеціаліст"
        loc = payload.personal.location
        skills = ", ".join(payload.skills[:6])
        base = f"{name} — {title} у Швейцарії"
        if loc:
            base += f" ({loc})"
        tail = ". Досвід адаптації до швейцарських стандартів, відповідальність, орієнтація на результат."
        if skills:
            tail = f". Ключові навички: {skills}." + tail
        return base + tail


@router.post("/cv-suggest", response_model=CVSuggestResponse)
def cv_suggest(payload: CVSuggestRequest, _: CurrentAdmin, db: Session = Depends(get_db)) -> CVSuggestResponse:
    """
    Suggest HR-style text based on CV data.
    Uses OpenAI if OPENAI_API_KEY is set, otherwise deterministic fallback.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return CVSuggestResponse(text=_fallback_generate(payload))

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = (
            "You are an HR assistant in Switzerland. Write concise, professional text.\n"
            f"Target: {payload.target}\n"
            f"Personal: {payload.personal.model_dump()}\n"
            f"Education: {[e.model_dump() for e in payload.education]}\n"
            f"Experience: {[e.model_dump() for e in payload.experience]}\n"
            f"Languages: {[l.model_dump() for l in payload.languages]}\n"
            f"Skills: {payload.skills}\n"
            "Rules: 1) Avoid buzzwords; 2) Use neutral tone; 3) Keep it under 90 words; "
            "4) For experience target, produce 3 bullet points starting with verbs."
        )
        chat = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=220,
        )
        text = (chat.choices[0].message.content or "").strip()
        return CVSuggestResponse(text=text or _fallback_generate(payload))
    except Exception:
        return CVSuggestResponse(text=_fallback_generate(payload))


