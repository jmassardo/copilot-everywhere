# Track: Senior / Staff Engineer

**Duration:** 75–80 minutes
**Surfaces:** VS Code, GitHub Copilot Chat, terminal, GitHub, cloud coding agent
**Outcome:** Investigate and resolve a customer-isolation incident that escaped
green CI, hand evidence between local Copilot sessions, and review an
independent maintenance change produced asynchronously.

---

## Scenario

Support escalated `INCIDENT-4552`:

> Enterprise customer `cust-001` filtered the orders endpoint by customer ID
> and received an order owned by `cust-002`. The unfiltered endpoint looked
> normal. Support reproduced it twice.

The test suite is green. Treat the report as a potential customer-data exposure
until engineering evidence proves otherwise. Do not dismiss the incident
because tests pass, and do not edit production code before you have a
reproduction.

## Before you begin

### 1. Open the repository and terminal

1. Open VS Code.
2. Select **File > Open Folder**.
3. Open the `copilot-everywhere` repository.
4. Select **Terminal > New Terminal**.
5. Change to the sample application:

```bash
cd sample-app
```

All commands in this track run from `sample-app/`.

### 2. Confirm you are not working on `main`

Run:

```bash
git branch --show-current
```

If the result is `main`, create a lab branch:

```bash
git switch -c lab/engineer-customer-isolation
```

Do not commit or discard another attendee's changes. If the branch already
contains changes you did not make, ask the facilitator for a clean lab branch.

### 3. Run the green baseline

macOS or Linux:

```bash
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
```

Windows PowerShell:

```powershell
.venv\Scripts\python -m pytest -q
.venv\Scripts\ruff check .
```

Expected:

```text
13 passed
All checks passed!
```

Warnings about `datetime.utcnow()` are expected and belong to a later,
independent maintenance task.

If tests or lint fail, stop and ask the facilitator for the prepared baseline.
A red baseline makes later red/green evidence unreliable.

### 4. Know the Copilot controls used in this lab

VS Code wording varies slightly by version:

1. Select the **Chat** or **Copilot** icon in the Activity Bar.
2. Select **New Chat** (`+`) to create an independent session.
3. Use the mode picker near the chat input:
   - Use **Ask** or **Plan** for read-only investigation.
   - Use **Agent** only when the exercise explicitly allows edits or commands.
4. Review every file edit and terminal command before accepting it.
5. Keep each named session separate. Do not paste both investigation jobs into
   one chat.

You do not need a custom agent. The regular local Copilot modes are sufficient.

### 5. Confirm the incident fixture is available

Do not inspect the storage implementation yet. In a terminal, run this
API-level reproduction:

```bash
.venv/bin/python - <<'PY'
from fastapi.testclient import TestClient

from app import store
from app.main import app

store.reset()
client = TestClient(app)
items = [
    {
        "sku": "WIDGET-1",
        "description": "Widget",
        "quantity": 1,
        "unit_price_cents": 1500,
    }
]
client.post("/orders", json={"customer_id": "cust-001", "items": items})
client.post("/orders", json={"customer_id": "cust-002", "items": items})
body = client.get("/orders", params={"customer_id": "cust-001"}).json()
print([(order["id"], order["customer_id"]) for order in body])
PY
```

The intended lab fixture returns one order owned by `cust-002`, reproducing the
report for a `cust-001` filter.

If it returns only `cust-001`, **do not introduce a defect yourself**. Show the
result to the facilitator and use the prepared incident branch or saved
reproduction. Continue only after the facilitator confirms the intended
fixture.

---

## Exercise 1 — Triage with two independent sessions

**15 minutes**

One session will reproduce the exact symptom. A second session will assess the
possible blast radius. These questions can run independently and should not
share assumptions.

### Step 1: Start the reproduction session

1. Open Copilot Chat.
2. Select **New Chat**.
3. Select **Ask** or **Plan** mode. If only Agent mode is available, explicitly
   forbid edits.
4. Name the session `Incident reproduction` if session naming is available.
5. Paste:

```text
Investigate INCIDENT-4552 as a read-only incident response.

Reported behavior:
GET /orders?customer_id=cust-001 can return an order owned by cust-002.
The full test suite currently passes.

Tasks:
1. Trace the request from the FastAPI route through storage.
2. Produce a minimal API-level reproduction using TestClient.
3. Identify the exact existing test that should have caught this.
4. Explain why that test can pass while customer ownership is wrong.
5. Cite the file and symbol for every conclusion.

Do not edit any file. Do not fix the bug. You may run read-only inspection
commands and tests, but stop after reporting the reproduction, root-cause
hypothesis, and missing test invariant.
```

