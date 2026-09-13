# Track: Data — DBA / Analytics Engineer / Data Scientist

**Surface emphasis:** github.com chat + CLI + IDE agent
**Matrix cell:** Repo holds the context · mostly synchronous
**5 exercises · ~15 min each · first 3 are core**

You own a schema you didn't design, data you didn't generate, and queries somebody wrote in a hurry three years ago before leaving the company.

---

## Read this first: your verification story is worse

Every other track in this lab leans on a test suite. Run `pytest`, get the truth in one second.

**You don't have that.**

A wrong query doesn't throw. It returns a number. A confident, plausible, correctly-formatted, **wrong** number — and it goes straight into a dashboard that someone makes a decision from.

> This is the most important thing in this track: *in data work, the failure mode is silent.* Software fails loudly. Analysis fails quietly and then gets presented to leadership.

So every exercise below asks you to build the verification *first*: a reconciliation query, a row count, a known-good total, a query plan. **If you can't cross-check a number, you can't delegate producing it.**

That's not a rule about AI. It's a rule about data work that AI makes urgent, because it's now trivial to generate a hundred plausible queries an hour.

| # | Exercise | Time | Core? |
|---|---|---|---|
| 1 | [Understand a schema you didn't design](#1--understand-a-schema-you-didnt-design) | 12 | ✅ |
| 2 | [Quantify the damage](#2--quantify-the-damage) | 18 | ✅ |
| 3 | [Make it fast, and prove it](#3--make-it-fast-and-prove-it) | 15 | ✅ |
| 4 | [Migrate without lying](#4--migrate-without-lying) | 15 | |
| 5 | [Analysis you'd actually defend](#5--analysis-youd-actually-defend) | 12 | |

---

## Setup

```bash
cd sample-app
python data/build_db.py
```

Builds `data/orders.db` — 2,060 customers, 50,000 orders, ~125,000 line items. Deterministic, so your numbers match your neighbor's exactly.

```bash
sqlite3 data/orders.db      # or any SQLite client / DBeaver / DataGrip
```

---

## 1 · Understand a schema you didn't design

**12 min · github.com chat — no clone required**

Before you query anything, understand what you inherited. Do this **in the browser**, against the repo, without opening the database.

Ask Copilot on github.com:

```
Read data/schema.sql. Explain the data model and how the tables relate.
```

```
What data integrity problems can you identify from this schema alone?
Be specific about what could go wrong at query time.
```

```
Compare data/schema.sql with app/models.py and app/pricing.py. Where does
the database representation disagree with the application's?
```

That third question is the one worth the whole exercise. The app uses **integer cents**. The warehouse uses **REAL**. Somebody, somewhere, is doing a lossy conversion and nobody documented where.

### The discipline

Write down the problems it claims exist. You are going to **verify every single one** in exercise 2 — not because the model is untrustworthy, but because "plausible schema criticism" is the easiest thing in the world to generate and the hardest to falsify without data.

**Done when:** you have a written list of suspected problems, each with a query you could run to confirm or refute it.

> **Why this surface:** zero setup, and it reads the schema *and* the application code together. The mismatch between them is invisible from inside either one.

---

## 2 · Quantify the damage

**18 min · CLI or IDE agent**

A suspected data quality problem is gossip. A **counted** one is a ticket.

Work through your list from exercise 1. For each, get a number.

### The ones that are actually there

Don't peek until you've tried. Use Copilot to help write the queries, but **decide for yourself what the right query is** — this is where a plausible-but-wrong query does real damage.

<details>
<summary><strong>Expected findings — open after you've counted</strong></summary>

| Problem | Count | Query shape |
|---|---|---|
| Orphaned orders — `customer_id` matches nothing | **394** | `LEFT JOIN customers ... WHERE c.id IS NULL` |
| Duplicate customers by case-variant email | **60** | `GROUP BY LOWER(email) HAVING COUNT(*) > 1` |
| Distinct `status` values (should be 4) | **7** | `SELECT DISTINCT status` — `paid`/`PAID`/`Paid` |
| NULL `discount_rate` | **7,113** | Ambiguous: "none applied" or "not recorded"? |
| Non-ISO timestamps | **2,596** | `created_at LIKE '%/%'` — US format mixed in |
| Money stored as `REAL` | all 50,000 | Compare against `app/models.py` |

</details>

### The one that isn't a counting problem

`discount_rate IS NULL` appears 7,113 times. Some of those mean "no discount applied." Some mean "we didn't record it."

**You cannot tell which from the data.** No query fixes this.

Write down what you'd need — a conversation with whoever owns the pipeline, a look at the ingest code, a decision from the business. This is the data equivalent of a *load-bearing decision*, and delegating it to anything, human or agent, without that conversation produces confident garbage.

### Build the reconciliation

Now the important part. Write one query you can re-run after **any** change to this database that answers: *is the data still internally consistent?*

Something like: total orders, total line items, sum of line-item value, count of orphans, count of distinct statuses — one row, five numbers.

Save it. You'll use it in exercise 4.

**Done when:** every suspected problem has a count, you've flagged the one that counting can't resolve, and you have a reconciliation query saved.

---

## 3 · Make it fast, and prove it

**15 min · CLI or IDE agent**

The dashboard query that powers the customer page:

```sql
SELECT c.id, c.email, COUNT(o.id) AS order_count, SUM(o.total_amount) AS lifetime_value
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.tier = 'enterprise'
GROUP BY c.id;
```

### Measure before you touch anything

```sql
EXPLAIN QUERY PLAN
SELECT c.id, c.email, COUNT(o.id), SUM(o.total_amount)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.tier = 'enterprise' GROUP BY c.id;
```

Read the output. You'll see:

```
SEARCH o USING AUTOMATIC COVERING INDEX (customer_id=?)
```

**Stop and appreciate that line.** SQLite is telling you, in plain language, that it had to *build an index at runtime, every time this query runs,* because you didn't give it one. That's the database filing a bug report against your schema.

### Diagnose with Copilot

```bash
sqlite3 data/orders.db "EXPLAIN QUERY PLAN SELECT ..." | copilot -p "What is this query plan telling me and what would fix it?"
```

Or ask the agent directly, giving it `data/schema.sql`.

### Fix and measure

Add the index. Re-run `EXPLAIN QUERY PLAN`. Confirm `AUTOMATIC COVERING INDEX` became a named index.

Then time it properly — both shapes:

| Shape | Before | After |
|---|---|---|
| The dashboard aggregate above | ~0.080s | ~0.019s |
| 300 point lookups (`WHERE customer_id = ?` in a loop) | ~0.96s | ~0.009s |

That second row is the N+1 pattern your ORM generates. **Roughly 100x.**

### The discipline

Ask Copilot for *more* index suggestions. Then reject most of them.

Every index costs write throughput and storage. An agent will happily suggest six. Which ones does an actual query in this repo need? That judgment is yours, and "the AI suggested it" is not an answer you can take to a schema review.

**Done when:** the plan no longer says `AUTOMATIC COVERING INDEX`, you've measured before and after, and you can justify every index you added.

---

## 4 · Migrate without lying

**15 min · IDE agent**

Fix the `status` column. Seven variants, four real states.

This is a data migration on a table you cannot afford to corrupt — the exact situation where "the agent wrote it and it looked fine" is a career event.

### The protocol

1. **Snapshot.** Run your reconciliation query from exercise 2. Write the numbers down.
2. **Get the counts per variant** before you touch anything. `GROUP BY status`.
3. **Ask for the migration** — normalize to lowercase, four canonical values, plus a `CHECK` constraint so it can't regress.
4. **Read it before running it.** Specifically: does it handle values you didn't anticipate? Is it idempotent? Can you roll it back?
5. **Run it.**
6. **Reconcile.** Row counts identical? Sum of `total_amount` unchanged? Do the per-status counts add up to the pre-migration totals?

### The question that matters

If your reconciliation numbers match, does that prove the migration was correct?

**No.** It proves nothing was *lost*. A migration that mapped every `PAID` to `cancelled` would pass a row-count check perfectly.

So: what's the *additional* check that would catch that? Write it. That gap — between "nothing was lost" and "everything is right" — is where data bugs live, and it's exactly the gap an agent's confident summary papers over.

**Done when:** statuses are normalized, a `CHECK` constraint exists, and you've run a verification that would catch a *mapping* error, not just a *loss* error.

### Stretch
Migrate `total_amount` from `REAL` to integer cents, matching the application. Prove no money was lost to floating-point rounding. This is harder than it looks and that's the point.

---

## 5 · Analysis you'd actually defend

**12 min · IDE agent or notebook**

Produce a real answer to a real question. Pick one:

- **Is the discount tier structure working?** Revenue and order volume by discount rate. Are the tiers driving larger orders or just discounting orders that would have happened?
- **What's the refund rate by customer tier,** and is the difference significant or noise?
- **Cohort retention:** do customers acquired in 2024 order more than those acquired in 2025?

### The rules

1. **Write your expected answer first.** One sentence, before you query. You're checking the analysis, not discovering it blind.
2. **Read every generated query before running it.** Specifically check the join grain — a fan-out through `line_items` will inflate every sum, and the number will look completely reasonable.
3. **Cross-check the headline number two ways.** If revenue-by-tier sums to something different than total revenue, one of them is wrong.
4. **Account for the dirty data.** Your orphaned orders and duplicate customers are still in there. Did you exclude them? Should you have? Say so explicitly in the output — an analysis that doesn't state its exclusions isn't finished.

**Done when:** you have a number, a cross-check that agrees with it, and a written statement of what you excluded and why.

> If you skipped rule 3 because the first number looked right — that's the exercise. Go back and do it.

---

## Track B — your own data

| # | What to use |
|---|---|
| 1 | A schema you inherited and have never fully read |
| 2 | The data quality problem you suspect but have never counted |
| 3 | Your slowest dashboard query — you know which one |
| 4 | A migration you've been putting off because it's scary |
| 5 | The analysis someone asked for that you haven't started |

> **Guardrails, and these are real:** work against a replica or a local dump, never production. Don't paste customer PII into a prompt. Don't let an agent run DDL against a live database. If your org has a data classification policy, this is the moment it applies — and "I was in a lab" is not a defense.

---

## Common failure modes

**The generated SQL ran and returned a number, so you moved on.**
The defining failure of this track. It always returns a number. Cross-check or don't report it.

**Join fan-out silently inflated your totals.**
The most common real bug in agent-written analytics SQL, and the hardest to spot because the result is *plausible*. Check your grain. `COUNT(DISTINCT o.id)` versus `COUNT(o.id)` is the tell.

**It suggested six indexes and you added all six.**
Every index is a write-path tax. Justify each one against an actual query or drop it.

**It confidently explained what a NULL means.**
It can't know. Neither can you, from the data. That one needs a human conversation, and accepting a plausible answer is how a reporting bug becomes a year of wrong numbers.

**Your migration passed reconciliation but you didn't check the mapping.**
Row counts prove nothing was lost. They do not prove anything is right.

---

## The point

Every other track in this lab verifies with a test suite that answers in one second. You don't have one, and that changes the calculus completely.

**Cheap verification is what buys autonomy.** Where verification is expensive or absent — which is most of data work — you get *less* autonomy, not more, no matter how good the model is.

That's not a limitation to work around. It's the actual answer to "how much should I delegate here," and it's why the most valuable thing you built today wasn't a query. It was the **reconciliation check** in exercise 2.

Build those first. They're what make everything else safe to hand off.
