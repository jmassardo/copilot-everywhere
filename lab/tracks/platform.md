# Track: Platform / DevEx Lead

**Surface emphasis:** Configuration artifacts + MCP
**Matrix cell:** Org holds the context
**5 exercises · ~15 min each · first 3 are core**

Your output isn't code. It's **leverage** — making two hundred other engineers faster without sitting next to each of them.

> **The through-line:** every exercise changes what an agent produces *without touching a model, a prompt, or a setting.* You're building the context supply chain, and it's the layer most orgs skip on their way from "we bought licenses" to "why isn't this working."

| # | Exercise | Time | Core? |
|---|---|---|---|
| 1 | [Prove the problem exists](#1--prove-the-problem-exists) | 15 | ✅ |
| 2 | [Scope it down](#2--scope-it-down) | 12 | ✅ |
| 3 | [Package a repeated workflow](#3--package-a-repeated-workflow) | 15 | ✅ |
| 4 | [Build a custom agent](#4--build-a-custom-agent) | 15 | |
| 5 | [Reach outside the repo](#5--reach-outside-the-repo) | 15 | |

---

## 1 · Prove the problem exists

**15 min · Repo instructions**

The sample app has a problem no model upgrade will fix:

- `routers/orders.py` raises `HTTPException` with a structured detail body
- `routers/customers.py` returns `{"error": ...}` with a **200 status**

Both patterns are in the codebase. An agent pattern-matching this repo **cannot know which one you want.** It guesses, and it's right about half the time.

That's not a capability gap. It's an **unwritten-knowledge gap**, and it's yours.

### Capture the "before"

In agent mode, ask:

```
Add a GET /orders/{order_id}/status endpoint returning just the order status.
Follow the conventions already used in this codebase.
```

**Don't accept the change.** Record which error style it picked and whether it explained the choice. Then discard it.

> Compare with the person next to you. If you got different conventions from the identical prompt on the identical repo, you've just demonstrated the entire problem.

### Write the instructions

Create `.github/copilot-instructions.md`. **Under 40 lines.** Cover only what an agent can't infer from the code:

- The error-handling convention — pick one, and state that `customers.py` is deprecated and must not be copied
- Verification expectations — which commands must pass
- Money is integer cents, never floats
- Timestamps are timezone-aware

> Resist writing everything. Every line loads on every interaction, competing for attention and costing tokens. A 400-line instructions file is a monument to a problem somebody solved once. **If a line doesn't change what the agent does, delete it.**

### Prove it

Start a **fresh session** — step 1's context will pollute the result otherwise. Run the identical prompt.

Then find the context indicator in your IDE and confirm the file actually loaded. This is the difference between trusting your configuration and verifying it.

**Done when:** same prompt, different output, and you can point at evidence it was loaded.

---

## 2 · Scope it down

**12 min · Path-scoped instructions**

Repo-wide instructions are the blunt instrument. Path-scoped rules load **only when relevant** — same guidance, a fraction of the always-on cost. This is the single most underused piece of the system.

Create `.github/instructions/tests.instructions.md`:

```markdown
---
applyTo: "sample-app/tests/**"
---
- Use the existing `client` and `reset_store` fixtures; don't build new ones.
- Assert on status codes and response bodies, not implementation details.
- One behavior per test. Name tests for the behavior, not the function.
```

Ask the agent to add a test for an existing endpoint. Check whether the scoped rules applied.

Then ask it to add a *non-test* file and confirm they **didn't**.

**Done when:** you've demonstrated the rules firing in one path and staying silent in another.

### Stretch
Add a second scoped file for `app/routers/**` encoding the error convention. Now ask yourself the design question: should that live in the scoped file, the repo-wide file, or both? Defend your answer.

---

## 3 · Package a repeated workflow

**15 min · Prompt files**

Instructions are passive — always on, shaping everything. Prompt files are **active**: you invoke them for a specific job.

Pick something your team genuinely repeats. Good candidates in this repo:

- Add a new endpoint following house conventions
- Generate characterization tests for an untested module
- Produce release notes from a diff
- Review a PR against a specific checklist

Write the prompt file. Give it a clear name, explicit scope, explicit constraints, and a defined deliverable.

Then **hand it to someone else at your table** and have them run it without explanation.

**Done when:** a colleague invoked it and got a useful result without you narrating.

> That last step is the actual test. A prompt file that only works when its author is standing there isn't leverage — it's a bookmark.

---

## 4 · Build a custom agent

**15 min · Custom agents**

A prompt file is a task. A custom agent is a **mode of work** — a persona plus tool restrictions.

Build one for a real role on your team. Suggestions:

**A migration agent** — may edit source and run tests, may *not* touch CI config or dependencies. Must verify before reporting done.

**A review agent** — read-only. Cannot edit anything. Reports findings against your conventions.

**A test-writer** — may only create files under `tests/`.

The restrictions are the interesting part. Ask yourself: what would I want an agent *unable* to do while it works unsupervised?

**Done when:** the agent runs, and you've confirmed it actually refuses something outside its scope.

---

## 5 · Reach outside the repo

**15 min · MCP**

Your codebase is maybe 40% of the context an engineer needs. The rest — what's broken right now, who owns this service, what was decided in that review, the state of production — is in systems the repo can't see.

MCP is where *"Copilot knows our codebase"* becomes *"Copilot knows our company."*

1. Ask a question that's unanswerable from the repo alone. Watch it fail or hedge.
2. Wire up an MCP server.
3. Ask again.
4. **Confirm the same configuration applies in the IDE, the CLI, and the cloud agent.** Build once, propagates everywhere.

> **Guardrail:** treat every MCP server like a new integration with production data access — because that's what it is. Don't connect systems you aren't authorized to connect in a lab. If you're unsure, skip this and do the stretch on exercise 2 instead.

**Done when:** the agent answered something it demonstrably couldn't answer fifteen minutes earlier.

---

## Track B — your own repo

The only exercise that needs real thought is the first one, and the question is:

> **What does every new hire get told in code review that isn't written down anywhere?**

That's your instructions file. It's usually three to six things and you already know all of them.

| # | What to find |
|---|---|
| 1 | A convention your team enforces socially but never documented |
| 2 | A directory with rules that don't apply elsewhere — tests, migrations, infra |
| 3 | The task your team does most often by hand |
| 4 | A job you'd want done with restricted permissions |
| 5 | The internal system Copilot most needs to see |

---

## Common failure modes

**Output didn't change in exercise 1.**
Filename and path first — that's the usual cause. Then a fresh session. Then ask whether your instruction was *actionable*; "write clean code" changes nothing.

**Output changed and got worse.**
Genuinely useful result. Your instructions are over-specified or contradict something real in the codebase. This is what "instructions are a code artifact that can have bugs" means in practice.

**You wrote 200 lines.**
Cut to 40. Then notice which 160 you didn't miss.

**It followed the convention in new code but didn't fix `customers.py`.**
Correct behavior. Instructions govern what it *writes*, not a mandate to refactor everything it reads.

---

## The point

You changed the output of an AI system without touching a model, a prompt, or a setting — by writing down something your team already knew but had never recorded.

**The tool didn't change. What it could see did.**

And notice the failure mode you *didn't* hit: none of this required a bigger budget, a better model, or a vendor conversation. It required someone to own it. **If nobody owns the context supply chain, it doesn't exist.**
