#!/usr/bin/env python3
"""Build the analytics replica used by the Data lab track.

Deterministic: same seed, same database, every time. Students comparing
results with each other will see identical numbers.

    python data/build_db.py

Every data-quality problem below is intentional and documented in
data/README.md. Don't "fix" them here — they're the exercise.
"""

from __future__ import annotations

import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent
DB_PATH = HERE / "orders.db"
SCHEMA = HERE / "schema.sql"

SEED = 42
N_CUSTOMERS = 2_000
N_ORDERS = 50_000
MAX_ITEMS_PER_ORDER = 4

TIERS = ["standard", "premium", "enterprise"]
SKUS = [
    ("WIDGET-1", "Standard widget", 15.00),
    ("WIDGET-2", "Reinforced widget", 29.50),
    ("GIZMO-9", "Gizmo, large", 40.00),
    ("GIZMO-3", "Gizmo, compact", 22.25),
    ("SPROCKET", "Sprocket assembly", 8.75),
    ("FLANGE-X", "Flange, industrial", 120.00),
]

# Seeded problem: the same logical status written five different ways.
STATUS_VARIANTS = ["paid", "PAID", "Paid", "shipped", "SHIPPED", "pending", "cancelled"]

FIRST = ["Mona", "Hubot", "Dana", "Raj", "Priya", "Sam", "Alex", "Jordan", "Kai", "Riley"]
LAST = ["Lisa", "Chen", "Okafor", "Patel", "Nguyen", "Garcia", "Smith", "Kowalski", "Haddad"]


def iso_with_tz(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def iso_without_tz(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def us_format(dt: datetime) -> str:
    return dt.strftime("%m/%d/%Y %H:%M")


def build() -> None:
    rng = random.Random(SEED)

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA.read_text())

    base = datetime(2024, 1, 1)

    customers = []
    for i in range(N_CUSTOMERS):
        first = rng.choice(FIRST)
        last = rng.choice(LAST)
        cid = f"cust-{i:05d}"
        email = f"{first.lower()}.{last.lower()}{i}@example.com"
        created = base + timedelta(days=rng.randint(0, 500))
        customers.append(
            (cid, email, f"{first} {last}", rng.choice(TIERS), iso_with_tz(created))
        )

    # Seeded problem: ~60 customers duplicated under a case-variant email.
    for i in rng.sample(range(N_CUSTOMERS), 60):
        cid, email, name, tier, created = customers[i]
        customers.append(
            (f"{cid}-dup", email.upper(), name, rng.choice(TIERS), created)
        )

    conn.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)

    valid_ids = [c[0] for c in customers]
    orders = []
    items = []
    refunds = []

    for i in range(N_ORDERS):
        oid = f"ord-{i:06d}"

        # Seeded problem: ~400 orders reference a customer that doesn't exist.
        if rng.random() < 0.008:
            customer_id = f"cust-{rng.randint(90_000, 99_999)}"
        else:
            customer_id = rng.choice(valid_ids)

        created = base + timedelta(days=rng.randint(0, 600), minutes=rng.randint(0, 1440))

        # Seeded problem: three different timestamp formats in one column.
        roll = rng.random()
        if roll < 0.70:
            created_str = iso_with_tz(created)
        elif roll < 0.95:
            created_str = iso_without_tz(created)
        else:
            created_str = us_format(created)

        subtotal = 0.0
        for _ in range(rng.randint(1, MAX_ITEMS_PER_ORDER)):
            sku, desc, price = rng.choice(SKUS)
            qty = rng.randint(1, 5)
            subtotal += qty * price
            items.append((oid, sku, desc, qty, price))

        if subtotal > 500:
            rate = 0.15
        elif subtotal > 200:
            rate = 0.10
        elif subtotal > 100:
            rate = 0.05
        else:
            rate = 0.0

        # Seeded problem: NULL discount_rate means "none applied" on some rows
        # and "we didn't record it" on others. Indistinguishable.
        if rate == 0.0 and rng.random() < 0.5:
            stored_rate = None
        elif rng.random() < 0.03:
            stored_rate = None
        else:
            stored_rate = rate

        total = round(subtotal * (1 - rate) * 1.0875, 2)
        status = rng.choice(STATUS_VARIANTS)
        orders.append((oid, customer_id, status, total, stored_rate, created_str))

        if status.lower() == "cancelled" and rng.random() < 0.4:
            refunds.append(
                (oid, round(total * rng.choice([0.5, 1.0]), 2), "customer request",
                 iso_with_tz(created + timedelta(days=rng.randint(1, 30))))
            )

    conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", orders)
    conn.executemany(
        "INSERT INTO line_items (order_id, sku, description, quantity, unit_price) "
        "VALUES (?,?,?,?,?)",
        items,
    )
    conn.executemany(
        "INSERT INTO refunds (order_id, amount, reason, created_at) VALUES (?,?,?,?)",
        refunds,
    )

    conn.commit()

    counts = {
        t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in ("customers", "orders", "line_items", "refunds")
    }
    conn.close()

    print(f"Built {DB_PATH}")
    for table, n in counts.items():
        print(f"  {table:<12} {n:>7,}")
    print("\nNo indexes were created. That is deliberate.")


if __name__ == "__main__":
    build()
