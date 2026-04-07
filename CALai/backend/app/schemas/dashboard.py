"""
Dashboard schemas — matches frontend DASHBOARD_STATS shape exactly.

Frontend expects:
{
  totalParses, jobsMatched, interviewsSecured, profileAppearances,
  recentActivity: [{ id, action, time }]
}
"""

from pydantic import BaseModel


class ActivityItem(BaseModel):
    id: str
    action: str
    time: str


class DashboardStatsResponse(BaseModel):
    """Matches frontend DASHBOARD_STATS shape exactly."""
    totalParses: int = 0
    jobsMatched: int = 0
    interviewsSecured: int = 0
    profileAppearances: int = 0
    recentActivity: list[ActivityItem] = []


class ApplicationItem(BaseModel):
    id: str
    jobTitle: str
    company: str
    status: str
    appliedAt: str
    matchScore: float | None = None


class ApplicationsResponse(BaseModel):
    applications: list[ApplicationItem]
    total: int = 0


class MatchTrendPoint(BaseModel):
    week: str
    avgScore: float


class MatchTrendResponse(BaseModel):
    data: list[MatchTrendPoint]
