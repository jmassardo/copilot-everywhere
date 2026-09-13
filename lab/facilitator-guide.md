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
| Data | 10–25% | Needs the database built — verify in setup |
| Platform | 10–20% | Small but high-influence |
| Product | 5–20% | **Often under-attended and over-valuable** |

> **If nobody picks Product:** push one or two people there — especially engineering managers, or anyone who says "I don't really write code anymore." That track has the highest surprise factor in the room and its results land hardest in the debrief.

> **If Platform is empty:** you run it. Do exercise 1 live from the front during setup and share the instructions file. Otherwise debrief question 3 has no answer.

> **If Data is empty:** that's survivable, but you lose debrief question 4 — which is the only place the room confronts a discipline where verification is genuinely hard. Consider seeding it with anyone who touches reporting, ETL, or a warehouse.

---

## Pre-lab, one week out

Send [setup.md](setup.md) with the track table and ask people to **pick a track in advance.** They arrive with the right tools installed, and you get a headcount for seating.

Ask for a reply confirming `copilot --version` works — Engineer and Data have no fallback without it. The replies you *don't* get tell you where your morning is going.

**Data track attendees:** ask them to run `python data/build_db.py` in advance and confirm the row counts. It takes about a second, but it's the step that silently blocks the whole track.

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

### Data
**The track that makes the lab's thesis land hardest**, because it's the one where verification is genuinely expensive.

**Open it with the framing, don't let them skip it.** Every other track has `pytest`. This one has a query that returns a plausible wrong number and no exception. If they internalize only that, the track worked.

**Exercise 2 is the core.** Counting the problems is easy; the valuable part is the `discount_rate IS NULL` ambiguity — 7,113 rows where NULL means two different things and **no query can tell you which.** Attendees will try to solve it technically. Let them try for a minute, then name it: this is a conversation, not a query.

**Exercise 3 has the best single artifact in the lab.** `EXPLAIN QUERY PLAN` returns `SEARCH o USING AUTOMATIC COVERING INDEX` — SQLite literally announcing it had to build an index at runtime because the schema didn't provide one. Point at it. The N+1 shape goes from ~0.96s to ~0.009s.

**Watch for:** accepting the first index suggestion list wholesale. Every index is a write-path tax. Make them justify each one.

**The trap to let them fall into:** join fan-out through `line_items` inflating every sum. It produces a *completely plausible* number. If someone reports revenue without cross-checking, that's your debrief material — with their permission.

---

## Cross-track connection

Two moments worth engineering deliberately.

**Platform → anyone.** Have a Platform attendee share their `.github/copilot-instructions.md` with an Engineer or Data attendee mid-lab, and have the recipient re-run an exercise with it in place. That's the most convincing demonstration in the lab, and it happens between two attendees rather than from the front.

**Data ↔ Engineer.** The analytics database stores money as `REAL`; the application uses integer cents. **Neither side knows.** If you have both tracks running, get one person from each to compare notes out loud during the debrief — it's a live example of a bug that's invisible from inside either codebase, and it's exactly the class of problem that needs org-level context rather than repo-level context.

---

## Expected failure points, ranked

1. **Copilot CLI not installed or authenticated** — by far the most common. Only fixable before the lab. Fallback: move them to Product, which needs none of it.
2. **Python version issues** — `pydantic` source-builds on 3.14. This repo's floor-pinned requirements handle it; people on a stale fork hit a Rust compile error.
3. **Data track: database not built** — one command, but it blocks everything. Check it during setup.
4. **Coding agent not enabled** for the org — hits Product exercise 4 and Engineer stretch work.
5. **Corporate proxy blocking MCP** — Platform exercise 5, which is why it's last and optional.
6. **Own-repo attendees picking something too large** — agent stalls, they conclude the tool is bad. Redirect to a subdirectory.

---

## Questions you will get

**"Which model should we be using?"**
Redirect to context. The gap between teams is almost never the model. The Platform track is the evidence.

**"How do we stop people rubber-stamping agent output?"**
Verification infrastructure, not policy. If tests and CI catch bad changes, rubber-stamping is survivable. If they don't, that problem predates Copilot. The Data track is the sharpest version of this — there's nothing to rubber-stamp *against*.

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
