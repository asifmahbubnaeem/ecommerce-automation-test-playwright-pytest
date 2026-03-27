from typing import Dict, Literal

from pydantic import BaseModel, HttpUrl


class AppConfig(BaseModel):
    env_name: str = "dev"
    site_name: str = "saucedemo"
    base_url: HttpUrl = "https://example.com"  # type: ignore[assignment]
    timeout: int = 10000
    headless: bool = True
    browser: Literal["chromium", "firefox", "chrome", "msedge"] = "chromium"
    trace: str = "retain-on-failure"
    video: str = "retain-on-failure"
    routes: Dict[str, str] = {}
    url_patterns: Dict[str, str] = {}

