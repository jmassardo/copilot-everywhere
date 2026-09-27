# Track: Platform / Developer Experience Lead

**Duration:** 75–80 minutes
**Surfaces:** VS Code, GitHub Copilot Chat, repository instructions, custom
agents, path-scoped instructions, pull requests
**Outcome:** Turn undocumented Orders Service conventions into a small,
testable paved road that helps Copilot make safe changes and stop when a human
decision is missing.

---

## Scenario

The Orders Service contains:

- two incompatible API error conventions;
- money represented in integer cents in application code;
- deprecated naive UTC timestamp creation;
- no documented refund, retention, or authorization policy; and
- no repository-level Copilot customization.

Autonomous work is beginning to arrive through pull requests. Your job is not
to repair one endpoint. Your job is to encode durable engineering standards,
bound an API-maintenance agent, and prove that the paved road changes behavior.

## Before you begin

### 1. Open the repository

1. Open VS Code.
2. Select **File > Open Folder**.
3. Open the `copilot-everywhere` repository.
4. Confirm the Explorer shows `sample-app`, `lab`, and `talk`.
5. Select **Terminal > New Terminal**.
6. Change to the application:

```bash
cd sample-app
```

### 2. Create a lab branch

Run:

```bash
git branch --show-current
```

If the result is `main`, create a branch:

```bash
git switch -c lab/platform-paved-road
```

The customization files in this lab belong at the repository root under
`.github/`, not under `sample-app/.github/`.

### 3. Verify the baseline

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

If the baseline is red, ask the facilitator for a clean branch before adding
customization.

### 4. Confirm customization support

1. Open Copilot Chat from the Activity Bar.
2. Confirm you can start a **New Chat**.
3. Open the mode or agent picker near the chat input.
4. Look for an option such as **Configure Custom Agents**, **Manage Agents**, or
   **Agent Customizations**.

The exact label varies by VS Code and GitHub Copilot version. If no
customization option appears, you can still create the Markdown files manually
in the paths specified below. If the custom agent does not appear after saving,
use **Developer: Reload Window** from the Command Palette.

### 5. Understand the three customization layers

| Layer | File | Purpose |
|---|---|---|
| Repository-wide instructions | `.github/copilot-instructions.md` | Durable standards for all relevant Copilot work |
| Custom agent | `.github/agents/orders-api-maintainer.agent.md` | A selectable, bounded mode of work |
| Path-scoped instructions | `.github/instructions/tests.instructions.md` | Guidance that applies only to matching files |

Do not copy the completed examples from `talk/demo-assets/platform/`. Those are
facilitator fallbacks. Build and test the customizations during the lab.

---

## Exercise 1 — Audit whether the repository is agent-ready

**15 minutes**

First observe what a normal agent does without durable instructions. The
request is intentionally under-specified: there is no approved refund policy.

### Step 1: Start a normal planning session

1. Open Copilot Chat.
2. Select **New Chat**.
3. Select the normal **Agent** or **Plan** mode, not a custom agent.
4. Name the session `Unconfigured refund planning` if possible.
5. Paste:

```text
Plan how to add a refund endpoint following this repository's conventions.

Inspect the application and tests. Identify the route, model, storage, and test
changes you would make. Plan only: do not edit files and do not run destructive
commands.
```

Do not add refund rules to the prompt. The point is to expose what the
repository fails to tell an agent.

### Step 2: Record every assumption

Read the plan and create a table in your notes:

| Topic | What the agent assumed | Repository evidence | Classification |
|---|---|---|---|
| Error response |  |  |  |
| Eligible order status |  |  |  |
| Full or partial refunds |  |  |  |
| Maximum refundable amount |  |  |  |
| Idempotency |  |  |  |
| Money representation |  |  |  |
| Authorization |  |  |  |

For each assumption, use one classification:

- **Inferable and consistent:** repository evidence points to one durable rule.
- **Conflicting precedent:** the repository contains incompatible examples.
- **Missing product decision:** customer behavior or policy has not been
  chosen.
- **Missing engineering standard:** the team may know a rule, but the
  repository does not state it reliably.

### Step 3: Inspect the conflicting evidence

Open these files side by side:

- `sample-app/app/routers/orders.py`
- `sample-app/app/routers/customers.py`
- `sample-app/app/models.py`
- `sample-app/app/pricing.py`

Look for:

- Orders errors raised as `HTTPException` with non-2xx status and structured
  `code` and `message`.
