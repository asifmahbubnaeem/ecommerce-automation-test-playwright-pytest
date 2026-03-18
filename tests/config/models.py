from pydantic import BaseModel, HttpUrl


class AppConfig(BaseModel):
    env_name: str = "dev"
    base_url: HttpUrl = "https://www.saucedemo.com"  # type: ignore[assignment]
    timeout: int = 10000
    headless: bool = True
    trace: str = "retain-on-failure"
    video: str = "retain-on-failure"

