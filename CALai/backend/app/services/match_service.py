"""
Match service — wraps the matching engine for service-layer use.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import ParsedResume
from app.models.job import Job
from app.models.user import User
from app.matching.ranker import compute_match_score
from app.parsing.skill_normalizer import get_display_name


async def get_skill_gaps(
    db: AsyncSession,
    user: User,
    top_n: int = 50,
) -> dict:
    """
    Analyze missing skills across top job matches.
    Returns skills that appear most frequently in relevant jobs
    but are missing from the user's resume.
    """
    # Get user's resume
    resume_result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    resume = resume_result.scalar_one_or_none()
    if not resume:
        return {"gaps": [], "total_jobs_analyzed": 0}

    user_skills = set(s.lower() for s in (resume.skills or []))

    # Get active jobs
    jobs_result = await db.execute(
        select(Job).where(Job.is_active.is_(True)).limit(200)
    )
    jobs = jobs_result.scalars().all()

    # Count skill frequencies in jobs where user lacks the skill
    skill_freq: dict[str, int] = {}
    for job in jobs:
        for skill in (job.required_skills or []):
            skill_lower = skill.lower()
            if skill_lower not in user_skills:
                skill_freq[skill_lower] = skill_freq.get(skill_lower, 0) + 1

    # Sort by frequency
    sorted_gaps = sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    total = len(jobs)
    gaps = []
    for skill, freq in sorted_gaps:
        gaps.append({
            "skill": get_display_name(skill),
            "frequency": freq,
            "percentage": round(freq / total * 100, 1) if total > 0 else 0,
        })

    return {
        "gaps": gaps,
        "total_jobs_analyzed": total,
    }
