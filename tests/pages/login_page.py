from playwright.sync_api import Page, expect

from .base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.goto("")

    def login(self, username: str, password: str) -> None:
        self.open()
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        self.wait_for_visible(self.ERROR_MESSAGE)
        return self.page.inner_text(self.ERROR_MESSAGE)

    def assert_login_error(self, expected_text: str) -> None:
        expect(self.page.locator(self.ERROR_MESSAGE)).to_contain_text(expected_text)

