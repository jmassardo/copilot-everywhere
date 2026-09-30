# Facilitator Guide

**Standard runtime:** 90 minutes
**Track work:** 75–80 minutes
**Shared debrief:** 10 minutes
**Workbench:** `sample-app/` and an authorized GitHub repository or fork

---

## Purpose of the lab

The four tracks use one Orders Service scenario to teach a shared operating
model:

1. Ground work in repository and customer evidence.
2. Separate independent questions into independent sessions.
3. Start read-only when the problem is not understood.
4. Increase agent autonomy only when scope and verification are explicit.
5. Preserve human ownership of product, contract, authorization, retention,
   and data-semantic decisions.
6. Review outputs against tests, diffs, plans, acceptance criteria, or
   reconciliation—not an agent's statement that it succeeded.

This is not a prompt-writing contest. Participants should leave with an
artifact and a workflow they could defend at work.

## What each track produces

| Track | Primary workflow | Required artifact |
|---|---|---|
| Engineer | Investigate, test, fix, hand off, delegate, review | Ownership regression test plus red/green evidence |
| Platform | Audit, encode standards, bound an agent, test activation | One customization rule that demonstrably changes or stops behavior |
| Product | Ground demand, classify, specify, delegate, accept | One delegatable issue and one explicitly non-delegatable decision issue |
| Data | Investigate read-only, reconcile, make one measured change, stop on ambiguity | Before/after plan with unchanged reconciliation, or a semantic-stop memo |

## Important fixture warning

The Engineer track expects the customer filter fixture to return another
customer's order while the original weak test remains green. Before class,
verify the exact branch participants will use.

The intended faulty implementation compares ownership incorrectly. If the
selected baseline already uses the correct equality comparison, the incident
will not reproduce. In that case:

1. Do not ask attendees to introduce a defect themselves.
2. Prepare a dedicated incident-fixture branch before class.
3. Confirm the weak test still passes on that branch.
4. Keep a saved API reproduction and prepared ownership-test diff as fallback.

The current repository state and the narrative may not always match after
demo rehearsals or earlier workshops. Preflight the actual branch; do not
assume.

---

## Delivery models

### Recommended 90-minute delivery

Complete environment setup before the scheduled session.

| Clock | Activity |
|---|---|
| 0:00–0:05 | Welcome, safety, track seating |
| 0:05–0:20 | Exercise 1 |
| 0:20–0:40 | Exercise 2 |
| 0:40–0:55 | Exercise 3 |
| 0:55–1:10 | Exercise 4 |
| 1:10–1:20 | Exercise 5 |
| 1:20–1:30 | Shared debrief |

### If setup must happen in the room

Allow 95 minutes, matching the schedule in the lab overview:

| Clock | Activity |
|---|---|
| 0:00–0:10 | Setup verification and track seating |
| 0:10–0:25 | Exercise 1 |
| 0:25–0:45 | Exercise 2 |
| 0:45–1:00 | Exercise 3 |
| 1:00–1:15 | Exercise 4 |
| 1:15–1:25 | Exercise 5 |
| 1:25–1:35 | Shared debrief |

For a strict 90-minute room booking, preinstall dependencies or shorten
Exercise 5. Do not remove the debrief; cross-track comparison is part of the
learning objective.

---

## Facilitator preparation

Complete these steps on the same operating systems, editor versions, and
GitHub environment participants will use.

### 1. Verify local dependencies

From the repository root:

```bash
cd sample-app
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
.venv/bin/python data/build_db.py
sqlite3 data/orders.db "SELECT COUNT(*) FROM orders;"
```

Expected:

```text
13 passed
All checks passed!
50000
```

On Windows, verify the equivalent `.venv\Scripts\python` commands.

### 2. Verify every seeded behavior

#### Engineer incident

Run the API-level reproduction from the Engineer track against the intended
attendee branch.

Expected on the incident fixture:

- request filter: `cust-001`;
- returned owner: `cust-002`;
- full suite: still green.

If the returned owner is `cust-001`, prepare or switch to the incident fixture.
Do not discover this mismatch during the session.

#### Platform ambiguity

Open:

