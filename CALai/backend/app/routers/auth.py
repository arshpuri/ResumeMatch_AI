"""
Auth router — /api/v1/auth/*
Endpoints: register, login, refresh, logout, me
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import DbSession, CurrentUser
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    UserResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: DbSession):
    """Email/password registration."""
    try:
        user = await auth_service.register_user(db, body.email, body.password, body.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    tokens = auth_service.create_tokens(user)
    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: DbSession):
    """Returns JWT access + refresh tokens."""
    user = await auth_service.authenticate_user(db, body.email, body.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    tokens = auth_service.create_tokens(user)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest):
    """Refresh access token using refresh token."""
    tokens = await auth_service.refresh_access_token(body.refresh_token)
    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    return tokens


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    """Invalidate refresh token (client should discard tokens)."""
    # In production, blacklist the refresh token via Redis
    return None


@router.get("/me", response_model=UserResponse)
async def get_me(user: CurrentUser):
    """Get current user from JWT."""
    return UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        status=user.status,
    )
