from decimal import Decimal

from playwright.sync_api import Page

from .base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    ITEM_TOTAL = ".summary_subtotal_label"
    TAX = ".summary_tax_label"
    TOTAL = ".summary_total_label"
    FINISH_BUTTON = "[data-test='finish']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def _extract_amount(self, text: str) -> Decimal:
        amount_str = text.split("$")[-1]
        return Decimal(amount_str)

    def get_item_total(self) -> Decimal:
        text = self.page.inner_text(self.ITEM_TOTAL)
        return self._extract_amount(text)

    def get_tax(self) -> Decimal:
        text = self.page.inner_text(self.TAX)
        return self._extract_amount(text)

    def get_total(self) -> Decimal:
        text = self.page.inner_text(self.TOTAL)
        return self._extract_amount(text)

    def finish_order(self) -> None:
        self.page.click(self.FINISH_BUTTON)

