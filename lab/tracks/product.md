# Track: Product / Dev-Adjacent

**Duration:** 75–80 minutes
**Surfaces:** GitHub.com, GitHub Copilot, Issues, pull requests, cloud coding
agent
**Outcome:** Turn an untriaged feedback queue into evidence-backed product
themes, separate objective defects from human decisions, write one
agent-ready issue, and accept or reject asynchronous output against observable
outcomes.

---

## Who this track is for

Choose this track if you are a product manager, business analyst, support lead,
technical program manager, or another role that shapes work without routinely
editing application code.

You do not need to know Python. You do need to distinguish:

- what a customer reported;
- what the repository confirms;
- what remains uncertain;
- which choices require a human owner; and
- what evidence proves that delegated work is complete.

## Ground rules

- Work in the browser.
- Use only this synthetic repository and feedback.
- Product owns problem framing, priority, scope, decisions, and acceptance.
- Copilot may summarize and investigate; it does not become the decision owner.
- Do not approve work merely because an agent or status check says “done.”
- Do not convert an unresolved policy choice into implementation criteria.

## Before you begin

### 1. Open the repository

1. Sign in to GitHub.
2. Open the `jmassardo/copilot-everywhere` repository or the fork supplied by
   your facilitator.
3. If you will create issues or assign a cloud coding agent, use a fork or
   training repository where you have write access.
4. Open `sample-app/FEEDBACK.md` in a browser tab.
5. Open `sample-app/README.md` in a second tab.

Do not use `sample-app/README.md` as the source of customer demand. It describes
the training fixture and can help verify repository behavior only after you
have mapped the raw feedback.

### 2. Open Copilot

Use the Copilot experience available in your organization:

- Open GitHub Copilot Chat from GitHub.com; or
- Open the Copilot app and attach or select this repository.

Confirm Copilot can answer a repository-grounded question:

```text
What is the purpose of sample-app/FEEDBACK.md? Cite the file.
```

If Copilot cannot access the repository, use a facilitator-provided shared
session or pair with an attendee who has access. Do not paste private
repository content into an unauthorized service.

### 3. Know how to verify a citation

When Copilot cites a file:

1. Open the citation in a new browser tab.
2. Confirm the quoted text or behavior appears in that file.
3. Check that the citation supports the claim, not merely the general topic.
4. Mark unsupported claims as assumptions.

You will verify at least three citations yourself in Exercise 1.

### 4. Know the cloud-agent fallback

Cloud coding agent access varies by organization. If the **Assign to Copilot**
or **Develop with Copilot** control is unavailable, you will still write and
audit the issue. A facilitator or engineer will run it locally, or you will
review a prepared fallback pull request in Exercise 5.

---

## Exercise 1 — Build an evidence-grounded demand map

**15 minutes**

The feedback queue mixes customer problems, requested solutions, engineering
concerns, and guesses about priority. Do not rank it yet.

### Step 1: Ask Copilot to map the raw feedback

With the repository selected, paste:

```text
Read sample-app/FEEDBACK.md.

Group every feedback item into themes. For each item, record:
- source ID or Slack author;
- source type;
- the customer or business problem described;
- any requested solution;
- any stated impact;
- urgency evidence; and
- uncertainty or hearsay.

Separate customer problems from requested solutions and technical risks.
Cite the exact feedback item for every row. Do not rank themes, recommend a
solution, or inspect implementation yet.
```

### Step 2: Review the first-pass map

The map should account for all feedback entries, including repeated refund
requests. Check that Copilot does not:

- treat “add a refund endpoint” as the only possible customer outcome;
- treat a salesperson's explanation for a lost deal as proven causation;
- combine the penny discrepancy with the exact-boundary report without
  evidence;
- turn an engineering warning into a customer promise; or
- omit the customer-isolation incident because it arrived most recently.

If items are missing, ask:

```text
List every source item from FEEDBACK.md exactly once and show which theme
contains it. Do not merge separate evidence into one citation.
```

### Step 3: Ground each theme in repository evidence

Continue:

```text
Now check each theme against the repository.

For each theme:
- cite the relevant file and function or route;
- state what the code confirms;
- state what the code contradicts;
- state what the code cannot answer; and
- label the evidence as customer report, repository fact, or unresolved.

Do not recommend priority or implementation yet.
```

Expected themes include:

- customer isolation;
- discount boundaries and financial reconciliation;
- API error compatibility;
- refund capability;
- timestamp behavior;
- customer deletion and orphaned orders; and
- missing pricing test coverage.

### Step 4: Verify at least three citations yourself

