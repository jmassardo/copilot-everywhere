# Copilot Everywhere — Persona Labs

**Duration:** 90 minutes
**Format:** Choose one persona track and complete one connected workflow
**Workbench:** the included `sample-app/` or an equivalent repository you own

---

## Pick one track

| Track | You are | Primary Copilot workflow |
|---|---|---|
| **[Engineer](tracks/engineer.md)** | Senior/staff engineer | Parallel sessions, agent selection, local implementation, cloud delegation |
| **[Platform](tracks/platform.md)** | Platform/DevEx lead | Repository instructions, custom agents, restrictions, rollout validation |
| **[Product](tracks/product.md)** | PM, BA, support lead, TPM | Repository-grounded discovery, issue design, delegation, acceptance |
| **[Data](tracks/data.md)** | DBA, analytics engineer, data scientist | Read-only investigation, parallel hypotheses, reconciliation, bounded change |

Each track is designed to take **75–80 minutes**, plus a **10-minute shared
debrief**. The first exercises establish context; later exercises build on their
artifacts. This is not a collection of five disconnected prompts.

## The shared scenario

Everyone works with the same Orders Service and backlog:

- A customer-isolation incident escaped despite green CI.
- Pricing has uncovered boundary and rounding defects.
- API error behavior is inconsistent.
- Refund requests lack product rules.
- Timestamp code is deprecated.
- The analytics replica is slow, internally inconsistent, and semantically
  ambiguous in places.

The talk shows these workflows in compressed form. The lab gives each persona
time to do the work properly: investigate, make decisions, select an agent,
hand work between sessions, delegate when appropriate, and review evidence.

## Why persona tracks

Copilot should meet people where they work. The lab does the same:

- Engineers do not write release notes as a proxy for using AI.
- PMs do not write unit tests to prove they are “technical.”
- Platform leads create reusable leverage rather than fixing one endpoint.
- Data professionals do not accept a plausible number without reconciliation.

## Schedule

| Clock | Activity |
|---|---|
| 0:00–0:10 | Setup verification and track seating |
| 0:10–0:25 | Exercise 1 |
| 0:25–0:45 | Exercise 2 |
| 0:45–1:00 | Exercise 3 |
| 1:00–1:15 | Exercise 4 |
| 1:15–1:25 | Exercise 5 / workflow closeout |
| 1:25–1:35 | Shared debrief |

For a strict 90-minute slot, begin setup before the official start or shorten
Exercise 5 to its required deliverable.

## Shared operating rules

1. Work on a branch or fork, never directly on `main`.
2. Use synthetic data and non-production systems only.
3. Keep independent questions in independent sessions.
4. Start with read-only/planning agents when the problem is not yet understood.
5. Delegate asynchronously only when scope and verification are explicit.
6. Review outputs at the level your persona owns.
7. A green agent summary is not evidence; point to the test, diff, query plan,
   acceptance criterion, or reconciliation result.

## Setup

Complete [setup.md](setup.md) before the lab.

## Shared debrief

Bring one artifact from your track:

- **Engineer:** the strengthened ownership test and session handoff.
- **Platform:** the instruction or custom-agent rule that changed behavior.
- **Product:** an issue criterion tied to evidence or a decision deliberately
  left undelegated.
- **Data:** a before/after query plan or a question the data could not answer.

Discuss:

1. Which session or agent did you choose first, and why?
2. What work ran concurrently without creating merge or reasoning conflicts?
3. What evidence let you increase autonomy?
4. Where did an agent need to stop for a human decision?
5. Which artifact would your team reuse on Monday?
