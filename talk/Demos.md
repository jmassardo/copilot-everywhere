# Persona Demo Run Sheet

**Total:** 40 minutes  
**Per persona:** 8–10 minutes  
**App:** `sample-app/`  
**Epic:** #1

---

# Before the talk

## Local setup

```bash
cd sample-app
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
.venv/bin/python data/build_db.py
```

Expected:

- `13 passed`
- Ruff clean
- 50,000 analytics orders
- #2 still reproduces despite green tests

## Open these tabs/windows

1. VS Code — `sample-app/`
2. GitHub — #2 customer-isolation incident
3. GitHub — #3 timestamp migration
4. GitHub — prepared fallback PR for #3
5. GitHub — `sample-app/FEEDBACK.md`
6. GitHub — #5 discount-boundary bug
7. GitHub — prepared fallback PR for #5
8. VS Code — Platform customization branch from #4
9. SQLite terminal/client — `data/orders.db`

## Prepare these VS Code sessions

- `Incident investigation`
- `Isolation blast radius`
- `Local implementation`
- `Platform policy`
- `Data quality`
- `Query performance`

## Safety

- Test account and synthetic data only.
- Never wait for a cloud agent on stage.
- Do not merge on stage.
- Keep fallback PRs ready.
- Rebuild `orders.db` after the Data demo.

---

# 1. Engineer — escaped customer-isolation defect

**Issue:** #2  
**Goal:** Show parallel sessions, agent selection, local implementation, and cloud delegation.

## 0:00 — Show green CI

Open #2, then run:

```bash
.venv/bin/python -m pytest -q
```

**Key takeaway:** Passing tests prove only the behavior they assert. Green CI
can coexist with a serious defect when the important invariant is missing.

## 1:00 — Start two sessions

### Session: Incident investigation

Select a planning/read-only agent:

> Investigate #2 without editing files. Trace the filtered orders request from
> the router to storage. Give me a minimal API-level reproduction and identify
> which existing test should have caught it.

### Session: Isolation blast radius

> Treat #2 as a possible customer-isolation defect. Find every path that fetches
> or filters orders by customer. Report affected endpoints, ownership
> safeguards, and relevant tests. Do not edit files.

**Key takeaway:** Use separate sessions for independent questions. Reproduction
and blast-radius analysis can run concurrently without mixing their context.

## 3:00 — Delegate independent work

Open #3 and assign it to the cloud coding agent.

**Key takeaway:** Delegate independent work when its scope and verification are
clear; do not make unrelated work block the incident response.

Move on immediately.

## 4:00 — Review both investigations

Expected:

- `orders.list_orders` calls `store.list_orders`.
- `store.list_orders` uses `!=`.
- The existing test checks only result count.
- The bug returns another customer’s order while the test stays green.

Ask the investigation session:

> Turn the reproduction into a regression-test specification. It must fail on
> customer ownership, not merely on result count.

## 6:00 — Hand off to the coding agent

Open `Local implementation`, select Agent:

> Implement the regression test from the investigation. Confirm it fails for
> the ownership violation, then make the smallest production fix. Run the
> focused test, full suite, and Ruff. Do not change unrelated seams.

Expected:

- Test asserts every result belongs to the requested customer.
- `!=` changes to `==`.
- Focused and full tests pass.

Review the diff in VS Code.

## 9:00 — Key takeaways

- Use read-only investigation before implementation.
- Keep reproduction and blast-radius analysis in separate sessions.
- Hand evidence—not a giant transcript—to the coding agent.
- Delegate independent, verifiable work to the cloud.

## Fallback

- Show saved investigation outputs.
- Open the prepared ownership-test diff.
- Run the strengthened test live.

---

# 2. Platform/DevEx — make safe behavior repeatable

**Issues:** #3 and #4  
**Goal:** Review asynchronous work, then show instructions and a bounded custom agent.

## 0:00 — Check the cloud task

Open the prepared or live PR for #3.

Ask Copilot on the PR:

> Review this PR against #3. Map each acceptance criterion to evidence in the
> diff or checks. Flag dependency, API, pricing, or analytics changes outside
> scope.

Check:

- Timezone-aware UTC is used consistently.
- API field names did not change.
- No unrelated dependencies or behavior changed.

**Key takeaway:** Green checks prove mechanics. They do not make compatibility
or policy decisions.

## 2:00 — Show the ambiguous repository

Open:

- `app/routers/orders.py`
- `app/routers/customers.py`

Point out:

- Orders use structured `HTTPException`.
- Customers return error dictionaries with HTTP 200.

In a normal Agent session:

> Add a refund endpoint following this repository’s conventions. Plan only.

Point out assumptions about:

- Error behavior
- Partial refunds
- Eligible states
- Maximum amount
- Idempotency

## 4:00 — Switch to the #4 branch

Show:

- `.github/copilot-instructions.md`
- `.github/agents/orders-api-maintainer.agent.md`

Key rules:

- Structured errors for new APIs
- Integer-cent money
- Timezone-aware UTC
- Existing contracts require explicit decisions
- No invented refund policy
- Focused tests, full suite, and Ruff

## 6:00 — Select the custom agent

Start a fresh session and select **Orders API Maintainer**:

> Add a refund endpoint following this repository’s conventions.

Expected:

- It does not edit immediately.
- It asks for refund policy and compatibility decisions.
- It identifies missing idempotency, limits, and eligible states.

