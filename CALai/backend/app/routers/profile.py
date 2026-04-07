"""
Profile router — /api/v1/profile/*
Endpoints: get, update, update skills, skill-gaps
"""

from fastapi import APIRouter, HTTPException, status

from app.dependencies import DbSession, CurrentUser
from app.schemas.user import (
    UserProfileResponse,
    ProfileUpdateRequest,
    SkillsUpdateRequest,
    SkillGapResponse,
)
from app.services import user_service, match_service

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


@router.get("", response_model=UserProfileResponse)
async def get_profile(user: CurrentUser, db: DbSession):
    """Full user profile."""
    return await user_service.get_user_profile(db, user)


@router.put("", response_model=UserProfileResponse)
async def update_profile(
    body: ProfileUpdateRequest,
    user: CurrentUser,
    db: DbSession,
):
    """Update profile fields."""
    await user_service.update_user_profile(db, user, body)
    return await user_service.get_user_profile(db, user)


@router.put("/skills")
async def update_skills(
    body: SkillsUpdateRequest,
    user: CurrentUser,
    db: DbSession,
):
    """Update skills (triggers match score recalc)."""
    try:
        updated = await user_service.update_user_skills(db, user, body.skills)
        return {"skills": updated, "message": "Skills updated. Match scores will be recalculated."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/skill-gaps", response_model=SkillGapResponse)
async def get_skill_gaps(user: CurrentUser, db: DbSession):
    """Missing skills analysis across top job matches."""
    result = await match_service.get_skill_gaps(db, user)
    return SkillGapResponse(**result)
