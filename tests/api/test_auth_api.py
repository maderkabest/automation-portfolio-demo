"""API tests for user authentication endpoints."""

import os

from src.api.services.auth_service import AuthService
from src.api.client import APIClient
from src.models.user import UserLogin

base_url = os.getenv("BASE_URL")


def test_register_returns_201(enter_user):
    """
    Verify user registration returns HTTP 201.
    API: Register new user via enter_user fixture.
    Assert: Response status code is 201.
    """
    user, response = enter_user
    assert response.status_code == 201


def test_login_returns_token(enter_user):
    """
    Verify login returns a valid JWT access token.
    API: Register user via enter_user fixture → login with credentials.
    Assert: Response contains "access_token".
    """
    user, _ = enter_user
    user = UserLogin(email=user.email, password=user.password)
    auth = AuthService(APIClient(base_url))
    response = auth.login(user)
    data = response.json()
    assert "access_token" in data