Choose three different themes. Recommended:

1. Open `sample-app/app/pricing.py` and confirm how exact discount thresholds
   are compared.
2. Open both `sample-app/app/routers/orders.py` and
   `sample-app/app/routers/customers.py` and confirm the error conventions
   differ.
3. Open `sample-app/app/store.py` and confirm deleting a customer does not
   define what should happen to existing orders.

Record:

| Claim | Citation | Supported? | What the citation does not prove |
|---|---|---|---|
|  |  | Yes / No |  |

If the current customer-isolation fixture does not reproduce the report,
preserve the support report as incident evidence and mark current-code
reproduction as unresolved. Do not rewrite history or ask Copilot to create a
defect.

### Step 5: Save the demand map

Copy the final map into your lab notes or a draft issue comment. Do not create
issues for every theme. The next exercise decides which items are ready.

**Checkpoint:** Every raw feedback item is represented, customer reports are
separate from code facts, and at least three citations have been manually
verified.

---

## Exercise 2 — Separate objective defects from human decisions

**15 minutes**

Delegation is safe only when “correct” behavior can be stated without the agent
inventing policy.

### Step 1: Apply the classification model

Ask Copilot:

```text
Classify each demand-map theme using exactly one primary class:

1. Objective defect: correct observable behavior can be stated and verified
   from approved evidence.
2. Product decision: a customer outcome or business policy must be chosen.
3. Contract decision: existing consumers may be affected and compatibility
   must be chosen.
4. Discovery: more evidence or data ownership is required before commitment.

For each classification, cite the evidence and list the unanswered question.
Do not turn an unanswered question into an assumption.
```

Use these expected examples to check the answer:

| Theme | Expected primary class | Why |
|---|---|---|
| Exact discount boundaries | Objective defect | Advertised thresholds and current behavior provide a testable mismatch |
| Refund capability | Product decision | Eligibility, partial refunds, limits, and idempotency are not defined |
| Customer endpoint errors | Contract decision | Changing HTTP 200 behavior may break existing consumers |
| Customer deletion | Product/retention decision | Cascade, restriction, archival, and retention are unresolved |
| Analytics `NULL` discount meaning | Discovery | The stored data cannot distinguish all meanings |
| Deprecated naive UTC creation | Objective technical maintenance | Desired timezone-aware UTC behavior is bounded |

If Copilot classifies refund work as an objective defect merely because two
prospects asked for it, correct it:

```text
The demand is evidenced, but which source defines eligible states, partial
refund behavior, maximum amount, idempotency, and authorization? Reclassify if
those choices are not made.
```

### Step 2: Rank with explicit criteria

Create a simple 1–3 scale:

| Criterion | 1 | 2 | 3 |
|---|---|---|---|
| Customer impact | Limited inconvenience | Material workflow or financial impact | Exposure, loss, or widespread breakage |
| Urgency | No time signal | Repeated or growing demand | Active incident or immediate risk |
| Decision readiness | Major policy missing | Some questions remain | Observable outcome is fully specified |

Ask:

```text
Score each theme from 1 to 3 for customer impact, urgency, and decision
readiness. Cite the evidence for each score. Show the three component scores;
do not hide them inside one total. Do not assume revenue, customer count, or
regulatory impact not present in the repository.
```

### Step 3: Add human business context

Copilot cannot infer your organization's risk tolerance or commitments. Change
at least one proposed score and record why. Example:

```text
Raise customer isolation to the highest urgency because our organization treats
cross-customer exposure as an incident regardless of the number of reports.
Preserve the original evidence and mark this as human-supplied business
context.
```

Do not ask Copilot to “choose the final priority.” You own the ranking.

### Step 4: Choose two issue candidates

Select:

1. **Agent-ready:** exact discount-boundary defect.
2. **Decision issue:** refund behavior or customer-error compatibility.

Do not create issues for every theme during this lab.

**Checkpoint:** You can explain which classifications came from evidence and
which priority judgment came from a human owner.

---

## Exercise 3 — Write one delegatable issue and one decision issue

**20 minutes**

The two issues should look intentionally different. One defines observable
implementation outcomes. The other organizes a decision without pretending it
has already been made.

### Step 1: Draft the objective defect issue

Ask Copilot:

```text
Draft a GitHub issue for the exact discount-boundary defect.

Use these sections:
- Problem
- Evidence
- Observable acceptance criteria
- Scope
- Non-goals
- Verification

Requirements:
- Use integer cents.
- Cover exactly 10,000, 20,000, and 50,000 cents.
- Cover one cent below every boundary.
- Require focused pricing tests, the full pytest suite, and Ruff.
- Exclude rounding changes, money-representation changes, API error changes,
  and unrelated refactoring.
- Cite FEEDBACK.md and the relevant pricing function.

Do not prescribe a broad implementation and do not combine the separate
one-penny rounding complaint with this boundary defect.
```

