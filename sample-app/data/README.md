# Analytics Replica

The workbench for the [Data lab track](../../lab/tracks/data.md).

A SQLite database that mirrors the orders service domain — and disagrees with it in several documented ways.

---

## Build it

```bash
cd sample-app
python data/build_db.py
```

Deterministic (`seed = 42`). Everyone in the lab gets identical numbers, which makes comparing results possible.

```
customers      2,060
orders        50,000
line_items   125,362
refunds        2,806
```

The `.db` file is gitignored — generate it locally, don't commit it.

---

## The seeded problems

Every one is intentional. Counts are exact and reproducible.

| # | Problem | Scale | Discoverable by |
|---|---|---|---|
| 1 | **Orphaned orders** — `customer_id` references nothing | 394 | `LEFT JOIN ... WHERE c.id IS NULL` |
| 2 | **Duplicate customers** under case-variant emails | 60 | `GROUP BY LOWER(email) HAVING COUNT(*) > 1` |
| 3 | **Status casing chaos** — 7 variants for 4 states | 50,000 rows | `SELECT DISTINCT status` |
| 4 | **Ambiguous NULLs** in `discount_rate` | 7,113 | Counting finds them; nothing resolves them |
| 5 | **Mixed timestamp formats** — ISO±TZ and US | 2,596 | `created_at LIKE '%/%'` |
| 6 | **Money as `REAL`** — app uses integer cents | all rows | Compare with `app/models.py` |
| 7 | **No indexes on foreign keys** | — | `EXPLAIN QUERY PLAN` |
| 8 | **No constraints** — no FKs, NOT NULLs, or CHECKs | — | Read `schema.sql` |

### Problem 4 is the important one

`discount_rate IS NULL` means "no discount applied" on some rows and "we never recorded it" on others. **The data cannot tell you which.**

No query resolves this. No model resolves this. It needs a human who owns the pipeline. It's in here because every real warehouse has one, and because it's the clearest example of a question that looks like a data problem and is actually a decision.

### Problem 7 is the measurable one

```sql
EXPLAIN QUERY PLAN
SELECT c.id, COUNT(o.id), SUM(o.total_amount)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.tier = 'enterprise' GROUP BY c.id;
```

```
SEARCH o USING AUTOMATIC COVERING INDEX (customer_id=?)
```

SQLite is telling you it built a throwaway index at runtime because the schema didn't provide one. Adding `CREATE INDEX idx_o_cust ON orders(customer_id)`:

| Query shape | Before | After |
|---|---|---|
| Dashboard aggregate | ~0.080s | ~0.019s |
| 300 point lookups (N+1) | ~0.96s | ~0.009s |

---

## Regenerating

```bash
rm data/orders.db && python data/build_db.py
```

Safe at any time. Students will do this after breaking a migration.

---

## Facilitators

**Don't fix these problems in `main`.** The database is a fixture.

If you fork this for your own org, the seams worth keeping are **4** (the unresolvable NULL) and **7** (the measurable missing index). Those two carry most of the track — one teaches that some questions aren't technical, the other gives a verifiable before/after.

Problem 6 exists to connect back to the application code: the warehouse and the app disagree about how money is represented, and neither one knows it.
