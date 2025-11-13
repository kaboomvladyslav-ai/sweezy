from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import os

from ..dependencies import get_db, require_premium
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


@router.post("/cv-suggest", response_model=CVSuggestResponse, dependencies=[require_premium()])
def cv_suggest(payload: CVSuggestRequest, db: Session = Depends(get_db)) -> CVSuggestResponse:
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


# --- Job application helper ---
class JobApplyRequest(BaseModel):
    jobTitle: str
    company: str | None = None
    description: str | None = None
    candidateSummary: str | None = None
    language: str | None = None  # 'en','de','ru','uk'


class JobApplyResponse(BaseModel):
    text: str


def _job_apply_fallback(req: JobApplyRequest) -> str:
    lang = (req.language or "en").lower()
    if lang.startswith("de"):
        return f"Sehr geehrte Damen und Herren,\n\nich bewerbe mich auf die Stelle \"{req.jobTitle}\"{(' bei ' + req.company) if req.company else ''}. Ich bringe relevante Erfahrung mit und arbeite sorgfältig, zuverlässig und kundenorientiert. Gerne überzeuge ich Sie in einem persönlichen Gespräch.\n\nFreundliche Grüsse\n"
    if lang.startswith("ru"):
        return f"Здравствуйте,\n\nПодаю заявку на позицию «{req.jobTitle}»{(' в компании ' + req.company) if req.company else ''}. Имею релевантный опыт, работаю аккуратно и ответственно, быстро обучаюсь. Буду рад обсудить детали на собеседовании.\n\nС уважением,\n"
    if lang.startswith("uk"):
        return f"Вітаю,\n\nХочу податися на позицію «{req.jobTitle}»{(' у компанії ' + req.company) if req.company else ''}. Маю релевантний досвід, працюю уважно та відповідально, швидко навчаюся. Буду радий обговорити деталі під час інтерв’ю.\n\nЗ повагою,\n"
    return f"Hello,\n\nI would like to apply for the “{req.jobTitle}” role{(' at ' + req.company) if req.company else ''}. I bring relevant experience, a reliable and detail‑oriented work style, and strong customer focus. I would welcome the opportunity to discuss how I can contribute.\n\nKind regards,\n"


@router.post("/job-apply", response_model=JobApplyResponse, dependencies=[require_premium()])
def job_apply(req: JobApplyRequest) -> JobApplyResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return JobApplyResponse(text=_job_apply_fallback(req))
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = (
            "You are an HR assistant in Switzerland. Write a short, professional application message/cover email.\n"
            f"Language: {req.language or 'en'}\n"
            f"Job Title: {req.jobTitle}\n"
            f"Company: {req.company or ''}\n"
            f"Job Description: {req.description or ''}\n"
            f"Candidate Summary: {req.candidateSummary or ''}\n"
            "Rules: 1) 90-140 words; 2) concise, neutral tone; 3) avoid clichés; 4) optionally include 2-3 bullet points; "
            "5) Swiss style; 6) no placeholders."
        )
        chat = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=260,
        )
        text = (chat.choices[0].message.content or "").strip()
        return JobApplyResponse(text=text or _job_apply_fallback(req))
    except Exception:
        return JobApplyResponse(text=_job_apply_fallback(req))


