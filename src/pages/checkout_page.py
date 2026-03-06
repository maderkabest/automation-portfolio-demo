"""Page Object for the checkout page."""

from src.pages.base_page import BasePage


class CheckoutPage(BasePage):
    def fill_address(self, street, city, state, country, postal_code):
        self.page.get_by_placeholder("Your street *").fill(street)
        self.page.get_by_placeholder("Your city *").fill(city)
        self.page.get_by_placeholder("State *").fill(state)
        self.page.get_by_placeholder("Your country *").fill(country)
        self.page.get_by_placeholder("Your Postcode *").fill(postal_code)

    def proceed_to_payment(self):
        self.page.get_by_role("button", name="Proceed to checkout").click()

    def payment_method(self, method):
        self.page.locator("select").select_option(method)

    def confirm(self):
        self.page.get_by_role("button", name="Confirm").click()
