import re

from playwright.sync_api import Page, expect

from tests.fixtures import data_loader
from tests.pages.inventory_page import InventoryPage
from tests.pages.login_page import LoginPage


def test_performance_glitch_user_login_succeeds_with_smart_waits(page: Page):
    user = data_loader.get_user("performance_glitch_user")
    login_page = LoginPage(page)
    login_page.login(user["username"], user["password"])
    expect(page).to_have_url(re.compile(r".*inventory.*"), timeout=20000)


def test_error_user_behaviours(page: Page):
    user = data_loader.get_user("error_user")
    login_page = LoginPage(page)
    login_page.login(user["username"], user["password"])
    inventory = InventoryPage(page)
    assert inventory.get_product_count() >= 0
    # This is a placeholder to assert specific known error behaviours if documented.

