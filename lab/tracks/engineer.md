# Track: Senior / Staff Engineer

**Duration:** 75–80 minutes
**Surfaces:** VS Code sessions, local coding agent, GitHub cloud coding agent
**Outcome:** Resolve a green-CI customer-isolation incident while safely running
independent maintenance work in parallel.

---

## Scenario

`INCIDENT-4552` reports that filtering orders for `cust-001` returns an order
owned by `cust-002`. The suite passes. Treat this as an escaped
customer-isolation defect, not a toy failing-test exercise.

## Exercise 1 — Triage with parallel sessions

**15 minutes**

Run the baseline:

```bash
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
```

Create two sessions.

### Session A — reproduction

Select a planning/read-only agent:

> Investigate INCIDENT-4552 without editing files. Trace the filtered orders
> request from HTTP route to storage. Produce a minimal API-level reproduction
> and identify the existing test that should have caught it.

### Session B — blast radius

> Treat INCIDENT-4552 as a possible customer-isolation defect. Find every path
> that fetches or filters orders by customer. Report ownership safeguards,
> affected endpoints, and relevant tests. Do not edit files.

Compare results. Resolve contradictions by asking each session for file and
symbol evidence.

**Deliverable:** a reproduction and a bounded blast-radius statement.

## Exercise 2 — Strengthen verification before fixing

**20 minutes**

Ask Session A to specify a regression test that verifies ownership, not merely
result count.

Hand that specification to a new coding-agent session:

> Add the ownership regression test only. Run it and stop after proving it fails
> for the reported behavior. Do not edit production code yet.

Inspect the failure. Then continue:

> Make the smallest production change that satisfies the ownership invariant.
> Run the focused test, full suite, and Ruff. Show the diff and identify any
> customer-isolation risk not covered by this fix.

Review:

- The test would fail if `!=` returned.
- Every filtered result belongs to the requested customer.
- The implementation change is narrow.
- Unrelated seeded defects remain untouched.

**Deliverable:** red/green evidence and a reviewed diff.

## Exercise 3 — Delegate independent work

**15 minutes**

Create or use an issue for replacing `datetime.utcnow()` with timezone-aware
UTC values. Include:

- Exact scope.
- Compatibility concerns.
- Explicit exclusions.
- Required test and lint commands.

Before delegating, compare its file scope with the incident fix. If your local
work still touches the same files, explain why the tasks are not safe to run in
parallel and narrow or postpone one.

Delegate the maintenance issue to the cloud coding agent. Stop watching it and
continue to Exercise 4.

**Deliverable:** an asynchronously running task with a defensible parallelism
decision.

## Exercise 4 — Practice session handoffs

**15 minutes**

Open a fresh reviewer session and give it only:

- The incident issue.
- The investigation summaries.
- The local diff.
- The test output.

Ask:

> Review this change for correctness and scope. Do not edit. Identify whether
> the regression test proves customer ownership, whether the implementation
> fixes the root cause, and what remains unverified.

Compare the review with your own. Send one follow-up back to the implementation
session if needed.

Then ask the implementation session to prepare the branch for a pull request.
Use GitHub's PR summary assistance on the actual PR rather than generating a PR
description in the terminal.

**Deliverable:** a clean investigation → implementation → review handoff.

## Exercise 5 — Review the cloud result

**10–15 minutes**

If the cloud task has completed, review:

- Acceptance-criterion coverage.
- Timestamp serialization changes.
- Dependency or API changes outside scope.
- Test and lint evidence.

If it has not completed, review the facilitator's prepared fallback PR or pair
with someone whose run has completed.

Leave an accept/revise comment. Do not merge merely because checks are green.

**Deliverable:** a human decision on asynchronously produced work.

## Done

You are done when you can show:

- Why CI was green while behavior was wrong.
- Two independent investigation sessions with distinct jobs.
- A regression test that verifies the missing invariant.
- A local agent handoff and review.
- An independent cloud task with an explicit acceptance decision.

## Own-repository variant

Use a production report or support escalation that lacks a reliable
reproduction. Choose a second, non-overlapping maintenance task for cloud
delegation. Do not manufacture a failure the existing suite would already
catch.
