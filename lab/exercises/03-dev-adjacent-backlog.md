# Exercise 3 — Fuzzy request to delegated pull request

**Persona:** Dev-adjacent — product manager, business analyst, support lead
**Surface:** github.com + coding agent
**Time:** 20 minutes
**Matrix cell:** Repo holds the context · spans synchronous and asynchronous

---

## The job

Turn a vague request into work engineers don't hate — and then get code to react to, without opening an editor.

A note on the word: these are **dev-adjacent** roles, not "non-technical" ones. "Non-technical" defines people by what they aren't, and it's usually wrong anyway. The PM who knows which service a request lands in is technical. They just don't commit. What they need is real codebase context reachable **without a clone and a build environment** — which is exactly what this surface provides.

> Everything in this exercise happens in a browser. If you open an IDE, you've left the exercise.

---

## The request

Here is your input. It is realistic, which is to say it's bad:

> *"Finance says our invoice totals are off by a few cents sometimes, and somebody complained that the bulk discount didn't apply on a $100 order. Also can we make the API error responses consistent? Support keeps getting confused."*

One sentence. Three unrelated problems. No acceptance criteria. No reproduction. This is what actually arrives.

---

## Step 1 · Ground it in the code (5 min)

On **github.com**, open Copilot chat against your fork and investigate. Don't decompose yet — find out what's true first.

Useful prompts:

```
Where is order pricing calculated in this repo, and what is the logic?
```

```
Is there test coverage for the pricing module?
```

```
How do the orders and customers routers differ in how they return errors?
```

**The beat to notice:** you are getting grounded answers about code you have not cloned. There is no local environment involved. That's the entire value proposition of this surface, and it's why it's the one that actually reaches dev-adjacent roles.

You should be able to confirm three facts before you move on:
1. The discount tiers use a strict `>` comparison
2. `pricing.py` has no tests
3. The two routers use incompatible error conventions

---

## Step 2 · Decompose (6 min)

That one-sentence request is at least three issues. Ask Copilot to break it down — and insist it reference real files and functions, not generic advice.

```
Break this stakeholder request into separate GitHub issues. For each one:
a clear title, the specific file and function involved, acceptance criteria
that could be verified by a test, and a note on whether it's a bug or a
change in behavior. Keep them independently shippable.
```

A good decomposition looks roughly like:

| Issue | Type | Notes |
|---|---|---|
| Discount tier boundary is exclusive | **Bug** | `discount_rate_for` uses `>`, should be `>=` |
| Pricing has no test coverage | **Gap** | Prerequisite for safely fixing the above |
| Rounding truncates instead of rounding | **Bug** | `int()` on float money |
| Unify error responses across routers | **Change** | Breaking API change — needs a decision, not just a fix |

**The distinction that matters:** the first three are bugs with objectively correct answers. The last one is a **decision** — it changes the API contract, and shipping it without a human deciding would be wrong no matter how good the code is.

Sort your issues into those two piles. Only one pile is safe to delegate.

---

## Step 3 · File them (2 min)

Create at least two issues on your fork. Real issues, not drafts.

Make them **agent-ready** — the same thing that makes them new-hire-ready:
- What's wrong, specifically
- Where, by file and function
- How you'd know it's fixed

> An issue that reads "discounts broken, pls fix" is useless to an agent. It's also useless to a human. That's not a coincidence, and it's the most portable lesson in this exercise.

---

## Step 4 · Delegate (4 min)

Pick the **discount boundary bug** — it's small, it has an objectively correct answer, and it's verifiable.

Assign it to the Copilot coding agent.

Then **stop.** Don't watch it. Start step 5 while it works — the whole point of an asynchronous surface is that you go do something else.

> **If your org doesn't have the coding agent enabled:** do this step in IDE agent mode instead and open the PR manually. You'll lose the async lesson but keep the review one.

---

## Step 5 · Review honestly (3 min)

When the PR appears, review it like a colleague's — not like a demo.

- Did it fix the boundary, or paper over it?
- Did it add a test? Does that test actually cover the boundary at exactly `10000`, or only the easy case either side?
- Did it follow **your exercise 2 instructions**?
- Did it touch anything it shouldn't have?

That fourth question is the interesting one. You wrote those instructions twenty minutes ago. **This is where you find out whether they worked.**

Leave a real review comment. Approve it, or request a change and say why.

---

## Track B — your own repo

Find a real request from a stakeholder — a Slack message, a ticket, an email. Something genuinely underspecified.

Run the same five steps: ground it in the code on github.com, decompose into issues that name real files, sort into *bugs* versus *decisions*, delegate one bug, review what comes back.

**The sorting step is the transferable skill.** Most teams delegate decisions by accident, then blame the tool for the outcome.

---

## Done when

- [ ] You answered three questions about the code without cloning it
- [ ] At least two issues exist on your fork with file-level detail and acceptance criteria
- [ ] You sorted them into "bug" and "decision" piles
- [ ] An agent-authored PR exists
- [ ] You left a real review comment on it

---

## Common failure modes

**The decomposition was generic.**
It gave you "improve error handling" instead of "customers.py returns 200 on failure." Push back and require file and function names. Grounded beats fluent.

**The agent fixed the boundary but added no test.**
Extremely common, and exactly why it belonged in your acceptance criteria. Ask for the test as a follow-up and notice how much cheaper that was than catching it in production.

**The PR is wrong in an interesting way.**
Best outcome available. Diagnose *why*: missing context, ambiguous issue, or genuine model error? Those three have completely different fixes, and only one of them is "wait for a better model."

**You delegated the error-response unification.**
Go look at what came back. It probably made a reasonable-looking choice that silently breaks every API consumer. This is the "load-bearing decision with a long half-life" failure mode, live.

---

## The point

Someone with no local environment produced a reviewed pull request from a one-sentence complaint.

Not because the agent is brilliant — but because the work was **routed correctly**: grounded on a surface with repo context, decomposed into verifiable units, sorted so only the safe pile got delegated.

The gap between "I have an idea" and "there is code to react to" collapsed from a sprint to a coffee break. For a lot of organizations *that specific gap* is the real bottleneck, not typing speed.

---

Next: **[Exercise 4 — Review at volume](04-maintainer-review.md)**