The acceptance table should be equivalent to:

| Subtotal | Expected rate |
|---:|---:|
| `9,999` cents | `0%` |
| `10,000` cents | `5%` |
| `19,999` cents | `5%` |
| `20,000` cents | `10%` |
| `49,999` cents | `10%` |
| `50,000` cents | `15%` |

### Step 2: Audit the bug issue

Ask:

```text
Audit this issue for autonomous implementation readiness.

Check:
- every acceptance criterion is observable;
- thresholds and one-cent-below behavior are explicit;
- no product or compatibility decision is hidden;
- rounding is explicitly excluded;
- verification commands are stated; and
- the scope is small enough for one pull request.

Return blocking gaps only. Do not rewrite the issue unless I approve a gap.
```

Resolve legitimate blocking gaps. Reject suggestions that expand the issue into
rounding, totals-response design, or API compatibility.

### Step 3: Create the bug issue

In your training repository or fork:

1. Select **Issues**.
2. Select **New issue**.
3. Use the title `Apply advertised discounts at exact tier boundaries`.
4. Paste the audited body.
5. Add appropriate repository labels if supplied by the facilitator.
6. Submit the issue.
7. Copy its URL into your notes.

If you do not have write access, keep the complete draft and use the
facilitator's prepared issue for delegation.

### Step 4: Draft the decision issue

Choose refund behavior or customer-error compatibility. The refund example
below is recommended.

Ask Copilot:

```text
Draft a decision issue titled "Define the Orders Service refund contract."

This is not an implementation issue. Use these sections:
- Customer evidence
- Decision to make
- Options and tradeoffs
- Required stakeholders
- Evidence needed
- Decision record
- Explicitly blocked implementation

Include unresolved questions for:
- eligible order states;
- full versus partial refunds;
- maximum refundable amount and cumulative refunds;
- idempotency;
- authorization;
- error behavior;
- audit or retention needs; and
- compatibility expectations.

Name a product owner and payments or finance owner as required decision owners.
Do not choose an option, invent acceptance criteria, or ask an agent to build
the endpoint.
```

### Step 5: Audit the decision issue

Ask:

```text
Audit this decision issue. Flag any sentence that makes an unresolved product,
financial, authorization, retention, or compatibility choice. Confirm that
implementation remains explicitly blocked until named owners record a
decision.
```

Create the issue if you have access, or save the draft. Apply a
facilitator-provided `needs-human` or blocked label if available.

### Step 6: Compare the issues

Complete:

| Question | Boundary bug | Refund decision |
|---|---|---|
| Is correct behavior known? | Yes | No |
| Can tests prove completion? | Yes | Not until policy is chosen |
| Is a human decision missing? | No material decision | Yes |
| Safe to delegate now? | Yes | No |

**Checkpoint:** You have one implementation-ready issue and one intentionally
non-delegatable decision issue with named owners.

---

## Exercise 4 — Delegate without waiting

**15 minutes**

Delegate only the objective boundary defect. Keep working while it runs.

### Step 1: Final readiness check

Open the boundary issue and confirm:

- exact thresholds are present;
- one-cent-below behavior is present;
- rounding is a non-goal;
- focused and full verification are required; and
- no unresolved product question remains.

If any item is missing, fix the issue before delegation.

### Step 2: Assign the cloud coding agent

GitHub controls vary by organization:

1. Open **Assignees** or **Develop with Copilot** on the issue.
2. Assign the GitHub Copilot coding agent.
3. Confirm GitHub shows the task as queued or in progress.
4. Record the task or issue link.
5. Leave the page.

Do not assign the refund decision issue.

If no cloud-agent control is available, ask a facilitator or engineer to run
the issue in a separate coding-agent session. Continue with the next step.

### Step 3: Do useful work while the task runs

Return to the refund decision issue. Use the remaining time to improve one
area:

- identify the actual product and finance decision owners;
- add evidence from the two refund requests;
- clarify which decision must precede implementation;
- define how the decision will be recorded; or
- separate an authorization question from refund amount policy.

This is the purpose of asynchronous delegation: progress on a different
human-owned task rather than watching the agent.

### Step 4: Check status once

Near the end of the exercise:

