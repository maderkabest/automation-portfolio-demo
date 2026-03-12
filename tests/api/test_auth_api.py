"""API tests for user authentication endpoints."""

import os

import allure
from src.api.services.auth_service import AuthService
from src.api.client import APIClient
from src.models.user import UserLogin

base_url = os.getenv("BASE_URL")


@allure.epic("User Management")
@allure.feature("Authentication API")
@allure.title("Register new user returns HTTP 201")
@allure.description("Verify that registering a new user via API returns a 201 Created status code.")
@allure.severity(allure.severity_level.CRITICAL)
def test_register_returns_201(enter_user):
    """
    Verify user registration returns HTTP 201.
    API: Register new user via enter_user fixture.
    Assert: Response status code is 201.
    """
    user, response = enter_user
    assert response.status_code == 201


@allure.epic("User Management")
@allure.feature("Authentication API")
@allure.title("Login with valid credentials returns access token")
@allure.description("Verify that an existing user can log in and receive a valid JWT access token in the response.")
@allure.severity(allure.severity_level.CRITICAL)
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
