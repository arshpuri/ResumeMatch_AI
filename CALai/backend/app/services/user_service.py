"""
User/Profile service — CRUD operations for user profile.
Computes profile completion score, formats response for frontend.
"""

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.resume import ParsedResume
from app.schemas.user import (
    UserProfileResponse,
    ExperienceItem,
    EducationItem,
    ProfileUpdateRequest,
)


async def get_user_profile(db: AsyncSession, user: User) -> UserProfileResponse:
    """
    Build the full profile response matching frontend USER_PROFILE shape.
    Merges data from User model + ParsedResume.
    """
    # Fetch resume data
    result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    resume = result.scalar_one_or_none()

    skills: list[str] = []
    experience: list[ExperienceItem] = []
    education: list[EducationItem] = []

    if resume and resume.parsed_data:
        # Extract skills
        skills = resume.skills or []

        # Extract experience from parsed_data
        parsed_exp = resume.parsed_data.get("experience", [])
        for i, exp in enumerate(parsed_exp):
            period = ""
            if exp.get("start_date"):
                end = exp.get("end_date", "Present")
                period = f"{exp['start_date']} - {end}"

            bullets = exp.get("achievements", [])
            if not bullets and exp.get("description"):
                bullets = [exp["description"]]

            experience.append(ExperienceItem(
                id=f"exp{i+1}",
                role=exp.get("title", ""),
                company=exp.get("company", ""),
                period=period,
                bullets=bullets,
            ))

        # Extract education from parsed_data
        parsed_edu = resume.parsed_data.get("education", [])
        for i, edu in enumerate(parsed_edu):
            period = ""
            if edu.get("start_date"):
                end = edu.get("end_date", "")
                period = f"{edu['start_date']} - {end}"

            degree = edu.get("degree", "")
            field = edu.get("field_of_study", "")
            if field and degree:
                degree = f"{degree} in {field}"

            education.append(EducationItem(
                id=f"edu{i+1}",
                degree=degree,
                institution=edu.get("institution", ""),
                period=period,
            ))

    completion = _compute_completion_score(user, resume)

    return UserProfileResponse(
        name=user.name,
        headline=user.headline or "",
        location=user.location or "",
        status=user.status or "Open to Work",
        completionScore=completion,
        skills=skills,
        experience=experience,
        education=education,
    )


async def update_user_profile(
    db: AsyncSession,
    user: User,
    data: ProfileUpdateRequest,
) -> User:
    """Update user profile fields."""
    if data.name is not None:
        user.name = data.name
    if data.headline is not None:
        user.headline = data.headline
    if data.location is not None:
        user.location = data.location
    if data.status is not None:
        user.status = data.status
    if data.phone is not None:
        user.phone = data.phone

    await db.flush()
    return user


async def update_user_skills(
    db: AsyncSession,
    user: User,
    skills: list[str],
) -> list[str]:
    """Update skills on the parsed resume."""
    result = await db.execute(
        select(ParsedResume).where(ParsedResume.user_id == user.id)
    )
    resume = result.scalar_one_or_none()
    if resume is None:
        raise ValueError("No resume found. Upload a resume first.")

    resume.skills = skills
    await db.flush()
    return skills


def _compute_completion_score(user: User, resume: ParsedResume | None) -> int:
    """Compute profile completion percentage (0-100)."""
    score = 0
    max_score = 100

    # Basic info (30 points)
    if user.name:
        score += 10
    if user.headline:
        score += 10
    if user.location:
        score += 5
    if user.phone:
        score += 5

    # Resume uploaded (20 points)
    if resume:
        score += 20

    # Skills (20 points)
    if resume and resume.skills:
        score += min(20, len(resume.skills) * 4)

    # Experience (15 points)
    if resume and resume.parsed_data:
        exp = resume.parsed_data.get("experience", [])
        if exp:
            score += 15

    # Education (15 points)
    if resume and resume.parsed_data:
        edu = resume.parsed_data.get("education", [])
        if edu:
            score += 15

    return min(score, max_score)
