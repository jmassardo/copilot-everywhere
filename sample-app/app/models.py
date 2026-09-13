from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

Tier = Literal["standard", "premium", "enterprise"]
OrderStatus = Literal["pending", "paid", "shipped", "cancelled"]


class LineItem(BaseModel):
    sku: str
    description: str
    quantity: int = Field(gt=0)
    unit_price_cents: int = Field(ge=0)


class Customer(BaseModel):
    id: str
    email: str
    name: str
    tier: Tier = "standard"
    created_at: datetime


class CustomerCreate(BaseModel):
    email: str
    name: str
    tier: Tier = "standard"


class Order(BaseModel):
    id: str
    customer_id: str
    items: list[LineItem]
    status: OrderStatus = "pending"
    created_at: datetime
    notes: Optional[str] = None


class OrderCreate(BaseModel):
    customer_id: str
    items: list[LineItem]
    notes: Optional[str] = None


class OrderTotals(BaseModel):
    subtotal_cents: int
    discount_rate: float
    discount_cents: int
    tax_cents: int
    total_cents: int
