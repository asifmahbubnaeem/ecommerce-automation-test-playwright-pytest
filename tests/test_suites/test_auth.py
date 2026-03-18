import pytest
from playwright.sync_api import Page

from tests.fixtures import data_loader
from tests.config import site
from tests.pages.login_page import LoginPage
from tests.utils.url_assertions import expect_on


def test_login_success_standard_user(page: Page):
    user = data_loader.get_user("standard_user")
    login_page = LoginPage(page)
    login_page.login(user["username"], user["password"])
    expect_on(page, "inventory")


@pytest.mark.parametrize("scenario", data_loader.get_invalid_login_scenarios())
def test_login_failure_invalid_credentials(page: Page, scenario):
    login_page = LoginPage(page)
    login_page.login(scenario["username"], scenario["password"])
    assert "Epic sadface" in login_page.get_error_message()


def test_locked_out_user_behavior(page: Page):
    locked_user = data_loader.get_user("locked_out_user")
    login_page = LoginPage(page)
    login_page.login(locked_user["username"], locked_user["password"])
    msg = login_page.get_error_message()
    assert "locked out" in msg.lower()


def test_logout_and_session_persistence(page: Page):
    user = data_loader.get_user("standard_user")
    login_page = LoginPage(page)
    login_page.login(user["username"], user["password"])
    page.click("#react-burger-menu-btn")
    with page.expect_navigation():
        page.click("#logout_sidebar_link")
    expect_on(page, "logged_out")
    page.goto(site.route("inventory"))
    expect_on(page, "logged_out")

