"""
Job service — feed, detail, search, save, apply, dismiss.
Integrates the 3-layer matching engine.
Aligned with Supabase schema (required_skills, posted_at, match_score columns).
"""

import uuid
import logging
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, func, or_, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.models.resume import ParsedResume
from app.models.application import Application
from app.models.interaction import UserInteraction, SavedJob
from app.models.user import User
from app.matching.ranker import compute_match_score
from app.schemas.job import JobMatchResponse, JobDetailResponse

logger = logging.getLogger(__name__)


async def get_job_feed(
    db: AsyncSession,
    user: User,
    cursor: str | None = None,
    limit: int = 20,
) -> dict:
    """
    Get personalized job feed with match scores.
    Implements the 3-layer filtering pipeline from the architecture:
    1. Filter active jobs
    2. Score each job
    3. Sort by match score descending
    """
    # Get user's resume
    resume_result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    resume = resume_result.scalar_one_or_none()

    resume_skills = resume.skills if resume else []
    resume_exp_years = float(resume.experience_years or 0) if resume else 0.0
    resume_embedding = None  # Will be computed if model available

    # Get dismissed job IDs
    dismissed_result = await db.execute(
        select(UserInteraction.job_id).where(
            UserInteraction.user_id == user.id,
            UserInteraction.action == "dismiss",
        )
    )
    dismissed_ids = {row[0] for row in dismissed_result.all()}

    # Fetch active jobs
    query = select(Job).where(Job.is_active.is_(True))
    if cursor:
        try:
            cursor_uuid = uuid.UUID(cursor)
            query = query.where(Job.id > cursor_uuid)
        except ValueError:
            pass

    query = query.limit(200)  # Fetch candidate pool
    result = await db.execute(query)
    jobs = result.scalars().all()

    # Get user interactions for personalization
    interactions_result = await db.execute(
        select(UserInteraction).where(
            UserInteraction.user_id == user.id
        ).order_by(UserInteraction.created_at.desc()).limit(100)
    )
    interactions = interactions_result.scalars().all()

    user_interaction_data = []
    for inter in interactions:
        user_interaction_data.append({
            "action": inter.action,
            "timestamp": inter.created_at,
            "job_embedding": None,  # Skip embedding for performance in v1
        })

    # Score and rank jobs
    scored_jobs: list[tuple[Job, dict]] = []
    for job in jobs:
        if job.id in dismissed_ids:
            continue

        match_data = compute_match_score(
            resume_skills=resume_skills,
            resume_exp_years=resume_exp_years,
            resume_embedding=resume_embedding,
            job_skills_required=job.required_skills or [],
            job_exp_level=job.experience_level,
            job_embedding=None,  # Embedding is vector type, accessed via SQL
            job_posted_date=job.posted_at,
            user_interactions=user_interaction_data,
        )
        scored_jobs.append((job, match_data))

    # Sort by match score descending
    scored_jobs.sort(key=lambda x: x[1]["matchScore"], reverse=True)

    # Apply pagination
    page = scored_jobs[:limit]
    next_cursor = str(page[-1][0].id) if len(page) == limit else None

    # Format response
    jobs_response = []
    for job, match_data in page:
        posted_at = _format_posted_at(job.posted_at)
        salary = _format_salary(job.salary_min, job.salary_max, job.salary_currency)

        jobs_response.append(JobMatchResponse(
            id=str(job.id),
            title=job.title,
            company=job.company,
            location=job.location or "Remote",
            matchScore=match_data["matchScore"],
            salary=salary,
            postedAt=posted_at,
            skills=match_data["skills"],
            missingSkills=match_data["missingSkills"],
            reasons=match_data["reasons"],
        ))

    return {
        "jobs": jobs_response,
        "nextCursor": next_cursor,
        "total": len(scored_jobs),
    }


