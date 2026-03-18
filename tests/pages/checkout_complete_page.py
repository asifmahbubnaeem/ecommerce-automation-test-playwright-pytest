from playwright.sync_api import Page, expect

from .base_page import BasePage


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def is_confirmation_displayed(self) -> bool:
        return self.page.locator(self.COMPLETE_HEADER).is_visible()

    def get_confirmation_text(self) -> str:
        return self.page.inner_text(self.COMPLETE_TEXT)

    def get_confirmation_header_text(self) -> str:
        return self.page.inner_text(self.COMPLETE_HEADER)

    def assert_confirmation(self) -> None:
        expect(self.page.locator(self.COMPLETE_HEADER)).to_be_visible()

