# Exercise 1 — Cross-cutting change from the terminal

**Persona:** Senior / staff engineer
**Surface:** Copilot CLI
**Time:** 18 minutes
**Matrix cell:** You hold the context · Synchronous

---

## The job

You know exactly what you want. You don't need help thinking. You need the change applied correctly across every file that's affected, and you need to know nothing broke.

This is the CLI's home turf, and the reason is specific: **the CLI is the only surface that composes with the rest of your tooling.** It reads stdin. It writes stdout. It goes in a pipe. Everything else is a destination.

---

## Track A — sample app

### Step 1 · Create the failure (2 min)

The repo currently passes lint. Turn on a rule it can't satisfy.

In `sample-app/pyproject.toml`:

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]   # add "UP"
```

Now confirm you've broken it:

```bash
ruff check .
# expected: 6 errors, all UP045
```

You now have a precise, machine-checkable definition of "done." Hold onto that feeling — it's the whole reason this task is safe to delegate.

### Step 2 · Delegate the fix (6 min)

From `sample-app/`, ask the CLI to fix the violations. Do **not** ask it to run `ruff --fix`; that's a one-liner and you'd learn nothing.

Instead, make it do the work an autofix can't do reliably:

```
Fix all UP045 lint violations in this project. Modernize the Optional[X]
annotations to X | None syntax. Update imports so nothing unused is left
behind. Run ruff check and pytest afterward and confirm both are clean.
```

**Watch for this:** does it run the tests on its own, read the output, and iterate? That's level-4 autonomy. If it just edits and stops, notice that — it means you're supervising more than you thought.

### Step 3 · Verify (3 min)

```bash
ruff check .    # must be clean
pytest -q       # must still be 13 passed
git diff        # read it — do you agree with every change?
```

That third command matters most. The first two tell you it *works*. Only the diff tells you whether you'd have written it that way.

### Step 4 · The composability beat (5 min)

This is the part that distinguishes the CLI from everything else. Pick one:

```bash
# Summarize your own change
git diff | copilot -p "Summarize this diff as a PR description. Note any risk."

# Generate a conventional commit from staged work
git diff --cached | copilot -p "Write a conventional commit message for this."

# Explain recent history to someone joining the repo
git log --oneline -20 | copilot -p "What has this repo been working on lately?"
```

Note what just happened: Copilot became a **component in a pipeline**, not a destination you visit.

### Stretch

Three files still call the deprecated `datetime.utcnow()`. Replace it with a timezone-aware equivalent across `store.py`, `routers/orders.py`, and `routers/customers.py`. Tests must stay green.

Harder version: do it *without* naming the files. Make the CLI find them.

---

## Track B — your own repo

Find work with this shape:

- A lint or type rule you could enable but haven't
- A deprecated API used in three or more files
- A signature change that ripples through callers
- A config or dependency migration touching several packages

Then follow the same four steps: **create a checkable failure → delegate → verify against your own suite → read the diff.**

If your repo spans multiple checkouts, even better — run the CLI from the parent directory and make it work across all of them. That's the case no editor handles well.

---

## Done when

- [ ] `ruff check .` is clean (or your equivalent rule passes)
- [ ] Your test suite is as green as when you started
- [ ] You have read the full diff and agree with it
- [ ] You have piped something into `copilot` at least once

---

## Common failure modes

**It fixed the lint but broke a test.**
Good. This is the exercise working. Feed the failure back rather than fixing it yourself — that loop is the thing you're evaluating.

**It changed more files than you expected.**
Ask it why before you revert. Sometimes it found a real instance you missed; sometimes it wandered. Telling those apart is the skill.

**It claimed success without running anything.**
Very common, and the reason "run the tests and confirm" belongs in your prompt. An agent that reports success it didn't verify is the single most expensive failure mode in this whole space.

**It stalled on a large repo.** *(Track B)*
Your scope was too wide. Narrow to a directory and run again. Scoping is a skill, not a workaround.

---

## The point

You gave an agent real autonomy over multiple files and it was *safe* — not because the model is trustworthy, but because `ruff` and `pytest` told you the truth in under a second.

**Cheap verification is what buys autonomy.** A team with a fast, trustworthy test suite can delegate far more than a team without one, using the identical tool.

That's the prerequisite nobody puts on the rollout plan.

---

Next: **[Exercise 2 — Build the context supply chain](02-platform-context.md)**