1. Return to the boundary issue.
2. Check whether a pull request exists.
3. If it does, open it for Exercise 5.
4. If it does not, stop checking and use the prepared fallback PR.

Do not repeatedly refresh. Cloud completion time is not the learning objective.

**Checkpoint:** Objective work is running asynchronously, the decision issue
remains unassigned, and you improved the decision record while waiting.

---

## Exercise 5 — Accept or reject against customer outcomes

**10–15 minutes**

Review the live or fallback pull request as a product owner. You are not
reviewing Python style.

### Step 1: Read the PR in this order

1. Linked issue.
2. Pull request summary.
3. Changed files overview.
4. Test/check results.
5. Copilot's acceptance map.

If the PR is not ready, use the facilitator's prepared boundary-fix PR.

### Step 2: Ask for an acceptance map

Use Copilot on the PR:

```text
Review this pull request against the linked discount-boundary issue.

Create a table with:
- each acceptance criterion;
- the observable before behavior;
- the observable after behavior;
- the test or diff evidence;
- status: satisfied, unsatisfied, or unclear.

Then flag:
- behavior outside the stated thresholds;
- rounding changes;
- money-representation changes;
- API error changes;
- unrelated refactoring; and
- missing one-cent-below coverage.

Explain outcomes in product language, not Python style.
```

### Step 3: Verify the outcome matrix

Confirm evidence for all six values:

| Subtotal | Required outcome |
|---:|---|
| `9,999` cents | No discount |
| `10,000` cents | 5% discount |
| `19,999` cents | 5% discount |
| `20,000` cents | 10% discount |
| `49,999` cents | 10% discount |
| `50,000` cents | 15% discount |

Also confirm:

- the one-penny invoice rounding complaint was not silently included;
- API response contracts did not change;
- money remains represented in integer cents;
- focused tests exist; and
- the full suite and Ruff are green.

If evidence is unclear, do not infer completion from the PR description. Ask
for the missing test or result.

### Step 4: Leave an acceptance decision

Accept example:

```text
Accepted against the issue outcomes. Exact 10,000, 20,000, and 50,000-cent
boundaries receive the advertised tiers; each one-cent-below case remains in
the lower tier. Rounding, money representation, and API behavior remain
outside this change. Focused and full verification are present.
```

Revise example:

```text
Revision requested. The issue requires observable coverage for <MISSING
BOUNDARY OR NON-GOAL>, but the PR does not yet demonstrate it. Please add that
evidence without expanding into rounding or API changes.
```

Do not approve because “the agent says all criteria pass.”

### Step 5: Draft the stakeholder update

Ask Copilot:

```text
Draft a stakeholder update in 100 words or fewer.

Include:
- what customer-visible boundary behavior changed;
- what verification supports acceptance;
- that the separate rounding concern was not addressed;
- that refund behavior still requires a human decision; and
- the state of any work still in progress.

Do not claim deployment or release unless the repository proves it.
```

Review and correct status language before sharing.

**Checkpoint:** You left an accept or revise decision tied to observable
outcomes and drafted a status update that keeps unresolved decisions visible.

---

## Done

You are finished when you can explain and show:

- [ ] Which facts came from customers or internal stakeholders.
- [ ] Which facts came from repository inspection.
- [ ] Which priority judgment came from a human owner.
- [ ] Why the exact boundary issue was safe to delegate.
- [ ] Why the refund or compatibility issue was not safe to delegate.
- [ ] How every acceptance criterion maps to observable PR evidence.
- [ ] What remains explicitly out of scope or undecided.

## If you get stuck

| Problem | Recovery |
|---|---|
| Copilot omits feedback items | Ask it to enumerate every source item exactly once. |
| A citation does not support the claim | Mark the claim unsupported and request a direct file citation. |
| Copilot combines boundary and rounding defects | Separate them; keep rounding as a non-goal for this issue. |
| Copilot chooses refund policy | Ask which approved source made that decision; move it back to the decision issue. |
| You cannot create issues | Save the complete drafts and use facilitator-prepared issues. |
| Cloud agent access is unavailable | Have an engineer run the issue locally or use the fallback PR. |
| Cloud work is still running | Stop polling and review the fallback PR. |
| The PR summary says “done” but evidence is missing | Request the specific boundary or non-goal evidence. |
| Review drifts into code style | Return to observable behavior, scope, compatibility, and checks. |

## Own-repository variant

Use a real feedback queue and one vague backlog item only in a repository you
are authorized to access. Remove customer names, credentials, and sensitive
content. Require direct links for claims, preserve uncertainty, and keep
contract, policy, retention, authorization, and financial choices with their
accountable human owners.
