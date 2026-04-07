"""
Redis cache helpers — caching strategy from 06_backend_and_database.md.
"""

import json
from typing import Any

import redis.asyncio as redis

from app.config import get_settings

settings = get_settings()

_redis_pool: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            encoding="utf-8",
        )
    return _redis_pool


async def cache_get(key: str) -> Any | None:
    """Get a cached value, returns None on miss."""
    r = await get_redis()
    raw = await r.get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw


async def cache_set(key: str, value: Any, ttl_seconds: int = 300):
    """Set a cache value with TTL (default 5 min)."""
    r = await get_redis()
    raw = json.dumps(value, default=str)
    await r.set(key, raw, ex=ttl_seconds)


async def cache_delete(key: str):
    """Delete a cache entry."""
    r = await get_redis()
    await r.delete(key)


async def cache_delete_pattern(pattern: str):
    """Delete all keys matching a pattern."""
    r = await get_redis()
    keys = []
    async for key in r.scan_iter(match=pattern):
        keys.append(key)
    if keys:
        await r.delete(*keys)


async def add_to_blacklist(jti: str, ttl_seconds: int):
    """Blacklist a JWT token ID (for logout)."""
    r = await get_redis()
    await r.set(f"blacklist:{jti}", "1", ex=ttl_seconds)


async def is_blacklisted(jti: str) -> bool:
    """Check if a JWT token ID is blacklisted."""
    r = await get_redis()
    return await r.exists(f"blacklist:{jti}") > 0
