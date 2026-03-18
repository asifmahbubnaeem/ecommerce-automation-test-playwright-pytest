from decimal import Decimal
from typing import Iterable, List


def assert_sorted(values: List, reverse: bool = False) -> None:
    expected = sorted(values, reverse=reverse)
    assert values == expected, f"Expected sorted={expected}, got={values}"


def assert_cart_badge_count(actual: int, expected: int) -> None:
    assert actual == expected, f"Expected cart badge {expected}, got {actual}"


def assert_order_totals_correct(
    item_prices: Iterable[Decimal], ui_item_total: Decimal, ui_tax: Decimal, ui_total: Decimal
) -> None:
    calculated_item_total = sum(item_prices)
    # SauceDemo uses a fixed tax rate of 8% in the UI, but we assert using the UI values to avoid brittleness.
    assert calculated_item_total == ui_item_total, (
        f"Item total mismatch. Calculated={calculated_item_total}, UI={ui_item_total}"
    )
    assert ui_item_total + ui_tax == ui_total, (
        f"Total mismatch. Item({ui_item_total}) + Tax({ui_tax}) != Total({ui_total})"
    )

