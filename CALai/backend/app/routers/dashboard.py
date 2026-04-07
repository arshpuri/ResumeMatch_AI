"""
Dashboard router — /api/v1/dashboard/*
Endpoints: stats, applications, match-trend, activity
"""

from fastapi import APIRouter

from app.dependencies import DbSession, CurrentUser
from app.schemas.dashboard import (
    DashboardStatsResponse,
    ApplicationsResponse,
    MatchTrendResponse,
)
from app.services import dashboard_service

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_stats(user: CurrentUser, db: DbSession):
    """Aggregated counts (new matches, applications, saved, avg score)."""
    return await dashboard_service.get_dashboard_stats(db, user)


@router.get("/applications", response_model=ApplicationsResponse)
async def get_applications(user: CurrentUser, db: DbSession):
    """Application tracker with status."""
    return await dashboard_service.get_applications(db, user)


@router.get("/match-trend", response_model=MatchTrendResponse)
async def get_match_trend(user: CurrentUser, db: DbSession):
    """Weekly match score averages."""
    return await dashboard_service.get_match_trend(db, user)


@router.get("/activity")
async def get_activity(user: CurrentUser, db: DbSession):
    """Recent user activity feed."""
    stats = await dashboard_service.get_dashboard_stats(db, user)
    return {"activity": [a.model_dump() for a in stats.recentActivity]}
