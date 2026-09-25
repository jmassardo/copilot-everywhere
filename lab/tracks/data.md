# Track: DBA / Analytics Engineer / Data Scientist

**Duration:** 75–80 minutes
**Surfaces:** VS Code sessions, read-only data agent, SQLite
**Outcome:** Investigate reconciliation and performance symptoms independently,
make one bounded change, and document what the data cannot answer.

---

## Setup

```bash
cd sample-app
.venv/bin/python data/build_db.py
```

Work only against `data/orders.db`, which is generated and disposable.

## Exercise 1 — Establish a read-only investigation mode

**15 minutes**

Create or select a data-investigator agent that may:

- Read application and analytics files.
- Run `SELECT`, `PRAGMA`, and `EXPLAIN QUERY PLAN`.
- Report hypotheses and findings separately.

It may not:

- Modify data or schema.
- Access production.
- Treat missing semantics as zero.

Ask it to compare `data/schema.sql`, `app/models.py`, and `app/pricing.py`.
Require a validation query for every claimed risk.

**Deliverable:** a list of testable hypotheses and a demonstrated read-only
boundary.

## Exercise 2 — Run parallel investigations

**20 minutes**

Create two sessions.

### Data quality

> Investigate why analytics lifetime value might not reconcile with application
> invoices. Use read-only queries. Check money representation, orphaned rows,
> duplicate customers, status values, timestamp formats, NULL semantics, and
> join fan-out.

### Query performance

> Investigate the enterprise lifetime-value dashboard query. Capture the query
> plan and timing. Recommend only changes supported by measured evidence.

Compare results without allowing one symptom to become the explanation for the
other.

**Deliverable:** separate quality and performance findings with evidence.

## Exercise 3 — Build reconciliation before repair

**15 minutes**

Write a repeatable reconciliation query or script that records:

- Customer, order, line-item, and refund counts.
- Orphan order count.
- Distinct status count.
- NULL discount-rate count.
- A monetary control total with its unit.

Run it twice and confirm deterministic output.

Document the expected seeded findings, including `7113` NULL discount rates and
`394` orphaned orders.

**Deliverable:** a baseline that can detect accidental data changes.

## Exercise 4 — Make one bounded performance change

**15 minutes**

Capture the dashboard plan showing:

```text
SEARCH o USING AUTOMATIC COVERING INDEX (customer_id=?)
```

Hand the evidence and reconciliation baseline to a write-capable migration
session:

> Add only the index supported by this query plan. Run reconciliation before
> and after. Re-run the identical plan. Stop if any count or control total
> changes.

Expected index:

```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

Expected plan names the index. Reject unrelated index suggestions.

**Deliverable:** before/after plan evidence and unchanged reconciliation.

## Exercise 5 — Write the decision memo the data requires

**10–15 minutes**

Investigate `discount_rate IS NULL`. Try to distinguish:

- No discount applied.
- Discount not recorded.

When the data cannot resolve the meaning, stop querying.

Write a short decision memo:

- What is known.
- What cannot be inferred.
- Who owns the missing semantics.
- What pipeline/schema change would prevent future ambiguity.
- Which analyses are unsafe until resolved.

Rebuild the database afterward:

```bash
.venv/bin/python data/build_db.py
```

**Deliverable:** an explicit human handoff rather than a fabricated answer.

## Done

You are done when every conclusion has one of:

- A query result.
- A query plan.
- A reconciliation invariant.
- An explicit “cannot be determined” with a named owner.

## Own-repository variant

Use a replica or local synthetic extract. Never allow the lab agent to mutate
production, access unauthorized data, or expose customer information.
