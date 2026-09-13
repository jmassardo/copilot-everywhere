# Facilitator Guide

Everything needed to run the 90-minute lab, including what breaks and when.

---

## The structural decision

Attendees pick **one track** and do five exercises inside it. They do not rotate.

This is deliberate, and worth defending out loud if asked. The earlier one-exercise-per-persona design made PMs write tests and engineers write release notes — teaching the wrong lesson twice. Copilot's claim is that it meets people where they work. The lab has to do the same or it undercuts the talk.

**Consequence for you:** four things happen at once in the room. Plan for it.

---

## Room shape

Works for 8 to 60. Above ~30 you want a second floater — setup failures cluster in the first fifteen minutes and one person can't unblock them all.

**Seat by track.** The single highest-leverage thing you control. Put a "Product" sign on one table, "Engineer" on another. It makes peer unblocking work and makes the debrief coherent.

### Expected distribution

Most rooms skew heavily to Engineer. Budget accordingly:

| Track | Typical share | Watch for |
|---|---|---|
| Engineer | 40–60% | May need two tables |
| Maintainer | 15–25% | Overlaps with Engineer; let people move |
| Platform | 10–20% | Small but high-influence |
| Product | 5–20% | **Often under-attended and over-valuable** |

> **If nobody picks Product:** push one or two people there — especially engineering managers, or anyone who says "I don't really write code anymore." That track has the highest surprise factor in the room and its results land hardest in the debrief.

> **If Platform is empty:** you run it. Do exercise 1 live from the front during setup and share the instructions file. Otherwise debrief question 3 has no answer.

---

## Pre-lab, one week out

Send [setup.md](setup.md) with the track table and ask people to **pick a track in advance.** They arrive with the right tools installed, and you get a headcount for seating.

Ask for a reply confirming `copilot --version` works — Engineer and Maintainer have no fallback without it. The replies you *don't* get tell you where your morning is going.

---

## Pre-lab, day of

- [ ] Sample app cloned, `pytest -q` green on your machine
- [ ] Your own fork ready to demo from
- [ ] A completed artifact for each track's exercise 1, parked in tabs as fallback
- [ ] Know your org's MCP policy — someone will ask
- [ ] Confirm the coding agent is available to attendees; if not, announce the Product exercise-4 fallback up front
- [ ] Track signs on tables

---

## Timing checkpoints

| Clock | Should be | If behind |
|---|---|---|
| 0:10 | Green baseline, everyone seated by track | Pair broken with working. Don't debug one laptop while 40 people wait. |
| 0:40 | Everyone into exercise 3 | Announce 4 and 5 are optional — many will have guessed already |
| 1:10 | People on 4, 5, or deepening | Start collecting debrief-worthy findings so you're not cold-starting |
| 1:22 | Debrief begins | **Stop people mid-exercise.** Protect this. |

The debrief is the only part where tracks hear each other, and the first thing to get eaten. Guard it.

---

## The framing to open with

Say this, roughly:

> "Every exercise has a checkable done condition — a passing test, a clean lint run, an acceptance criterion you wrote. That's not lab hygiene, that's the lesson. The reason you can safely give an agent this much autonomy is that you can cheaply tell whether it was right. Teams with good verification can delegate far more than teams without it, using the identical tool."

Then the track framing:

> "You're doing one track. You will not write code you wouldn't normally write. If you're a PM, you're doing PM work — I'm not going to make you write a unit test to prove a point."

That second line reliably gets a laugh from people who've been burned by vendor labs, and it buys you their attention.

---

## Per-track notes

### Engineer
**Most likely to succeed unaided.** Exercise 1 is deliberately easy — it builds confidence before anything conceptual.

**The beat to amplify:** when someone's agent runs tests, reads a failure, and fixes itself, have them say it out loud to the room. Most people have never seen level-4 autonomy and it rewrites their mental model on the spot.

**Watch for:** people running `ruff --fix` and declaring victory. Redirect — the point is the agent loop, not the autofixer.

**Exercise 2 is the sleeper.** Characterization testing to *discover* a bug rather than fix a known one is a technique most engineers haven't used. If the room is strong, spend extra time here.

### Platform
**Hardest to facilitate**, because the payoff is invisible if people rush exercise 1's "before."

