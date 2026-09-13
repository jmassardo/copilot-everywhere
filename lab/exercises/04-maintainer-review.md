# Exercise 4 — Review at volume

**Persona:** Maintainer / reviewer / on-call
**Surface:** Code review
**Time:** 15 minutes
**Matrix cell:** Repo holds the context · Asynchronous

---

## The job

You are reviewing more code than you can physically read. Nobody schedules this work — it arrives.

The framing that makes this useful: **automated review is triage, not judgment.** It is not reviewing your code. It's doing the first pass so that when a human arrives, they spend attention on design and correctness instead of "you forgot a null check."

---

## Step 1 · Create something worth reviewing (4 min)

You need a PR with real problems in it. Open one deliberately.

On a new branch, add this to `sample-app/app/routers/orders.py`:

```python
@router.post("/{order_id}/refund")
def refund_order(order_id: str, amount: float, reason: str = None):
    order = store.get_order(order_id)
    totals = pricing.calculate_totals(order.items)
    if amount > totals.total_cents / 100:
        return {"error": "refund exceeds order total"}
    order.status = "cancelled"
    store.save_order(order)
    print(f"Refunded {amount} for order {order_id}: {reason}")
    return {"refunded": amount, "order": order_id}
```

Commit it, push, and open a PR against your fork.

<details>
<summary><strong>What's wrong with it (don't read until after step 2)</strong></summary>

1. **No auth check** — anyone can refund any order
2. **`order` can be `None`** — unhandled, crashes on unknown ID
3. **`float` for money** — the codebase uses integer cents everywhere else
4. **Wrong error convention** — returns 200 with an error body; this file raises `HTTPException`
5. **Mutable default footgun** — `reason: str = None` should be `Optional[str] = None`
6. **`print` instead of logging** — no structured audit trail for a *financial* operation
7. **No test**
8. **No idempotency** — double-submit refunds twice
9. **Status set to `cancelled`** for a refund, conflating two different states

Nine real problems in ten lines. Some are mechanical. Some require knowing the domain.
</details>

---

## Step 2 · Let the automated review run (3 min)

Request a Copilot review on the PR.

While it runs, **write down two problems you'd expect any competent reviewer to catch.** Commit to your predictions before you see the results — otherwise you'll read its findings and think "yes, obviously" about things you'd have missed.

---

## Step 3 · Score it honestly (5 min)

Go through the comments and sort every one into three buckets:

| Bucket | Meaning |
|---|---|
| **Caught** | Real problem, correctly identified |
| **Missed** | Real problem, no comment |
| **Noise** | Comment that isn't worth a human's attention |

Then answer the question that actually matters for your team:

> Of the things it caught — how many would I have caught on a Friday afternoon, on my fourth review of the day?

That's the honest measure. Not "is it as good as me at my best." **Is it better than the review that would otherwise have happened.**

Check specifically:

- Did it catch the missing auth check? *(security, highest stakes)*
- Did it catch the float-for-money inconsistency? *(needs codebase context)*
- Did it flag the error-convention mismatch? **If you wrote exercise 2's instructions, this is where they pay off — or don't.**
- Did it notice the missing test?
- Did it catch the idempotency problem? *(needs domain reasoning — the hardest one)*

---

## Step 4 · Decide your policy (3 min)

You now have evidence. Answer three questions for your actual team:

1. **What would you automate on every PR?** The categories where it's consistently right and humans are consistently bored.
2. **What stays human, always?** Where it was quiet or wrong, and the stakes are high.
3. **What's the failure mode you'd worry about?** Be specific. "People rubber-stamp whatever it approves" is the common one — is that a real risk on your team, and what would you do about it?

Write the answers down. This is the most directly actionable output of the whole lab.

---

## Stretch — the on-call path

If you have a few minutes and an MCP server wired from exercise 2:

Use the **CLI** to investigate a failure — CI logs, application logs, metrics. Ask it to narrow the cause.

The lesson to look for: it's good at **narrowing** and bad at **concluding**. Great at "these three commits touched the affected path, and this one changed the timeout." Bad at "this is definitely the root cause." Treat its output as a shortlist, never a verdict.

---

## Track B — your own repo

Use a real open PR, or open one from a branch you already have.

The scoring exercise transfers exactly. The policy questions in step 4 are the real deliverable — you're deciding what your team automates on Monday.

> If your PRs are large, this works better on a single focused one. Automated review on a 2,000-line refactor produces volume, not signal — which is itself a finding worth knowing.

---

## Done when

- [ ] A PR with real problems exists on your fork
- [ ] An automated review has run on it
- [ ] You sorted every comment into caught / missed / noise
- [ ] You can name **one thing it caught and one thing it missed**
- [ ] You've written down what you'd automate and what stays human

---

## Common failure modes

**It caught almost everything and you're suspicious.**
Reasonable. Check whether it caught the *hard* ones — idempotency and the status-conflation issue need domain reasoning, not pattern matching. Mechanical catches are table stakes.

**It generated a lot of noise.**
Useful finding, and it's usually a context problem rather than a tool problem. Noise is what automated review produces when it doesn't know your conventions — which is an argument for exercise 2, not against exercise 4.

**It missed the auth check.**
Worth sitting with. Security review is exactly where "it caught most things" is least comforting, and it's the clearest argument for keeping a human in the loop on a defined category rather than trusting a general-purpose pass.

**Your team already does all of this manually and well.**
Then the value here isn't quality, it's **latency**. Review wait time is usually the largest single chunk of dead time in a delivery pipeline, and almost nobody measures it because it's nobody's job.

---

## The point

Review and incident work are asynchronous and interrupt-driven by nature. Nobody plans them. That makes them a natural fit for async surfaces — and usually the **fastest ROI a team can find**, for the unglamorous reason that nobody was optimizing that queue before.

But notice what determined the quality of what you just saw: not the model. **The context.** The same review, run against a repo with clear written conventions, is a meaningfully different product than one run against a repo without them.

Which is the whole argument of this lab, arriving from a fourth direction.

---

## You're done

Back to the **[syllabus](../README.md#debrief-questions)** for the debrief questions.
