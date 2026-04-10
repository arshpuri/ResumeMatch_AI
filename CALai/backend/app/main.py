"""
FastAPI application entrypoint.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, resume, jobs, profile, dashboard

# Import models so they register with Base.metadata
import app.models  # noqa: F401

settings = get_settings()

logging.basicConfig(
    level=logging.DEBUG if settings.APP_DEBUG else logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: verify DB connection. Shutdown: dispose engine."""
    logger.info("Starting ResumeMatch AI Backend...")

    # Verify database connection (skip create_all for Supabase — tables already exist)
    try:
        async with engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("Database connection verified ✅")
    except Exception as e:
        logger.warning(f"Database connection failed: {e}")
        logger.warning("Backend starting without DB — set DATABASE_URL in .env")

    # Ensure S3 bucket exists
    try:
        from app.utils.storage import ensure_bucket_exists
        ensure_bucket_exists()
        logger.info("S3 bucket ready.")
    except Exception as e:
        logger.warning(f"S3 bucket setup skipped: {e}")

    yield

    # Shutdown
    await engine.dispose()
    logger.info("Backend shutdown complete.")


app = FastAPI(
    title="ResumeMatch AI",
    description="Backend API for ResumeMatch AI — resume parsing, job matching, and recommendations.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(jobs.router)
app.include_router(profile.router)
app.include_router(dashboard.router)


# ── Health check ──
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "resumematch-backend", "version": "1.0.0"}


@app.get("/api/v1/health", tags=["health"])
async def api_health():
    return {"status": "ok"}
