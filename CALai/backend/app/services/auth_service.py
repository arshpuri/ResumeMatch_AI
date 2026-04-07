"""
Auth service — handles registration, login, token management.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.utils.cache import add_to_blacklist


async def register_user(
    db: AsyncSession,
    email: str,
    password: str,
    name: str,
) -> User:
    """Register a new user with email/password."""
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == email))
    existing = result.scalar_one_or_none()
    if existing:
        raise ValueError("Email already registered")

    user = User(
        email=email,
        password_hash=hash_password(password),
        name=name,
        auth_provider="email",
    )
    db.add(user)
    await db.flush()
    return user


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> User | None:
    """Verify email/password and return the user if valid."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        return None
    if user.password_hash is None:
        return None  # OAuth-only user
    if not verify_password(password, user.password_hash):
        return None

    # Update last login
    user.last_login_at = datetime.now(timezone.utc)
    return user


def create_tokens(user: User) -> dict:
    """Generate access + refresh token pair for a user."""
    user_id = str(user.id)
    access_token = create_access_token({"sub": user_id, "role": user.role})
    refresh_token = create_refresh_token(user_id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def refresh_access_token(refresh_token_str: str) -> dict | None:
    """Validate a refresh token and issue new tokens."""
    payload = decode_refresh_token(refresh_token_str)
    if payload is None:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    # Blacklist the old refresh token
    jti = payload.get("jti", "")
    exp = payload.get("exp", 0)
    import time
    ttl = max(0, int(exp - time.time()))
    if jti and ttl > 0:
        await add_to_blacklist(jti, ttl)

    access_token = create_access_token({"sub": user_id})
    new_refresh = create_refresh_token(user_id)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh,
        "token_type": "bearer",
    }
