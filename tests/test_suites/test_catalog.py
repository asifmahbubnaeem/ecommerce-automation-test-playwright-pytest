from playwright.sync_api import Page

from tests.fixtures import data_loader
from tests.pages.inventory_page import InventoryPage
from tests.pages.login_page import LoginPage
from tests.utils.assertions import assert_sorted
from tests.utils.visual import compare_image_srcs


def _login_as(page: Page, user_key: str) -> InventoryPage:
    user = data_loader.get_user(user_key)
    login_page = LoginPage(page)
    login_page.login(user["username"], user["password"])
    return InventoryPage(page)


def test_product_listing_loads_correctly(page: Page):
    inventory_page = _login_as(page, "standard_user")
    assert inventory_page.get_product_count() > 0
    names = inventory_page.get_product_names()
    prices = inventory_page.get_product_prices()
    assert len(names) == len(prices) > 0


def test_sort_by_name_az(page: Page):
    inventory_page = _login_as(page, "standard_user")
    inventory_page.sort_by("az")
    names = inventory_page.get_product_names()
    assert_sorted(names)


def test_sort_by_name_za(page: Page):
    inventory_page = _login_as(page, "standard_user")
    inventory_page.sort_by("za")
    names = inventory_page.get_product_names()
    assert_sorted(names, reverse=True)


def test_sort_by_price_low_high(page: Page):
    inventory_page = _login_as(page, "standard_user")
    inventory_page.sort_by("lohi")
    prices = inventory_page.get_product_prices()
    assert_sorted(prices)


def test_sort_by_price_high_low(page: Page):
    inventory_page = _login_as(page, "standard_user")
    inventory_page.sort_by("hilo")
    prices = inventory_page.get_product_prices()
    assert_sorted(prices, reverse=True)


def test_problem_user_image_mismatches(page: Page):
    standard_inventory = _login_as(page, "standard_user")
    baseline_srcs = standard_inventory.get_product_image_srcs()
    page.context.clear_cookies()

    problem_inventory = _login_as(page, "problem_user")
    problem_srcs = problem_inventory.get_product_image_srcs()

    assert not compare_image_srcs(
        baseline_srcs, problem_srcs
    ), "Expected image src mismatches for problem_user"

