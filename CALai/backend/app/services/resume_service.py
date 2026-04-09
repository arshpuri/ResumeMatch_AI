"""
Resume service — upload, parse, CRUD operations.
Aligned with Supabase schema (file_key, confidence_score, parsing_status columns).
"""

import asyncio
import io
import logging
import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import ParsedResume
from app.models.user import User
from app.parsing.pipeline import run_parsing_pipeline
from app.utils.storage import upload_file, delete_file
from app.utils.cache import cache_delete_pattern

logger = logging.getLogger(__name__)


async def upload_and_parse_resume(
    db: AsyncSession,
    user: User,
    file_bytes: bytes,
    filename: str,
    content_type: str,
) -> dict:
    """
    Upload resume to S3 and trigger async parsing.
    If user already has a resume, replace it.
    """
    # Determine file type
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ("pdf", "docx", "doc", "txt"):
        raise ValueError(f"Unsupported file type: {ext}. Use PDF, DOCX, or TXT.")

    # Upload to S3
    file_obj = io.BytesIO(file_bytes)
    object_key = upload_file(file_obj, filename, content_type)

    # Delete existing resume if any
    result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        try:
            delete_file(existing.file_key)
        except Exception:
            pass
        await db.delete(existing)
        await db.flush()

    # Create new resume record
    resume = ParsedResume(
        user_id=user.id,
        file_key=object_key,
        file_name=filename,
        file_size=len(file_bytes),
        mime_type=content_type,
        parsed_data={},
        skills=[],
        parsing_status="processing",
    )
    db.add(resume)
    await db.flush()

    # Run parsing pipeline (in background-ish — we await it but emit SSE events)
    user_id_str = str(user.id)
    try:
        parsed = await run_parsing_pipeline(file_bytes, ext, user_id_str)

        if "error" not in parsed:
            resume.raw_text = parsed.get("raw_text", "")
            resume.parsed_data = parsed.get("parsed_data", {})
            resume.skills = parsed.get("skills", [])
            resume.experience_years = parsed.get("experience_years", 0)
            resume.keywords = parsed.get("keywords", [])
            resume.confidence_score = parsed.get("parsing_confidence", 0)
            resume.parsing_status = "completed"

            # Update user headline from parsed data if not set
            personal = resume.parsed_data.get("personal_info", {})
            if not user.headline and personal.get("name"):
                summary = resume.parsed_data.get("summary", "")
                if summary:
                    user.headline = summary[:200]
            if not user.location and personal.get("location"):
                user.location = personal["location"]
            if not user.phone and personal.get("phone"):
                user.phone = personal["phone"]

            await db.flush()
        else:
            resume.parsing_status = "failed"
            resume.parsing_error = parsed.get("error", "Unknown error")
            await db.flush()
    except Exception as e:
        logger.error(f"Resume parsing failed: {e}")
        resume.parsing_status = "failed"
        resume.parsing_error = str(e)
        await db.flush()

    # Invalidate caches
    await cache_delete_pattern(f"profile:{user_id_str}*")
    await cache_delete_pattern(f"job_feed:{user_id_str}*")

    return {
        "id": str(resume.id),
        "file_key": object_key,
        "file_name": filename,
        "message": "Resume uploaded. Parsing started.",
    }


async def get_parsed_resume(db: AsyncSession, user: User) -> ParsedResume | None:
    """Get the user's parsed resume."""
    result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    return result.scalar_one_or_none()


async def update_parsed_resume(
    db: AsyncSession,
    user: User,
    skills: list[str] | None = None,
    parsed_data: dict | None = None,
) -> ParsedResume:
    """Manually update parsed resume fields."""
    result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    resume = result.scalar_one_or_none()
    if resume is None:
        raise ValueError("No resume found.")

    if skills is not None:
        resume.skills = skills
    if parsed_data is not None:
        resume.parsed_data = parsed_data

    await db.flush()

    # Invalidate caches
    await cache_delete_pattern(f"job_feed:{str(user.id)}*")

    return resume


async def delete_resume(db: AsyncSession, user: User):
    """Delete the user's resume and parsed data."""
    result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    resume = result.scalar_one_or_none()
    if resume:
        try:
            delete_file(resume.file_key)
        except Exception:
            pass
        await db.delete(resume)
        await db.flush()
        await cache_delete_pattern(f"profile:{str(user.id)}*")
        await cache_delete_pattern(f"job_feed:{str(user.id)}*")
