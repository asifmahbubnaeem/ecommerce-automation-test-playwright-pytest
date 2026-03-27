from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import BrowserContext, Page, sync_playwright

from tests.config.loader import load_app_config
from tests.config.models import AppConfig
from tests.fixtures import data_loader
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage




@pytest.fixture(scope="session")
def app_config() -> AppConfig:
    return load_app_config()


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser_context_factory(playwright_instance, app_config: AppConfig):
    def _factory() -> BrowserContext:
        # Support Firefox and Chrome-family browsers through config/env.
        if app_config.browser == "firefox":
            browser = playwright_instance.firefox.launch(headless=app_config.headless)
        elif app_config.browser in {"chrome", "msedge"}:
            browser = playwright_instance.chromium.launch(
                headless=app_config.headless,
                channel=app_config.browser,
            )
        else:
            browser = playwright_instance.chromium.launch(headless=app_config.headless)
        context = browser.new_context(
            base_url=str(app_config.base_url),
        )
        return context

    return _factory


@pytest.fixture
def context(browser_context_factory) -> Generator[BrowserContext, None, None]:
    context = browser_context_factory()
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def standard_user():
    return data_loader.get_user("standard_user")


@pytest.fixture
def login_as_standard_user(page: Page, standard_user):
    login_page = LoginPage(page)
    login_page.login(standard_user["username"], standard_user["password"])
    return InventoryPage(page)


def pytest_configure(config: pytest.Config) -> None:
    reports_dir = Path("reports/html")
    reports_dir.mkdir(parents=True, exist_ok=True)
    config.option.htmlpath = str(reports_dir / "report.html")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield  # type: ignore[misc]
    report = outcome.get_result()
    if report.failed and "page" in item.fixturenames:
        page: Page = item.funcargs["page"]
        screenshots_dir = Path("reports/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        file_path = screenshots_dir / f"{item.name}.png"
        page.screenshot(path=str(file_path), full_page=True)
        print(f"\n[screenshot] Failure screenshot saved: {file_path.resolve()}\n", flush=True)