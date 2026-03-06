"""Page Object for the product detail page."""

from src.pages.base_page import BasePage


class ProductPage(BasePage):
    def add_to_cart(self):
        self.page.locator("[data-test='add-to-cart']").click()