- `sample-app/app/routers/orders.py`
- `sample-app/app/routers/customers.py`

Confirm the first uses structured `HTTPException` responses and the second
returns error dictionaries with HTTP 200. Confirm no refund policy exists.

#### Product boundary behavior

From `sample-app/`, run:

```bash
.venv/bin/python - <<'PY'
from app.pricing import discount_rate_for

for subtotal in (9_999, 10_000, 19_999, 20_000, 49_999, 50_000):
    print(subtotal, discount_rate_for(subtotal))
PY
```

The intended defect misses the advertised tier at exact `10_000`, `20_000`,
and `50_000`-cent boundaries.

#### Data controls

Run:

```bash
sqlite3 -header -column data/orders.db "
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
  (SELECT COUNT(*) FROM orders WHERE discount_rate IS NULL) AS null_discount_rates,
  (SELECT printf('%.2f', SUM(total_amount)) FROM orders) AS order_total_dollars;
"
```

Expected:

| Control | Value |
|---|---:|
| Customers | `2060` |
| Orders | `50000` |
| Line items | `125362` |
| Refunds | `2806` |
| Orphan orders | `394` |
| Distinct statuses | `7` |
| NULL discount rates | `7113` |
| Order total dollars | `14183118.39` |

Capture the baseline plan:

```bash
sqlite3 data/orders.db "
EXPLAIN QUERY PLAN
SELECT c.id, COUNT(o.id), SUM(o.total_amount)
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.tier = 'enterprise'
GROUP BY c.id;
"
```

Expected operation:

```text
SEARCH o USING AUTOMATIC COVERING INDEX (customer_id=?)
```

### 3. Prepare GitHub work

Use a training repository or fork. Do not use issues and pull requests that
could trigger production automation.

Prepare:

- a customer-isolation incident issue from
  `talk/demo-assets/issues/customer-isolation-incident.md`;
- a timestamp migration issue from
  `talk/demo-assets/issues/timezone-migration.md`;
- a discount-boundary issue from
  `talk/demo-assets/issues/discount-boundaries.md`;
- a decision issue for refund behavior, marked blocked or `needs-human`;
- a completed fallback timestamp pull request; and
- a completed fallback discount-boundary pull request.

The fallback PRs should remain unmerged so every cohort can review the same
evidence.

### 4. Prepare Platform fallback assets

Confirm the fallback branch `demo/platform-customization` contains:

```text
.github/copilot-instructions.md
.github/agents/orders-api-maintainer.agent.md
```

The completed examples are also available under:

```text
talk/demo-assets/platform/
```

Do not place the fallback customizations on the attendee baseline. The Platform
track needs an authentic before/after comparison.

### 5. Prepare saved outputs

Prepared screenshots and source frames are available in
[`fallback-captures/`](fallback-captures/). The
[`walkthrough`](fallback-captures/walkthrough.md) maps each capture to the
exercise and review question.

The package covers:

- Engineer API reproduction;
- Engineer blast-radius report;
- failing ownership regression test;
- passing focused and full tests after the fix;
- normal-agent refund assumptions;
- custom-agent refund stop;
- path-scoped instruction activation;
- Product demand map;
- Product acceptance matrix;
- Data baseline reconciliation;
- Data before/after query plans; and
- Data semantic-stop memo.

Use these only when live tooling is unavailable or time expires. A fallback
should preserve the review exercise, not become a lecture.

### 6. Verify Copilot and GitHub capabilities

Before participants arrive:

- Start two separate VS Code chat sessions.
- Confirm Ask/Plan and Agent modes are available.
- Confirm workspace custom agents can be created or manually loaded.
- Confirm repository and path-scoped instructions are recognized.
- Confirm GitHub Copilot can access the training repository.
- Confirm whether cloud coding agent assignment is available.
- Record which participants or tables need fallback workflows.

### 7. Reset the workspace

Before each cohort:

1. Use a clean training branch.
2. Remove live-generated Platform customization files.
3. Remove any lab-added focused tests.
4. Rebuild `sample-app/data/orders.db`.
5. Confirm `idx_orders_customer_id` is absent.
6. Re-run pytest and Ruff.
7. Confirm fallback PRs remain open and unmerged.

