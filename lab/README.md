# Copilot Everywhere — Lab Syllabus

**Duration:** 90 minutes
**Format:** Hands-on, four exercises, one per persona
**Works with:** the included [sample app](../sample-app/) *or* your own repository

---

## What this lab is

The talk argues that most "Copilot doesn't work for this" complaints are **routing mistakes** — the right work sent to the wrong surface. This lab makes you do the routing yourself, four times, as four different people.

You will not use the same surface twice.

## What this lab is not

Not a prompt-writing workshop. Not a tour of every feature. You will spend most of your time on two questions:

1. Which surface does this work belong on?
2. **How would I know if it came back right?**

That second question is the spine of the whole lab. Every exercise below has an explicit, checkable *done* condition — a passing test, a lint result, a diff you can read. If you finish an exercise and can't point at evidence, you haven't finished it.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| GitHub account with Copilot enabled | Any paid tier |
| Copilot CLI installed and authenticated | Exercise 1 is CLI-only |
| An IDE with Copilot (VS Code or equivalent) | Agent mode available |
| Access to github.com | Exercises 3 and 4 |
| Python 3.11+ | Only if using the sample app |
| A repo you can open PRs against | Only if using your own repo |

Full setup and verification steps: **[setup.md](setup.md)**. Do this *before* the lab starts — setup is timeboxed to 10 minutes and it is not enough time to install from scratch.

---

## Choose your track

Every exercise works two ways. Pick one at the start and stay with it.

### Track A — the sample app
A small FastAPI orders service with deliberately seeded problems: an inconsistent error-handling pattern, an untested pricing module with a real boundary bug, a deprecated API used across several files, and no Copilot configuration of any kind.

Choose this if you can't use company code in a lab, you want predictable results, or you want to compare outcomes with the person next to you.

### Track B — your own repo
Every exercise lists a "**Your repo**" variant describing the *shape* of work to find rather than the exact task.

Choose this if you have a repo you know well and can open PRs against. The learning is better. The failure modes are messier. Both of those are true at once.

> **Track B guardrail:** work on a branch, don't run agents against production config, and don't wire MCP servers to systems you aren't authorized to connect. If you have to think about whether it's okay, use Track A for that exercise.

---

## Schedule

| Time | Block | Persona | Surface |
|---|---|---|---|
| 0:00 | [Setup & baseline](setup.md) | — | — |
| 0:10 | [Exercise 1](exercises/01-staff-engineer-cli.md) | Senior / staff engineer | **CLI** |
| 0:28 | [Exercise 2](exercises/02-platform-context.md) | Platform / DevEx lead | **Context config** |
| 0:48 | [Exercise 3](exercises/03-dev-adjacent-backlog.md) | Dev-adjacent (PM / BA) | **github.com + coding agent** |
| 1:08 | [Exercise 4](exercises/04-maintainer-review.md) | Maintainer / reviewer | **Code review + PR** |
| 1:23 | Debrief | — | — |

Exercises are ordered deliberately. Exercise 2 produces the configuration that exercises 3 and 4 consume — you will watch your own context work change the agent's output. **Don't skip 2.**

---

## The exercises

### 1. Cross-cutting change from the terminal
*Senior / staff engineer · 18 min · CLI*

Turn on a lint rule that the codebase doesn't currently satisfy, then use the CLI to fix the fallout across every affected file. Use the test suite as the verification signal.

**Done when:** `ruff check .` is clean and all tests still pass.

### 2. Build the context supply chain
*Platform / DevEx lead · 20 min · Configuration + MCP*

The repo has no Copilot configuration. Write repo instructions that encode a convention the codebase itself contradicts, then prove the configuration changed the output. Optionally wire an MCP server.

**Done when:** you can show the same prompt producing different output before and after, and explain why.

### 3. Fuzzy request to delegated pull request
*Dev-adjacent · 20 min · github.com + coding agent*

Start from a vague stakeholder request. Decompose it into issues grounded in the actual codebase, then assign one to the coding agent and review what comes back.

**Done when:** an agent-authored PR exists and you have written a real review of it.

### 4. Review at volume
*Maintainer / reviewer · 15 min · Code review*

Review the PR from exercise 3 — plus a deliberately flawed one. Find what the agent review caught, what it missed, and decide what your team would actually automate.

**Done when:** you can name one thing the automated review caught and one thing it missed.

---

## Debrief questions

Save 7 minutes. These are the questions worth arguing about:

1. Which exercise did the tool do best on, and what did that task have in common with the others it struggled with?
2. Where did you spend more time verifying than you would have spent just doing the work?
3. What did exercise 2's configuration change about exercises 3 and 4? Was it worth writing?
4. Which of these four workflows would survive contact with your actual team on Monday — and what would have to be true first?
5. What's the first thing you'd automate at home, and how would you know it was working?

---

## If you finish early

- Run the same exercise on a *different* surface and compare. Exercise 1 in agent mode instead of the CLI is the most instructive.
- Deliberately break your exercise 2 instructions — write a convention that's wrong — and watch the agent confidently propagate it. This is the "stale instructions are worse than no instructions" lesson, and experiencing it is worth more than hearing it.
- Try exercise 3's decomposition from the Copilot mobile app.

---

## Facilitators

See **[facilitator-guide.md](facilitator-guide.md)** for timing checkpoints, expected failure points, room-management notes, and what to do when someone's environment is broken.
