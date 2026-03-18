from playwright.sync_api import Page

from tests.fixtures import data_loader
from tests.pages.cart_page import CartPage
from tests.pages.inventory_page import InventoryPage
from tests.pages.login_page import LoginPage
from tests.utils.assertions import assert_cart_badge_count


def _login_and_go_to_inventory(page: Page) -> InventoryPage:
    user = data_loader.get_user("standard_user")
    login_page = LoginPage(page)
    login_page.login(user["username"], user["password"])
    return InventoryPage(page)


def test_add_single_item_updates_cart_badge(page: Page):
    inventory_page = _login_and_go_to_inventory(page)
    first_item_name = inventory_page.get_product_names()[0]
    inventory_page.add_to_cart(first_item_name)
    count = inventory_page.get_cart_badge_count()
    assert_cart_badge_count(count, 1)


def test_add_multiple_items_appear_in_cart(page: Page):
    inventory_page = _login_and_go_to_inventory(page)
    names = inventory_page.get_product_names()[:2]
    for name in names:
        inventory_page.add_to_cart(name)
    inventory_page.open_cart()
    cart_page = CartPage(page)
    cart_items = cart_page.get_cart_items()
    for name in names:
        assert name in cart_items


def test_remove_item_updates_cart(page: Page):
    inventory_page = _login_and_go_to_inventory(page)
    names = inventory_page.get_product_names()[:2]
    for name in names:
        inventory_page.add_to_cart(name)
    inventory_page.open_cart()
    cart_page = CartPage(page)
    cart_page.remove_item(names[0])
    remaining = cart_page.get_cart_items()
    assert names[0] not in remaining


def test_cart_persists_across_navigation(page: Page):
    inventory_page = _login_and_go_to_inventory(page)
    name = inventory_page.get_product_names()[0]
    inventory_page.add_to_cart(name)
    inventory_page.open_cart()
    page.click("#continue-shopping")
    inventory_page.open_cart()
    cart_page = CartPage(page)
    items = cart_page.get_cart_items()
    assert name in items