Do not use a broad reset command in a workspace containing participant work.
Reset only the prepared facilitator copy or replace it with a known clean
training checkout.

---

## Room and staffing plan

### Seating

Group attendees by track so they can compare artifacts and share access:

| Track | Primary need | Useful pairing |
|---|---|---|
| Engineer | VS Code, terminal, multiple sessions | Pair one strong debugger with one reviewer |
| Platform | Customization-capable VS Code | Pair unsupported editor versions with a working machine |
| Product | Browser repository and issue access | Pair read-only participants with someone who can create issues |
| Data | Python, SQLite, terminal | Pair missing SQLite clients with a prepared environment |

For more than 30 participants, use a second facilitator. Most help requests
cluster in the first 15 minutes and again when cloud tasks are reviewed.

### Accessibility and inclusion

- Share the lab links before the session.
- Keep all commands and prompts in the written track; do not require copying
  from a projected terminal.
- Read expected visual indicators aloud.
- Allow keyboard-only navigation and pairing.
- Avoid requiring public speaking during the debrief; a partner may present an
  artifact.
- Never ask participants to expose company or customer data.

### Materials

- Display the lab overview and current clock.
- Keep fallback links in a facilitator-only document.
- Provide paper or a shared note template for evidence tables.
- Make the strict stop time visible five minutes before the debrief.

---

## Opening script

Use this framing:

> The talk showed these workflows in compressed form. This lab includes the
> parts real work requires: investigation, decisions, handoffs, verification,
> and review. Your goal is not to finish five prompts. Your goal is to produce
> one workflow artifact you would defend at work.

Then:

> Keep independent questions in independent sessions. Start read-only when you
> do not understand the problem. Delegate only bounded work. Review evidence,
> not an agent's confidence. If customer, contract, authorization, retention,
> or data meaning is missing, stop and name the human owner.

Finally:

> This repository is synthetic. Do not connect the lab to production or paste
> private data into a tool that is not approved by your organization.

### Track selection

Ask participants to choose based on the work they own:

- **Engineer:** escaped behavior, tests, implementation, review.
- **Platform:** reusable instructions and bounded agents.
- **Product:** demand, decisions, issues, and acceptance.
- **Data:** evidence, reconciliation, measured schema change, semantic limits.

Do not assign Product attendees to write Python or Data attendees to clean
seeded data. The tracks deliberately preserve role ownership.

---

## Facilitation cadence

### At the start of every exercise

1. Announce the remaining time.
2. State the artifact, not just the activity.
3. Remind attendees whether the session is read-only or write-capable.
4. Point to the fallback condition.

### While circulating

Ask:

- “What evidence supports that?”
- “Is that observed, inferred, or decided?”
- “Why is this safe to do in parallel?”
- “What is the stop condition?”
- “What would make this result unacceptable?”

Avoid solving the seeded problem immediately. Ask questions that restore the
workflow.

### Five minutes before the debrief

Announce:

> Stop starting new work. Capture the best artifact you have, record what
> remains incomplete, and choose one person or pair to share.

An explicit incomplete result with evidence is better than a rushed,
unreviewed change.

---

## Engineer facilitation

### Learning objective

Green CI can coexist with an exposure when tests assert the wrong invariant.
Copilot sessions should divide investigation, implementation, and review rather
than accumulate one unbounded conversation.

### Exercise 1: investigation

Watch for:

- two genuinely different sessions;
- API-level reproduction before code edits;
- a blast-radius statement bounded by call paths; and
- recognition that result count does not prove ownership.

If both sessions receive the same prompt, ask:

> Which question can one session answer without the other's context?

If an attendee opens the storage file and immediately announces the operator,
redirect:

> Show the customer-visible reproduction and explain why the test passed.

If the fixture does not reproduce, move the attendee to the prepared incident
branch or saved evidence. Do not have them edit in the defect.

### Exercise 2: red before green

Required sequence:

1. Test-only edit.
2. Failure on ownership.
3. Minimal production fix.
4. Focused tests.
5. Full tests.
6. Ruff.

Reject a regression test that asserts only:

