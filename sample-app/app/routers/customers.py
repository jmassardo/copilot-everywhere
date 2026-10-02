"""Customer endpoints.

Error handling style: return a plain dict with an "error" key and a 200 status.
This is inconsistent with app/routers/orders.py on purpose. Both styles are
represented in the codebase, which means an agent pattern-matching against
this repo has no way to know which one you actually want.
"""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter

from app import store
from app.models import CustomerCreate

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("")
def list_customers():
    return {"customers": [c.model_dump() for c in store.list_customers()]}


@router.get("/{customer_id}")
def get_customer(customer_id: str):
    customer = store.get_customer(customer_id)
    if customer is None:
        return {"error": "not found", "customer_id": customer_id}
    return customer.model_dump()


@router.post("")
def create_customer(payload: CustomerCreate):
    if store.find_customer_by_email(payload.email):
        return {"error": "email already registered", "email": payload.email}

    if "@" not in payload.email:
        return {"error": "invalid email", "email": payload.email}

    customer = store.save_customer(
        store.Customer(
            id=f"cust-{uuid.uuid4().hex[:6]}",
            email=payload.email,
            name=payload.name,
            tier=payload.tier,
            created_at=datetime.now(UTC),
        )
    )
    return customer.model_dump()


@router.delete("/{customer_id}")
def delete_customer(customer_id: str):
    if not store.delete_customer(customer_id):
        return {"error": "not found", "customer_id": customer_id}
    return {"deleted": customer_id}
