"""API tests for user authentication endpoints."""

import os

from dotenv import load_dotenv
from src.api.services.auth_service import AuthService
from src.api.client import APIClient
from src.models.user import UserLogin

load_dotenv()
base_url = os.getenv("BASE_URL")


def test_register_returns_201(enter_user):
    user, response = enter_user
    assert response.status_code == 201


def test_login_returns_token(enter_user):
    user, _ = enter_user
    user = UserLogin(email=user.email, password=user.password)
    auth = AuthService(APIClient(base_url))
    response = auth.login(user)
    data = response.json()
    assert "access_token" in data
