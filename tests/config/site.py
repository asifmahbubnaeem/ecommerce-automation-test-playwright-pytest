import re
from functools import lru_cache
from urllib.parse import urljoin

from tests.config.loader import load_app_config


@lru_cache(maxsize=1)
def config():
    return load_app_config()


def base_url() -> str:
    return str(config().base_url).rstrip("/")


def route(name: str) -> str:
    routes = config().routes or {}
    path = routes.get(name)
    if not path:
        raise KeyError(f"Unknown route '{name}'. Known routes: {sorted(routes.keys())}")
    return urljoin(base_url() + "/", path.lstrip("/"))


def pattern(name: str) -> re.Pattern[str]:
    patterns = config().url_patterns or {}
    raw = patterns.get(name)
    if raw:
        # `{base_url}` is replaced with an escaped base url, so patterns remain portable.
        escaped_base = re.escape(base_url())
        resolved = raw.replace("{base_url}", escaped_base)
        return re.compile(resolved)

    # Fallback: if a route exists, match the full resolved route exactly.
    try:
        url = route(name)
    except KeyError as e:
        raise KeyError(
            f"Unknown url pattern '{name}'. Known patterns: {sorted(patterns.keys())}"
        ) from e

    return re.compile(rf"^{re.escape(url)}$")

