# Track: DBA / Analytics Engineer / Data Scientist

**Duration:** 75–80 minutes
**Surfaces:** VS Code, GitHub Copilot Chat, terminal, SQLite
**Outcome:** Use separate Copilot sessions to investigate data quality and query
performance, establish a repeatable reconciliation baseline, make one measured
performance change, and document a question that the available data cannot
answer.

---

## Scenario

You support an analytics replica for an Orders Service. Two concerns arrived at
the same time:

1. The enterprise customer lifetime-value dashboard is slow.
2. Analytics totals may not reconcile with application invoices.

These symptoms might have the same cause, but you must not assume that they do.
You will investigate them independently, require evidence for every claim, and
allow a write only after you have a reconciliation baseline.

This lab uses synthetic data. Do not connect Copilot or any command in this lab
to a production database.

## Before you begin

### 1. Open the correct folder

1. Open VS Code.
2. Select **File > Open Folder**.
3. Open the `copilot-everywhere` repository.
4. In the Explorer, confirm that you can see `sample-app`, `lab`, and
   `talk`.

All terminal commands in this lab start from `sample-app/`. In VS Code, select
**Terminal > New Terminal**, then run:

```bash
cd sample-app
```

If your terminal prompt already ends in `sample-app`, do not run `cd
sample-app` again.

### 2. Build the disposable database

macOS or Linux:

```bash
.venv/bin/python data/build_db.py
```

Windows PowerShell:

```powershell
.venv\Scripts\python data/build_db.py
```

The final lines should include:

```text
customers      2,060
orders        50,000
line_items   125,362
refunds        2,806

No indexes were created. That is deliberate.
```

If the virtual environment does not exist, stop and complete
[`lab/setup.md`](../setup.md) before continuing.

### 3. Verify SQLite can read the database

Run:

```bash
sqlite3 data/orders.db "SELECT COUNT(*) FROM orders;"
```

Expected result:

```text
50000
```

If `sqlite3` is not recognized, install the SQLite command-line client or use a
facilitator-provided environment. Do not substitute a production database.

### 4. Know the Copilot controls used in this lab

VS Code labels can vary slightly by version, but the workflow is the same:

1. Select the **Chat** or **Copilot** icon in the Activity Bar.
2. Select **New Chat** (`+`) to create a separate session.
3. Use the mode picker near the chat input to select **Agent** when Copilot
   needs to inspect files or run terminal commands.
4. Review every proposed terminal command before approving it.
5. Use **New Chat** again whenever this lab says to create another session.
   Do not erase and reuse the previous session; the separation is intentional.

You do not need to create a custom agent for this lab. Use the regular local
Copilot agent and give it the explicit read-only instructions below. If your
facilitator has already supplied a data-investigator agent, you may select it
instead.

> **Safety rule:** During Exercises 1–3, approve only commands that read the
> database: `SELECT`, `PRAGMA`, and `EXPLAIN QUERY PLAN`. Reject `INSERT`,
> `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `REPLACE`, and `VACUUM`.

---

## Exercise 1 — Establish a read-only investigation mode

**15 minutes**

The purpose of this exercise is to prove that Copilot can investigate without
changing the database. You will also compare the analytics schema with the
application's data model and pricing logic.

### Step 1: Start a dedicated investigation session

1. Open Copilot Chat.
2. Select **New Chat**.
3. Select **Agent** mode.
4. Name the session `Data contract investigation` if your VS Code version
   supports naming sessions.
5. Paste the following prompt:

```text
You are investigating a local synthetic SQLite analytics replica.

Scope:
- Database: data/orders.db
- Files you may read: data/schema.sql, app/models.py, and app/pricing.py
- Do not use data/README.md as evidence; it contains facilitator answers.

Safety boundary:
- Do not edit any file.
- Do not modify data or schema.
- Run only SELECT, PRAGMA, and EXPLAIN QUERY PLAN statements.
- Do not run CREATE, INSERT, UPDATE, DELETE, DROP, ALTER, REPLACE, or VACUUM.
- Do not access any network service or production system.
- Treat NULL as unknown unless repository evidence defines its meaning.

