from playwright.sync_api import Page

from tests.fixtures import data_loader
from tests.pages.inventory_page import InventoryPage
from tests.pages.login_page import LoginPage
from tests.utils.url_assertions import expect_on

ERROR_USER_SORT_ALERT_MESSAGE = (
    "Sorting is broken! This error has been reported to Backtrace."
)
INVENTORY_ITEM = ".inventory_item"


def _assert_error_user_sort_shows_alert(page: Page, sort_option: str) -> None:
    user = data_loader.get_user("error_user")
    login_page = LoginPage(page)
    login_page.login(user["username"], user["password"])
    inventory = InventoryPage(page)
    assert inventory.get_product_count() >= 0
    dialog_messages = []

    def handle_dialog(dialog) -> None:
        dialog_messages.append(dialog.message)
        dialog.accept()

    page.once("dialog", handle_dialog)
    inventory.sort_by(sort_option)

    assert dialog_messages == [ERROR_USER_SORT_ALERT_MESSAGE]


def _login_as_error_user(page: Page) -> InventoryPage:
    user = data_loader.get_user("error_user")
    login_page = LoginPage(page)
    login_page.login(user["username"], user["password"])
    return InventoryPage(page)


def test_performance_glitch_user_login_succeeds_with_smart_waits(page: Page):
    user = data_loader.get_user("performance_glitch_user")
    login_page = LoginPage(page)
    login_page.login(user["username"], user["password"])
    expect_on(page, "inventory", timeout=20000)


def test_error_user_sort_za_shows_alert(page: Page):
    _assert_error_user_sort_shows_alert(page, "za")


def test_error_user_sort_lohi_shows_alert(page: Page):
    _assert_error_user_sort_shows_alert(page, "lohi")


def test_error_user_sort_hilo_shows_alert(page: Page):
    _assert_error_user_sort_shows_alert(page, "hilo")


def test_error_user_first_two_products_remove_does_not_work(page: Page):
    inventory = _login_as_error_user(page)
    assert inventory.get_product_count() >= 4

    first_product_button = page.locator(INVENTORY_ITEM).nth(0).locator("button")
    second_product_button = page.locator(INVENTORY_ITEM).nth(1).locator("button")

    first_product_button.click()
    second_product_button.click()
    assert inventory.get_cart_badge_count() == 2

    first_product_button.click()
    second_product_button.click()
    assert inventory.get_cart_badge_count() == 2


def test_error_user_third_and_fourth_products_add_to_cart_does_not_work(page: Page):
    inventory = _login_as_error_user(page)
    assert inventory.get_product_count() >= 4
    assert inventory.get_cart_badge_count() == 0

    third_product_button = page.locator(INVENTORY_ITEM).nth(2).locator("button")
    fourth_product_button = page.locator(INVENTORY_ITEM).nth(3).locator("button")

    third_product_button.click()
    fourth_product_button.click()

    assert inventory.get_cart_badge_count() == 0

def test_intentional_fail_case_2(page: Page):
    inventory = _login_as_error_user(page)
    assert inventory.get_product_count() >= 4
    assert inventory.get_cart_badge_count() == 0

    third_product_button = page.locator(INVENTORY_ITEM).nth(2).locator("button")
    fourth_product_button = page.locator(INVENTORY_ITEM).nth(3).locator("button")

    third_product_button.click()
    fourth_product_button.click()

    assert inventory.get_cart_badge_count() == 1

def test_duplicate_check_for_pr_merge_error_user(page: Page):
    inventory = _login_as_error_user(page)
    assert inventory.get_product_count() >= 4
    assert inventory.get_cart_badge_count() == 0

    first_product_button = page.locator(INVENTORY_ITEM).nth(0).locator("button")
    second_product_button = page.locator(INVENTORY_ITEM).nth(1).locator("button")

    first_product_button.click()
    second_product_button.click()
    
    assert inventory.get_cart_badge_count() == 2

def test_intentional_fail_case_3(page: Page):
    inventory = _login_as_error_user(page)
    assert inventory.get_product_count() >= 4
    assert inventory.get_cart_badge_count() == 0

    first_product_button = page.locator(INVENTORY_ITEM).nth(0).locator("button")
    second_product_button = page.locator(INVENTORY_ITEM).nth(1).locator("button")

    first_product_button.click()
    second_product_button.click()
    
    assert inventory.get_cart_badge_count() == 3

