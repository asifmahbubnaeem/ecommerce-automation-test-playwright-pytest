import re
from pathlib import Path
from typing import Optional

from playwright.sync_api import Page, expect

from tests.config.loader import load_app_config


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.config = load_app_config()

    @property
    def base_url(self) -> str:
        return str(self.config.base_url)

    def goto(self, path: str = "") -> None:
        url = f"{self.base_url}{path}"
        self.page.goto(url)

    def expect_url_contains(self, fragment: str) -> None:
        # Playwright expects a string or regex, not a predicate function.
        expect(self.page).to_have_url(re.compile(rf".*{re.escape(fragment)}.*"))

    def screenshot(self, name: str, subdir: str = "screenshots") -> Path:
        reports_dir = Path("reports") / subdir
        reports_dir.mkdir(parents=True, exist_ok=True)
        file_path = reports_dir / f"{name}.png"
        self.page.screenshot(path=str(file_path), full_page=True)
        return file_path

    def wait_for_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        self.page.wait_for_selector(selector, state="visible", timeout=timeout or self.config.timeout)

