import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

from .models import AppConfig


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_app_config() -> AppConfig:
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env", override=False)

    env_name = os.getenv("ENV", "dev")
    site_name = os.getenv("E2E_SITE") or os.getenv("SITE") or "saucedemo"

    base_cfg = _load_yaml(project_root / "tests" / "config" / "base.yml")
    env_cfg = _load_yaml(project_root / "tests" / "config" / f"{env_name}.yml")
    sites_cfg = _load_yaml(project_root / "tests" / "config" / "sites.yml")
    site_cfg = (sites_cfg.get(site_name) or {}) if isinstance(sites_cfg, dict) else {}

    merged: Dict[str, Any] = {**base_cfg, **env_cfg, **site_cfg}

    # Allow env vars to override specific keys
    base_url = os.getenv("BASE_URL")
    if base_url:
        merged["base_url"] = base_url

    headless = os.getenv("HEADLESS")
    if headless is not None:
        merged["headless"] = headless.lower() == "true"

    merged["env_name"] = env_name
    merged["site_name"] = site_name

    return AppConfig(**merged)

