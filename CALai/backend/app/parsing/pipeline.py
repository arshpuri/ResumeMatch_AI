"""
Resume parsing pipeline orchestrator — from implementation plan Component 4.
Orchestrates: Upload → Text Extraction → Section Detection → LLM Parse → Skill Normalization → DB Storage.
Emits SSE progress events.
"""

import asyncio
import logging
import uuid
from datetime import datetime

from app.parsing.extractor import extract_text
from app.parsing.section_detector import detect_sections
from app.parsing.llm_parser import parse_with_llm
from app.parsing.skill_normalizer import normalize_skills, get_display_name

logger = logging.getLogger(__name__)

# Global dict to track parsing progress per user_id
_parsing_progress: dict[str, list[dict]] = {}


def get_parsing_progress(user_id: str) -> list[dict]:
    """Get current parsing progress events for a user."""
    return _parsing_progress.get(user_id, [])


def clear_parsing_progress(user_id: str):
    """Clear parsing progress after client has consumed it."""
    _parsing_progress.pop(user_id, None)


def _emit_progress(user_id: str, step: str, progress: int, status: str, message: str | None = None):
    """Record a progress event."""
    event = {
        "step": step,
        "progress": progress,
        "status": status,
        "message": message,
    }
    _parsing_progress.setdefault(user_id, []).append(event)
    logger.info(f"Parsing [{user_id}]: {step} - {progress}% - {status}")


async def run_parsing_pipeline(
    file_bytes: bytes,
    file_type: str,
    user_id: str,
) -> dict:
    """
    Execute the full resume parsing pipeline.
    Returns a dict with all parsed data ready for DB storage.
    """
    # Clear any previous progress
    _parsing_progress[user_id] = []

    # ── Step 1: Text Extraction ──
    _emit_progress(user_id, "extracting", 10, "in_progress", "Extracting text from document...")
    try:
        raw_text = extract_text(file_bytes, file_type)
        if not raw_text or len(raw_text.strip()) < 20:
            _emit_progress(user_id, "extracting", 25, "error", "Could not extract sufficient text from document.")
            return {"error": "Insufficient text extracted", "raw_text": raw_text}
        _emit_progress(user_id, "extracting", 25, "done", "Text extraction complete.")
    except Exception as e:
        _emit_progress(user_id, "extracting", 25, "error", str(e))
        raise

    # Small delay to let SSE stream send events
    await asyncio.sleep(0.5)

    # ── Step 2: Section Detection ──
    _emit_progress(user_id, "sections", 30, "in_progress", "Detecting resume sections...")
    try:
        sections = detect_sections(raw_text)
        _emit_progress(user_id, "sections", 50, "done", f"Detected {len(sections)} sections.")
    except Exception as e:
        _emit_progress(user_id, "sections", 50, "error", str(e))
        sections = {}

    await asyncio.sleep(0.5)

    # ── Step 3: LLM Structured Extraction ──
    _emit_progress(user_id, "parsing", 55, "in_progress", "AI is analyzing your resume...")
    try:
        parsed_data = await parse_with_llm(raw_text, sections)
        _emit_progress(user_id, "parsing", 80, "done", "Resume structure extracted.")
    except Exception as e:
        logger.error(f"LLM parsing error: {e}")
        _emit_progress(user_id, "parsing", 80, "error", f"Parsing error: {str(e)}")
        parsed_data = {}

    await asyncio.sleep(0.5)

    # ── Step 4: Skill Normalization ──
    _emit_progress(user_id, "normalizing", 85, "in_progress", "Normalizing skills...")

    # Collect all skills from parsed data
    all_raw_skills: list[str] = []
    skills_data = parsed_data.get("skills", {})
    if isinstance(skills_data, dict):
        for category_skills in skills_data.values():
            if isinstance(category_skills, list):
                all_raw_skills.extend(category_skills)
    elif isinstance(skills_data, list):
        all_raw_skills.extend(skills_data)

    # Also grab from experience technologies
    for exp in parsed_data.get("experience", []):
        tech = exp.get("technologies_used", [])
        if isinstance(tech, list):
            all_raw_skills.extend(tech)

    normalized_skills = normalize_skills(all_raw_skills)
    display_skills = [get_display_name(s) for s in normalized_skills]

    _emit_progress(user_id, "normalizing", 90, "done", f"Normalized {len(display_skills)} skills.")

    await asyncio.sleep(0.3)

    # ── Step 5: Compute metadata ──
    _emit_progress(user_id, "matching", 92, "in_progress", "Computing experience years...")

    experience_years = _compute_experience_years(parsed_data.get("experience", []))
    keywords = parsed_data.get("keywords", [])
    confidence = _compute_confidence(parsed_data, raw_text)

    _emit_progress(user_id, "matching", 100, "done", "Parsing complete! Redirecting...")

    return {
        "raw_text": raw_text,
        "parsed_data": parsed_data,
        "skills": display_skills,
        "normalized_skills": normalized_skills,
        "experience_years": experience_years,
        "keywords": keywords if isinstance(keywords, list) else [],
        "parsing_confidence": confidence,
        "parser_version": "1.0.0",
    }


def _compute_experience_years(experiences: list[dict]) -> float:
    """Estimate total years of experience from parsed experience entries."""
    if not experiences:
        return 0.0

    total_months = 0
    for exp in experiences:
        start = exp.get("start_date", "")
        end = exp.get("end_date", "")

        if not start:
            continue

        try:
            start_parts = start.split("-")
            start_year = int(start_parts[0])
            start_month = int(start_parts[1]) if len(start_parts) > 1 else 1

            if end and end.lower() != "present":
                end_parts = end.split("-")
                end_year = int(end_parts[0])
                end_month = int(end_parts[1]) if len(end_parts) > 1 else 12
            else:
                end_year = datetime.now().year
                end_month = datetime.now().month

            months = (end_year - start_year) * 12 + (end_month - start_month)
            total_months += max(0, months)
        except (ValueError, IndexError):
            # If date parsing fails, estimate 2 years per entry
            total_months += 24

    return round(total_months / 12.0, 1)


def _compute_confidence(parsed_data: dict, raw_text: str) -> float:
    """
    Compute parsing confidence score (0.0 to 1.0) based on how many
    fields were successfully extracted.
    """
    score = 0.0
    max_score = 8.0

    personal = parsed_data.get("personal_info", {})
    if personal.get("name"):
        score += 1.0
    if personal.get("email"):
        score += 1.0
    if parsed_data.get("summary"):
        score += 1.0
    if parsed_data.get("skills"):
        skills = parsed_data["skills"]
        if isinstance(skills, dict):
            total_skills = sum(len(v) for v in skills.values() if isinstance(v, list))
        else:
            total_skills = len(skills) if isinstance(skills, list) else 0
        if total_skills > 0:
            score += 1.5
    if parsed_data.get("experience"):
        score += 1.5
    if parsed_data.get("education"):
        score += 1.0
    if parsed_data.get("keywords"):
        score += 1.0

    return round(min(score / max_score, 1.0), 2)
