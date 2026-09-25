# Track: Platform / Developer Experience Lead

**Duration:** 75–80 minutes
**Surfaces:** VS Code, repository customization, agent picker, pull requests
**Outcome:** Build and validate a paved road for safe Orders Service changes.

---

## Scenario

The repository contains conflicting API conventions, undocumented money and
timestamp rules, and autonomous work arriving through pull requests. Your job
is not to fix one endpoint. It is to make safe behavior repeatable.

## Exercise 1 — Audit agent readiness

**15 minutes**

In a fresh normal-agent session, ask:

> Add a refund endpoint following this repository's conventions. Plan only; do
> not edit.

Record every assumption it makes:

- Error response shape.
- Eligible order states.
- Full versus partial refunds.
- Maximum refundable amount.
- Idempotency.
- Money representation.

Inspect the repository and classify each assumption as:

- Inferable and consistent.
- Conflicting precedent.
- Missing product decision.
- Missing engineering standard.

**Deliverable:** an agent-readiness gap list grounded in repository evidence.

## Exercise 2 — Write durable repository instructions

**15 minutes**

Create `.github/copilot-instructions.md`. Keep it focused on durable standards:

- New API errors use structured `HTTPException` responses.
- Existing customer error behavior is a compatibility concern.
- Application money uses integer cents.
- New timestamps are timezone-aware UTC.
- Required verification commands.
- Existing product decisions must not be invented.

Start a fresh session and confirm the file appears in the context indicator.
Ask a small planning question and verify the response applies the standards.

Remove any instruction that does not measurably change behavior.

**Deliverable:** concise instructions plus evidence they loaded.

## Exercise 3 — Build a bounded custom agent

**20 minutes**

Create `orders-api-maintainer.agent.md`.

The agent should be able to:

- Read and edit application and test code.
- Run focused tests, the full suite, and Ruff.

It should be unable or instructed not to:

- Change dependencies or CI.
- Modify analytics fixtures.
- Change an existing API contract without an approved decision.
- Invent refund policy.

Give it stop conditions for missing monetary, authorization, compatibility, or
retention rules.

Select the custom agent and repeat the refund task.

Expected: it asks for decisions instead of fabricating an endpoint contract.

Test one allowed request and one prohibited request.

**Deliverable:** a custom agent whose boundaries are demonstrated, not merely
documented.

## Exercise 4 — Add path-scoped guidance

**15 minutes**

Create scoped instructions for tests:

```markdown
---
applyTo: "sample-app/tests/**"
---
- Reuse existing fixtures.
- Assert resource ownership when filtering by customer.
- Assert status and response body for API behavior.
- One observable behavior per test.
```

Run one test-generation task and confirm the scoped instructions load. Then run
a non-test task and confirm they do not.

Discuss whether ownership assertions belong only in test guidance or also in
the repository-wide security expectations.

**Deliverable:** proof that guidance activates only in its intended scope.

## Exercise 5 — Validate against asynchronous work

**10–15 minutes**

Review a cloud-agent pull request such as the timestamp migration.

Use your instructions and custom review criteria to answer:

- Would the agent have received the same standards?
- Did the PR cross a stop condition?
- Which checks prove mechanics, and which policy decisions still need humans?
- What rollout telemetry would show whether this paved road improves outcomes?

Revise one instruction or agent boundary based on the review.

**Deliverable:** one evidence-driven customization improvement.

## Done

You are done when another attendee can select your agent and get the intended
safe behavior without you narrating beside them.

## Own-repository variant

Start with the recurring review comments every new hire receives. Encode only
the durable standards, then test them against a real task with an allowed path,
a prohibited path, and a missing-decision path.