### Step 2: Start the blast-radius session

Without waiting for the first session:

1. Select **New Chat** again.
2. Select **Ask** or **Plan** mode.
3. Name the session `Isolation blast radius`.
4. Paste:

```text
Treat INCIDENT-4552 as a possible customer-isolation defect.

Independently inspect every path in sample-app that:
- accepts a customer identifier;
- fetches, lists, creates, or deletes orders;
- looks up a customer for order behavior; or
- asserts order ownership in tests.

Report:
1. potentially affected endpoint or function;
2. current ownership safeguard;
3. relevant tests;
4. whether the incident is confirmed, ruled out, or not exercised there; and
5. exact file and symbol evidence.

Do not edit files. Do not propose a broad refactor. Distinguish confirmed blast
radius from code that merely deserves review.
```

### Step 3: Review permissions and output

Approve file reads and test execution. Reject edits. If a session proposes a
change, reply:

```text
Remain read-only. Record the proposed change as a hypothesis and finish the
evidence report.
```

The reproduction report should identify:

- the `GET /orders` route;
- the storage filtering function;
- an API call that requests one customer and receives another customer's
  order; and
- a test that checks only result count rather than the owner of each result.

The blast-radius report should not call every order endpoint vulnerable merely
because it is related to orders. Require a specific data path and safeguard
assessment.

### Step 4: Reconcile contradictions

Compare both reports. If they disagree, ask the session making the broader
claim:

```text
Point to the exact call path and test evidence for that claim. Label it
unverified if the repository does not demonstrate it.
```

Write a two-sentence blast-radius statement in your notes:

1. What behavior is confirmed?
2. Which related paths were reviewed but are not proven affected?

**Checkpoint:** You have an API-level reproduction, a missing ownership
invariant, and a bounded blast-radius statement. No files have changed.

---

## Exercise 2 — Strengthen verification before fixing

**20 minutes**

You will first add a test that fails for the reported ownership violation.
Only after observing the failure will you allow a production change.

### Step 1: Ask for a regression-test specification

Return to `Incident reproduction` and paste:

```text
Turn the confirmed reproduction into a regression-test specification.

The test must:
- create one order for cust-001 and one for cust-002;
- request GET /orders?customer_id=cust-001;
- assert that the response succeeds;
- assert the expected number of results; and
- assert that every returned order belongs to cust-001.

Explain which assertion catches the escaped defect and why the existing count
assertion does not. Do not edit files.
```

Copy the resulting specification, not the entire conversation.

### Step 2: Hand the specification to an implementation session

1. Select **New Chat**.
2. Select **Agent** mode.
3. Name the session `Incident implementation`.
4. Paste:

```text
Implement only the following regression-test specification:

<PASTE THE TEST SPECIFICATION HERE>

Rules for this phase:
- Edit tests only.
- Do not edit application code.
- Keep the test at the API boundary.
- Reuse the existing fixtures and item helper.
- Run only the new or directly affected test.
- Stop after showing that the test fails because a returned order belongs to
  the wrong customer.

If the test passes, do not weaken it and do not modify production code. Report
that the supplied fixture does not reproduce the incident.
```

### Step 3: Inspect the red result

Before continuing, verify:

- The failure compares an actual returned `customer_id` with the requested ID.
- The failure is not caused by a typo, import error, or broken fixture.
- The test would fail if the filtering comparison returned other customers.
- Production code is unchanged.

Use the **Source Control** view or run:

```bash
git diff -- tests/test_orders.py
```

The diff should contain only the strengthened regression test.

If the test passes despite the prepared fixture, stop and ask the facilitator.
Do not manufacture a failure by changing expected values.

### Step 4: Authorize the smallest production fix

Continue in `Incident implementation`:

```text
The regression test now fails for the customer-ownership violation.

Make the smallest production change that restores this invariant:
every order returned for a customer_id filter belongs to that customer.

Do not refactor storage, alter unrelated endpoints, change pricing, standardize
API errors, or modify timestamps.

Then run:
1. the focused ownership test;
2. the full pytest suite; and
3. Ruff.

Show the production diff, exact commands, and results. Report any related
customer-isolation risk that remains unverified.
```

### Step 5: Review the change yourself

Do not rely only on Copilot's summary.

1. Open the Source Control diff.
2. Confirm the test asserts ownership, not only length.
3. Confirm the production change is limited to the filtering condition.
4. Confirm unrelated seeded defects remain untouched.
5. Run the verification yourself:

macOS or Linux:

```bash
.venv/bin/python -m pytest -q tests/test_orders.py
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
```

Windows PowerShell:

