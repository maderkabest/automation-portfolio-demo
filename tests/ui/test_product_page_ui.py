"""UI tests for product details."""

import os
from playwright.sync_api import expect
from dotenv import load_dotenv

load_dotenv()
ui_url = os.getenv("UI_URL")


def test_product_page_displays_details(browser):
    """
    Verify product page displays required details.
    UI:  Navigate to home → click first product → verify product page.
    Assert: Name and price visible, "Out of stock" not visible, "Add to cart" button visible.
    """
    page = browser
    page.goto(f"{ui_url}")
    page.locator("[data-test='product-name']").first.click()
    page.wait_for_load_state("networkidle")
    expect(page.locator("[data-test='product-name']")).to_be_visible()
    expect(page.locator("[data-test='unit-price']")).to_be_visible()
    expect(page.get_by_text("Out of stock")).not_to_be_visible()
    expect(page.get_by_role("button", name="Add to cart")).to_be_visible()
