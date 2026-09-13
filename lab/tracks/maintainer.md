# Track: Maintainer / Reviewer / On-Call

**Surface emphasis:** Code review + coding agent + CLI
**Matrix cell:** Repo holds the context · Asynchronous
**5 exercises · ~15 min each · first 3 are core**

You're reviewing more code than you can physically read. Or it's 2am and something is broken. Nobody schedules this work — it arrives.

> **The through-line:** automated review is **triage, not judgment.** It isn't reviewing your code. It's doing the first pass so that when a human shows up, they spend attention on design and correctness instead of "you forgot a null check."

| # | Exercise | Time | Core? |
|---|---|---|---|
| 1 | [Score a review honestly](#1--score-a-review-honestly) | 15 | ✅ |
| 2 | [Triage at volume](#2--triage-at-volume) | 12 | ✅ |
| 3 | [Narrow an incident](#3--narrow-an-incident) | 15 | ✅ |
| 4 | [Write your automation policy](#4--write-your-automation-policy) | 12 | |
| 5 | [Assess release risk](#5--assess-release-risk) | 12 | |

---

## 1 · Score a review honestly

**15 min · Code review**

### Create something worth reviewing

Copy [`lab/fixtures/refund-endpoint.py`](../fixtures/refund-endpoint.py) into `sample-app/app/routers/orders.py`, commit on a branch, push, and open a PR against your fork.

It's ten lines with nine real problems. Don't look them up yet.

### Predict before you look

Request a Copilot review. **While it runs, write down two problems you expect it to catch and one you expect it to miss.**

Commit to predictions first. Otherwise you'll read the findings and think "yes, obviously" about things you'd never have spotted — hindsight bias eats this exercise alive.

### Score it

Sort every comment into three buckets:

| Bucket | Meaning |
|---|---|
| **Caught** | Real problem, correctly identified |
| **Missed** | Real problem, no comment |
| **Noise** | Not worth a human's attention |

<details>
<summary><strong>Answer key — open only after scoring</strong></summary>

1. **No auth check** — anyone can refund any order
2. **`order` can be `None`** — crashes on unknown ID
3. **`float` for money** — codebase uses integer cents everywhere else
4. **Wrong error convention** — returns 200 with an error body; this file raises `HTTPException`
5. **`reason: str = None`** — should be `Optional[str]`
6. **`print` instead of logging** — no audit trail on a *financial* operation
7. **No test**
8. **No idempotency** — double-submit refunds twice
9. **Status set to `cancelled`** — conflates refund with cancellation

Items 1, 3, and 8 are the interesting ones. 1 is the highest stakes. 3 requires codebase context. 8 requires domain reasoning.
</details>

### The question that actually matters

Not *"is it as good as me at my best?"* but:

> **How many of these would I have caught on a Friday afternoon, on my fourth review of the day?**

That's the honest comparison — against the review that would otherwise have happened, not against your idealized self.

**Done when:** every comment is bucketed and you can name one real catch and one real miss.

> **If you did the platform track's exercise 1:** check whether it flagged the error-convention mismatch. That's where your instructions file pays off — or doesn't.

---

## 2 · Triage at volume

**12 min · github.com**

Reviewing isn't the only queue. Open [`sample-app/FEEDBACK.md`](../../sample-app/FEEDBACK.md) — twelve raw items from support, sales, and engineers.

You're not going to fix these. You're going to decide **what deserves a human this week.**

```
Group these into themes. For each, tell me the likely root cause in this
codebase, the blast radius if we change it, and whether fixing it is a
breaking change for API consumers.
```

Then the maintainer's question, which is different from the PM's:

```
Which of these can be fixed safely without a design discussion, and which
ones change a contract and need a decision first?
```

That split is your week. The first pile can be delegated or batched. The second needs a meeting, and **pretending otherwise is how APIs break.**

Notice: several items share one root cause. Triage that collapses twelve inputs into four causes is worth more than triage that prioritizes twelve tickets.

**Done when:** you can name which items are safe to delegate today and which are blocked on a decision.

---

## 3 · Narrow an incident

**15 min · CLI**

The 2am scenario. The lesson: it's good at **narrowing** and bad at **concluding.**

### Break something

Have someone at your table introduce a subtle bug in `app/` without telling you where. Or use this one: in `app/pricing.py`, change `TAX_RATE` to `0.875`.

### Investigate with evidence, not vibes

Don't paste the repo and ask what's wrong. Feed it signal:

```bash
pytest -q 2>&1 | tail -40 | copilot -p "Diagnose this. Name the file and line before changing anything."
```

```bash
git log --oneline -10 | copilot -p "Which of these commits could plausibly affect order totals?"
```

```bash
git diff HEAD~1 | copilot -p "Could this diff explain a 10x error in tax calculation?"
```

### The discipline

Treat the output as a **shortlist, not a verdict.** Check whether the reasoning holds, not just whether the answer is right — on an easy bug the answer is free and the reasoning is where you learn whether to trust it on a hard one.

**Done when:** you found the bug and can say whether the agent's reasoning was actually sound or just lucky.

> **Why reproduction matters:** a failing test is a *specification of wrongness*. Vague production weirdness isn't. Getting to a reproduction is the human's job — and it's the step that converts an unsafe task into a safe one.

---

## 4 · Write your automation policy

**12 min · No tooling — this one's a decision**

You now have evidence from exercises 1–3. Turn it into policy.

Answer three questions for your **actual team**, in writing:

**1. What runs on every PR, automatically?**
The categories where it's consistently right and humans are consistently bored. Be specific — "style and convention violations," not "code review."

**2. What stays human, always?**
Where it was quiet, wrong, or where the stakes make "usually right" unacceptable. Security and contract changes are the usual answers. What are yours?

**3. What's the failure mode you'd worry about, and what would you do about it?**
"People rubber-stamp whatever it approves" is the common one. Is that a real risk on your team? What's the countermeasure — and is it policy, or is it verification infrastructure?

> That third question has a better answer than most people reach for. If your tests and CI catch bad changes, rubber-stamping is survivable. If they don't, that problem **predates Copilot** and no review policy fixes it.

**Done when:** three written answers you'd actually propose to your team on Monday.

This is the most directly actionable output of the whole lab.

---

## 5 · Assess release risk

**12 min · github.com or CLI**

The other half of the maintainer job: deciding whether to ship.

Pick two:

**Risk-assess a diff.**
```bash
git diff main...HEAD | copilot -p "What's the riskiest change here and why? What would you test manually before shipping?"
```

**Generate release notes with a risk section.**
```
Write release notes for these merged changes. Include a section on what
could break for existing API consumers.
```

**Find the untested blast radius.**
```
Which parts of this codebase have the highest ratio of business logic to
test coverage? Where would a bug be most expensive?
```

**Draft the rollback plan.** What would you need to undo this, and how would you know you needed to?

**Done when:** you have a risk assessment you'd attach to a release, including at least one thing you'd verify by hand.

---

## Track B — your own repo

| # | What to use |
|---|---|
| 1 | A real open PR — a focused one, not a 2,000-line refactor |
| 2 | Your actual issue backlog, or the last 20 closed issues |
| 3 | A recent incident you can reconstruct, or a flaky test |
| 4 | Your team, your policy — this one is always Track B |
| 5 | Your next release |

> Automated review on a huge PR produces volume, not signal. That's itself a finding worth knowing, and an argument for smaller PRs that has nothing to do with AI.

---

## Common failure modes

**It caught almost everything and you're suspicious.**
Reasonable. Check whether it caught the *hard* ones — idempotency and status-conflation need domain reasoning, not pattern matching. Mechanical catches are table stakes.

**It generated a lot of noise.**
Usually a context problem, not a tool problem. Noise is what automated review produces when it doesn't know your conventions — an argument *for* the platform track, not against this one.

**It missed the auth check.**
Sit with that. Security is exactly where "it caught most things" is least comforting, and the clearest argument for keeping a human on a defined category rather than trusting a general pass.

**Your team already reviews well and manually.**
Then the value isn't quality, it's **latency.** Review wait time is usually the largest single chunk of dead time in a delivery pipeline, and almost nobody measures it because it's nobody's job.

---

## The point

Review and incident work are asynchronous and interrupt-driven by nature. That makes them a natural fit for async surfaces — and usually the **fastest ROI a team can find**, for the unglamorous reason that nobody was optimizing that queue before.

But notice what determined the quality of what you saw: not the model. **The context.** The same review, run against a repo with written conventions, is a meaningfully different product than one run without them.

Which is this lab's argument, arriving from a fourth direction.
