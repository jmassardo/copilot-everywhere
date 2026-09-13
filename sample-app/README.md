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
| 1 | Two incompatible error-handling conventions | `routers/orders.py` vs `routers/customers.py` | Ex 2, 4 |
| 2 | Discount tier boundary is exclusive (`>` not `>=`) | `pricing.discount_rate_for` | Ex 3, 4 |
| 3 | Money truncated via `int()` on floats | `pricing.calculate_totals` | Ex 3 |
| 4 | Zero test coverage for pricing | no `tests/test_pricing.py` | Ex 3 |
| 5 | Deprecated `datetime.utcnow()` in 3 files | `store.py`, both routers | Ex 1 stretch |
| 6 | `UP` lint rule disabled, 6 violations waiting | `pyproject.toml` | Ex 1 |
| 7 | No Copilot configuration at all | repo root | Ex 2 |

### Seam 2, demonstrated

```python
>>> from app.pricing import discount_rate_for
>>> discount_rate_for(10_000)   # exactly $100.00
0.0                             # should be 0.05
>>> discount_rate_for(50_000)   # exactly $500.00
0.1                             # should be 0.15
```

An order for exactly $100.00 gets no discount. One cent more gets 5%. This is the bug behind the stakeholder complaint in exercise 3.

### Seam 1, why it matters

Both error conventions are present in the codebase, which means an agent pattern-matching this repo **cannot infer which one you want.** It will guess, and it will be right about half the time.

That's not a model limitation. It's unwritten knowledge — which is what exercise 2 fixes.

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

If you fork this for your own org, the seams worth preserving are **1** (ambiguous convention) and **4** (untested module with a real bug) — those two carry most of the lab's weight.