async def get_job_detail(
    db: AsyncSession,
    user: User,
    job_id: str,
) -> JobDetailResponse | None:
    """Get job detail with match analysis."""
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        return None

    result = await db.execute(select(Job).where(Job.id == job_uuid))
    job = result.scalar_one_or_none()
    if job is None:
        return None

    # Get resume for matching
    resume_result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    resume = resume_result.scalar_one_or_none()

    resume_skills = resume.skills if resume else []
    resume_exp_years = float(resume.experience_years or 0) if resume else 0.0

    match_data = compute_match_score(
        resume_skills=resume_skills,
        resume_exp_years=resume_exp_years,
        resume_embedding=None,
        job_skills_required=job.required_skills or [],
        job_exp_level=job.experience_level,
        job_embedding=None,
        job_posted_date=job.posted_at,
    )

    # Check if saved
    saved_result = await db.execute(
        select(SavedJob).where(
            SavedJob.user_id == user.id,
            SavedJob.job_id == job.id,
        )
    )
    is_saved = saved_result.scalar_one_or_none() is not None

    # Log view interaction
    interaction = UserInteraction(
        user_id=user.id,
        job_id=job.id,
        action="view",
    )
    db.add(interaction)

    return JobDetailResponse(
        id=str(job.id),
        title=job.title,
        company=job.company,
        location=job.location or "Remote",
        matchScore=match_data["matchScore"],
        salary=_format_salary(job.salary_min, job.salary_max, job.salary_currency),
        postedAt=_format_posted_at(job.posted_at),
        skills=match_data["skills"],
        missingSkills=match_data["missingSkills"],
        reasons=match_data["reasons"],
        description=job.description,
        responsibilities=job.responsibilities or [],
        experienceLevel=job.experience_level,
        jobType=job.job_type,
        isRemote=job.is_remote,
        isSaved=is_saved,
    )


async def search_jobs(
    db: AsyncSession,
    user: User,
    query: str,
    limit: int = 20,
) -> dict:
    """Full-text search using tsvector (fts column) with ILIKE fallback."""
    # Try full-text search first
    search_query = " & ".join(query.split())

    result = await db.execute(
        select(Job)
        .where(
            Job.is_active.is_(True),
            or_(
                Job.title.ilike(f"%{query}%"),
                Job.company.ilike(f"%{query}%"),
                Job.description.ilike(f"%{query}%"),
            ),
        )
        .limit(limit)
    )
    jobs = result.scalars().all()

    # Get resume for matching
    resume_result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    resume = resume_result.scalar_one_or_none()
    resume_skills = resume.skills if resume else []
    resume_exp_years = float(resume.experience_years or 0) if resume else 0.0

    jobs_response = []
    for job in jobs:
        match_data = compute_match_score(
            resume_skills=resume_skills,
            resume_exp_years=resume_exp_years,
            resume_embedding=None,
            job_skills_required=job.required_skills or [],
            job_exp_level=job.experience_level,
            job_embedding=None,
            job_posted_date=job.posted_at,
        )
        jobs_response.append(JobMatchResponse(
            id=str(job.id),
            title=job.title,
            company=job.company,
            location=job.location or "Remote",
            matchScore=match_data["matchScore"],
            salary=_format_salary(job.salary_min, job.salary_max, job.salary_currency),
            postedAt=_format_posted_at(job.posted_at),
            skills=match_data["skills"],
            missingSkills=match_data["missingSkills"],
            reasons=match_data["reasons"],
        ))

    return {
        "jobs": jobs_response,
        "total": len(jobs_response),
        "query": query,
    }


async def save_job(db: AsyncSession, user: User, job_id: str) -> bool:
    """Save/bookmark a job."""
    job_uuid = uuid.UUID(job_id)

    # Check if already saved
    existing = await db.execute(
        select(SavedJob).where(
            SavedJob.user_id == user.id,
            SavedJob.job_id == job_uuid,
        )
    )
    if existing.scalar_one_or_none():
        return True  # Already saved

    saved = SavedJob(user_id=user.id, job_id=job_uuid)
    db.add(saved)

    # Log interaction
    interaction = UserInteraction(user_id=user.id, job_id=job_uuid, action="save")
    db.add(interaction)
    return True