**Insist on the before/after.** People want to skip to writing instructions. Without the before, the proof step proves nothing.

**Seed the moment:** during exercise 1, find two people who got *different* error conventions from the identical prompt. Have them announce it. That's the whole argument, delivered by an attendee instead of by you.

**Watch for:** 200-line instructions files. Warmly — "which 160 of those change what the agent does?"

**Output didn't change?** Filename and path first, fresh session second, actionability third. It's almost always the first.

### Product
**The track most likely to exceed expectations, and most likely to be under-attended.**

**Enforce browser-only.** Engineers who wandered in will drift to an IDE by reflex. The constraint is the lesson.

**The bug-vs-decision sort in exercise 3 is the highest-value five minutes in the lab.** Don't let it get rushed. If compressing, take time from exercise 1.

**Exercise 4's framing needs protecting:** they review against *acceptance criteria*, not code quality. If you see a PM squinting at syntax, redirect. "Does it do what you asked?" is the only question.

**Terminology:** use *dev-adjacent*, never "non-technical." If an attendee says it, one gentle sentence is worth it — the distinction is operationally useful, not just polite.

### Maintainer
**Expect discomfort writing the deliberately bad PR.** Some engineers resist committing bad code. Frame it as building a test fixture.

**The prediction step matters.** If people see the review output before writing their own expectations, hindsight bias eats the exercise. Make them write first.

**Exercise 4 is the real deliverable** — it's what they take back to their team. Give it the full twelve minutes even if you're behind elsewhere.

---

## Cross-track connection

If Platform and any other track are both running, engineer this moment:

Have a Platform attendee share their `.github/copilot-instructions.md` with an Engineer or Maintainer attendee mid-lab. The Maintainer track's exercise 1 explicitly checks whether the error-convention mismatch got flagged — **with instructions it usually does, without it usually doesn't.**

That's the most convincing demonstration in the entire lab, and it happens between two attendees rather than from the front.

---

## Expected failure points, ranked

1. **Copilot CLI not installed or authenticated** — by far the most common. Only fixable before the lab. Fallback: move them to Product, which needs none of it.
2. **Python version issues** — `pydantic` source-builds on 3.14. This repo's floor-pinned requirements handle it; people on a stale fork hit a Rust compile error.
3. **Coding agent not enabled** for the org — hits Product exercise 4 and Engineer stretch work.
4. **Corporate proxy blocking MCP** — Platform exercise 5, which is why it's last and optional.
5. **Own-repo attendees picking something too large** — agent stalls, they conclude the tool is bad. Redirect to a subdirectory.

---

## Questions you will get

**"Which model should we be using?"**
Redirect to context. The gap between teams is almost never the model. The Platform track is the evidence.

**"How do we stop people rubber-stamping agent PRs?"**
Verification infrastructure, not policy. If tests and CI catch bad changes, rubber-stamping is survivable. If they don't, that problem predates Copilot.

**"Is this going to replace developers?"**
It changes what's scarce. When producing code gets cheaper, deciding what to build and verifying whether it's right become the bottleneck. Most orgs aren't staffed for that shift.

**"What about juniors?"**
The risk isn't that they use it — it's using level-4 autonomy before they can evaluate level-4 output. Pair the autonomy ladder to the experience ladder deliberately.

**"Can we wire up our internal systems?"**
Yes, and treat every MCP server as a new integration with production data access. Scope permissions, audit reach, don't let individuals connect arbitrary servers unreviewed.

**"Why didn't I get to do the other tracks?"**
The materials are public — all four are in the repo. Point them at another track's exercise 1 as homework.

---

## Running talk and lab together

The lab assumes the talk's vocabulary: routing, the autonomy ladder, the four layers, cheap verification. Running both back to back, skip the concept framing in each track and reference the talk directly.

Standalone, the tracks carry enough context on their own — but budget 5 extra minutes up front for the routing matrix and the verification thesis. Take it from exercise 5.

---

## After

Ask for two things before people leave:

1. **One workflow they're changing on Monday.** Specific, not aspirational.
2. **One thing that didn't work.** You'll learn more from these than from the praise, and it tells you which exercise to rewrite.