```text
len(results) == 1
```

The test must inspect each returned `customer_id`.

If Copilot edits production and tests together, have the attendee reject the
production edit, restore the test-only phase, and obtain a meaningful failure.

### Exercise 3: cloud delegation

The timestamp task may touch a file also touched by the incident but should
operate on different symbols and behavior. Ask attendees to state:

- exact overlapping files;
- whether the same lines or symbols overlap;
- whether the incident diff is stable; and
- what integration review is needed.

Do not accept “different issue” as a parallel-safety argument.

### Exercise 4: handoff

The reviewer receives:

- incident;
- reproduction/blast-radius summary;
- test specification;
- diff; and
- command results.

It should not receive a giant transcript. If the review is generic, ask for
blocking/non-blocking findings tied to diff evidence.

### Exercise 5: cloud result

Redirect style-only review toward:

- timezone awareness;
- serialization compatibility;
- file scope;
- dependency and analytics exclusions; and
- verification.

### Engineer required artifact rubric

| Criterion | Pass |
|---|---|
| Reproduction | API request demonstrates wrong ownership |
| Test | Asserts every filtered result belongs to requested customer |
| Red/green | Fails before production fix and passes afterward |
| Scope | Production change is limited to root cause |
| Verification | Focused, full pytest, and Ruff evidence |
| Handoff | Fresh reviewer can decide from compact evidence |

---

## Platform facilitation

### Learning objective

Durable repository context belongs in instructions; role-specific boundaries
belong in a custom agent; file-specific practices belong in scoped
instructions. Each layer must be behaviorally tested.

### Exercise 1: unconfigured baseline

Do not supply refund policy. The normal agent should expose missing:

- eligible states;
- partial-refund behavior;
- amount limits;
- idempotency;
- authorization;
- error compatibility; and
- audit or retention rules.

If an attendee treats the agent's plausible choices as repository conventions,
ask:

> Which file or approved decision establishes that rule?

### Exercise 2: repository instructions

Check the file is at:

```text
.github/copilot-instructions.md
```

Common mistake:

```text
sample-app/.github/copilot-instructions.md
```

The file should contain durable rules only. Remove broad style advice and
invented product policy.

Evidence of success is a fresh session referencing the file and behaving
differently, not merely the file's existence.

### Exercise 3: custom agent

The **Orders API Maintainer** must demonstrate three paths:

| Path | Request | Expected |
|---|---|---|
| Missing decision | Add refund endpoint | Stops and requests policy |
| Prohibited | Change dependencies and CI | Refuses or reroutes |
| Allowed | Plan an existing-contract test | Proceeds within app/test scope |

If the custom agent implements refunds immediately, have the participant add
explicit stop conditions and start a fresh test session.

### Exercise 4: scoped instructions

Check:

```yaml
---
applyTo: "sample-app/tests/**"
---
```

The test task should reference the scoped file. A README-only task should not.
If both do, troubleshoot path/frontmatter and restart the chat.

Ask participants whether customer ownership is merely a test convention or a
repository-wide security expectation. The answer may vary, but it must be
deliberate.

### Exercise 5: asynchronous validation

The improvement must be justified by a real PR observation. Reject:

- one-off details;
- duplicated instructions;
- vague “be careful” language; and
- policy the platform team does not own.

### Platform required artifact rubric

| Criterion | Pass |
|---|---|
| Gap audit | Distinguishes conflict, missing policy, and standards |
| Repository instructions | Load in fresh session and alter behavior |
| Agent boundaries | Allowed, prohibited, and stop paths demonstrated |
| Scoped guidance | Applies to tests and not unrelated files |
| Iteration | PR review produces one durable improvement |

---

## Product facilitation

### Learning objective

Product can use Copilot for repository-grounded discovery and asynchronous
delivery without delegating product judgment or reviewing code syntax.

### Exercise 1: demand map

Ensure every source item in `FEEDBACK.md` appears. Watch for these errors:

- requested solution presented as the underlying problem;
- sales attribution treated as proven causation;
- exact-boundary and penny-rounding complaints combined;
- unsupported repository citations; and
- incident evidence omitted because current code differs.

