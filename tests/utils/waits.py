from playwright.sync_api import Page


def wait_for_network_idle(page: Page, timeout: int = 10000) -> None:
    page.wait_for_load_state("networkidle", timeout=timeout)

