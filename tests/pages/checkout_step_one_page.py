from playwright.sync_api import Page

from .base_page import BasePage


class CheckoutStepOnePage(BasePage):
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.page.fill(self.FIRST_NAME_INPUT, first_name)
        self.page.fill(self.LAST_NAME_INPUT, last_name)
        self.page.fill(self.POSTAL_CODE_INPUT, postal_code)

    def continue_to_step_two(self) -> None:
        self.page.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        self.wait_for_visible(self.ERROR_MESSAGE)
        return self.page.inner_text(self.ERROR_MESSAGE)

