# Copilot CLI Session

> [!NOTE]
> - **Session ID:** `61cf2da5-da48-4734-b907-afc0977938c8`  
> - **Started:** 9/27/2026, 10:18:43 AM  
> - **Duration:** 34s  
> - **Exported:** 9/27/2026, 10:19:18 AM  

---

<sub>3s</sub>

### User

Read-only investigation of INCIDENT-4552. Do not invoke subagents and do not edit files. Run the existing focused test and a minimal TestClient reproduction of GET /orders?customer_id=cust-001 after creating one order for cust-001 and one for cust-002. Trace only the GET /orders route into storage. Identify the faulty predicate and explain exactly why tests/test_orders.py::test_list_orders_filters_by_customer remains green. Return a concise report under 500 words with file and line citations, then stop.

---

<sub>7s</sub>

### Copilot

I’ll inspect the focused route, storage implementation, and test, then run only the requested test and reproduction.

---

<sub>7s</sub>

### `glob`

****/*orders*.py**

"**/*orders*.py"

```
./tests/test_orders.py
./app/routers/orders.py
```


---

<sub>7s</sub>

### `rg`

**test_list_orders_filters_by_customer|customer_id|GET /orders**

"test_list_orders_filters_by_customer|customer_id|GET /orders" in **/*.py

<details>
<summary>6 matches</summary>

```
./app/store.py
./tests/test_orders.py
./app/routers/customers.py
./app/routers/orders.py
./data/build_db.py
./app/models.py
```

</details>


---

<sub>7s</sub>

### `glob`

**{pyproject.toml,requirements*.txt,README*,Makefile}**

"{pyproject.toml,requirements*.txt,README*,Makefile}"

```
./data/README.md
./README.md
./pyproject.toml
./requirements.txt
```


---

<sub>10s</sub>

### `view`

**view the file at /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/app/routers/orders.py.**

/Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/app/routers/orders.py

<details>
<summary>64 lines</summary>

```
"""Order endpoints.

Error handling style: raise HTTPException with a structured detail body.
See app/routers/customers.py for a second, incompatible style.
"""

import uuid
from datetime import datetime

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
        created_at=datetime.utcnow(),
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
```

</details>


---

<sub>10s</sub>

### `view`

**view the file at /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/app/store.py.**

/Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/app/store.py

<details>
<summary>59 lines</summary>

```
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
        orders = [o for o in orders if o.customer_id != customer_id]
    return orders


def save_order(order: Order) -> Order:
    _orders[order.id] = order
    return order


def delete_order(order_id: str) -> bool:
    return _orders.pop(order_id, None) is not None


seed()
```

</details>


---

<sub>10s</sub>

### `view`

**view the file at /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/tests/test_orders.py.**

/Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/tests/test_orders.py

<details>
<summary>50 lines</summary>

```
import pytest
from fastapi.testclient import TestClient

from app import store
from app.main import app


@pytest.fixture(autouse=True)
def reset_store():
    store.reset()
    yield
    store.reset()


@pytest.fixture
def client():
    return TestClient(app)


def _items():
    return [
        {"sku": "WIDGET-1", "description": "Widget", "quantity": 2, "unit_price_cents": 1500},
        {"sku": "GIZMO-9", "description": "Gizmo", "quantity": 1, "unit_price_cents": 4000},
    ]


def test_create_order_returns_201(client):
    response = client.post("/orders", json={"customer_id": "cust-001", "items": _items()})
    assert response.status_code == 201
    body = response.json()
    assert body["customer_id"] == "cust-001"
    assert body["status"] == "pending"
    assert len(body["items"]) == 2


def test_create_order_unknown_customer_returns_400(client):
    response = client.post("/orders", json={"customer_id": "nope", "items": _items()})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "customer_not_found"


def test_create_order_empty_items_returns_400(client):
    response = client.post("/orders", json={"customer_id": "cust-001", "items": []})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "empty_order"


def test_get_order_returns_the_order(client):
    created = client.post("/orders", json={"customer_id": "cust-001", "items": _items()}).json()
    response = client.get(f"/orders/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_order_returns_404(client):
    response = client.get("/orders/ord-missing")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "order_not_found"


def test_list_orders_filters_by_customer(client):
    client.post("/orders", json={"customer_id": "cust-001", "items": _items()})
    client.post("/orders", json={"customer_id": "cust-002", "items": _items()})

    assert len(client.get("/orders").json()) == 2
    assert len(client.get("/orders", params={"customer_id": "cust-002"}).json()) == 1


def test_delete_order_returns_204(client):
    created = client.post("/orders", json={"customer_id": "cust-001", "items": _items()}).json()
    assert client.delete(f"/orders/{created['id']}").status_code == 204
    assert client.get(f"/orders/{created['id']}").status_code == 404
```

</details>


---

<sub>10s</sub>

### `view`

**view the file at /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/pyproject.toml.**

/Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/pyproject.toml

<details>
<summary>9 lines</summary>

```
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py311"

# Exercise 1 has students add "UP" here and fix the resulting fallout.
[tool.ruff.lint]
select = ["E", "F", "I", "B"]
```

</details>


---

<sub>10s</sub>

### `glob`

**app/{main,app}.py**

"app/{main,app}.py"

```
./app/main.py
```


---

<sub>10s</sub>

### `glob`

**tests/{conftest.py,test_*.py}**

"tests/{conftest.py,test_*.py}"

```
./tests/test_orders.py
./tests/test_customers.py
```


---

<sub>16s</sub>

### Copilot

The route passes the query parameter unchanged to storage; I’m now verifying the focused assertion and capturing the filtered response for `cust-001`.

---

<sub>16s</sub>

### `bash`

**Run focused order filter test**

$ python -m pytest -q tests/test_orders.py::test_list_orders_filters_by_customer

```
/bin/bash: python: command not found
<shellId: 0 completed with exit code 127>
```


---

<sub>16s</sub>

### `bash`

**Reproduce customer order filtering**

$ python - <<'PY'
from fastapi.testclient import TestClient
from app import store
from app.main import app

items = [{"sku": "WIDGET-1", "description": "Widget", "quantity": 1, "unit_price_cents": 100}]
store.reset()
with TestClient(app) as client:
    first = client.post("/orders", json={"customer_id": "cust-001", "items": items})
    second = client.post("/orders", json={"customer_id": "cust-002", "items": items})
    response = client.get("/orders", params={"customer_id": "cust-001"})
    print("POST cust-001:", first.status_code, first.json()["id"])
    print("POST cust-002:", second.status_code, second.json()["id"])
    print("GET /orders?customer_id=cust-001:", response.status_code)
    print("returned:", [(order["id"], order["customer_id"]) for order in response.json()])
PY

```
/bin/bash: python: command not found
<shellId: 1 completed with exit code 127>
```


---

<sub>20s</sub>

### Copilot

`python` is unavailable in this environment; I’m rerunning the same two checks with the installed `python3` interpreter.

---

<sub>21s</sub>

### `bash`

**Run focused order filter test**

$ python3 -m pytest -q tests/test_orders.py::test_list_orders_filters_by_customer

<details>
<summary>16 lines</summary>

```
ERROR: found no collectors for /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/tests/test_orders.py::test_list_orders_filters_by_customer


==================================== ERRORS ====================================
____________________ ERROR collecting tests/test_orders.py _____________________
ImportError while importing test module '/Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/tests/test_orders.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_orders.py:2: in <module>
    from fastapi.testclient import TestClient
E   ModuleNotFoundError: No module named 'fastapi'
=========================== short test summary info ============================
ERROR tests/test_orders.py
1 error in 0.02s
<shellId: 2 completed with exit code 4>
```

</details>


---

<sub>21s</sub>

### `bash`

**Reproduce customer order filtering**

$ python3 - <<'PY'
from fastapi.testclient import TestClient
from app import store
from app.main import app

items = [{"sku": "WIDGET-1", "description": "Widget", "quantity": 1, "unit_price_cents": 100}]
store.reset()
with TestClient(app) as client:
    first = client.post("/orders", json={"customer_id": "cust-001", "items": items})
    second = client.post("/orders", json={"customer_id": "cust-002", "items": items})
    response = client.get("/orders", params={"customer_id": "cust-001"})
    print("POST cust-001:", first.status_code, first.json()["id"])
    print("POST cust-002:", second.status_code, second.json()["id"])
    print("GET /orders?customer_id=cust-001:", response.status_code)
    print("returned:", [(order["id"], order["customer_id"]) for order in response.json()])
PY

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'fastapi'
<shellId: 3 completed with exit code 1>
```


---

<sub>25s</sub>

### Copilot

The system interpreter lacks project dependencies, so I’m locating the repository’s existing virtual environment or configured test runner before restoring anything.

---

<sub>25s</sub>

### `bash`

**Locate project Python environment**

$ ls -la && find .. -maxdepth 3 -type f \( -path '*/bin/python' -o -path '*/bin/pytest' \) -print

