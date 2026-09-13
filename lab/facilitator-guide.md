# Facilitator Guide

Everything you need to run the 90-minute lab, including what breaks and when.

---

## Room shape

Works for 8 to 60 people. Above ~30 you need a second floater, because setup failures cluster in the first fifteen minutes and one person cannot unblock them all.

**Ideal:** tables of 4–6. Exercises 2 and 4 have compare-with-your-neighbor beats that fall flat when people are in rows.

---

## Pre-lab, one week out

Send the [setup instructions](setup.md) with an explicit warning that **in-class setup is 10 minutes and that is verification time, not install time.**

Ask people to reply confirming `copilot --version` works. The replies you *don't* get tell you where your morning is going.

---

## Pre-lab, day of

- [ ] Sample app cloned, `pytest -q` green on your machine
- [ ] Your own fork ready to demo from
- [ ] A completed PR for each exercise, parked in tabs as a fallback
- [ ] Know your org's MCP policy — someone will ask whether they can wire up an internal server
- [ ] Confirm the coding agent is available to attendees; if not, exercise 3 needs its fallback path announced up front

---

## Timing checkpoints

| Clock | Should be | If behind |
|---|---|---|
| 0:10 | Everyone has a green baseline | Pair the broken with the working. Don't debug one laptop while 40 people wait. |
| 0:28 | Exercise 1 verified | Cut the composability step to a demo you run from the front |
| 0:48 | Exercise 2 instructions written | Skip the MCP step entirely — it's already marked optional |
| 1:08 | Exercise 3 PR delegated | Have people review *your* pre-made agent PR instead of waiting for theirs |
| 1:23 | Exercise 4 scored | Cut the stretch; go straight to the policy questions |

**Protect the debrief.** It's the only part where people hear each other's results, and it's the first thing that gets eaten. If you're at 1:25 with people mid-exercise, stop them.

---

## The single most important framing

Say this at the start, in roughly these words:

> "Every exercise has a checkable done condition — a passing test, a clean lint run, a diff you can read. That's not lab hygiene. That's the actual lesson. The reason you can safely give an agent this much autonomy is that you can cheaply tell whether it was right. Teams with good verification infrastructure can delegate far more than teams without it, using the exact same tool."

If people leave with only that, the lab worked.

---

## Per-exercise notes

### Exercise 1 — CLI

**Where people get stuck:** CLI not authenticated. Catch this in setup or you'll lose them for the full 18 minutes with no fallback.

**The beat to call out loudly:** when someone's agent runs the tests, reads a failure, and fixes itself — get them to say it out loud to the room. Most people have never seen level-4 autonomy and it changes their mental model on the spot.

**Expected outcome:** nearly everyone succeeds. This exercise is deliberately the easy one — it builds confidence before exercise 2 gets conceptual.

**Watch for:** people running `ruff --fix` and declaring victory. Redirect them; the point is the agent loop, not the autofixer.

### Exercise 2 — Context

**The hardest exercise to facilitate**, because the payoff is invisible if people rush step 1.

**Insist on the before/after.** People want to skip straight to writing instructions. Without the "before," step 3 proves nothing and the lesson evaporates.

**The moment that lands:** two people at the same table got *different* error conventions from the identical prompt on the identical repo in step 1. Seed this — walk the room during step 1 and find a mismatched pair, then have them announce it.

**Watch for:** 200-line instructions files. Call it out warmly. "Which 160 of those lines change what the agent does?"

**If someone's output doesn't change in step 3:** filename and path first, fresh session second, actionability third. In that order, it's almost always the first one.

### Exercise 3 — Dev-adjacent

**Announce the fallback up front** if the coding agent isn't available in your org, or you'll have people stuck at step 4 with no path.

**Enforce the browser-only rule.** Engineers will drift into an IDE by reflex. The constraint is the lesson.

**The bug / decision sort is the highest-value five minutes in the lab.** Don't let it get rushed. If you're compressing, take time from step 1, not step 2.

**Terminology:** use *dev-adjacent*, not "non-technical." If an attendee uses "non-technical," it's worth one gentle sentence — the distinction is real and it's operationally useful, not just polite.

### Exercise 4 — Review

**Expect the PR to be uncomfortable to write.** Some engineers resist committing deliberately bad code. Frame it as building a test fixture.

**The prediction step matters.** If people read the review results before writing down their own expectations, hindsight bias eats the exercise. Make them write first.

**Step 4's policy questions are the real deliverable.** This is the part attendees take back to their teams. Give it the full three minutes even if you're behind elsewhere.

---

## Expected failure points, ranked

1. **Copilot CLI not installed or authenticated** — by far the most common. Only fixable before the lab.
2. **Python version issues** — `pydantic` source builds on 3.14. The repo's floor-pinned requirements handle this; people using a stale fork will hit it.
3. **Coding agent not enabled** for the org — affects exercise 3 step 4.
4. **Corporate proxy blocking MCP** — exercise 2 step 5 is optional for exactly this reason.
5. **People using their own repo pick one that's too large** — agent stalls, they conclude the tool is bad. Redirect to a subdirectory.

---

## Questions you will get

**"Which model should we be using?"**
Redirect to context. The gap between teams is almost never the model — it's what their tools can see. Exercise 2 is the evidence.

**"How do we stop people rubber-stamping agent PRs?"**
Verification infrastructure, not policy. If tests and CI catch bad changes, rubber-stamping is survivable. If they don't, that problem predates Copilot.

**"Is this going to replace developers?"**
It changes what's scarce. When producing code gets cheaper, deciding what to build and verifying whether it's right become the bottleneck. Most orgs aren't staffed for that shift.

**"What about juniors?"**
The risk isn't that they use it. It's using level-4 autonomy before they can evaluate level-4 output. Pair the autonomy ladder to the experience ladder deliberately.

**"Can we wire up our internal systems?"**
Yes, and treat every MCP server like a new integration with production data access — because that's what it is. Scope permissions, audit reach, don't let individuals connect arbitrary servers to internal systems unreviewed.

---

## If you're running the talk and lab together

The lab assumes the talk's vocabulary — routing, the autonomy ladder, the four layers, cheap verification. If you're running both, skip the concept framing in each exercise and reference the talk directly.

If the lab is standalone, the exercises carry enough context on their own, but budget an extra 5 minutes up front for the routing matrix and the verification thesis. Take it from exercise 4's stretch.

---

## After

Ask for two things in the room before people leave:

1. **One workflow they're changing on Monday.** Specific, not aspirational.
2. **One thing that didn't work.** You'll learn more from these than from the positive feedback, and it tells you which exercise to rewrite.
