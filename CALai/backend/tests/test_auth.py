"""
Tests for auth endpoints.
"""

import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_register_and_login(client):
    # Register
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPass123!",
            "name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPass123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    # Get current user
    token = data["access_token"]
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword",
        },
    )
    assert response.status_code == 401
