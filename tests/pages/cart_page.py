from typing import List

from playwright.sync_api import Page

from .base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    REMOVE_BUTTON = "button[data-test^='remove-']"
    CHECKOUT_BUTTON = "[data-test='checkout']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def get_cart_items(self) -> List[str]:
        return self.page.locator(self.CART_ITEM_NAME).all_text_contents()

    def remove_item(self, name: str) -> None:
        item = self.page.locator(self.CART_ITEM).filter(has_text=name)
        item.locator(self.REMOVE_BUTTON).click()

    def proceed_to_checkout(self) -> None:
        self.page.click(self.CHECKOUT_BUTTON)

