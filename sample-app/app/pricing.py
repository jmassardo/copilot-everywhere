"""Order pricing: subtotal, volume discount, tax.

Note: this module has no test coverage. That is not an accident.
"""

from app.models import LineItem, OrderTotals

TAX_RATE = 0.0875

# (subtotal threshold in cents, discount rate)
DISCOUNT_TIERS: list[tuple[int, float]] = [
    (50_000, 0.15),
    (20_000, 0.10),
    (10_000, 0.05),
]

TIER_MULTIPLIERS = {
    "standard": 1.0,
    "premium": 0.95,
    "enterprise": 0.90,
}


def subtotal_cents(items: list[LineItem]) -> int:
    total = 0
    for item in items:
        total += item.quantity * item.unit_price_cents
    return total


def discount_rate_for(subtotal: int) -> float:
    for threshold, rate in DISCOUNT_TIERS:
        if subtotal > threshold:
            return rate
    return 0.0


def calculate_totals(items: list[LineItem], tier: str = "standard") -> OrderTotals:
    subtotal = subtotal_cents(items)
    rate = discount_rate_for(subtotal)

    discount = subtotal * rate
    discounted = subtotal - discount
    discounted = discounted * TIER_MULTIPLIERS.get(tier, 1.0)

    tax = discounted * TAX_RATE
    total = discounted + tax

    return OrderTotals(
        subtotal_cents=subtotal,
        discount_rate=rate,
        discount_cents=int(discount),
        tax_cents=int(tax),
        total_cents=int(total),
    )