Show the customization/context indicator.

## 9:00 — Key takeaways

- Repository instructions carry durable engineering standards.
- Custom agents define a bounded mode of work.
- Stop conditions are as important as implementation instructions.
- A safe agent asks for missing policy instead of inventing it.

## Fallback

- Show the completed #3 PR.
- Show saved generic-agent and custom-agent responses.
- Open the instruction and agent files live.

---

# 3. Product Manager — decide, specify, delegate

**Issues:** #5 and #6  
**Goal:** Ground feedback in code, separate bugs from decisions, and review outcomes.

## 0:00 — Triage the feedback

Open `sample-app/FEEDBACK.md` on GitHub.

Ask:

> Group this feedback into customer problems, technical risks, and requested
> solutions. Cite every source item. Check each theme against the repository and
> label what the code confirms, contradicts, or cannot answer.

Expected themes:

- Customer isolation
- Discount boundaries and reconciliation
- API error compatibility
- Refund capability
- Timestamp behavior
- Customer deletion and orphaned orders

## 3:00 — Separate bugs from decisions

Ask:

> Sort the themes into objective defects and product or contract decisions. For
> each defect, name the verification signal. For each decision, list the
> unanswered question.

Call out:

- #5 discount boundary = objective bug
- #6 refund behavior = product decision
- Customer HTTP status behavior = compatibility decision
- Customer deletion = retention/cascade decision

**Key takeaway:** Delegating an unresolved decision does not remove the
decision; it makes the assumption less visible.

## 5:00 — Audit the issue

Open #5:

> Audit #5 against the feedback and repository. Map every acceptance criterion
> to evidence. Flag hidden decisions and scope that could absorb the separate
> rounding defect.

Check:

- Exact thresholds
- One cent below each threshold
- Focused tests
- Rounding explicitly excluded

## 7:00 — Delegate

Assign #5 to the cloud coding agent.

Move immediately to the prepared fallback PR.

## 8:00 — Review as a PM

Ask on the PR:

> Explain the observable behavior change. Map each acceptance criterion to a
> test or changed outcome. Flag anything outside scope.

Check outcomes—not Python style:

- Exact thresholds work.
- Values below thresholds stay in the lower tier.
- Rounding did not change.
- API contracts did not change.

## 9:30 — Key takeaways

- Product owns evidence, priority, decisions, scope, and acceptance.
- Objective defects can be delegated when “done” is explicit.
- Product and contract decisions remain human-owned.
- Review agent work against outcomes, not implementation syntax.

## Fallback

- Use the prepared #5 issue and PR.
- Show #6 as blocked with `needs-human`.

---

# 4. DBA/Data Scientist — investigate before changing

**Issues:** #7 and #8  
**Goal:** Use read-only investigation, parallel sessions, measured change, and an explicit human stop.

## 0:00 — Select the read-only agent

Select **Orders Data Investigator**.

### Session: Data quality

> Compare `data/schema.sql` with the application models and pricing logic.
> Investigate why lifetime value might not reconcile. Propose read-only
> validation queries and separate hypotheses from confirmed findings.

### Session: Query performance

> Analyze the enterprise lifetime-value dashboard query. Capture the query plan
> and recommend only changes supported by plan evidence. Do not modify files or
> data.

## 3:00 — Review the findings

Data-quality findings:

- App money uses integer cents.
- Analytics money uses `REAL`.
- Orphaned orders exist.
- Status values are inconsistent.
- NULL discount meaning is ambiguous.

Performance finding:

```text
SEARCH o USING AUTOMATIC COVERING INDEX (customer_id=?)
```

**Key takeaway:** One measured query-plan problem supports one targeted index,
not a speculative index sweep.

## 5:00 — Implement only the measured fix

Use a write-capable Agent session:

> Implement only the measured index from #7. Run reconciliation before and
> after. Re-run the identical query plan. Stop if any count or control total
> changes.

Expected:

```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

Expected plan:

```text
SEARCH o USING INDEX idx_orders_customer_id (customer_id=?)
```

## 7:00 — Show where the agent stops

Run:

```bash
sqlite3 data/orders.db \
"SELECT COUNT(*) FROM orders WHERE discount_rate IS NULL;"
```

Expected:

```text
7113
```

Ask:

> Which NULL rows mean “no discount” and which mean “not recorded”?

Expected answer: the data cannot determine that.

Open #8 and show `status:blocked` plus `needs-human`.

## 9:00 — Key takeaways

- Start data investigations with read-only access.
- Keep data-quality and performance hypotheses separate.
- Give write-capable agents measured changes and reconciliation invariants.
- When data cannot verify meaning, stop and involve the human owner.

## Fallback

- Show saved before/after plans.
- Run the NULL count live.
- Open #8.

## Reset

```bash
.venv/bin/python data/build_db.py
```

---

# Close

Show #1 and its work-item checklist.

| Work | State |
|---|---|
| #2 customer isolation | Investigated and fixed locally |
| #3 timestamps | Completed asynchronously |
| #4 platform customization | Reusable guardrails |
| #5 discount boundary | Delegated and reviewed |
| #6 refund contract | Blocked on product decision |
| #7 analytics index | Measured change |
| #8 NULL semantics | Blocked on data-owner decision |

## Key takeaway

The personas are not using four unrelated Copilot products. They are routing
different work through the right sessions, agents, and autonomy levels while
keeping ownership and verification visible.
