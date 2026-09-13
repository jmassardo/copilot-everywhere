"""In-memory persistence for the workshop app.

Deliberately simple: no database, no migrations, no async. The interesting
parts of this codebase are the seams, not the storage.
"""

from datetime import datetime
from typing import Optional

from app.models import Customer, Order

_customers: dict[str, Customer] = {}
_orders: dict[str, Order] = {}


def reset() -> None:
    _customers.clear()
    _orders.clear()
    seed()


def seed() -> None:
    save_customer(
        Customer(
            id="cust-001",
            email="mona@example.com",
            name="Mona Lisa",
            tier="standard",
            created_at=datetime.utcnow(),
        )
    )
    save_customer(
        Customer(
            id="cust-002",
            email="hubot@example.com",
            name="Hubot",
            tier="enterprise",
            created_at=datetime.utcnow(),
        )
    )


def get_customer(customer_id: str) -> Optional[Customer]:
    return _customers.get(customer_id)


def find_customer_by_email(email: str) -> Optional[Customer]:
    for customer in _customers.values():
        if customer.email == email:
            return customer
    return None


def list_customers() -> list[Customer]:
    return list(_customers.values())


def save_customer(customer: Customer) -> Customer:
    _customers[customer.id] = customer
    return customer


def delete_customer(customer_id: str) -> bool:
    return _customers.pop(customer_id, None) is not None


def get_order(order_id: str) -> Optional[Order]:
    return _orders.get(order_id)


def list_orders(customer_id: Optional[str] = None) -> list[Order]:
    orders = list(_orders.values())
    if customer_id:
        orders = [o for o in orders if o.customer_id == customer_id]
    return orders


def save_order(order: Order) -> Order:
    _orders[order.id] = order
    return order


def delete_order(order_id: str) -> bool:
    return _orders.pop(order_id, None) is not None


seed()