- Customer errors returned as plain dictionaries with HTTP 200.
- Application money fields ending in `_cents`.
- Timestamp creation using `datetime.utcnow()`.
- No application refund route or refund policy.

Ask the session:

```text
For each assumption in your plan, cite the exact file and symbol that supports
it. If the repository has conflicting examples or no evidence, label the
assumption unresolved instead of choosing one.
```

### Step 4: Identify customization candidates

Use this decision rule:

- Encode a rule only if it is durable, broadly applicable, and already owned by
  engineering.
- Do not encode refund eligibility, limits, idempotency behavior, retention,
  or authorization because those decisions are missing.
- Preserve existing customer endpoint behavior as a compatibility concern; do
  not silently standardize it.

**Checkpoint:** You have a gap list that distinguishes conflicting precedent,
missing policy, and durable standards. No files have changed.

---

## Exercise 2 — Write and prove repository-wide instructions

**15 minutes**

Repository instructions should be short enough to be followed and specific
enough to change behavior.

### Step 1: Ask Copilot to draft the file

Create a new Copilot Chat session named `Repository instructions`, select
**Agent**, and paste:

```text
Create .github/copilot-instructions.md at the repository root.

Keep it concise and include only these durable Orders Service standards:
- New API errors use FastAPI HTTPException with an appropriate non-2xx status.
- Structured error details have stable code and human-readable message fields.
- Existing customer endpoint error behavior is a compatibility concern and
  must not be changed without an approved contract decision.
- Application money uses integer cents; do not introduce floating-point money.
- New timestamps are timezone-aware UTC.
- Do not invent refund, retention, authorization, or compatibility policy.
- Before completion, run focused tests, the full pytest suite, and Ruff, and
  report exact commands and results.

Do not add product decisions. Do not edit application code.
```

Review the proposed file before accepting it.

### Step 2: Check placement and scope

The resulting path must be:

```text
.github/copilot-instructions.md
```

It must not be:

```text
sample-app/.github/copilot-instructions.md
```

Open the file and remove:

- generic advice such as “write clean code”;
- rules already enforced unambiguously by tooling;
- invented refund behavior; or
- instructions unrelated to this repository.

### Step 3: Start a fresh session

Instructions are evaluated in new chat context.

1. Save the file.
2. Select **New Chat**.
3. Select the normal **Agent** or **Plan** mode.
4. Name it `Instruction verification`.
5. Ask:

```text
Plan a new Orders Service API endpoint that can fail validation.
Do not edit files. State the error shape, money representation, timestamp
expectation, verification sequence, and any decisions that require a human.
Cite the repository instructions you are applying.
```

### Step 4: Verify that the file loaded

Depending on VS Code version, the chat may show a **References**, **Used
context**, or similar section. Confirm it includes
`.github/copilot-instructions.md`.

The response should apply:

- structured non-2xx errors for a new endpoint;
- integer-cent money;
- timezone-aware UTC;
- the focused/full/lint verification sequence; and
- a stop for missing policy.

If the file is not referenced:

1. Confirm it is saved at the repository root.
2. Start another new chat.
3. Reload the VS Code window if necessary.
4. Ask the verification question again.

### Step 5: Prove a measurable difference

Compare the unconfigured refund plan from Exercise 1 with the new response.
Record at least one behavior that changed because of the instructions, such as
refusing to copy the customer router's 200-on-error convention into a new API.

If nothing changed, revise or remove the ineffective instruction. A file that
exists but does not alter behavior is not a successful paved road.

**Checkpoint:** A fresh session references the instruction file and visibly
applies at least one durable standard.

---

## Exercise 3 — Build and test a bounded custom agent

**20 minutes**

The repository instructions apply broadly. The custom agent adds an explicit
role, permitted scope, verification responsibilities, and stop conditions.

### Step 1: Open the custom-agent editor

Use either method supported by your VS Code version:

- Open the agent picker and select **Configure Custom Agents** or
  **Create new custom agent**; or
- Open the Command Palette and search for **Chat: New Custom Agent** or
  **Configure Custom Agents**.

Choose a **workspace** agent so the file is stored in this repository.

If your version has no editor, manually create:

```text
.github/agents/orders-api-maintainer.agent.md
```

### Step 2: Generate the agent

Ask Copilot to create the workspace agent with this request:

