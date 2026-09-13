# Setup & Baseline

**Timebox in class: 10 minutes.** That is only enough time to *verify* a working setup, not build one. Do the install section before you arrive.

---

## First: pick your track

You'll do one [persona track](README.md#pick-your-track), not all four. What you need to install depends on which:

| Track | Needs |
|---|---|
| **Product** | A browser and a GitHub account. That's genuinely it. |
| **Maintainer** | Browser + Copilot CLI (exercise 3 only) |
| **Engineer** | Copilot CLI + an IDE with agent mode + Python |
| **Platform** | IDE with agent mode + Python, MCP optional |

---

## Before the lab

### 1. Copilot access

Active Copilot subscription on your GitHub account. Confirm at [github.com/settings/copilot](https://github.com/settings/copilot).

**All tracks need this.**

### 2. Copilot CLI

**Engineer and Maintainer tracks.** Install and authenticate:

```bash
copilot --version
```

If that fails, follow the [CLI install docs](https://docs.github.com/copilot) and come back. The Engineer track has no fallback without it.

### 3. IDE with Copilot

**Engineer and Platform tracks.** VS Code, a JetBrains IDE, or equivalent — with agent mode available, not just completions. The Platform track needs to show you which context files got loaded.

### 4. Python 3.11+

**Engineer, Platform, and Maintainer tracks** (sample app only).

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

The Product and Maintainer tracks need somewhere to open pull requests. Fork the repo to your own account and work from your fork.

> **Product track:** you only need the fork. You never have to clone or install anything — exercises 1 through 5 all happen in a browser.

---

## Track B — your own repo setup

Pick a repository where **all** of these are true:

- [ ] You understand the code well enough to spot a wrong answer
- [ ] There's a test suite you can run locally, and it currently passes
- [ ] You can push branches and open PRs
- [ ] Nothing in it is so sensitive that you'd hesitate to let an agent read it

Then find your raw material. What you need depends on your track:

| Track | What to find |
|---|---|
| **Engineer** | A lint rule you could enable or a deprecated API in 3+ files; a module with logic and no tests |
| **Platform** | A convention your team enforces socially but never wrote down |
| **Product** | Your real unsorted feedback, and the vaguest request in your backlog |
| **Maintainer** | An open PR, your issue backlog, and a recent incident you can reconstruct |

> If you can't find raw material for an exercise, switch to Track A for that one. Mixing is fine.

---

## Baseline checklist

Run this before the clock starts:

- [ ] You've picked a track
- [ ] `copilot --version` works *(Engineer, Maintainer)*
- [ ] IDE opens the repo and Copilot agent mode responds *(Engineer, Platform)*
- [ ] github.com loads and you can see your fork *(all tracks)*
- [ ] `pytest -q` shows 13 passed *(sample app)*
- [ ] `ruff check .` is clean *(sample app)*
- [ ] Your own test suite passes on a clean checkout *(own repo)*
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
  FEEDBACK.md            12 unsorted support tickets and Slack messages
```

Five things are true about this codebase, and each one matters to at least one track:

1. **The two routers handle errors incompatibly.** Both styles are present, so an agent pattern-matching this repo can't know which one you want. *(Platform, Maintainer)*
2. **`pricing.py` has no tests.** It also has a real boundary bug. *(Engineer, Product)*
3. **`datetime.utcnow()` is deprecated and used in three files.** *(Engineer)*
4. **`FEEDBACK.md` is twelve unsorted complaints**, several sharing one root cause. *(Product, Maintainer)*
5. **There is no Copilot configuration whatsoever.** *(Platform fixes this)*

None of that is accidental.
