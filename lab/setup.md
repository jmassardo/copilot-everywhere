# Setup & Baseline

**Timebox in class: 10 minutes.** That is only enough time to *verify* a working setup, not to build one. Do the install section before you arrive.

---

## Before the lab

### 1. Copilot access

You need an active Copilot subscription on your GitHub account. Confirm at [github.com/settings/copilot](https://github.com/settings/copilot).

### 2. Copilot CLI

Install and authenticate. Exercise 1 is CLI-only and there's no fallback.

```bash
copilot --version
```

If that fails, follow the [CLI install docs](https://docs.github.com/copilot) and come back.

### 3. IDE with Copilot

VS Code, a JetBrains IDE, or equivalent — with agent mode available, not just completions. Exercise 2 needs to show you which context files got loaded.

### 4. Python 3.11+ (Track A only)

```bash
python3 --version
```

> **Known issue:** on Python 3.14, exact-pinned `pydantic` builds from source and fails. This repo floor-pins its dependencies to avoid that. If you hit a Rust/`maturin`/`pyo3` compile error during install, you are almost certainly on an exact-pinned fork — use the `requirements.txt` in this repo as-is.

---

## Track A — sample app setup

```bash
git clone https://github.com/jmassardo/copilot-everywhere.git
cd copilot-everywhere/sample-app

python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Verify your baseline

Everything must be green before you start. If it isn't, fix that first — every exercise uses the test suite as its verification signal, and a red baseline makes every result meaningless.

```bash
pytest -q
# expected: 13 passed

ruff check .
# expected: All checks passed!
```

Optionally, run the service:

```bash
uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs
```

### Fork it

Exercises 3 and 4 need somewhere to open pull requests. Fork the repo to your own account and work from your fork.

---

## Track B — your own repo setup

Pick a repository where **all** of these are true:

- [ ] You understand the code well enough to spot a wrong answer
- [ ] There's a test suite you can run locally, and it currently passes
- [ ] You can push branches and open PRs
- [ ] Nothing in it is so sensitive that you'd hesitate to let an agent read it

Then find your raw material — you'll need one of each:

| Exercise | What to find |
|---|---|
| 1 | A lint rule you could turn on, or a deprecated API used in 3+ files |
| 2 | A convention your team follows that **isn't written down anywhere** |
| 3 | A real feature request vague enough to need decomposition |
| 4 | An open PR, or one you can create |

> If you can't find raw material for an exercise, switch to Track A for that one. Mixing tracks is fine.

---

## Baseline checklist

Run this before the clock starts. Every box checked:

- [ ] `copilot --version` works
- [ ] IDE opens the repo and Copilot agent mode responds
- [ ] github.com loads and you can see your fork
- [ ] Track A: `pytest -q` shows 13 passed
- [ ] Track A: `ruff check .` is clean
- [ ] Track B: your test suite passes on a clean checkout
- [ ] You're on a branch, not `main`

---

## What's in the sample app

Worth two minutes of reading before you start — the exercises assume you've seen this.

```
sample-app/
  app/
    main.py              FastAPI wiring
    models.py            Pydantic models
    store.py             In-memory persistence
    pricing.py           Subtotal, discount, tax
    routers/
      orders.py          Error style A: raises HTTPException
      customers.py       Error style B: returns {"error": ...} with a 200
  tests/
    test_orders.py       7 tests
    test_customers.py    6 tests
```

Four things are true about this codebase, and each one matters later:

1. **The two routers handle errors incompatibly.** Both styles are present, so an agent pattern-matching this repo has no way to know which one you want. (Exercise 2)
2. **`pricing.py` has no tests.** It also has a real bug. (Exercises 3 and 4)
3. **`datetime.utcnow()` is deprecated and used in three files.** (Exercise 1, stretch)
4. **There is no Copilot configuration whatsoever.** No instructions, no prompt files, no MCP. (Exercise 2 fixes this)

None of that is accidental.
