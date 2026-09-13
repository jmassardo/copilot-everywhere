# Track: Senior / Staff Engineer

**Surface emphasis:** Copilot CLI
**Matrix cell:** You hold the context · Synchronous
**5 exercises · ~15 min each · first 3 are core**

You know what you want. You don't need help thinking. You need the change applied correctly across every file it touches, and you need to know nothing broke.

> **The through-line:** every exercise below gives you a machine-checkable definition of "done" *before* you delegate. That's not lab hygiene — it's the reason you can safely hand an agent this much autonomy.

| # | Exercise | Time | Core? |
|---|---|---|---|
| 1 | [Cross-cutting migration](#1--cross-cutting-migration) | 15 | ✅ |
| 2 | [Close a test gap on code you didn't write](#2--close-a-test-gap) | 15 | ✅ |
| 3 | [Copilot as a pipeline component](#3--copilot-as-a-pipeline-component) | 10 | ✅ |
| 4 | [Debug from a reproduction](#4--debug-from-a-reproduction) | 15 | |
| 5 | [Make it repeatable](#5--make-it-repeatable) | 15 | |

---

## 1 · Cross-cutting migration

**15 min · CLI**

### Create the failure first

In `sample-app/pyproject.toml`, add `"UP"` to the lint selection:

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

```bash
ruff check .      # 6 errors, all UP045
```

You now have a precise, machine-checkable target.

### Delegate

From `sample-app/`, ask the CLI to fix it. Don't ask for `ruff --fix` — that's a one-liner and teaches you nothing.

```
Fix all UP045 lint violations. Modernize Optional[X] annotations to X | None.
Clean up any imports that become unused. Run ruff check and pytest afterward
and confirm both pass.
```

**Watch for:** does it run the tests itself, read the output, and iterate? That's level-4 autonomy. If it edits and stops, you're supervising more than you thought.

### Verify

```bash
ruff check .     # clean
pytest -q        # still 13 passed
git diff         # read every line — would you have written it this way?
```

**Done when:** lint clean, tests green, and you've read the full diff.

### Stretch
Three files still call deprecated `datetime.utcnow()`. Fix them **without naming the files** — make the CLI find them.

---

## 2 · Close a test gap

**15 min · CLI or agent mode**

`app/pricing.py` handles money and has **zero test coverage.** It also has at least one real bug. You're going to find it by writing tests, not by reading code.

### Characterize before you fix

Ask for tests that describe what the code *currently does* — not what it should do:

```
Write pytest tests for app/pricing.py covering subtotal_cents,
discount_rate_for, and calculate_totals. Cover the tier boundaries exactly
(10000, 20000, 50000) and just above and below each. Assert current
behavior, don't fix anything yet.
```

Run them. They should all pass — they describe reality.

### Now read the boundary tests

```bash
pytest tests/test_pricing.py -v -k boundary
```

Look at what the test asserts for a subtotal of exactly `10000`. The discount rate is `0.0`. The pricing page promises 5% at $100.

**You just found the bug by writing a test that passes.** That's the characterization-test technique, and it's the safest way to touch code you don't own.

### Fix it

Change the assertion to what's *correct*, watch it fail, then fix `discount_rate_for`. Red, green.

**Done when:** `tests/test_pricing.py` exists, the boundary is `>=`, and the full suite is green.

### Stretch
`calculate_totals` truncates with `int()` instead of rounding. Write a test that proves the components don't reconcile with the total, then fix it.

---

## 3 · Copilot as a pipeline component

**10 min · CLI**

This is what distinguishes the CLI from every other surface. It reads stdin and writes stdout. It goes in a pipe.

Run at least three:

```bash
# Your own change, summarized
git diff | copilot -p "Summarize this diff as a PR description. Flag any risk."

# Conventional commit from staged work
git diff --cached | copilot -p "Write a conventional commit message."

# Onboard someone to recent history
git log --oneline -20 | copilot -p "What has this repo been working on lately?"

# Explain a test failure without scrolling
pytest -q 2>&1 | tail -40 | copilot -p "What broke and what's the likely cause?"

# Audit dependencies
cat requirements.txt | copilot -p "Which of these have had recent CVEs? Flag anything I should pin harder."
```

**Done when:** you've piped into `copilot` three times and gotten something you'd actually use.

Everything else in this lab is a destination you visit. **This is a component.**

---

## 4 · Debug from a reproduction

**15 min · CLI**

Agents are excellent at fixing a failing test and bad at "prod is weird." The difference is that a failing test is a *specification of wrongness.* This exercise is about producing one.

### Break something realistically

Have a colleague (or the agent) introduce a subtle bug somewhere in `app/` without telling you where. Alternatively, use this one:

In `app/store.py`, change `list_orders` to filter with `!=` instead of `==`.

### Reproduce first, delegate second

```bash
pytest -q        # you now have a failing test
```

**Do not** paste the whole repo at the agent and ask what's wrong. Give it the reproduction:

```bash
pytest -q 2>&1 | tail -30 | copilot -p "Diagnose this failure. Name the file and line you'd change and explain why before changing anything."
```

**The beat to notice:** it narrows fast and confidently. Check whether its *reasoning* is right, not just its answer — on a bug this small the answer is easy and the reasoning is where you learn whether to trust it on a hard one.

**Done when:** the suite is green and you can explain why the agent's diagnosis was right or wrong.

---

## 5 · Make it repeatable

**15 min · CLI + config**

You've done the same kind of work three times now. Make it a tool.

Pick one:

**A custom agent** scoped to migration work — restricted tools, a specific persona, explicit instructions to always verify with tests before reporting done.

**A prompt file** for your most repeated task: characterization tests, dependency bumps, release notes from a diff.

**A script.** Run the CLI headless over a list of repos or directories and collect the results. This is where the composability from exercise 3 becomes leverage rather than a party trick.

**Done when:** you can invoke it by name and it does the thing without you re-explaining context.

---

## Track B — your own repo

Every exercise maps directly:

| # | What to find |
|---|---|
| 1 | A lint/type rule you could enable, or a deprecated API in 3+ files |
| 2 | A module with real logic and no tests. You have one. |
| 3 | Your own git history and test output — works anywhere |
| 4 | A bug you can reproduce, or a flaky test you've been ignoring |
| 5 | The task you've done manually more than three times this month |

If your repo spans multiple checkouts, run the CLI from the parent directory. That's the case no editor handles well and it's where the CLI earns its keep.

---

## Common failure modes

**It fixed the lint but broke a test.**
The exercise working as designed. Feed the failure back rather than fixing it yourself — that loop is the thing you're evaluating.

**It claimed success without running anything.**
Very common, and the reason "run the tests and confirm" belongs in your prompt. An agent reporting unverified success is the most expensive failure mode in this space.

**It changed more files than expected.**
Ask why before reverting. Sometimes it found a real instance you missed. Telling that apart from wandering is the skill.

**It stalled on a large repo.** *(Track B)*
Scope was too wide. Narrow to a directory. Scoping is a skill, not a workaround.

---

## The point

You gave an agent real autonomy over multiple files and it was safe — not because the model is trustworthy, but because `ruff` and `pytest` told you the truth in under a second.

**Cheap verification is what buys autonomy.** A team with a fast, trustworthy suite can delegate far more than a team without one, using the identical tool. That's the prerequisite nobody puts on the rollout plan.