```powershell
.venv\Scripts\python -m pytest -q tests/test_orders.py
.venv\Scripts\python -m pytest -q
.venv\Scripts\ruff check .
```

Expected:

- all tests in `tests/test_orders.py` pass;
- the full suite passes (`13` tests if the existing weak test was strengthened,
  or `14` if a separate regression test was added); and
- `All checks passed!` from Ruff.

### Step 6: Record red/green evidence

In your notes, record:

- the failing assertion before the production change;
- the focused passing command afterward;
- the full-suite and lint results; and
- the two files changed.

**Checkpoint:** The strengthened test failed for customer ownership, the
smallest production change made it pass, and the full baseline remains green.

---

## Exercise 3 — Delegate independent maintenance work

**15 minutes**

The incident response is local and urgent. A separate timestamp migration is
well-specified enough to run asynchronously, but you must assess overlap before
delegating it.

### Step 1: Open or create the timestamp issue

If the facilitator supplied an issue named **Replace deprecated naive UTC
timestamps**, open it. Otherwise:

1. Open the repository on GitHub.
2. Select **Issues > New issue**.
3. Use the title `Replace deprecated naive UTC timestamps`.
4. Paste:

```markdown
## Problem

Application code uses `datetime.utcnow()`, which produces naive datetime
values and is deprecated in current Python.

## Acceptance criteria

- Replace application uses with timezone-aware UTC values.
- Preserve existing API field names and response structure.
- Add or adjust focused tests if serialized values change.
- Run the full pytest suite and Ruff.

## Non-goals

- Do not change dependencies.
- Do not change pricing behavior.
- Do not modify generated analytics data.
- Do not standardize unrelated API error behavior.
```

Do not add broader datetime cleanup that the issue cannot verify.

### Step 2: Compare scope before parallelizing

Return to VS Code and ask the `Incident implementation` session:

```text
List the exact files and symbols changed for the incident fix. Then identify
the files and symbols the timezone issue is likely to change. Assess semantic
and merge-conflict risk. Do not edit anything.
```

The timestamp task touches application timestamp creation in storage and
routers. It may share a file with the incident fix even though it changes
different symbols or lines. Record:

- shared files;
- whether the same symbols or behavior are involved;
- whether the local diff is already stable; and
- what you will inspect when integrating.

If your incident work expanded into timestamp-related code, do not delegate
yet. Finish or narrow the incident change first.

### Step 3: Assign the cloud coding agent

GitHub labels and buttons vary by organization:

1. Open the timestamp issue.
2. Use the issue's **Assignees** or **Develop with Copilot** control.
3. Assign the GitHub Copilot coding agent.
4. Confirm that the issue contains the acceptance criteria, non-goals, and
   verification commands before starting.
5. Wait only until GitHub shows that the task was accepted or started.
6. Record the issue or task link.
7. Return to VS Code. Do not repeatedly refresh the cloud task.

If cloud coding agents are unavailable, give the issue to a facilitator or
another attendee to run in a separate coding-agent session. You will review a
prepared fallback pull request in Exercise 5.

**Checkpoint:** The timestamp task is running asynchronously, and you recorded
why its scope is safe enough to proceed alongside the now-bounded incident
change.

---

## Exercise 4 — Practice an evidence-only session handoff

**15 minutes**

A reviewer should not need the implementation session's entire transcript.
Give a fresh session only the problem, investigation artifacts, diff, and test
evidence.

### Step 1: Assemble the handoff packet

Collect:

1. The `INCIDENT-4552` report.
2. Your two-sentence blast-radius statement.
3. The regression-test specification.
4. The current diff:

```bash
git diff -- app/store.py tests/test_orders.py
```

5. The focused test, full-suite, and Ruff results.

Do not include unrelated chat speculation.

### Step 2: Start a reviewer session

1. Select **New Chat**.
2. Select **Ask** or **Plan** mode.
3. Name it `Incident review`.
4. Paste:

```text
Review this customer-isolation change. Do not edit files.

Incident:
<PASTE INCIDENT REPORT>

Confirmed blast radius:
<PASTE BLAST-RADIUS STATEMENT>

Regression-test specification:
<PASTE SPECIFICATION>

Diff:
<PASTE DIFF>

Verification:
<PASTE COMMANDS AND RESULTS>

Review for:
1. whether the test proves every filtered result belongs to the requested
   customer;
2. whether the production change fixes the root cause;
3. whether the change is narrower than the incident requires;
4. whether the evidence is internally consistent; and
5. what remains unverified.

Classify findings as blocking or non-blocking and cite the relevant diff line.
```

### Step 3: Compare the review with your own

Reject generic praise. A useful review must answer:

