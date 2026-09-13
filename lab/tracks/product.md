# Track: Product / Dev-Adjacent

**Who this is for:** product managers, business analysts, support leads, technical program managers
**Surface emphasis:** github.com + Copilot app + coding agent
**Matrix cell:** Repo holds the context · spans synchronous and asynchronous
**5 exercises · ~15 min each · first 3 are core**

---

## Before you start: two ground rules

**1. You will not write code in this track.** Not tests, not fixes, not snippets. Every exercise is work you already do — understanding a system, sorting demand, specifying work, deciding whether it's done, and telling people about it. The tool just removes the part where you had to wait for an engineer to answer a question.

**2. Everything happens in a browser.** No clone, no terminal, no local environment. If you open an IDE, you've left the track.

> **On the label:** these are **dev-adjacent** roles, not "non-technical" ones. "Non-technical" defines people by what they aren't, and it's usually wrong — the PM who knows which service a request lands in *is* technical, they just don't commit. What dev-adjacent people need is real codebase context reachable without a build environment. That's exactly what this surface is.

| # | Exercise | Time | Core? |
|---|---|---|---|
| 1 | [Answer your own questions](#1--answer-your-own-questions) | 12 | ✅ |
| 2 | [Triage the demand](#2--triage-the-demand) | 15 | ✅ |
| 3 | [Specify it properly](#3--specify-it-properly) | 18 | ✅ |
| 4 | [Delegate and accept](#4--delegate-and-accept) | 15 | |
| 5 | [Tell everyone](#5--tell-everyone) | 12 | |

---

## 1 · Answer your own questions

**12 min · github.com chat**

Every PM has a list of questions they're waiting on an engineer to answer. This is that wait, deleted.

Open Copilot chat on github.com against the sample app repo — **which you have not cloned, and will not.**

Get grounded answers to all five:

1. *Where is order pricing calculated, and what's the actual logic?*
2. *What discount tiers exist and at what thresholds?*
3. *Is there test coverage on the pricing code?*
4. *How do the orders and customers endpoints differ in how they report errors?*
5. *What would break for an API consumer if we changed the customers endpoint to return proper HTTP error codes?*

That last one is a **blast-radius question** — normally a Slack thread and a two-day wait.

### The discipline

For each answer, ask yourself: *could I repeat this to an engineer without embarrassing myself?* If not, ask a follow-up. Fluent and wrong is the failure mode here, and the defense is asking for the specific file and function.

**Done when:** you can state three concrete facts about a codebase you've never opened, each anchored to a real file.

> **Why this surface:** zero setup. This is the one your whole org can reach, and it's why "Copilot is a developer tool" is an expensive misunderstanding.

---

## 2 · Triage the demand

**15 min · github.com or Copilot app**

Open [`sample-app/FEEDBACK.md`](../../sample-app/FEEDBACK.md). Twelve raw items: support tickets, sales notes, engineer grumbling. Nobody has sorted it.

This is your actual job, and it's the one everyone hand-waves.

### Cluster it

```
Group this feedback into themes. For each theme: how many items mention it,
which customer segment is affected, and whether it's a bug, a missing
feature, or a design decision we never made.
```

You should find several items pointing at the **same underlying cause** — that's the point of the exercise. Ticket 4488 and Ticket 4471 aren't separate problems.

### Cross-reference against reality

Now ground the themes in code, the way you did in exercise 1:

```
For each theme, check the repo and tell me whether the root cause is
visible in the code, and where.
```

This is the step that separates you from a spreadsheet. You're not guessing at impact — you can see it.

### Rank it

```
Rank these themes by customer impact and implementation risk. Flag anything
that's a breaking change for existing API consumers.
```

**Push back on the ranking.** It doesn't know your business. If it ranks the penny-rounding issue above the double-charge issue, say so and make it justify itself.

**Done when:** twelve raw items have become four or five themes, each with a root cause, an affected segment, and a ranking you'd defend in a planning meeting.

---

## 3 · Specify it properly

**18 min · github.com Issues**

Take your top two themes and turn them into work engineers won't hate.

### Decompose

```
Break this theme into independently shippable GitHub issues. For each:
a clear title, the specific file and function involved, acceptance criteria
that could be verified by a test, and whether it's a bug or a behavior change.
```

**Insist on file and function names.** If you get "improve error handling," push back and ask where. Grounded beats fluent, every time.

### The sort that matters most

Divide your issues into two piles:

| Pile | Meaning | Safe to delegate? |
|---|---|---|
| **Bug** | There's an objectively correct answer | Yes |
| **Decision** | Someone has to choose; changes a contract | **No** |

The discount boundary is a bug — `>` should be `>=`, and there's no debate. Unifying the error responses is a **decision**: it breaks every existing API consumer, and shipping it without a human choosing would be wrong no matter how good the code is.

> Most teams delegate decisions by accident and then blame the tool for the outcome. This sort is the most transferable thing in this track.

### File them

Create at least two real issues on your fork. Make them **agent-ready**, which is the same thing as new-hire-ready:

- What's wrong, specifically
- Where, by file and function
- How you'd know it's fixed

An issue reading "discounts broken pls fix" is useless to an agent. It's equally useless to a human. That's not a coincidence.

**Done when:** two or more issues exist with file-level detail and testable acceptance criteria, sorted into bugs and decisions.

---

## 4 · Delegate and accept

**15 min · Coding agent**

Pick a **bug** from your pile — never a decision. The discount boundary is ideal: small, objectively correct, verifiable.

Assign it to the Copilot coding agent. Then **stop watching it.** Move to exercise 5 while it works. The entire value of an asynchronous surface is that you go do something else.

> **No coding agent in your org?** Ask an engineer at your table to run it in IDE agent mode and open the PR. You'll keep the acceptance lesson, which is the important half.

### Review as a PM, not as an engineer

When the PR arrives, you are **not** reviewing code quality. That's not your job and pretending otherwise is how these labs lose people.

You're answering exactly one question: **does this satisfy the acceptance criteria I wrote?**

Ask Copilot to help you read it:

```
Explain what this pull request changes, in terms of observable behavior.
Does it satisfy these acceptance criteria? [paste yours]
What behavior would a customer notice that they didn't before?
```

Then check three things yourself:

- Does the described behavior match what you asked for?
- Is there a test proving the boundary case specifically — or just the easy cases?
- Did it change anything you *didn't* ask for? (That's a scope question, and scope is absolutely your job.)

Leave a real comment. Accept it, or send it back with a reason.

**Done when:** you've accepted or rejected an agent-authored PR against criteria you wrote — without evaluating a single line of syntax.

---

## 5 · Tell everyone

**12 min · Copilot app or github.com**

Work that shipped and nobody heard about may as well not have shipped. This is the part of the job that always gets cut, and it's the easiest to give back to yourself.

Pick two:

**Release notes for customers.**
```
Read the merged changes in this repo and write release notes for a
non-technical customer audience. Lead with what they'll notice. No
internal jargon, no file names.
```

**A stakeholder update.**
```
Summarize this week's repo activity for a leadership audience. What
shipped, what's in flight, what's blocked. Under 200 words.
```

**A response to the customer who complained.** Take ticket 4488 from the feedback file and write the reply — acknowledging the bug, explaining the fix, no jargon.

**A backlog health summary.** What's open, what's stale, what themes dominate.

### The discipline

Rewrite whatever comes back in your own voice before you'd send it. It's a first draft, not a final one — and your stakeholders can tell the difference.

**Done when:** you have a communication artifact you'd genuinely send, grounded in what actually changed rather than what you remember changing.

---

## Track B — your own repo

Everything maps directly, and honestly the sample app is training wheels:

| # | What to use |
|---|---|
| 1 | Five questions about your product you're currently waiting on an engineer for |
| 2 | Your real, unsorted feedback — tickets, Slack, call notes |
| 3 | The vaguest request in your backlog right now |
| 4 | One small, unambiguous bug — resist the interesting one |
| 5 | The status update you owe someone this week |

> **Guardrail:** if your repo is sensitive, do exercises 1–3 against the sample app and only bring your own material to 5. Grounded reading of company code in a lab setting is a policy question, not a technical one.

---

## Common failure modes

**The answers were fluent but vague.**
You didn't ask for specifics. Every question should end with "which file and function?" Fluency without grounding is the failure mode of this whole surface.

**The decomposition gave you generic advice.**
Same fix. "Improve error handling" is not an issue; "customers.py returns 200 on failure" is.

**You delegated a decision.**
Go look at what came back. It probably made a reasonable-looking choice that silently breaks every consumer. That's the "load-bearing decision with a long half-life" failure mode, live and in your own hands.

**The agent's PR had no test.**
Extremely common, and precisely why it belonged in your acceptance criteria. Notice how much cheaper catching it here was than catching it in production.

**You started reviewing the code.**
Stop. Re-read your acceptance criteria and review against those. If you can't tell whether the criteria were met, your criteria were too vague — and that's the finding.

---

## The point

You went from twelve unsorted complaints to a reviewed pull request without a local environment, a clone, or a single line of code.

Not because the agent is brilliant — because the work was **routed correctly**: grounded on a surface with real repo context, sorted so only the safe pile got delegated, and accepted against criteria you wrote in advance.

The gap between "I have an idea" and "there is something to react to" collapsed from a sprint to a coffee break. For most organizations **that specific gap is the bottleneck** — not how fast engineers type.