<details>
<summary>14 lines</summary>

```
total 32
drwxr-xr-x@ 12 jenna  staff   384 Sep 27 10:15 .
drwxr-xr-x@  9 jenna  staff   288 Sep 27 10:15 ..
drwxr-xr-x@  6 jenna  staff   192 Sep 27 10:15 .pytest_cache
drwxr-xr-x@  5 jenna  staff   160 Sep 27 10:15 .ruff_cache
drwxr-xr-x@  7 jenna  staff   224 Sep 27 10:15 .venv
drwxr-xr-x@  9 jenna  staff   288 Sep 27 10:15 app
drwxr-xr-x@  5 jenna  staff   160 Sep 27 10:15 data
-rw-r--r--@  1 jenna  staff  2999 Sep 27 10:15 FEEDBACK.md
-rw-r--r--@  1 jenna  staff   242 Sep 27 10:15 pyproject.toml
-rw-r--r--@  1 jenna  staff  3969 Sep 27 10:15 README.md
-rw-r--r--@  1 jenna  staff   312 Sep 27 10:15 requirements.txt
drwxr-xr-x@  5 jenna  staff   160 Sep 27 10:15 tests
<shellId: 4 completed with exit code 0>
```

</details>


---

<sub>25s</sub>

### `view`

**view the file at /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/README.md.**

/Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/README.md

<details>
<summary>77 lines</summary>

````
# Sample App — Orders Service

A small FastAPI service used as the workbench for the [Copilot Everywhere lab](../lab/README.md).

It is deliberately imperfect. Every flaw below is load-bearing for an exercise.

---

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest -q          # 13 passed
ruff check .       # All checks passed!

uvicorn app.main:app --reload    # http://127.0.0.1:8000/docs
```

> Dependencies are floor-pinned (`>=`) rather than exact-pinned. Exact pins force source builds when no wheel matches the student's interpreter — `pydantic-core` on Python 3.14 is the usual casualty, and it fails with a Rust compile error that derails a lab.

---

## Layout

```
app/
  main.py              FastAPI wiring
  models.py            Pydantic models
  store.py             In-memory persistence, seeded with 2 customers
  pricing.py           Subtotal, volume discount, tax
  routers/
    orders.py          Error style A: raises HTTPException
    customers.py       Error style B: returns {"error": ...} with 200
tests/
  test_orders.py       7 tests
  test_customers.py    6 tests
```

---

## The seeded seams

| # | Seam | Where | Used by |
|---|---|---|---|
| 1 | Two incompatible error-handling conventions | `routers/orders.py` vs `routers/customers.py` | Platform, Product |
| 2 | Discount tier boundary is exclusive (`>` not `>=`) | `pricing.discount_rate_for` | Product |
| 3 | Money truncated via `int()` on floats | `pricing.calculate_totals` | Product, Data |
| 4 | Zero test coverage for pricing | no `tests/test_pricing.py` | Product |
| 5 | Deprecated `datetime.utcnow()` in 3 files | `store.py`, both routers | Engineer, Platform |
| 6 | `UP` lint rule disabled, 6 violations waiting | `pyproject.toml` | Optional extension |
| 7 | No Copilot configuration at all | repo root | Platform track |
| 8 | Customer filter returns another customer's orders while the weak test stays green | `store.list_orders`, `test_list_orders_filters_by_customer` | Engineer track |

### Seam 2, demonstrated

```python
>>> from app.pricing import discount_rate_for
>>> discount_rate_for(10_000)   # exactly $100.00
0.0                             # should be 0.05
>>> discount_rate_for(50_000)   # exactly $500.00
0.1                             # should be 0.15
```

An order for exactly $100.00 gets no discount. One cent more gets 5%. This is
the objective bug the Product track turns into agent-ready work.

### Seam 1, why it matters

Both error conventions are present in the codebase, which means an agent pattern-matching this repo **cannot infer which one you want.** It will guess, and it will be right about half the time.

That's not a model limitation. It's unwritten knowledge — which the Platform
track turns into durable instructions and agent boundaries.

### Seam 8, why it matters

The customer filter uses `!=` instead of `==`, but the existing test only checks
that one result is returned. With one order per customer, both the correct and
incorrect implementations return a list of length one. CI stays green while the
service returns another customer's data.

This is the incident behind the Engineer track. Students start from a credible
support escalation, reproduce the behavior, strengthen the test, and only then
fix the implementation.

---

## Baseline contract

The suite is green and lint is clean **on purpose.** Every exercise uses them as its verification signal, so a red baseline makes every result meaningless.

If you've broken it and want to get back:

```bash
git checkout -- .
pytest -q && ruff check .
```

---

## Facilitators

Don't fix these seams in `main`. The whole app is a fixture.

If you fork this for your own org, the seams worth preserving are **1**
(ambiguous convention), **4** (untested money code), and **8** (green tests
masking a customer-isolation defect). Those carry most of the lab's weight.
````

</details>


---

<sub>25s</sub>

### `view`

**view the file at /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/requirements.txt.**

/Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/requirements.txt

<details>
<summary>9 lines</summary>

```
# Floor-pinned rather than exact-pinned on purpose: students show up with
# whatever Python they have, and exact pins force source builds when no
# matching wheel exists (pydantic-core on Python 3.14 is the usual casualty).
fastapi>=0.115
uvicorn[standard]>=0.34
pydantic>=2.10
pytest>=8.3
httpx>=0.28
ruff>=0.8
```

</details>


---

<sub>29s</sub>

### `bash`

**Run focused order filter test**

$ .venv/bin/python -m pytest -q tests/test_orders.py::test_list_orders_filters_by_customer

<details>
<summary>22 lines</summary>

```
.                                                                        [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

app/store.py:29
tests/test_orders.py::test_list_orders_filters_by_customer
tests/test_orders.py::test_list_orders_filters_by_customer
  /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/app/store.py:29: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    created_at=datetime.utcnow(),

app/store.py:38
tests/test_orders.py::test_list_orders_filters_by_customer
tests/test_orders.py::test_list_orders_filters_by_customer
  /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/app/store.py:38: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    created_at=datetime.utcnow(),

tests/test_orders.py::test_list_orders_filters_by_customer
tests/test_orders.py::test_list_orders_filters_by_customer
  /Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/app/routers/orders.py:56: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    created_at=datetime.utcnow(),

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
1 passed, 9 warnings in 0.13s
<shellId: 5 completed with exit code 0>
```

</details>


---

<sub>29s</sub>

### `bash`

**Reproduce customer order filtering**

$ .venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import store
from app.main import app

items = [{"sku": "WIDGET-1", "description": "Widget", "quantity": 1, "unit_price_cents": 100}]
store.reset()
with TestClient(app) as client:
    first = client.post("/orders", json={"customer_id": "cust-001", "items": items})
    second = client.post("/orders", json={"customer_id": "cust-002", "items": items})
    response = client.get("/orders", params={"customer_id": "cust-001"})
    print("POST cust-001:", first.status_code, first.json()["id"])
    print("POST cust-002:", second.status_code, second.json()["id"])
    print("GET /orders?customer_id=cust-001:", response.status_code)
    print("returned:", [(order["id"], order["customer_id"]) for order in response.json()])
PY

<details>
<summary>7 lines</summary>

```
/Users/jenna/code/copilot-worktrees/copilot-everywhere/engineer-recording/sample-app/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
  from starlette.testclient import TestClient as TestClient  # noqa
POST cust-001: 201 ord-ff2ec4a6
POST cust-002: 201 ord-aad2f27c
GET /orders?customer_id=cust-001: 200
returned: [('ord-aad2f27c', 'cust-002')]
<shellId: 6 completed with exit code 0>
```

</details>


---

<sub>34s</sub>

### Copilot

**INCIDENT-4552 confirmed:** `GET /orders?customer_id=cust-001` incorrectly returned the order belonging to `cust-002`.

- **Trace:** The FastAPI route accepts `customer_id` and passes it unchanged to `store.list_orders(customer_id)` ([app/routers/orders.py:16-18](app/routers/orders.py#L16-L18)).
- **Faulty predicate:** Storage filters with `o.customer_id != customer_id` ([app/store.py:60-64](app/store.py#L60-L64)). This explicitly excludes the requested customer and returns every other customer’s orders. The predicate must use equality to implement customer filtering.
- **Reproduction:** After creating one order for each customer, `GET /orders?customer_id=cust-001` returned HTTP 200 with only the `cust-002` order.
- **Why the focused test stays green:** The test creates exactly one order per customer, requests `cust-002`, and asserts only `len(response) == 1` ([tests/test_orders.py:57-62](tests/test_orders.py#L57-L62)). Both correct and inverted predicates produce one result: correct filtering returns the single `cust-002` order; the faulty predicate returns the single `cust-001` order. The test never asserts the returned order’s `customer_id`.

The requested focused test passed: **1 passed**. No files were changed.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