Require attendees to open and verify at least three citations.

### Exercise 2: classification and priority

Protect these distinctions:

- Discount boundary: objective defect.
- Refund capability: product decision.
- Customer HTTP status: compatibility decision.
- Customer deletion: retention/cascade decision.
- Analytics NULL meaning: discovery/data ownership.

Copilot may propose scores. The attendee must add at least one explicit piece
of human business context and own the final ranking.

If a participant asks Copilot to prioritize without criteria, ask:

> Which business value or risk tolerance did the model infer without evidence?

### Exercise 3: two issue types

The boundary issue must include:

- `10_000`, `20_000`, and `50_000` cents;
- one cent below each threshold;
- focused tests, full pytest, and Ruff;
- rounding as a non-goal; and
- no unrelated API or money-representation changes.

The refund decision issue must not contain implementation acceptance criteria.
It must name owners and keep implementation blocked.

If an attendee creates many issues, redirect them to the two required
artifacts. The lab teaches issue quality, not backlog volume.

### Exercise 4: delegation

Only the objective boundary issue is delegated. The refund decision remains
human-owned.

Attendees should check status once and continue useful work. If they repeatedly
refresh, ask:

> What decision work can you advance while implementation runs?

### Exercise 5: acceptance

Product reviews:

- exact observable thresholds;
- one-cent-below behavior;
- non-goals;
- customer-visible outcome; and
- check evidence.

Redirect Python-style discussion to the Engineer track or reviewer. Product may
ask for code explanations, but acceptance rests on behavior and scope.

### Product required artifact rubric

| Criterion | Pass |
|---|---|
| Demand map | Every source item represented and cited |
| Evidence | Customer, repository, and human context separated |
| Bug issue | Observable, bounded, verifiable |
| Decision issue | Owners and open questions; implementation blocked |
| PR decision | Each criterion mapped to outcome evidence |

---

## Data facilitation

### Learning objective

Data work begins read-only, keeps quality and performance hypotheses separate,
uses reconciliation before writes, and explicitly stops when stored data cannot
answer a semantic question.

### Exercises 1–2: read-only enforcement

Approve only:

- `SELECT`;
- `PRAGMA`; and
- `EXPLAIN QUERY PLAN`.

If an attendee creates an index early:

1. Stop the session.
2. Rebuild `data/orders.db`.
3. Restart from the read-only boundary.

The quality and performance sessions must be separate. If one symptom becomes
the unsupported cause of the other, ask for the query that connects them.

### Exercise 3: reconciliation

The money total must come directly from `orders`. Joining orders to line items
or refunds before summing can multiply values.

Require:

- one-row output;
- explicit dollar unit;
- exact expected values; and
- two identical runs.

The baseline detects some accidental changes but does not prove every row or
business meaning is correct.

### Exercise 4: bounded index

Approve only:

