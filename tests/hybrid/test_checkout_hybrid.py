"""Hybrid tests: API setup → UI actions → API assertions."""

import os

from src.api.client import APIClient
from src.api.services.auth_service import AuthService
from src.api.services.invoice_service import InvoiceService
from src.api.services.product_service import ProductService
from src.models.user import UserLogin
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage
from src.pages.product_page import ProductPage
from playwright.sync_api import expect

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


def test_e2e_checkout_flow_with_api_setup_and_api_assertion(enter_user, browser):
    """
    Verify full E2E checkout lifecycle.
    API: Register + login → get JWT token → fetch first in-stock product.
    UI:  Inject token → navigate to product → add to cart → complete checkout form.
    Assert: "Thanks for your order!" visible in UI, invoice exists via API.
    """
    user, _ = enter_user
    credentials = UserLogin(email=user.email, password=user.password)
    auth = AuthService(APIClient(base_url))
    token = auth.login(credentials).json()["access_token"]

    client = APIClient(base_url)
    product_service = ProductService(client)
    products = product_service.get_all().json()["data"]
    product_id = next(p["id"] for p in products if p["in_stock"] is True)

    page = browser
    page.evaluate("localStorage.clear()")
    page.evaluate(f"localStorage.setItem('auth-token', '{token}')")
    page.goto(f"{ui_url}/product/{product_id}")
    page.wait_for_load_state("networkidle")
    ProductPage(page).add_to_cart()
    page.locator("[data-test='nav-cart']").click()
    page.wait_for_load_state("networkidle")
    CartPage(page).proceed_to_checkout()  # opens cart review page
    page.wait_for_load_state("networkidle")
    CartPage(page).proceed_to_checkout()  # proceeds to checkout form
    page.wait_for_load_state("networkidle")

    checkout = CheckoutPage(page)
    checkout.fill_address(
        street=user.address.street,
        city=user.address.city,
        state=user.address.state,
        country=user.address.country,
        postal_code=user.address.postal_code,
    )
    checkout.proceed_to_payment()
    checkout.payment_method("Cash on Delivery")
    checkout.confirm()
    expect(page.get_by_text("Payment was successful")).to_be_visible()
    checkout.confirm()
    expect(page.get_by_text("Thanks for your order!")).to_be_visible()
    invoice_service = InvoiceService(APIClient(base_url))
    invoices = invoice_service.get_all(token).json()
    assert len(invoices["data"]) > 0
