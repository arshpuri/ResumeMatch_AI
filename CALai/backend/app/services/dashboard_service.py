"""
Dashboard service — aggregated stats, applications, match trends, activity.
Response format matches frontend DASHBOARD_STATS shape exactly.
Aligned with Supabase schema (match_score column).
"""

import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.resume import ParsedResume
from app.models.application import Application
from app.models.interaction import UserInteraction, SavedJob
from app.models.job import Job
from app.schemas.dashboard import (
    DashboardStatsResponse,
    ActivityItem,
    ApplicationItem,
    ApplicationsResponse,
    MatchTrendPoint,
    MatchTrendResponse,
)


async def get_dashboard_stats(
    db: AsyncSession,
    user: User,
) -> DashboardStatsResponse:
    """
    Compute aggregated dashboard stats.
    Matches frontend DASHBOARD_STATS shape:
    { totalParses, jobsMatched, interviewsSecured, profileAppearances, recentActivity }
    """
    # Total parses (number of resumes parsed)
    parse_result = await db.execute(
        select(func.count(ParsedResume.id)).where(ParsedResume.user_id == user.id)
    )
    total_parses = parse_result.scalar() or 0

    # Jobs matched (active jobs count as available matches)
    jobs_result = await db.execute(
        select(func.count(Job.id)).where(Job.is_active.is_(True))
    )
    jobs_matched = jobs_result.scalar() or 0

    # Interviews secured (applications with status 'interviewing')
    interview_result = await db.execute(
        select(func.count(Application.id)).where(
            Application.user_id == user.id,
            Application.status == "interviewing",
        )
    )
    interviews_secured = interview_result.scalar() or 0

    # Profile search appearances (view interactions on user's applications)
    view_result = await db.execute(
        select(func.count(UserInteraction.id)).where(
            UserInteraction.user_id == user.id,
            UserInteraction.action.in_(["view", "click"]),
        )
    )
    profile_appearances = view_result.scalar() or 0

    # Recent activity
    recent_result = await db.execute(
        select(UserInteraction)
        .where(UserInteraction.user_id == user.id)
        .order_by(UserInteraction.created_at.desc())
        .limit(10)
    )
    recent_interactions = recent_result.scalars().all()

    recent_activity = []
    for i, inter in enumerate(recent_interactions):
        action_text = _format_action(inter.action, inter.job)
        time_text = _format_relative_time(inter.created_at)
        recent_activity.append(ActivityItem(
            id=f"act{i+1}",
            action=action_text,
            time=time_text,
        ))

    # If no real activity, provide meaningful empty state
    if not recent_activity:
        recent_activity.append(ActivityItem(
            id="act1",
            action="Welcome to ResumeMatch AI! Upload your resume to get started.",
            time="Just now",
        ))

    return DashboardStatsResponse(
        totalParses=total_parses if total_parses > 0 else 1,
        jobsMatched=jobs_matched,
        interviewsSecured=interviews_secured,
        profileAppearances=profile_appearances,
        recentActivity=recent_activity,
    )


async def get_applications(
    db: AsyncSession,
    user: User,
) -> ApplicationsResponse:
    """Get user's application history."""
    result = await db.execute(
        select(Application)
        .where(Application.user_id == user.id)
        .order_by(Application.applied_at.desc())
    )
    apps = result.scalars().all()

    items = []
    for app in apps:
        job = app.job
        items.append(ApplicationItem(
            id=str(app.id),
            jobTitle=job.title if job else "Unknown",
            company=job.company if job else "Unknown",
            status=app.status,
            appliedAt=app.applied_at.isoformat() if app.applied_at else "",
            matchScore=float(app.match_score) if app.match_score else None,
        ))

    return ApplicationsResponse(applications=items, total=len(items))


async def get_match_trend(
    db: AsyncSession,
    user: User,
) -> MatchTrendResponse:
    """Get weekly average match scores for charting."""
    # Generate last 12 weeks of data
    now = datetime.now(timezone.utc)
    data = []

    for i in range(11, -1, -1):
        week_start = now - timedelta(weeks=i)
        week_label = week_start.strftime("%b %d")

        # Query average match score for that week
        week_end = week_start + timedelta(weeks=1)
        result = await db.execute(
            select(func.avg(Application.match_score)).where(
                Application.user_id == user.id,
                Application.applied_at >= week_start,
                Application.applied_at < week_end,
            )
        )
        avg = result.scalar()
        data.append(MatchTrendPoint(
            week=week_label,
            avgScore=round(float(avg), 1) if avg else 0.0,
        ))

    return MatchTrendResponse(data=data)


def _format_action(action: str, job) -> str:
    """Format an interaction action for display."""
    job_title = job.title if job else "a job"
    company = job.company if job else ""

    action_map = {
        "view": f"Viewed {job_title}",
        "click": f"Clicked on {job_title}",
        "save": f"Saved {job_title} at {company}",
        "unsave": f"Removed {job_title} from saved",
        "apply": f"Applied to {job_title} at {company}",
        "dismiss": f"Dismissed {job_title}",
    }
    return action_map.get(action, f"{action} on {job_title}")


def _format_relative_time(dt: datetime | None) -> str:
    """Format datetime as relative time string."""
    if not dt:
        return "Just now"

    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    delta = now - dt
    seconds = int(delta.total_seconds())

    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        mins = seconds // 60
        return f"{mins} min{'s' if mins != 1 else ''} ago"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hr{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = seconds // 86400
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return dt.strftime("%b %d, %Y")
