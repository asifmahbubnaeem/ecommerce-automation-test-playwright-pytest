from typing import List

from playwright.sync_api import Page

from .base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    INVENTORY_ITEM_IMG = ".inventory_item_img img"
    SORT_DROPDOWN = ".select_container select, select[data-test='product_sort_container'], select.product_sort_container"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def get_product_count(self) -> int:
        return self.page.locator(self.INVENTORY_ITEM).count()

    def get_product_names(self) -> List[str]:
        return self.page.locator(self.INVENTORY_ITEM_NAME).all_text_contents()

    def get_product_prices(self) -> List[float]:
        prices_text = self.page.locator(self.INVENTORY_ITEM_PRICE).all_text_contents()
        return [float(p.replace("$", "")) for p in prices_text]

    def get_product_image_srcs(self) -> List[str]:
        return self.page.locator(self.INVENTORY_ITEM_IMG).evaluate_all("elements => elements.map(e => e.src)")

    def wait_for_product_images_complete(self, timeout: int | None = None) -> None:
        """
        Wait until all product <img> elements report `complete === true`.
        Broken images typically keep reporting `complete === true` with `naturalWidth === 0`.
        """
        self.page.wait_for_function(
            """
            () => {
                const imgs = document.querySelectorAll('.inventory_item_img img');
                return imgs.length > 0 && Array.from(imgs).every(i => i.complete);
            }
            """,
            timeout=timeout or self.config.timeout,
        )

    def assert_product_images_loaded(self, timeout: int | None = None) -> None:
        self.wait_for_product_images_complete(timeout=timeout)
        natural_widths = self.page.locator(self.INVENTORY_ITEM_IMG).evaluate_all(
            "elements => elements.map(e => e.naturalWidth)"
        )
        assert all(w > 0 for w in natural_widths), (
            "Expected all product images to load (naturalWidth > 0). "
            f"Got naturalWidth values: {natural_widths}"
        )

    def sort_by(self, option_value: str) -> None:
        self.page.select_option(self.SORT_DROPDOWN, option_value)

    def add_to_cart(self, product_name: str) -> None:
        item = self.page.locator(self.INVENTORY_ITEM).filter(has_text=product_name)
        item.locator("button").click()

    def open_cart(self) -> None:
        self.page.click(self.CART_LINK)

    def get_cart_badge_count(self) -> int:
        if not self.page.locator(self.CART_BADGE).is_visible():
            return 0
        return int(self.page.inner_text(self.CART_BADGE))