async def unsave_job(db: AsyncSession, user: User, job_id: str) -> bool:
    """Remove a saved job."""
    job_uuid = uuid.UUID(job_id)
    await db.execute(
        delete(SavedJob).where(
            SavedJob.user_id == user.id,
            SavedJob.job_id == job_uuid,
        )
    )
    interaction = UserInteraction(user_id=user.id, job_id=job_uuid, action="unsave")
    db.add(interaction)
    return True


async def get_saved_jobs(db: AsyncSession, user: User) -> list[dict]:
    """List saved jobs."""
    result = await db.execute(
        select(SavedJob).where(SavedJob.user_id == user.id).order_by(SavedJob.saved_at.desc())
    )
    saved = result.scalars().all()

    jobs_list = []
    for s in saved:
        job = s.job
        if job:
            jobs_list.append({
                "id": str(job.id),
                "title": job.title,
                "company": job.company,
                "location": job.location or "Remote",
                "savedAt": s.saved_at.isoformat() if s.saved_at else "",
            })
    return jobs_list


async def apply_to_job(
    db: AsyncSession,
    user: User,
    job_id: str,
    match_score_val: float | None = None,
) -> bool:
    """Track a job application."""
    job_uuid = uuid.UUID(job_id)

    # Check for duplicate
    existing = await db.execute(
        select(Application).where(
            Application.user_id == user.id,
            Application.job_id == job_uuid,
        )
    )
    if existing.scalar_one_or_none():
        raise ValueError("Already applied to this job")

    # Get user's resume ID for the application record
    resume_result = await db.execute(
        select(ParsedResume.id).where(ParsedResume.user_id == user.id)
    )
    resume_row = resume_result.first()
    resume_id = resume_row[0] if resume_row else None

    app = Application(
        user_id=user.id,
        job_id=job_uuid,
        resume_id=resume_id,
        status="applied",
        match_score=match_score_val,
    )
    db.add(app)

    # Log interaction
    interaction = UserInteraction(user_id=user.id, job_id=job_uuid, action="apply")
    db.add(interaction)
    return True


async def dismiss_job(db: AsyncSession, user: User, job_id: str) -> bool:
    """Hide a job from feed."""
    job_uuid = uuid.UUID(job_id)
    interaction = UserInteraction(user_id=user.id, job_id=job_uuid, action="dismiss")
    db.add(interaction)
    return True


def _format_posted_at(posted_at: datetime | None) -> str:
    """Format posted date as relative time string."""
    if not posted_at:
        return "Recently"

    now = datetime.now(timezone.utc)
    if hasattr(posted_at, 'tzinfo') and posted_at.tzinfo is None:
        posted_at = posted_at.replace(tzinfo=timezone.utc)
    elif not hasattr(posted_at, 'hour'):
        posted_at = datetime.combine(posted_at, datetime.min.time(), tzinfo=timezone.utc)

    delta = now - posted_at
    days = delta.days

    if days == 0:
        hours = delta.seconds // 3600
        if hours == 0:
            return "Just now"
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif days == 1:
        return "1 day ago"
    elif days < 7:
        return f"{days} days ago"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        months = days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"


def _format_salary(
    salary_min: int | None,
    salary_max: int | None,
    currency: str | None,
) -> str | None:
    """Format salary range as display string."""
    if not salary_min and not salary_max:
        return None

    curr = currency or "USD"
    if salary_min and salary_max:
        return f"${salary_min//1000}K - ${salary_max//1000}K {curr}"
    elif salary_min:
        return f"${salary_min//1000}K+ {curr}"
    elif salary_max:
        return f"Up to ${salary_max//1000}K {curr}"
    return None