```text
Create a workspace custom agent named Orders API Maintainer for safely
maintaining the sample-app Orders Service.

It may:
- read and edit application and test code;
- run focused tests, the full pytest suite, and Ruff.

It must not:
- change dependencies or CI;
- modify analytics fixtures;
- change an existing API contract without an approved decision;
- invent refund, money, authorization, retention, or compatibility policy.

Before editing, it must identify the observable contract and supporting
repository evidence. It must stop and request a decision when required policy
or compatibility rules are missing. It should make the smallest change that
satisfies an approved contract and report files, commands, results, and
remaining risk.
```

### Step 3: Review the agent file

The file should begin with frontmatter similar to:

```yaml
---
name: Orders API Maintainer
description: Safely maintain Orders Service endpoints within approved contracts
user-invocable: true
target: vscode
---
```

Then inspect the body for:

- a before-edit contract check;
- allowed application and test scope;
- dependency, CI, and analytics exclusions;
- stop conditions for missing policy;
- smallest-change language; and
- focused tests, full suite, and Ruff.

Do not rely on a long persona description as a substitute for boundaries.

### Step 4: Make the agent available

1. Save the file.
2. Open a new Copilot chat.
3. Open the agent picker.
4. Select **Orders API Maintainer**.

If it does not appear, reload the VS Code window and reopen the picker.

### Step 5: Test a missing-decision request

Paste:

```text
Add a refund endpoint following this repository's conventions.
```

Expected behavior:

- The agent does not immediately edit.
- It identifies the conflicting error precedent.
- It asks for eligible states, full versus partial behavior, amount limits,
  idempotency, authorization, and compatibility decisions.

If it invents a contract, revise the stop conditions and retest in a new chat.

### Step 6: Test a prohibited request

Start a new chat with **Orders API Maintainer** and paste:

```text
Upgrade FastAPI in requirements.txt and change CI to test the new version.
```

Expected behavior: the agent refuses or stops because dependencies and CI are
outside its permitted scope. It may explain where the task should be routed,
but it must not edit.

### Step 7: Test an allowed request

Start another new chat with the custom agent and paste:

```text
Plan only: add a focused API test proving that deleting a missing order returns
the existing 404 status and structured order_not_found error code. Cite the
existing endpoint contract. Do not edit yet.
```

Expected behavior:

- It identifies the existing `DELETE /orders/{order_id}` behavior.
- It proposes a test in `tests/test_orders.py`.
- It reuses existing fixtures.
- It does not request a new product decision.
- It does not propose unrelated application changes.

**Checkpoint:** The same agent stopped on missing policy, refused prohibited
scope, and planned a permitted change.

---

## Exercise 4 — Add and verify path-scoped test guidance

**15 minutes**

Now add guidance that should activate only when Copilot works on test files.

### Step 1: Create the scoped instruction file

Create:

```text
.github/instructions/tests.instructions.md
```

Add:

```markdown
---
applyTo: "sample-app/tests/**"
---

- Reuse existing fixtures.
- Assert resource ownership when filtering by customer.
- Assert both status and response body for API behavior.
- Keep one observable behavior per test.
```

Save the file.

### Step 2: Run a test-generation task

Start a new chat with **Orders API Maintainer** and paste:

```text
Implement one focused test for the existing behavior of deleting a missing
order: the response must be 404 and the structured detail code must be
order_not_found.

Edit tests only. Reuse existing fixtures. Run the focused test and stop.
```

Before accepting the edit, inspect the chat's references or context list.
Confirm `tests.instructions.md` is included when the test file is in scope.

Review the proposed test:

- It is in `sample-app/tests/test_orders.py`.
- It uses the existing `client` fixture.
- It asserts both status and response body.
- It tests one observable behavior.
- It does not alter application code.

Run:

```bash
.venv/bin/python -m pytest -q tests/test_orders.py
```

The file should now contain one additional passing test.

### Step 3: Prove the scope does not apply elsewhere

Start another new chat and select the normal Agent or the custom agent. Ask:

```text
Plan a documentation-only update to sample-app/README.md explaining the health
endpoint. Do not edit. List the instruction files in your active context.
```

The repository-wide `.github/copilot-instructions.md` may apply. The
test-scoped `.github/instructions/tests.instructions.md` should not be active
for a README-only task.

If the test instructions appear to apply everywhere:

1. Verify the frontmatter delimiter is present.
2. Verify `applyTo` is exactly `"sample-app/tests/**"`.
3. Save the file and retry in a new chat.

### Step 4: Decide where ownership guidance belongs

The scoped instructions say filtered-customer tests must assert ownership.
Discuss:

- Is that merely a testing pattern?
- Or is customer isolation a repository-wide security expectation?

If the team considers it a durable security invariant, add one concise
repository-wide rule such as:

```markdown
- Customer-filtered results must preserve customer ownership; tests must assert
  ownership, not only result count.
```

Do not add it automatically. Record why it belongs at one scope or the other.

**Checkpoint:** The test guidance applied to a test task, did not apply to a
README-only task, and produced a focused passing test.

---

## Exercise 5 — Improve the paved road using asynchronous work

**10–15 minutes**

Use a cloud-agent pull request, such as the prepared timezone migration, as an
external validation of your customizations.

### Step 1: Open the pull request

Use the live cloud-agent result if available. Otherwise open the facilitator's
prepared fallback PR for **Replace deprecated naive UTC timestamps**.

Read:

- the linked issue;
- the changed files;
- test and lint checks; and
- the agent's summary.

### Step 2: Review through the paved-road lens

Ask Copilot on the PR or in a read-only session:

```text
Review this pull request against:
- .github/copilot-instructions.md;
- .github/agents/orders-api-maintainer.agent.md; and
- the linked issue.

For each relevant rule, cite diff or check evidence.
Answer:
1. Would the implementing agent have received the same durable standards?
2. Did the PR cross an agent stop condition?
3. Which checks prove mechanics?
4. Which compatibility or policy decisions still require a human?
5. What change to the instruction or agent boundary would have prevented the
   most important review concern?

Do not edit files.
```

### Step 3: Make one evidence-driven improvement

Choose one finding that is:

- durable across future tasks;
- not already obvious from the repository;
- within engineering ownership; and
- specific enough to change agent behavior.

Edit either the repository instructions or custom agent. Examples include
clarifying that serialized timestamp compatibility must be tested or requiring
the agent to report API representation changes.

Do not encode a one-off implementation detail from this PR.

### Step 4: Retest the revised rule

Start a fresh chat using **Orders API Maintainer** and ask a small planning
question that exercises the revised rule. Confirm the response changes as
intended.

### Step 5: Capture rollout telemetry

Record two measures you would track during a real rollout:

- **Adoption:** percentage of eligible tasks using the custom agent.
- **Outcome:** frequency of review comments about errors, money, timestamps,
  missing policy, or out-of-scope changes.

Avoid measuring only prompt count or chat volume. The paved road should reduce
rework and unsafe assumptions.

**Checkpoint:** A real or fallback PR produced one justified customization
improvement, and a fresh session demonstrated the revised behavior.

---

## Done

You are finished when another attendee can use the repository without you
narrating beside them and can demonstrate:

- [ ] An agent-readiness gap list grounded in repository evidence.
- [ ] Repository-wide instructions that load in a fresh session.
- [ ] A custom agent that stops on missing policy.
- [ ] A prohibited request that the custom agent refuses.
- [ ] An allowed request that remains within scope.
- [ ] Path-scoped instructions that apply only to tests.
- [ ] One evidence-driven customization improvement from PR review.

## If you get stuck

| Problem | Recovery |
|---|---|
| Customization controls are not visible | Create the documented files manually, save, and reload VS Code. |
| Instructions do not appear in context | Verify the root `.github/` path, save, and start a new chat. |
| The custom agent does not appear | Verify the `.github/agents/*.agent.md` path and frontmatter, then reload the window. |
| The refund request causes immediate edits | Strengthen the stop conditions and retest in a fresh session. |
| The prohibited dependency request is accepted | Make the dependency and CI boundary explicit in the agent file. |
| Test guidance applies to non-test work | Correct the `applyTo` frontmatter and restart the session. |
| The instruction file becomes very long | Keep only durable, measurable standards; move role-specific behavior to the agent. |
| Cloud work is unavailable | Use the facilitator's prepared timestamp PR. |

## Cleanup

Do not merge these lab customizations into a shared baseline. If the facilitator
asks you to reset, remove only the files you created during this track:

```text
.github/copilot-instructions.md
.github/agents/orders-api-maintainer.agent.md
.github/instructions/tests.instructions.md
```

Also revert only the focused test you added in Exercise 4. Do not discard other
attendees' work.

## Own-repository variant

Start with recurring review comments that every new hire receives. Encode only
durable standards that engineering already owns. Test the result against an
allowed path, a prohibited path, and a missing-decision path. Treat a
customization as successful only when it measurably changes behavior and
reduces unsafe assumptions.
