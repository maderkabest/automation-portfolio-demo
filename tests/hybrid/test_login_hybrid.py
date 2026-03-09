"""Hybrid tests: API setup → UI actions."""

import os
import re
from src.pages.login_page import LoginPage
from playwright.sync_api import expect
from dotenv import load_dotenv

load_dotenv()
ui_url = os.getenv("UI_URL")


def test_user_can_login_with_valid_credentials(enter_user, browser):
    """
    Verify UI login flow with API-created user.
    API: Register user via API (enter_user fixture).
    UI:  Navigate to login page → submit credentials.
    Assert: Redirected to /account, heading "My account" visible.
    """
    user, _ = enter_user
    email = user.email
    password = user.password

    page = browser

    login_page = LoginPage(page)
    login_page.navigate(f"{ui_url}/auth/login")
    login_page.login(email, password)

    expect(page).to_have_url(re.compile(r".*/account"))
    expect(page.get_by_role("heading", name="My account")).to_be_visible()
