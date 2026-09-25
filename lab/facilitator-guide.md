# Facilitator Guide

**Lab runtime:** 90 minutes
**Track work:** 75–80 minutes
**Shared debrief:** 10 minutes

---

## What changed

The lab no longer teaches isolated prompts or contrived failures. Each track
completes one realistic workflow using the same Orders Service backlog.

The key Engineer scenario is deliberately green in CI: the customer-filter test
checks only result count, so the wrong customer's order still satisfies it.
Do not “fix the baseline” before attendees begin.

## Room setup

Seat by track. Four workflows run concurrently.

| Track | Primary need | Facilitator watchpoint |
|---|---|---|
| Engineer | Multiple sessions and agent handoffs | Do they reproduce before editing? |
| Platform | Customization support | Do boundaries change behavior? |
| Product | Browser repository access | Are decisions kept human-owned? |
| Data | Generated SQLite database | Are writes blocked until reconciliation? |

For rooms above 30, use a second facilitator. Setup and cloud-agent access issues
cluster early.

## Before the session

- [ ] Confirm baseline: 13 tests pass and Ruff is clean.
- [ ] Confirm `INCIDENT-4552` reproduces despite the green suite.
- [ ] Prepare GitHub issues for the timestamp migration and discount boundary.
- [ ] Prepare completed fallback PRs for both cloud tasks.
- [ ] Save example outputs for the Engineer investigation sessions.
- [ ] Prepare a branch with repository instructions and the custom API agent.
- [ ] Confirm the custom agent stops on missing refund decisions.
- [ ] Build the analytics database and capture before/after query plans.
- [ ] Confirm the `7113` NULL discount count.
- [ ] Know which attendees lack cloud-agent access.

## Timing

| Clock | Expected state |
|---|---|
| 0:10 | Setup verified; tracks seated |
| 0:25 | First artifact complete |
| 0:45 | Investigation/context phase complete |
| 1:00 | Implementation or customization underway |
| 1:15 | Review/acceptance phase |
| 1:25 | Stop work and begin debrief |

Do not let setup consume the debrief. Pair broken environments with a working
neighbor or use prepared artifacts.

## Opening framing

> The talk showed these workflows in ten minutes each. You have roughly eighty
> minutes because real work includes investigation, decisions, handoffs,
> verification, and review. Your goal is not to finish five prompts. Your goal
> is to complete one workflow you would defend at work.

Then:

> Keep independent questions in independent sessions. Start read-only when you
> do not understand the problem. Delegate only bounded work. Bring evidence to
> the debrief, not an agent's claim that it succeeded.

## Engineer facilitation

### Preserve the surprise

Do not point out the `!=` operator. Let the investigation find it.

If attendees say “tests pass, so the incident is wrong,” ask what invariant the
existing test actually asserts.

### Parallel sessions

The reproduction and blast-radius sessions must have different objectives.
If attendees paste the same broad prompt into both, stop and have them rewrite
one.

### Cloud delegation

The timestamp task is independent only after the incident fix is bounded. Ask
attendees to compare file scope before delegation. If their local agent is also
editing router/store timestamps, the work is not safely parallel.

### Required artifact

A regression test that asserts ownership, not list length.

## Platform facilitation

### Instructions are not the whole exercise

The custom agent must demonstrate:

- One allowed action.
- One prohibited action.
- One missing-decision stop.

A long persona prompt without restrictions or stop conditions is incomplete.

### Refund scenario

Do not provide refund policy. The correct agent behavior is to identify missing
decisions rather than invent them.

### Required artifact

One customization rule that visibly changes or stops behavior.

## Product facilitation

### Protect the bug/decision distinction

The discount boundary is delegatable. Refund policy, customer deletion, and
breaking error semantics are not ready until someone chooses a contract.

If attendees create implementation criteria for an unresolved decision, ask:
“Who chose that behavior, and where is the evidence?”

### PR review

PMs review observable behavior, acceptance, and scope. Redirect anyone trying
to assess Python style.

### Required artifact

One delegatable issue and one decision issue that intentionally cannot be sent
to an agent.

## Data facilitation

### Enforce read-only investigation

The first two exercises must not mutate the database. If attendees add an index
before capturing reconciliation and the query plan, rebuild and restart that
phase.

### Separate symptoms

Slow performance and financial mismatch are not automatically one root cause.
The separate sessions exist to resist premature convergence.

### Preserve the semantic stop

`discount_rate IS NULL` cannot be disambiguated from the data. Let attendees
try, then require an explicit human/data-contract handoff.

### Required artifact

A before/after plan plus unchanged reconciliation, or an explicit
“cannot determine” memo with a named owner.

## Cloud-agent fallback

Cloud completion time is nondeterministic.

1. Attendees should delegate once and continue.
2. Do not poll repeatedly.
3. At review time, use their result if complete.
4. Otherwise use the prepared PR and perform the same acceptance exercise.

The learning objective is routing and review, not waiting for infrastructure.

## Shared debrief

Ask one representative from each track to show the required artifact.

Then ask:

1. What did your first agent/session know, and what was deliberately withheld?
2. Which tasks ran concurrently, and why were they safe to separate?
3. What evidence allowed more autonomy?
4. Where did an agent correctly stop?
5. Which reusable artifact outlives today's task?

Close with:

> The value did not come from putting Copilot everywhere. It came from routing
> work to the right session, agent, and autonomy level—and preserving the human
> decisions that make the result correct.
