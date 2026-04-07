"""
Jobs router — /api/v1/jobs/*
Endpoints: feed, detail, search, save, unsave, saved, apply, dismiss
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import DbSession, CurrentUser
from app.schemas.job import (
    JobFeedResponse,
    JobDetailResponse,
    JobSearchResponse,
    JobActionResponse,
)
from app.services import job_service

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


@router.get("/feed", response_model=JobFeedResponse)
async def get_job_feed(
    user: CurrentUser,
    db: DbSession,
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=50),
):
    """Personalized job feed (paginated, cursor-based)."""
    result = await job_service.get_job_feed(db, user, cursor=cursor, limit=limit)
    return JobFeedResponse(**result)


@router.get("/search", response_model=JobSearchResponse)
async def search_jobs(
    user: CurrentUser,
    db: DbSession,
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
):
    """Full-text search (pg_trgm trigram matching)."""
    result = await job_service.search_jobs(db, user, query=q, limit=limit)
    return JobSearchResponse(**result)


@router.get("/saved")
async def get_saved_jobs(user: CurrentUser, db: DbSession):
    """List saved jobs."""
    saved = await job_service.get_saved_jobs(db, user)
    return {"jobs": saved}


@router.get("/{job_id}", response_model=JobDetailResponse)
async def get_job_detail(
    job_id: str,
    user: CurrentUser,
    db: DbSession,
):
    """Job detail with match analysis breakdown."""
    result = await job_service.get_job_detail(db, user, job_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return result


@router.post("/{job_id}/save", response_model=JobActionResponse)
async def save_job(job_id: str, user: CurrentUser, db: DbSession):
    """Bookmark a job."""
    try:
        await job_service.save_job(db, user, job_id)
        return JobActionResponse(success=True, message="Job saved")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{job_id}/save", response_model=JobActionResponse)
async def unsave_job(job_id: str, user: CurrentUser, db: DbSession):
    """Remove bookmark."""
    try:
        await job_service.unsave_job(db, user, job_id)
        return JobActionResponse(success=True, message="Job unsaved")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{job_id}/apply", response_model=JobActionResponse)
async def apply_to_job(job_id: str, user: CurrentUser, db: DbSession):
    """Track application."""
    try:
        await job_service.apply_to_job(db, user, job_id)
        return JobActionResponse(success=True, message="Application submitted")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/{job_id}/dismiss", response_model=JobActionResponse)
async def dismiss_job(job_id: str, user: CurrentUser, db: DbSession):
    """Hide from feed."""
    await job_service.dismiss_job(db, user, job_id)
    return JobActionResponse(success=True, message="Job dismissed")
