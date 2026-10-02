"""Order endpoints.

Error handling style: raise HTTPException with a structured detail body.
See app/routers/customers.py for a second, incompatible style.
"""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status

from app import pricing, store
from app.models import Order, OrderCreate, OrderTotals

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[Order])
def list_orders(customer_id: str | None = None) -> list[Order]:
    return store.list_orders(customer_id)


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str) -> Order:
    order = store.get_order(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "order_not_found", "message": f"No order with id {order_id}"},
        )
    return order


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate) -> Order:
    customer = store.get_customer(payload.customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "customer_not_found",
                "message": f"No customer with id {payload.customer_id}",
            },
        )

    if not payload.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "empty_order", "message": "An order needs at least one line item"},
        )

    order = Order(
        id=f"ord-{uuid.uuid4().hex[:8]}",
        customer_id=payload.customer_id,
        items=payload.items,
        created_at=datetime.now(UTC),
        notes=payload.notes,
    )
    return store.save_order(order)


@router.get("/{order_id}/totals", response_model=OrderTotals)
def get_order_totals(order_id: str) -> OrderTotals:
    order = store.get_order(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "order_not_found", "message": f"No order with id {order_id}"},
        )

    customer = store.get_customer(order.customer_id)
    tier = customer.tier if customer else "standard"
    return pricing.calculate_totals(order.items, tier)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: str) -> None:
    if not store.delete_order(order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "order_not_found", "message": f"No order with id {order_id}"},
        )
