from src.pages.base_page import BasePage


class LoginPage(BasePage):
    def login(self, email, password):
        self.page.get_by_placeholder("Your email").fill(email)
        self.page.get_by_placeholder("Your password").fill(password)
        self.page.get_by_role("button", name="Login").click()
