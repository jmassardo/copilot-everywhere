# Exercise 2 — Build the context supply chain

**Persona:** Platform / DevEx lead
**Surface:** Repo configuration (+ MCP if time allows)
**Time:** 20 minutes
**Matrix cell:** Org holds the context

---

## The job

Your output isn't code. It's **leverage** — making the other two hundred engineers faster without sitting next to each of them.

The sample app has a problem that no model upgrade will fix. Look at the two routers:

- `routers/orders.py` raises `HTTPException` with a structured `detail` body
- `routers/customers.py` returns `{"error": ...}` with a **200 status**

Both patterns are in the codebase. An agent pattern-matching this repo has no way to know which one you actually want — so it will guess, and it will be right about half the time.

That's not a capability gap. **That's an unwritten-knowledge gap**, and it's yours to close.

> This exercise produces the configuration that exercises 3 and 4 consume. Don't skip it.

---

## Step 1 · Establish the "before" (4 min)

Before you write any configuration, capture what the agent does *without* it.

In your IDE, in agent mode, ask:

```
Add a GET /orders/{order_id}/status endpoint that returns just the order
status. Follow the conventions already used in this codebase.
```

**Do not accept the change.** You only want to see what it produces.

Record two things:
1. Which error-handling style did it pick — orders-style or customers-style?
2. Did it explain the choice, or just make one?

Compare with the person next to you. If you picked different styles from the same prompt on the same repo, you've just demonstrated the entire problem.

Discard the change.

---

## Step 2 · Write the instructions (6 min)

Create `.github/copilot-instructions.md` in the repo root.

**Scope discipline matters here more than completeness.** You are not documenting the project. You are writing down the decisions an agent cannot infer from the code — and nothing else.

Cover at minimum:

- **The error-handling convention.** Pick one. State that `customers.py` is the deprecated pattern and must not be copied.
- **The verification expectation.** Tests and lint must pass; say which commands.
- **Money handling.** Integer cents, never floats.
- **Timestamps.** Timezone-aware, not `utcnow()`.

Keep it under 40 lines.

> **Resist the urge to write everything.** Every line you add is loaded on every interaction, competing for attention and costing tokens. A 400-line instructions file is usually a monument to a problem somebody solved once. If a line doesn't change what the agent *does*, delete it.

---

## Step 3 · Prove it worked (4 min)

Start a **fresh** session — context from step 1 will pollute the result otherwise.

Run the identical prompt from step 1.

Now check:
- Did it pick the convention you specified?
- Can you see the instructions file being loaded? Most IDEs show a references or context indicator. **Find it.** This is the difference between trusting your configuration and verifying it.

If nothing changed, debug it before moving on — file in the wrong place, wrong filename, or a session that didn't reload. A configuration you *believe* is working but isn't is worse than none, because you'll stop questioning wrong output.

---

## Step 4 · Scope something narrower (3 min)

Repo-wide instructions are the blunt instrument. Add a path-scoped rule that applies only to tests.

Create `.github/instructions/tests.instructions.md`:

```markdown
---
applyTo: "sample-app/tests/**"
---
- Use the existing `client` and `reset_store` fixtures; don't build new ones.
- Assert on status codes and response bodies, not implementation details.
- One behavior per test. Name tests for the behavior, not the function.
```

Ask the agent to add a test for an existing endpoint and see whether the scoped rules apply.

**Why this matters:** path-scoped instructions load *only when relevant*. Same guidance, a fraction of the always-on cost. This is the single most underused piece of the whole system.

---

## Step 5 · MCP (3 min, optional)

If you have an MCP server available — GitHub, a service catalog, observability, anything — wire it up now and ask a question that is unanswerable from the repo alone.

The beat to notice: the same configuration applies in your IDE, your CLI, **and** the cloud agent. Build context once, it propagates everywhere.

If you don't have one handy, skip it. Don't spend exercise 3's time here.

> **Guardrail:** don't connect MCP servers to systems you aren't authorized to connect in a lab setting. If you're unsure, skip this step.

---

## Track B — your own repo

Same five steps. The only real work is step 2, and the question to answer is:

> **What does every new hire on my team get told in code review that isn't written down anywhere?**

That's your instructions file. It's usually three to six things, and you already know all of them.

Then prove it with the before/after in steps 1 and 3, using any task where your team has a real convention.

---

## Done when

- [ ] `.github/copilot-instructions.md` exists and is under 40 lines
- [ ] A path-scoped instructions file exists
- [ ] You ran the **same prompt** before and after and the output changed
- [ ] You found the context indicator and confirmed the file was actually loaded
- [ ] You can explain *why* the output changed

---

## Common failure modes

**Output didn't change.**
Check the filename and path first — that's the usual cause. Then confirm you started a fresh session. Then check whether your instruction was actually *actionable*; "write clean code" changes nothing.

**Output changed, but got worse.**
Genuinely useful result. Your instructions are probably over-specified or contradict something real in the codebase. This is what "instructions are a code artifact that can have bugs" means in practice.

**You wrote 200 lines.**
Cut it to 40. Then notice which 160 lines you didn't miss.

**It followed the convention in new code but didn't fix `customers.py`.**
Correct behavior. Instructions govern what it *writes*, not a mandate to refactor everything it reads. Fixing `customers.py` is a separate, deliberate task — which is exercise 3's raw material.

---

## The point

You just changed the output of an AI system without touching a model, a prompt, or a setting — by writing down something your team already knew but had never recorded.

**The tool didn't change. What it could see did.**

That's layer 2 of the four-layer rollout, and it's the layer most organizations skip entirely on their way from "we bought licenses" to "why isn't this working."

---

Next: **[Exercise 3 — Fuzzy request to delegated PR](03-dev-adjacent-backlog.md)**