- Would the test fail if the faulty comparison returned?
- Is the API boundary exercised?
- Is unfiltered behavior preserved?
- Is there any unsupported claim about authorization beyond this endpoint?
- Did the change touch unrelated seams?

If the review finds a real gap, send only that finding back to `Incident
implementation`:

```text
The reviewer found this blocking gap:
<PASTE FINDING>

Verify the finding. If valid, make the smallest correction and rerun the
focused test, full suite, and Ruff. If invalid, respond with file and test
evidence.
```

### Step 4: Prepare for a pull request

Ask `Incident implementation`:

```text
Prepare this branch for a pull request without committing or pushing.
Summarize the incident, root cause, ownership invariant, files changed,
verification results, and remaining risk. Do not include unrelated work.
```

Review the Source Control diff one final time. If your environment permits
opening a PR, use GitHub's PR summary assistance on the actual diff. Do not
merge during the lab.

**Checkpoint:** A fresh reviewer could make a meaningful correctness decision
from the compact handoff packet without access to the implementation chat.

---

## Exercise 5 — Review the asynchronous result

**10–15 minutes**

Review the timestamp task as a human owner. Green checks are necessary but do
not prove scope or compatibility.

### Step 1: Open the result

1. Return to the timestamp issue on GitHub.
2. If Copilot opened a pull request, open it.
3. If it is still running, use the facilitator's fallback PR or pair with
   someone whose task completed.
4. Do not wait or repeatedly poll.

### Step 2: Ask Copilot for an acceptance map

In the PR's Copilot experience, or a new read-only chat with the PR diff
attached, ask:

```text
Review this pull request against the linked timestamp issue.

For each acceptance criterion:
- quote the criterion;
- cite the changed file and behavior that satisfies it;
- cite the test or check that verifies it; and
- mark it satisfied, unsatisfied, or unclear.

Also flag:
- changes to API field names or response structure;
- dependency changes;
- pricing or analytics changes;
- unrelated API error changes; and
- missing focused tests for serialization behavior.

Do not propose additional refactors.
```

### Step 3: Perform the acceptance review

Check the PR yourself:

- Every application use of `datetime.utcnow()` in scope is addressed.
- Replacement datetimes are timezone-aware UTC.
- Response field names and structures are unchanged.
- Dependency files did not change.
- Pricing and generated analytics files did not change.
- The full test suite and Ruff ran.
- Any serialization change is intentional and tested.

### Step 4: Leave an accept or revise comment

Use one of these patterns.

Accept:

```text
Accepted against the issue criteria. The PR replaces the in-scope naive UTC
creation points, preserves response structure, stays within the stated
non-goals, and includes passing test and lint evidence.
```

Revise:

```text
Revision requested. Acceptance criterion "<QUOTE>" is not yet demonstrated.
Please add or correct <SPECIFIC EVIDENCE OR CHANGE> and rerun the focused
tests, full suite, and Ruff. Do not expand into unrelated API behavior.
```

Do not merge merely because checks are green.

**Checkpoint:** You made and documented a human acceptance decision on
asynchronously produced work.

---

## Done

You are finished when you can show:

- [ ] A green baseline and an API-level reproduction of the escaped behavior.
- [ ] Two independent investigation sessions with distinct objectives.
- [ ] A regression test that fails on ownership rather than result count.
- [ ] A minimal production fix with focused, full-suite, and lint evidence.
- [ ] A compact investigation-to-implementation-to-review handoff.
- [ ] A parallelism decision for the timestamp task.
- [ ] An accept or revise decision on the asynchronous result.

## If you get stuck

| Problem | Recovery |
|---|---|
| The API reproduction returns only the requested customer | Do not create a defect. Ask for the prepared incident fixture or saved reproduction. |
| Copilot edits during investigation | Reject the edit and restate the read-only instruction. |
| The new regression test passes before the fix | Confirm the intended fixture with the facilitator; do not weaken the assertion. |
| The test fails for setup or syntax rather than ownership | Fix the test setup before touching production code. |
| The incident change grows into a refactor | Revert only the proposed expansion and restate the narrow ownership invariant. |
| Cloud agent access is unavailable | Use a separate local session or the prepared fallback PR. |
| The cloud task is still running | Stop polling and review the fallback result. |
| The reviewer gives only a summary | Ask for blocking/non-blocking findings with diff evidence. |

## Own-repository variant

Use a real production report or support escalation that lacks a reliable
reproduction. Remove customer data and credentials before sharing context.
Choose a second maintenance task only after comparing file, symbol, contract,
and migration scope. Do not manufacture a failure the existing suite would
already catch, and do not delegate unresolved security or product decisions.
