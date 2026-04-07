"""
Resume router — /api/v1/resume/*
Endpoints: upload, get, update, delete, parsing-status (SSE)
"""

import asyncio
import json

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import DbSession, CurrentUser
from app.schemas.resume import (
    ResumeUploadResponse,
    ParsedResumeResponse,
    ResumeUpdateRequest,
)
from app.services import resume_service
from app.parsing.pipeline import get_parsing_progress, clear_parsing_progress

router = APIRouter(prefix="/api/v1/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    user: CurrentUser = None,
    db: DbSession = None,
):
    """Accept PDF/DOCX, store in S3, trigger async parse."""
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Maximum 10MB.",
        )

    content_type = file.content_type or "application/octet-stream"
    file_bytes = await file.read()
    filename = file.filename or "resume.pdf"

    try:
        result = await resume_service.upload_and_parse_resume(
            db, user, file_bytes, filename, content_type
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return ResumeUploadResponse(**result)


@router.get("", response_model=ParsedResumeResponse)
async def get_resume(user: CurrentUser, db: DbSession):
    """Return parsed resume for current user."""
    resume = await resume_service.get_parsed_resume(db, user)
    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume found. Upload one first.",
        )

    return ParsedResumeResponse(
        id=str(resume.id),
        file_type=resume.file_type,
        skills=resume.skills or [],
        experience_years=float(resume.experience_years) if resume.experience_years else None,
        keywords=resume.keywords or [],
        parsing_confidence=float(resume.parsing_confidence) if resume.parsing_confidence else None,
        parsed_data=resume.parsed_data or {},
    )


@router.put("", response_model=ParsedResumeResponse)
async def update_resume(
    body: ResumeUpdateRequest,
    user: CurrentUser,
    db: DbSession,
):
    """Manually edit parsed fields."""
    try:
        resume = await resume_service.update_parsed_resume(
            db, user, skills=body.skills, parsed_data=body.parsed_data
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return ParsedResumeResponse(
        id=str(resume.id),
        file_type=resume.file_type,
        skills=resume.skills or [],
        experience_years=float(resume.experience_years) if resume.experience_years else None,
        keywords=resume.keywords or [],
        parsing_confidence=float(resume.parsing_confidence) if resume.parsing_confidence else None,
        parsed_data=resume.parsed_data or {},
    )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(user: CurrentUser, db: DbSession):
    """Delete resume + parsed data."""
    await resume_service.delete_resume(db, user)
    return None


@router.get("/parsing-status")
async def parsing_status(user: CurrentUser):
    """
    Server-Sent Events stream for real-time parsing progress.
    Frontend connects to this endpoint to show parsing progress UI.
    """
    user_id = str(user.id)

    async def event_stream():
        last_index = 0
        max_wait = 120  # Timeout after 2 minutes
        waited = 0

        while waited < max_wait:
            events = get_parsing_progress(user_id)

            if len(events) > last_index:
                for event in events[last_index:]:
                    data = json.dumps(event)
                    yield f"data: {data}\n\n"
                last_index = len(events)

                # Check if parsing is complete
                if events and events[-1].get("progress", 0) >= 100:
                    clear_parsing_progress(user_id)
                    break

                if events and events[-1].get("status") == "error":
                    clear_parsing_progress(user_id)
                    break

            await asyncio.sleep(0.5)
            waited += 0.5

        # Send a final done event if we timed out
        yield f"data: {json.dumps({'step': 'complete', 'progress': 100, 'status': 'done'})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
