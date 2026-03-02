"""UI tests for user authentication flows."""

import os
import re
from dotenv import load_dotenv
from src.pages.login_page import LoginPage
from playwright.sync_api import sync_playwright, expect

load_dotenv()


def test_user_can_login_with_valid_credentials(enter_user):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()

        user, _ = enter_user
        email = user.email
        password = user.password
        ui_url = os.getenv("UI_URL")

        login_page = LoginPage(page)
        login_page.navigate(f"{ui_url}/auth/login")
        login_page.login(email, password)

        expect(page).to_have_url(re.compile(r".*/account"))
        expect(page.get_by_role("heading", name="My account")).to_be_visible()
