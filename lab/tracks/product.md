# Track: Product / Dev-Adjacent

**Duration:** 75–80 minutes
**Surfaces:** GitHub.com, Copilot app, Issues, cloud coding agent
**Outcome:** Convert raw demand into decisions and agent-ready work, then accept
or reject asynchronous output without reviewing code syntax.

---

## Ground rules

- Everything happens in the browser.
- You own problem framing, priority, scope, and acceptance.
- You do not pretend product decisions are implementation details.
- You do not approve a change merely because an agent or check says “done.”

## Exercise 1 — Build a grounded demand map

**15 minutes**

Open `sample-app/FEEDBACK.md` and ask:

> Group the feedback into customer problems, technical risks, and requested
> solutions. Cite every source item. Do not rank or recommend yet.

Then ask:

> Check each theme against the repository. Cite the file and function that
> confirms or contradicts it, and label anything the code cannot answer.

Verify at least three citations yourself.

**Deliverable:** a theme map separating evidence from requested solutions.

## Exercise 2 — Separate bugs from decisions

**15 minutes**

For each theme, classify it:

| Class | Meaning |
|---|---|
| Objective defect | Correct behavior can be stated and verified |
| Product decision | Customer outcome or policy must be chosen |
| Contract decision | Existing consumers may be affected |
| Discovery | More evidence is required before commitment |

Expected examples:

- Discount boundary: objective defect.
- Refund capability: product decision.
- Customer error status: contract decision.
- Customer deletion: retention/cascade decision.
- NULL discount semantics: discovery and data ownership.

Rank the themes using customer impact, urgency, and decision readiness. Push
back on Copilot's ranking with business context it cannot infer.

**Deliverable:** a prioritized, defensible classification.

## Exercise 3 — Write two different kinds of issue

**20 minutes**

Create:

1. An agent-ready issue for the exact discount-boundary bug.
2. A decision issue for refund behavior or customer-error compatibility.

The bug issue needs:

- Evidence.
- Observable acceptance criteria.
- Exact scope and non-goals.
- Verification.

The decision issue needs:

- Options and tradeoffs.
- A named decision owner.
- Compatibility or policy questions.
- Evidence required before implementation.

Ask Copilot to audit both. Reject any implementation language that disguises an
unmade decision.

**Deliverable:** one delegatable issue and one deliberately non-delegatable
decision issue.

## Exercise 4 — Delegate and monitor

**15 minutes**

Assign the objective bug to the cloud coding agent. Continue working rather
than watching it.

Use the remaining time to refine the decision issue or inspect another active
work item. Check the cloud task status once; do not repeatedly poll.

If cloud agents are unavailable, ask an engineer or facilitator to run the
issue in a coding-agent session and open a pull request.

**Deliverable:** asynchronous work in progress plus a useful task completed
while it ran.

## Exercise 5 — Accept against outcomes

**10–15 minutes**

Review the resulting or prepared fallback PR.

Ask:

> Explain the observable behavior change. Map each acceptance criterion to a
> test or diff outcome. Flag behavior outside scope.

Check:

- Exact thresholds.
- One-cent-below behavior.
- Non-goals remained unchanged.
- Customer-visible outcome matches the issue.

Leave an accept/revise comment. Then draft a short stakeholder update describing
what changed, what remains a decision, and what is still in progress.

**Deliverable:** an acceptance decision and stakeholder update.

## Done

You are done when you can explain:

- Which facts came from customers.
- Which facts came from code.
- Which choices came from a human owner.
- Why one issue was safe to delegate and another was not.

## Own-repository variant

Use a real feedback queue and one vague backlog item. Remove sensitive content,
ground claims in a repository you are authorized to access, and keep contract
or policy choices with their human owners.
