"""Page Object for the shopping cart page."""

from src.pages.base_page import BasePage


class CartPage(BasePage):
    def proceed_to_checkout(self):
        self.page.get_by_role("button", name="Proceed to checkout").click()
