# Copilot Everywhere — Lab Syllabus

**Duration:** 90 minutes
**Format:** Pick one persona track. Five exercises, all appropriate to that role.
**Works with:** the included [sample app](../sample-app/) *or* your own repository

---

## Pick your track

You do **one** track, not all four. Choose the one closest to how you actually spend your day.

| Track | You are | Surface emphasis |
|---|---|---|
| **[Engineer](tracks/engineer.md)** | Senior / staff engineer | Copilot CLI |
| **[Platform](tracks/platform.md)** | Platform / DevEx lead | Configuration + MCP |
| **[Product](tracks/product.md)** | PM, BA, support lead, TPM | github.com + coding agent |
| **[Data](tracks/data.md)** | DBA, analytics engineer, data scientist | github.com + CLI + SQL |

Each track has five exercises. The **first three are core** — do those. Four and five exist so fast movers don't run out, and so you have something to take home.

> **Not sure?** Pick the track matching the work you'd most like to get time back on. If you split your week evenly between two, take the one you're *worse* at.

---

## Why tracks instead of a shared sequence

An earlier version of this lab walked everyone through one exercise per persona. It had a fatal flaw: it made product managers write tests and engineers write release notes.

That teaches the wrong lesson twice. The PM concludes this stuff isn't for them. The engineer concludes the PM exercises are filler.

**Copilot's actual claim is that it meets people where they already work.** A lab should do the same. So every exercise in every track is work that persona genuinely does.

---

## What this lab is

The talk argues that most "Copilot doesn't work for this" complaints are **routing mistakes** — the right work sent to the wrong surface. This lab makes you route your own work, five times, in your own role.

Two questions run through every exercise:

1. Which surface does this work belong on?
2. **How would I know if it came back right?**

That second one is the spine. Every exercise has an explicit, checkable *done* condition. If you finish and can't point at evidence, you haven't finished.

---

## Prerequisites

| Requirement | Needed for |
|---|---|
| GitHub account with Copilot enabled | All tracks |
| Access to github.com | All tracks |
| Copilot CLI, installed and authenticated | **Engineer**, Data |
| IDE with Copilot agent mode | **Platform**, Engineer, Data |
| Python 3.11+ | Sample app and the analytics database |
| A SQLite client | **Data** only |
| A repo you can open PRs against | Own-repo track only |

Full setup: **[setup.md](setup.md)**. Do it **before** the lab — in-class setup is 10 minutes, and that's verification time, not install time.

> **The product track needs the least.** If you're a PM, a browser and a GitHub account carry you through all five exercises. That isn't a limitation of the track — it's the point of it.

---

## Choose your material

### Track A — the sample app
A small FastAPI orders service with deliberately seeded problems: an ambiguous error convention, an untested pricing module with a real boundary bug, a deprecated API used across several files, twelve unsorted customer complaints, and no Copilot configuration at all.

It also ships an **analytics replica** — a 50,000-order SQLite database with orphaned rows, duplicate customers, seven spellings of four statuses, missing indexes, and a NULL whose meaning nobody recorded.

Pick this if you can't use company code in a lab, want predictable results, or want to compare with your neighbor.

### Track B — your own repo
Every exercise has a "**Your repo**" variant describing the *shape* of work to find. Better learning, messier failure modes. Both are true at once.

> **Guardrail:** work on a branch, don't point agents at production config, and don't wire MCP servers to systems you aren't authorized to connect. If you have to think about whether it's okay, use Track A for that exercise.

---

## Schedule

| Time | Block |
|---|---|
| 0:00 | [Setup & baseline verification](setup.md) |
| 0:10 | Exercise 1 |
| 0:25 | Exercise 2 |
| 0:40 | Exercise 3 |
| 0:55 | Exercise 4 *(or go deeper on 1–3)* |
| 1:10 | Exercise 5 *(or go deeper on 1–3)* |
| 1:22 | Debrief — **all tracks together** |

Timings are per-track guidance; exercises run 12 to 18 minutes. **Three finished properly beats five rushed.**

---

## What each track covers

**[Engineer](tracks/engineer.md)** — cross-cutting migration · characterization tests on untested code · Copilot in a shell pipeline · debugging from a reproduction · packaging it into a reusable agent

**[Platform](tracks/platform.md)** — proving the unwritten-knowledge gap exists · path-scoped instructions · prompt files a colleague can run cold · custom agents with tool restrictions · MCP

**[Product](tracks/product.md)** — answering your own codebase questions · triaging raw feedback into themes · specifying agent-ready issues and sorting bugs from decisions · delegating and accepting against acceptance criteria · release notes and stakeholder comms

**[Data](tracks/data.md)** — reading a schema you inherited · quantifying data quality problems instead of gossiping about them · query plans and the index that's actually needed · migrating without lying about it · analysis you'd defend in a review

---

## Debrief — everyone together

Save 8 minutes. This is the only part where tracks hear each other, and it's where the lab's argument closes.

1. **Round the room by track:** what was the single most useful thing your track did?
2. Where did you spend more time verifying than you'd have spent just doing the work?
3. **For the platform track:** did anyone else's results change because of configuration you wrote?
4. **For the data track:** how was your verification story different from everyone else's — and what did that cost you?
5. What did the tool do *worst* at — and was that a capability limit or a routing mistake?
6. Which of these workflows survives contact with your actual team on Monday, and what has to be true first?

> Questions 3 and 4 are the ones to protect. Question 3 shows context propagating between attendees. Question 4 is where the room discovers that "how much can I delegate" depends on how cheaply you can check the answer — and that it varies enormously by discipline.

---

## If you finish early

- **Run an exercise on a different surface** and compare. The engineer track's exercise 1 in agent mode instead of the CLI is the most instructive swap available.
- **Break your configuration deliberately.** Write an instruction that's subtly wrong and watch an agent confidently propagate it. Experiencing "stale instructions are worse than none" beats hearing it.
- **Try another track's exercise 1.** Fifteen minutes in someone else's shoes is the cheapest empathy in the building.

---

## Facilitators

See **[facilitator-guide.md](facilitator-guide.md)** for track balancing, timing checkpoints, expected failure points, and what to do when someone's environment is broken.
