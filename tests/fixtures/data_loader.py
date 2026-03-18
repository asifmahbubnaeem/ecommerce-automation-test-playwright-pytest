import json
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_user(user_type: str) -> Dict[str, Any]:
    data = _load_json(FIXTURES_DIR / "users.json")
    if user_type not in data:
        raise KeyError(f"Unknown user type: {user_type}")
    return data[user_type]


def get_invalid_login_scenarios() -> List[Dict[str, Any]]:
    return _load_json(FIXTURES_DIR / "invalid_logins.json")