First set PRAGMA query_only = ON and verify it returns 1. Then compare the
analytics schema with the application model and pricing implementation.
For every risk you report, include:
1. the exact file and symbol or schema column that raised the concern;
2. a hypothesis, clearly labeled as a hypothesis;
3. a read-only validation query;
4. the query result; and
5. what the result does and does not prove.

Do not fix anything. Stop after presenting an evidence table.
```

### Step 2: Review the proposed actions

Copilot may ask permission to read files or run terminal commands.

1. Approve reads of:
   - `data/schema.sql`
   - `app/models.py`
   - `app/pricing.py`
   - `data/orders.db`
2. Approve SQL only if it begins with `SELECT`, `PRAGMA`, or
   `EXPLAIN QUERY PLAN`.
3. Reject any proposed write.
4. If Copilot proposes a write, reply:

```text
That action violates the read-only boundary. Continue using only SELECT,
PRAGMA, and EXPLAIN QUERY PLAN.
```

### Step 3: Verify the boundary yourself

Open a second terminal from **Terminal > New Terminal**, change to
`sample-app/` if needed, and start SQLite:

```bash
sqlite3 data/orders.db
```

At the `sqlite>` prompt, enter each line:

```sql
PRAGMA query_only = ON;
PRAGMA query_only;
```

The second statement must return:

```text
1
```

Now deliberately test the guard:

```sql
CREATE INDEX should_not_be_created ON orders(customer_id);
```

Expected result:

```text
Runtime error: attempt to write a readonly database
```

Exit SQLite:

```text
.quit
```

This error is a successful demonstration of the safety boundary. The test
index was not created.

### Step 4: Check Copilot's evidence

The investigation should identify at least these contract risks:

- The application represents money as integer cents, while analytics stores
  money as SQLite `REAL`.
- The application model requires a discount rate, while analytics allows
  `discount_rate` to be `NULL`.
- The analytics schema has no foreign keys, `NOT NULL` constraints, or status
  check constraint.
- Application order statuses are a four-value lowercase literal, while the
  replica may contain other representations.

Do not accept a risk merely because it sounds plausible. For example,
`discount_rate` being nullable is file evidence; the number of affected rows
must come from a query.

**Checkpoint:** You have a table of hypotheses with file evidence, validation
queries, results, and limitations. You have also demonstrated that a write
fails while `query_only` is enabled.

---

## Exercise 2 — Run independent quality and performance investigations

**20 minutes**

Use two new sessions so that a data-quality concern does not become an
unsupported explanation for a performance concern.

### Step 1: Create the data-quality session

1. In Copilot Chat, select **New Chat**.
2. Select **Agent** mode.
3. Name it `Data quality` if session naming is available.
4. Paste:

```text
Investigate why analytics lifetime value might not reconcile with application
invoices.

Use only the local synthetic database data/orders.db and repository files.
Set PRAGMA query_only = ON before querying. Do not edit files or data, and do
not use data/README.md as evidence.

Investigate each category independently:
- money representation and units;
- orders whose customer_id has no matching customer;
- logical duplicate customers, including case-only email differences;
- distinct status values and casing;
- timestamp formats;
- NULL discount-rate semantics; and
- join fan-out between orders, line_items, and refunds.

For each category, show the exact SQL, the result, and an interpretation.
Separate observed facts from hypotheses. A fact from one category must not be
presented as the cause of another category without a query that connects them.
Do not recommend or make repairs yet.
```

Allow this session to work while you start the performance session. You do not
need to wait for it to finish first.

### Step 2: Create the query-performance session

1. Select **New Chat** again.
2. Select **Agent** mode.
3. Name it `Query performance` if possible.
4. Paste:

```text
Investigate the enterprise lifetime-value dashboard query against the local
synthetic SQLite database data/orders.db.

Use this exact query and do not rewrite it:

SELECT c.id, COUNT(o.id), SUM(o.total_amount)
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.tier = 'enterprise'
GROUP BY c.id;

Safety:
- Set PRAGMA query_only = ON.
- Run only SELECT, PRAGMA, and EXPLAIN QUERY PLAN.
- Do not edit any file or modify data or schema.
- Do not use data/README.md as evidence.

Capture:
1. the exact query plan;
2. the wall-clock timing for the unchanged query;
3. which plan operation indicates avoidable work;
4. one narrowly scoped recommendation supported by that evidence; and
5. what must be measured before and after a future change.

