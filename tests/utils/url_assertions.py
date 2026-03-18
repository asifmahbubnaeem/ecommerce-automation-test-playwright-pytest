from __future__ import annotations

from typing import Optional

from playwright.sync_api import Page, expect

from tests.config import site


def expect_on(page: Page, name: str, timeout: Optional[int] = None) -> None:
    expect(page).to_have_url(site.pattern(name), timeout=timeout)


def expect_logged_out(page: Page, timeout: Optional[int] = None) -> None:
    expect_on(page, "logged_out", timeout=timeout)