```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

The required post-change evidence is:

- plan names `idx_orders_customer_id`;
- reconciliation is unchanged; and
- the query itself is unchanged.

Do not require a fixed millisecond improvement. Hardware and caching vary.

### Exercise 5: semantic stop

`discount_rate IS NULL` cannot be classified row-by-row as “no discount” or
“not recorded” from the stored columns. Let attendees investigate correlations,
then require the stop.

If an attendee or agent confidently classifies all rows, ask:

> Which stored field records why the value is NULL?

The memo must name the order-to-analytics pipeline owner and identify unsafe
analyses.

### Data required artifact rubric

| Criterion | Pass |
|---|---|
| Safety | Read-only boundary demonstrated |
| Separation | Quality and performance reports remain independent |
| Reconciliation | Exact one-row baseline captured twice |
| Change | One evidenced index only |
| Verification | Named plan plus unchanged controls |
| Semantic stop | Unknown meaning and human owner explicitly documented |

---

## Cloud-agent fallback protocol

Cloud completion time is nondeterministic. Use this protocol consistently:

1. The participant delegates once.
2. Confirm GitHub accepted or queued the task.
3. The participant records the link and continues.
4. Check status once near review time.
5. If complete, review the participant's result.
6. If incomplete, open the prepared fallback PR.
7. Perform the same acceptance exercise.

Do not let participants spend lab time polling. The learning objective is task
routing and review, not cloud queue behavior.

If cloud assignment fails:

- preserve the issue as the scope artifact;
- run it in a separate local coding-agent session if practical; or
- use the fallback PR.

Do not broaden the issue to “make the agent try harder.”

---

## Troubleshooting matrix

| Symptom | Likely cause | Facilitator action |
|---|---|---|
| `.venv/bin/python` not found | Setup incomplete or wrong folder | Complete setup and confirm terminal is in `sample-app/` |
| Tests fail before work begins | Dirty or incorrect baseline | Move to prepared clean branch; do not debug unrelated work in lab time |
| Incident does not reproduce | Baseline contains corrected filter | Use prepared incident fixture or saved evidence |
| Custom agent not listed | Wrong path, invalid frontmatter, stale window | Check `.github/agents/*.agent.md`, save, reload window |
| Instructions not referenced | Wrong `.github` location or old session | Move to repository root, save, start fresh chat |
| Scoped rules apply everywhere | Missing or incorrect `applyTo` | Correct frontmatter and restart chat |
| GitHub issue controls unavailable | Read-only repository or plan limitation | Use fork, partner, or prepared issue |
| Cloud task never completes | Queue or entitlement | Switch to fallback PR at review time |
| SQLite cannot open database | Wrong directory or database not built | `cd sample-app`, then run `data/build_db.py` |
| Data counts differ | Database changed or fan-out query | Rebuild database; rerun scalar-subquery reconciliation |
| Data timing varies | Hardware/cache variation | Judge named plan change, not fixed runtime |
| Copilot invents policy | Missing stop instruction | Ask for approved source; move question to human-owned decision |

---

## Shared debrief

### Transition

At the stop time, say:

> Stop editing and capture your current evidence. An incomplete but reviewed
> artifact is acceptable. An unreviewed “done” result is not.

Ask one person or pair from each track to share for no more than two minutes.

### What each track shows

- **Engineer:** failing ownership assertion and passing result after the narrow
  fix, or the compact reviewer handoff.
- **Platform:** one prompt before and after customization, showing changed or
  stopped behavior.
- **Product:** the delegatable boundary issue beside the blocked refund
  decision issue.
- **Data:** the before/after plan and unchanged controls, or the semantic-stop
  memo.

### Debrief questions

Ask:

1. What did the first session know, and what was deliberately withheld?
2. Which work ran concurrently, and what made that safe?
3. What evidence allowed more autonomy?
4. Where did Copilot correctly stop for a human?
5. Which artifact is reusable after today?

If time permits:

6. Which confident answer became weaker after citation or test review?
7. Which instruction belonged globally, to one agent, or to one path?
8. Which metric would reveal whether this workflow improves outcomes?

### Closing script

> The value did not come from putting Copilot everywhere. It came from routing
> work to the right session, agent, and autonomy level; giving each one the
> evidence and boundaries it needed; and preserving the human decisions that
> make the result correct.

---

## After the session

### Reset

On facilitator-controlled training copies:

1. Preserve exemplary anonymous artifacts if participants consent.
2. Do not merge exercise pull requests into the shared baseline.
3. Close or reset temporary training issues according to your cohort process.
4. Remove generated Platform customization files from the live-work branch.
5. Rebuild `sample-app/data/orders.db`.
6. Verify `idx_orders_customer_id` is absent.
7. Restore the intended Engineer incident fixture for the next cohort.
8. Run the full pytest suite and Ruff.

### Retrospective

Record:

- setup failures by type;
- percentage of participants using fallbacks;
- exercises that consistently exceeded time;
- prompts that caused unsafe assumptions;
- customization activation problems by editor version;
- cloud-task completion rate before review time; and
- quality of required artifacts.

Revise the written steps when several participants fail at the same point. Do
not treat repeated documentation confusion as an attendee skill problem.

### Do not collect

Do not collect:

- private prompts containing company data;
- customer identifiers;
- repository credentials;
- proprietary code;
- chat transcripts without consent; or
- productivity rankings of individual participants.

Measure workflow friction and artifact quality, not individual prompt volume.