Do not create the index. Stop after reporting the evidence and recommendation.
```

### Step 3: Confirm the performance evidence manually

From a terminal in `sample-app/`, start SQLite:

```bash
sqlite3 data/orders.db
```

At the `sqlite>` prompt, enable timing:

```text
.timer on
```

Then paste the exact plan statement:

```sql
EXPLAIN QUERY PLAN
SELECT c.id, COUNT(o.id), SUM(o.total_amount)
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.tier = 'enterprise'
GROUP BY c.id;
```

Look for this operation:

```text
SEARCH o USING AUTOMATIC COVERING INDEX (customer_id=?)
```

SQLite is creating a temporary automatic index for this query because the
schema does not provide a persistent index on `orders.customer_id`.

Run the query itself twice:

```sql
SELECT c.id, COUNT(o.id), SUM(o.total_amount)
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.tier = 'enterprise'
GROUP BY c.id;
```

Record both timings shown after `Run Time:`. Use the second timing as the
before-change comparison to reduce one-time startup effects. Your exact timing
will depend on your computer; the query plan is the more portable evidence.

Exit SQLite:

```text
.quit
```

### Step 4: Compare the sessions without merging their explanations

Return to each Copilot session and review its result. Create a simple comparison
in your notes:

| Question | Data-quality session | Performance session |
|---|---|---|
| What was observed? | Record row-level or contract findings | Record plan and timing |
| What evidence supports it? | Record query and result | Record plan operation |
| What remains a hypothesis? | Record unproven causes | Record expected index effect |
| Was any data changed? | Must be no | Must be no |

If either session claims that malformed data caused the slow plan, or that the
missing index caused reconciliation differences, ask:

```text
Show the specific evidence connecting those two symptoms. If there is none,
restate them as independent findings.
```

### Step 5: Check the seeded quality results

Your exact queries may differ, but they should establish:

| Check | Expected result |
|---|---:|
| Orders with no matching customer | `394` |
| Logical duplicate email groups using `LOWER(email)` | `60` |
| Distinct stored status values | `7` |
| Rows with `discount_rate IS NULL` | `7113` |
| Timestamps containing `/` | `2596` |

If a number differs, verify that the database was rebuilt from the provided
script and that your query did not multiply rows through a one-to-many join.

**Checkpoint:** You have two independent reports: quality findings supported
by row counts and performance findings supported by a plan and timing.

---

## Exercise 3 — Build reconciliation before allowing repair

**15 minutes**

Before changing the database, create a control query that will reveal accidental
changes to row counts or money totals.

### Step 1: Ask Copilot to construct the baseline

Return to the `Data quality` session and paste:

```text
Create one read-only SQLite reconciliation statement using scalar subqueries.
It must return exactly one row with these named columns:
- customers
- orders
- line_items
- refunds
- orphan_orders
- distinct_statuses
- null_discount_rates
- order_total_dollars

The monetary control must be SUM(orders.total_amount), formatted to two decimal
places, and explicitly labeled as dollars. Do not join line_items or refunds
into that SUM because one-to-many joins could multiply the order total.

Show the SQL only first. Do not edit a file and do not change the database.
```

Review the proposed SQL. Confirm that each count is an independent scalar
subquery and that the money total comes only from `orders`.

### Step 2: Run the reconciliation yourself

The final statement should be equivalent to:

```sql
SELECT
  (SELECT COUNT(*) FROM customers) AS customers,
  (SELECT COUNT(*) FROM orders) AS orders,
  (SELECT COUNT(*) FROM line_items) AS line_items,
  (SELECT COUNT(*) FROM refunds) AS refunds,
  (
    SELECT COUNT(*)
    FROM orders AS o
    LEFT JOIN customers AS c ON c.id = o.customer_id
    WHERE c.id IS NULL
  ) AS orphan_orders,
  (SELECT COUNT(DISTINCT status) FROM orders) AS distinct_statuses,
  (
    SELECT COUNT(*)
    FROM orders
    WHERE discount_rate IS NULL
  ) AS null_discount_rates,
  (
    SELECT printf('%.2f', SUM(total_amount))
    FROM orders
  ) AS order_total_dollars;
