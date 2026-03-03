"""Hybrid tests: API setup → UI actions → DB assertions."""

import os

from src.api.services.auth_service import AuthService
from playwright.sync_api import expect
from src.models.user import UserLogin
from src.api.client import APIClient
from src.api.services.cart_service import CartService
from src.pages.checkout_page import CheckoutPage
from src.api.services.product_service import ProductService
from dotenv import load_dotenv

load_dotenv()
ui_url = os.getenv("UI_URL")
base_url = os.getenv("BASE_URL")


def test_ui_access_via_token_injection_should_be_authorized(enter_user, browser):
    """
    Test session restoration via API token.
    1. Obtain JWT via API.
    2. Inject token into browser localStorage.
    3. Verify UI recognizes user session without manual login.
    """
    user, _ = enter_user
    first_name = user.first_name
    user = UserLogin(email=user.email, password=user.password)
    auth = AuthService(APIClient(base_url))
    response = auth.login(user)
    data = response.json()
    token = data["access_token"]

    page = browser
    page.goto(ui_url)
    page.evaluate("localStorage.clear()")
    page.evaluate(f"localStorage.setItem('auth-token', '{token}')")
    page.goto(ui_url)

    expect(page.get_by_text(first_name)).to_be_visible()


def test_e2e_checkout_flow_with_api_setup_and_db_persistence(enter_user, browser, db_connection):
    """
    Verify full checkout lifecycle:
    - Setup: Create cart and add items via API (Hybrid approach).
    - UI: Complete shipping and payment forms.
    - Assert: Ensure order record is correctly persisted in the database.
    """
    user, response = enter_user
    user_id = response.json()["id"]
    credentials = UserLogin(email=user.email, password=user.password)
    auth = AuthService(APIClient(base_url))
    token = auth.login(credentials).json()["access_token"]

    client = APIClient(base_url)
    product_service = ProductService(client)
    cart_service = CartService(client)
    products = product_service.get_all().json()["data"]
    product_id = next(p["id"] for p in products if p["in_stock"] is True)
    cart_service.add_item(user_id, product_id, 1)

    page = browser
    page.goto(ui_url)
    page.evaluate("localStorage.clear()")
    page.evaluate(f"localStorage.setItem('auth-token', '{token}')")
    page.goto(ui_url)

    page.goto(f"{ui_url}/checkout")
    CheckoutPage(page).fill_address(
        street=user.address.street,
        city=user.address.city,
        state=user.address.state,
        country=user.address.country,
        postal_code=user.address.postal_code,
    )
    CheckoutPage(page).proceed_to_payment()
    CheckoutPage(page).payment_method("Cash on Delivery")
    CheckoutPage(page).confirm()

    cur = db_connection.cursor()
    cur.execute("SELECT * FROM orders WHERE billing_user_id = %s", (user_id,))
    order = cur.fetchone()
    cur.close()
    assert order is not None