```

Start SQLite:

```bash
sqlite3 data/orders.db
```

Make the output readable:

```text
.headers on
.mode column
```

Paste the reconciliation statement. Expected values:

| Control | Expected value |
|---|---:|
| `customers` | `2060` |
| `orders` | `50000` |
| `line_items` | `125362` |
| `refunds` | `2806` |
| `orphan_orders` | `394` |
| `distinct_statuses` | `7` |
| `null_discount_rates` | `7113` |
| `order_total_dollars` | `14183118.39` |

Run the exact same statement a second time. Every value must match the first
run. Copy the query and both result rows into your lab notes; this is the
baseline you will hand to the write-capable session.

Exit SQLite:

```text
.quit
```

### Step 3: Explain what the baseline protects

Ask Copilot:

```text
Explain in no more than five bullets which accidental changes this baseline
would detect and which changes it would miss. Keep facts separate from
assumptions.
```

A good answer should note that the baseline can detect changed row counts,
orphan count, status cardinality, NULL count, or aggregate order dollars. It
does not prove that every individual row is unchanged, that amounts are
correct, or that the meaning of NULL is known.

**Checkpoint:** The same reconciliation statement produced the same one-row
result twice, and you recorded its unit and limitations.

---

## Exercise 4 — Make one bounded performance change

**15 minutes**

You may now allow one database write. The approved change is limited to the
index supported by the captured plan. Do not repair quality findings in this
exercise.

### Step 1: Open a new write-capable session

1. In Copilot Chat, select **New Chat**.
2. Select **Agent** mode.
3. Name it `Bounded index change` if possible.
4. Paste the following prompt, replacing `<PASTE RESULT>` with your recorded
   reconciliation row:

```text
Make one bounded performance change to the disposable local database
data/orders.db.

Evidence:
- The unchanged dashboard query plan contains:
  SEARCH o USING AUTOMATIC COVERING INDEX (customer_id=?)
- The approved index is exactly:
  CREATE INDEX idx_orders_customer_id ON orders(customer_id);
- The pre-change reconciliation result is:
  <PASTE RESULT>

Procedure:
1. Run the reconciliation query and stop if it differs from the supplied
   baseline.
2. Confirm idx_orders_customer_id does not already exist.
3. Create only idx_orders_customer_id on orders(customer_id).
4. Run the identical reconciliation query again.
5. Stop and report an error if any reconciliation value changes.
6. Run EXPLAIN QUERY PLAN for the exact unchanged dashboard query.
7. Run the unchanged dashboard query twice and report the second timing.
8. Show every SQL statement and its result.

Do not edit schema.sql or build_db.py. Do not add another index. Do not repair
or normalize any data. Do not claim success unless the plan names
idx_orders_customer_id and reconciliation is unchanged.
```

### Step 2: Review and approve the single write

Approve the `CREATE INDEX` statement only if it is exactly:

```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

Reject suggestions for:

- an index on `line_items`;
- a multi-column index;
- data cleanup;
- schema constraints;
- changes to the dashboard query; or
- edits to `data/schema.sql` or `data/build_db.py`.

Those changes may be reasonable in another task, but the captured evidence does
not justify them here.

### Step 3: Verify the result

The post-change plan must include:

```text
SEARCH o USING INDEX idx_orders_customer_id (customer_id=?)
```

The wording around that line can vary by SQLite version. The important result
is that the named persistent index replaces `AUTOMATIC COVERING INDEX`.

The post-change reconciliation values must exactly match:

```text
2060 | 50000 | 125362 | 2806 | 394 | 7 | 7113 | 14183118.39
```

Compare the before and after timings, but do not require a specific speedup.
Laptop hardware, SQLite version, and file-system caching affect timing. The
named plan change plus unchanged reconciliation is the required evidence.

If Copilot reports that the index already exists, rebuild the database using
the command from **Before you begin**, recapture the baseline plan, and retry
this exercise once.

**Checkpoint:** The plan names `idx_orders_customer_id`, every reconciliation
value is unchanged, and no unrelated change was made.

---

## Exercise 5 — Write the decision memo the data requires

**10–15 minutes**

Some `NULL` discount rates mean no discount was applied. Others mean the value
was not recorded. The database does not contain a field that distinguishes
those meanings. Your goal is to discover the limit of the evidence and stop
rather than invent an answer.

### Step 1: Return to a read-only session

Return to the `Data quality` session. Do not use the write-capable index
session for this analysis.

Paste:

```text
Investigate discount_rate IS NULL using read-only queries.

Try to determine whether each NULL means:
A. no discount was applied; or
B. the discount was not recorded.

You may inspect correlations with order total, line-item subtotal, customer
tier, status, and timestamp. For every query, explain what it can establish and
what it cannot establish. Do not turn a correlation or reconstructed estimate
into a fact.

Stop querying when the available columns cannot distinguish A from B for all
affected rows. Then state exactly why the distinction is not identifiable from
this data.
```

Review Copilot's answer carefully. It may infer that some orders appear
consistent with a zero discount or that some appear to have missing data.
Neither inference supplies the missing provenance for every row. There is no
column that records why the value is `NULL`.

If Copilot claims it resolved every row, reply:

```text
Which stored field records whether NULL means "no discount" versus "not
recorded"? If no such field exists, retract the row-level classification and
state the limitation.
```

### Step 2: Write the human handoff

Ask:

```text
Write a decision memo of 150-250 words with these headings:

Known
Cannot be inferred
Decision owner
Proposed data-contract change
Unsafe analyses

Name the team that owns the order-to-analytics pipeline as the decision owner.
Recommend preserving provenance with an explicit discount status or reason,
plus validation that distinguishes zero from missing. Do not invent a business
rule or backfill existing rows without owner approval.
```

Review the memo. It must say:

- `7113` rows have a `NULL` discount rate.
- The current data cannot distinguish all legitimate zero-discount cases from
  missing-record cases.
- The order-to-analytics pipeline owner must define the semantics and backfill
  policy.
- A future schema or pipeline contract must preserve the distinction.
- Analyses that treat every `NULL` as zero, or every `NULL` as an unknown
  discount, are unsafe until the owner decides the contract.

This explicit stop is a successful result. It is better than a confident,
fabricated classification.

### Step 3: Restore the lab database

The index in Exercise 4 was intentionally added only to the disposable
database. Rebuild the database so the repository is ready for the next person.

macOS or Linux:

```bash
.venv/bin/python data/build_db.py
```

Windows PowerShell:

```powershell
.venv\Scripts\python data/build_db.py
```

Verify that the named index is gone:

```bash
sqlite3 data/orders.db "PRAGMA index_list('orders');"
```

No row should name `idx_orders_customer_id`.

**Checkpoint:** You produced a memo that names the evidence, the limit of the
evidence, the human owner, and the required future data-contract change.

---

## Done

You are finished when you have all five artifacts:

- [ ] A demonstrated read-only boundary and an evidence table comparing the
      analytics schema with the application.
- [ ] Separate data-quality and query-performance findings.
- [ ] A deterministic reconciliation result captured twice.
- [ ] Before/after plans showing the automatic index replaced by
      `idx_orders_customer_id`, with reconciliation unchanged.
- [ ] A decision memo that says what cannot be determined and names the owner
      of the missing semantics.

Every conclusion must be backed by one of:

- a query and result;
- a query plan;
- a reconciliation invariant; or
- an explicit “cannot be determined” statement with a named owner.

## If you get stuck

| Problem | Recovery |
|---|---|
| Copilot proposes a write in Exercises 1–3 | Reject it and repeat the read-only boundary prompt. |
| Counts do not match the checkpoints | Rebuild `data/orders.db`, then rerun the query without extra joins. |
| `idx_orders_customer_id` already exists | Rebuild the database and restart Exercise 4. |
| Timing does not improve | Verify the post-change plan names the index; timing varies by machine. |
| Copilot treats every `NULL` as zero | Ask which stored field proves that meaning. |
| A session mixes quality and performance causes | Ask for evidence connecting the symptoms; otherwise separate them. |

## Own-repository variant

Use only a local synthetic extract or an authorized replica. Replace the
expected counts with baselines from that approved dataset. Never allow Copilot
to mutate production, access unauthorized data, expose customer information,
or infer missing business semantics without an accountable owner.
