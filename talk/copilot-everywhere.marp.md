---
marp: true
title: Copilot Everywhere
description: Picking the right surface for the right work — a routing framework for GitHub Copilot across the IDE, CLI, cloud agent, code review, and beyond.
author: Jenna Massardo
paginate: true
theme: default
style: |
  section {
    font-family: Avenir Next, Avenir, Helvetica, Arial, sans-serif;
    background: linear-gradient(135deg, #f4f7fb 0%, #eef6ff 45%, #f8fbff 100%);
    color: #102033;
    padding: 52px;
  }

  h1, h2, h3 {
    color: #0c4a7d;
    letter-spacing: 0.2px;
  }

  h1 {
    font-size: 1.9em;
    margin-bottom: 0.3em;
  }

  h2 {
    font-size: 1.45em;
    margin-bottom: 0.35em;
  }

  h3 {
    font-size: 1.05em;
    margin-bottom: 0.2em;
  }

  p, li {
    font-size: 0.94em;
    line-height: 1.4;
  }

  strong {
    color: #083b65;
  }

  code {
    background: #e9f3ff;
    color: #0a3f69;
    border-radius: 6px;
    padding: 0.1em 0.3em;
  }

  table {
    font-size: 0.78em;
    border-collapse: collapse;
    width: 100%;
  }

  th {
    background: #d9ecff;
    color: #0b4674;
    text-align: left;
    padding: 8px;
  }

  td {
    background: rgba(255, 255, 255, 0.75);
    padding: 8px;
    border-top: 1px solid #d3e6fb;
  }

  blockquote {
    border-left: 5px solid #2f80c7;
    background: rgba(255, 255, 255, 0.7);
    padding: 10px 14px;
    border-radius: 8px;
    margin: 0.6em 0;
    font-size: 0.9em;
  }

  .lead {
    font-size: 1.1em;
    color: #184f7d;
  }

  .small {
    font-size: 0.75em;
    color: #36516b;
  }

  .pill {
    display: inline-block;
    border: 1px solid #86b4dc;
    border-radius: 999px;
    padding: 0.15em 0.6em;
    margin-right: 0.25em;
    font-size: 0.7em;
    color: #0f4f83;
    background: #e9f3ff;
  }

  .demo {
    display: inline-block;
    border: 1px solid #d98a2b;
    border-radius: 6px;
    padding: 0.15em 0.6em;
    font-size: 0.7em;
    color: #8a4b06;
    background: #fdf1e0;
    letter-spacing: 0.5px;
  }

  .big {
    font-size: 1.35em;
    color: #0c4a7d;
    line-height: 1.35;
  }
---

# Copilot Everywhere

<p class="lead">Picking the right surface for the right work</p>

<span class="pill">IDE</span>
<span class="pill">CLI</span>
<span class="pill">Cloud Agent</span>
<span class="pill">Code Review</span>
<span class="pill">github.com</span>
<span class="pill">Copilot App</span>

> Audience promise: leave knowing which mode fits which workflow — and how to roll this out to people who work nothing like you.

<!--
0:00 · DO NOT START HERE. Cold open first, on a browser, before any slide.
Assign the issue live, then land on: "I never opened an editor."
Only after that beat, advance to this title slide and introduce yourself.
TOTAL BUDGET: 72 min content / 10 Q&A / 8 buffer.
-->

---

<!-- _class: lead -->

## First, a delegation

<p class="big">I'm assigning a real issue to the coding agent right now.</p>

<p class="lead">We'll come back to it around minute 60.</p>

<span class="demo">LIVE DEMO</span>

<p class="small">No editor was opened in the making of this pull request.</p>

<!--
This slide is just a bookmark. Say "we'll come back to it" and MOVE ON.
Do not linger. The demo already happened.
-->

---

## The Pitch You've Already Heard

**"Copilot is an AI pair programmer."**

- True in 2022
- Now the least interesting thing about it
- A pair programmer sits next to you

What actually happened:

<p class="lead">Copilot stopped requiring you to be sitting anywhere in particular.</p>

<!--
0:06 · Key beat: a pair programmer SITS NEXT TO YOU. Co-presence is the defining trait.
That's the thing that broke.
-->

---

## So This Isn't a Feature Tour

Same capability. Radically different ergonomics.

- Your editor
- Your terminal
- A browser tab
- A pull request
- Your phone
- **Increasingly: without you present at all**

> Choosing the wrong surface is the #1 reason people conclude "this doesn't work for my workflow."

<p class="lead">This is a <strong>routing</strong> problem. Given a piece of work — where should it go?</p>

<!--
SLOW DOWN. This is the thesis of the whole talk.
Examples of routing mistakes: 12-repo migration in an IDE chat window.
Two-line fix with a full agent. Question about a repo you never cloned, asked in an editor.
-->

---

## Session Flow

1. The mental model: three dials, not eight products
2. When *not* to reach for it
3. The surface map
4. Four personas, four surfaces, one codebase
5. The context supply chain
6. What effective implementation actually looks like
7. Measuring what the business cares about

<p class="small">Demos are live against a real repo. Some will be imperfect. That's the point.</p>

<!--
Two housekeeping notes, say both out loud:
1. Live demos WILL be imperfect — deliberate. Eight flawless demos = a commercial.
2. Wide room: new folks → persona block. Veterans → context + measurement blocks.
   Everyone stays for "when not to."
-->

---

## Every Copilot Interaction Is Three Things

| Dial | Question it answers |
|---|---|
| **Context** | What can it see? |
| **Autonomy** | How far does it run before checking in? |
| **Surface** | Where do you meet it? |

> The surfaces aren't different products. They're different **default settings** on the first two dials.

<p class="small">Once you know a surface's context scope and autonomy ceiling, you can reason about tasks you've never tried.</p>

<!--
The reframe: surfaces aren't different products, they're different DEFAULTS on context + autonomy.
Why it matters: makes the model PREDICTIVE, not descriptive.
They can derive use cases without me enumerating them.
-->

---

## The Autonomy Ladder

| Level | What it does | You are... |
|---|---|---|
| **1 — Completion** | Predicts the next edit | Driving |
| **2 — Chat / Ask** | Answers, you apply | Driving |
| **3 — Edit** | Proposes multi-file diffs | Approving |
| **4 — Agent** | Plans, edits, runs, iterates | Supervising |
| **5 — Async agent** | Same, without you in the loop | Reviewing |

<!--
Vocabulary I reuse all talk. One sentence per level, fast.
*** CUT CANDIDATE #2 *** — if behind, talk these five levels aloud and skip to next slide.
-->

---

## Where Most Teams Actually Live

<p class="big">Levels 1 and 2.<br/>And they think that's the product.</p>

- The gap between **no Copilot** and **level 2** is real
- The gap between **level 2** and **level 4** is *larger*
- Most orgs have never crossed it

> If your adoption metric is a flat line at "tab completion," you haven't found the product yet.

<!--
Be precise about the gap size — don't hand-wave:
  no Copilot → L2 = real
  L2 → L4 = BIGGER, and most orgs never made it
Close: "you haven't found the product. You've found the on-ramp."
-->

---

# When *Not* to Reach for It

<p class="lead">The credibility section.</p>

<!--
0:13 → 0:21 · 8 min. NEVER CUT THIS BLOCK.
Why early + on purpose: you can't trust anyone's advice about a tool
until you've heard them describe its limits specifically.
-->

---

## It's a Cost Model, Not a Rule List

Every interaction costs you two things:

- **Tokens**
- **The review effort to verify what came back**

<p class="big">The tool is a bad deal whenever verification costs more than doing it yourself.</p>

<!--
Why a cost model and not rules: rules don't generalize, cost models do.
Token cost = obvious + boring. VERIFICATION cost = the one that decides.
Deliver the bottom line slowly. Everything after this is a corollary.
-->

---

## Six Places Verification Costs Too Much

**1. Work where you can't articulate "done"**
No acceptance criteria → no target → endless review loops

**2. Load-bearing decisions with long half-lives**
Schema design, auth models, public APIs, service boundaries
*A plausible-sounding wrong answer here costs you 18 months*

**3. When the codebase is the wrong teacher**
It pattern-matches your existing code — including the pattern you're escaping

<!--
#1 fix isn't "don't use it" — it's use a SEPARATE session to draft criteria, then START OVER clean.
#2 the naive version is wrong. It reasons fine. The problem is ASYMMETRY —
   plausible-sounding is exactly what it's best at. Use as challenger, not author.
#3 hits platform teams hardest. Punchline:
   "a very fast, very confident junior who has read only your worst code and assumed it was intentional."
-->

---

## Six Places Verification Costs Too Much

**4. Debugging you haven't reproduced**
Excellent at fixing a failing test. Terrible at "prod is weird at 3am."
*Reproduction is the human's job*

**5. Genuinely novel work**
Not "new to you" — new to the world. Rare. But it becomes a fluent, confident distraction

**6. Compliance-critical output you can't attribute**
Know the policy before, not after

<!--
#4 a failing test is a SPECIFICATION OF WRONGNESS. Vague prod weirdness isn't.
   "Reproduction is the human's job."
#5 genuinely novel = new to the WORLD, not new to you. Rare.
#6 five-minute conversation with legal that some of you have avoided for a year.
-->

---

## Notice What's Missing From That List

<p class="big">None of those are<br/>"the model isn't smart enough."</p>

They're all about **where the verification burden lands.**

> That's a workflow design problem. And workflow design problems are solvable.

<p class="lead">Most of what looks like a model limitation is a routing mistake.</p>

<!--
PAUSE before this. Let them look back at the six.
The pivot: "not smart enough" is unsolvable — you just wait for a better model.
"Where verification lands" is a WORKFLOW DESIGN problem. Solvable. By you. This quarter.
-->

---

## The Real Question

Not: *"Can Copilot do this?"*

<p class="big">"Can I cheaply tell whether it did it right?"</p>

Cheap verification is what converts a risky task into a safe one:

<span class="pill">Test suite</span>
<span class="pill">Type checker</span>
<span class="pill">Linter</span>
<span class="pill">Repro case</span>
<span class="pill">CI</span>

> Teams with strong verification infrastructure can safely give Copilot dramatically more autonomy. **That's the prerequisite nobody talks about.**

<!--
MOST IMPORTANT LINE IN THE FIRST HALF. Slow way down.
Cheap verification already has a name and you own it: tests, types, linters, repro, CI.
Kicker: "Everybody's asking which model is best. Almost nobody's asking whether their
test suite is good enough to let an agent run unsupervised. Same question, different clothes."
FORESHADOW: this returns in the implementation block.
-->

---

# The Surface Map

<p class="lead">Nine minutes. Existence and ergonomics only.</p>

---

## The Routing Matrix

|  | **Synchronous** | **Asynchronous** |
|---|---|---|
| **You hold the context** | IDE inline / chat, CLI | — |
| **Repo holds the context** | dotcom chat, Copilot app | Coding agent, code review |
| **Org holds the context** | Spaces / knowledge bases | Agent + org instructions |

<p class="small">We'll point back at this after every demo today.</p>

<!--
0:21 · Read this matrix properly ONCE. It's the spine of the talk.
Call out the EMPTY cell: you hold context + async = impossible.
If it's only in your head you can't hand it off. → previews the context section.
-->

---

## What Each Surface Is Uniquely Good At

| Surface | Sees | Autonomy | Uniquely good at |
|---|---|---|---|
| **IDE — inline & chat** | Open files, workspace | Low–mid | Tight loops, context already loaded |
| **IDE — agent mode** | Workspace, terminal, tools | High | Multi-file changes you want to watch |
| **CLI** | Filesystem, shell, MCP | High | Anything that isn't one repo in one editor |
| **Coding agent** | Repo, CI, issue context | Async | Work you delegate and review as a PR |
| **Code review** | Diff + repo context | Async | First-pass consistency on the boring stuff |
| **github.com chat** | Repos, issues, PRs, org | Low–mid | Code you haven't cloned |
| **Copilot app** | Repos, issues, your work | Mid | Triage and thinking away from a keyboard |
| **Spaces / knowledge** | Curated context | — | Reusable org context across all of the above |

<!--
DO NOT READ THIS TABLE. Point at the LAST COLUMN only.
Not "what can it do" (everything, badly) — what is it UNIQUELY good at.
Hit 4-5 rows fast, then move. They get the deck.
-->

---

## The Part That Actually Matters

The CLI and cloud agent are the powerhouses. That's where the leverage is.

**But that's not why this matters at org scale.**

<p class="big">The person who only opens a browser and the person who lives in tmux are getting the same assistant with the same context.</p>

> Consistency across surfaces is the feature. Everything else is packaging.

<!--
Concede first: CLI + cloud agent ARE the powerhouses. Don't undersell them.
THEN pivot — that's not why it matters at org scale.
The PM writing an epic and the staff engineer doing a cross-repo refactor
draw on the SAME understanding of your codebase.
-->

---

## Rapid Fire

<span class="demo">LIVE DEMO</span> &nbsp; **CLI** — one command, non-trivial result

<span class="demo">LIVE DEMO</span> &nbsp; **github.com chat** — a question about a repo I never cloned

<span class="demo">LIVE DEMO</span> &nbsp; **Code review** — a PR that already has agent comments

<p class="small">The other five surfaces get covered inside the persona demos. On purpose.</p>

<!--
~90 SEC EACH. Hard stop. Three only.
1 CLI → "never left the terminal, never needed an editor"
2 dotcom → say out loud you've never cloned it. "Zero setup. Dev-adjacent folks can reach this."
3 review → *** CUT CANDIDATE #1 *** reappears in persona 4 anyway
SHOULD BE AT 0:30 LEAVING THIS SLIDE.
-->

---

# Four Personas

<p class="lead">Four surfaces. One codebase.</p>

<!--
0:30 → 0:56 · 26 min · ~6 min each. THE HEART OF THE TALK.
Same repo every time — because "consistency is the feature" should be
DEMONSTRATED, not asserted.
-->

---

## Who We're Following

| Persona | Core job | Surface |
|---|---|---|
| **Senior / staff engineer** | Changes bigger than one repo | CLI + code review |
| **Platform / DevEx lead** | Making 200 other people faster | MCP + org config |
| **Product manager / BA** <span class="small">dev-adjacent</span> | Fuzzy idea → backlog engineers don't hate | Copilot app + dotcom |
| **DBA / analytics engineer** | A schema you didn't design, data you didn't generate | dotcom + CLI + SQL |

<p class="small">Same three beats each: the real job → live demo → which cell on the matrix, and why.</p>

<!--
The three beats build a rhythm the room can follow. Keep them strict.
Beat 1 = the JOB, not the feature (30 sec)
Beat 2 = live demo (3-4 min)
Beat 3 = point at the matrix cell + why (1 min)
-->

---

## Persona 1 — Senior / Staff Engineer

### The job
Changes spanning more repos than you can hold in your head, where you already know exactly what you want.

<span class="demo">LIVE DEMO</span> &nbsp; Cross-repo change from the terminal — tests as the feedback signal

<span class="demo">LIVE DEMO</span> &nbsp; Then ship it: **agent review on the resulting PR** — what it caught, and honestly, what it missed

> Composability is the CLI's real superpower. Review is triage, not judgment.

**Why this surface:** You have the context. The work escapes a single workspace. **The CLI is the only surface where Copilot composes with the rest of your tooling.**

<!--
TWO DEMOS HERE — they're one workflow, not two topics. Make the change, then review it.

DEMO A: cross-repo dep upgrade w/ real API breakage. Terminal 18pt+.
CRITICAL BEAT — narrate the test suite as its OWN feedback signal:
  "it just failed, and it's reading its own failure."
Optional: piping. `git diff | copilot -p "..."` earns the terminal people.

DEMO B: push it, open a PR, agent review runs.
MUST DO: point at something it MISSED, out loud.
  Most credibility you'll earn all session.
Framing: TRIAGE, not judgment — first pass so humans spend attention on design,
not nitpicks. Review latency is the biggest chunk of dead time in most pipelines
and nobody optimizes it because it's nobody's job.

*** CUT CANDIDATE #3 *** — drop DEMO B if behind; rapid-fire already showed review.
Matrix: TOP LEFT for the change, MIDDLE-RIGHT for the review. Say both.
Kicker: everything else is a destination; the CLI is a COMPONENT.
-->

---

## Persona 2 — Platform / DevEx Lead

### The job
Making the other 200 engineers faster without sitting next to each of them. Their output is *leverage*, not code.

<span class="demo">LIVE DEMO</span> &nbsp; Wire up an MCP server live — Copilot reaches a system it couldn't see 30 seconds ago

**The advanced beat:** the same config now applies in the IDE, the CLI, *and* the cloud agent. Build context once, it propagates.

**Why this surface:** MCP is where *"Copilot knows our codebase"* becomes *"Copilot knows our company."*

<!--
HIGHEST-RISK DEMO. Have the recording ready.
Four beats: ask something it CAN'T answer → wire up live → same question, now answered
→ show same config applies in IDE + CLI + cloud agent.
The argument: your codebase is ~40% of the context an engineer needs.
The rest — what's broken, who owns this, what we decided, state of prod — is NOT in the repo.
Matrix: BOTTOM ROW, org context. The row most orgs have completely empty.
-->

---

## Persona 3 — Product Manager / BA

### The job
Turning a fuzzy idea into a backlog engineers don't hate.

> I don't call these roles *non-technical*. I call them **dev-adjacent.**
> You work next to the code and you shape it — you're just not the one merging it.

<span class="demo">LIVE DEMO</span> &nbsp; Messy spec → epic → issues, informed by the actual codebase

> The difference between this and pasting your spec into a chatbot is that **this one has read the code.**

**The advanced beat:** assign one of those issues straight to the coding agent.

<p class="lead">A PM just opened a pull request without writing code.</p>

<!--
Set up the TERM deliberately: not "non-technical" — DEV-ADJACENT.
"Non-technical" defines someone by what they aren't, and it's usually wrong.
The PM who knows which service a request lands in IS technical — they just don't commit.
Operational payoff: dev-adjacent people need REAL codebase context;
they just need to reach it without a clone and a build env.

DEMO beat 2 is the money beat — point at the line where it names a REAL service.
"This one has read the code."

After assigning to the agent: PAUSE. Then caveat honestly —
that PR won't be perfect and shouldn't merge unreviewed. Overclaiming here
undoes the credibility from the "when not to" block.
Real point: idea → code-to-react-to collapsed from a sprint to a coffee break.
Matrix: MIDDLE ROW, spans both columns.
-->

---

## Persona 4 — DBA / Analytics Engineer

### The job
A schema you didn't design. Data you didn't generate. Queries somebody wrote in a hurry before they left.

<span class="demo">LIVE DEMO</span> &nbsp; Read an inherited schema on dotcom · find where the warehouse and the app disagree about money · `EXPLAIN QUERY PLAN`

**But here's the twist:**

<p class="big">A wrong query doesn't throw.<br/>It returns a plausible number.</p>

<!--
THIS PERSONA COMPLICATES THE THESIS ON PURPOSE. Don't rush to the twist.

DEMO beats:
1. dotcom chat: "explain this schema" — no clone, no DB connection
2. The money mismatch: warehouse stores REAL, app uses integer cents.
   NEITHER CODEBASE KNOWS. Invisible from inside either one.
3. EXPLAIN QUERY PLAN -> "SEARCH o USING AUTOMATIC COVERING INDEX"
   SQLite literally announcing it built a throwaway index because the schema
   didn't provide one. Best single artifact in the talk. Point at it.
   Add the index: N+1 shape goes 0.96s -> 0.009s. ~100x.

Then the twist slide. Setup line:
"Every other persona today had a test suite. This one doesn't."
Matrix: spans rows — dotcom for schema, CLI for query work.
SHOULD BE AT 0:56 LEAVING THIS BLOCK.
-->

---

## The Persona That Breaks the Pattern

Every other persona today had a test suite. **This one doesn't.**

- Software fails **loudly** — exceptions, red CI, failing tests
- Analysis fails **quietly**, then gets presented to leadership

> Remember: cheap verification is what buys autonomy.

<p class="big">Where verification is expensive, you get <em>less</em> autonomy — no matter how good the model is.</p>

<!--
The most intellectually honest slide in the talk. Deliver it slowly.

This is NOT a walk-back of the earlier thesis — it's the thesis applied
honestly to a discipline where the answer comes out different.

If someone in the room does data work, this is the moment they decide
you're worth listening to, because everyone else sells them the opposite.

The practical upshot to say out loud:
"So the highest-value thing a data team can build right now isn't a prompt
library. It's reconciliation checks. Those are what make everything else
safe to hand off."
-->

---

## What Just Happened

Four personas. Four different surfaces. **One underlying capability.**

That's not fragmentation — that's the tool meeting each of them where they already work.

But notice something else:

<p class="big">Every demo depended on Copilot knowing things specific to <em>this</em> repo and <em>this</em> org.</p>

> That's not free.

<!--
THE PIVOT INTO THE SECOND HALF. Beat before the last line.
Walk it back through all four:
  refactor + review needed our conventions · MCP was ENTIRELY external context
  PM demo only worked because it could read real services
  the schema demo found a money mismatch only visible from OUTSIDE both codebases
None of that arrived in the box.
-->

---

# The Cold Open, Revisited

<span class="demo">LIVE DEMO</span>

<p class="lead">It's been working this whole time. I never supervised it.</p>

<!--
0:56 · NEVER CUT.
*** DO NOT PERFORM DELIGHT. *** No "wow, look at that!"
The room will smell it and you'll spend all the credibility from the "when not to" block.
Review it like a colleague's PR: read description, read diff honestly,
name ONE thing that's good and WHY, name ONE thing you'd change, check tests pass.
Fallback: completed PR from the same issue, already open in another tab.
-->

---

## What the Agent Got Wrong

<p class="big">It didn't know our convention for X.</p>

That is **not** the model being dumb.

That is **me not telling it.**

> The shift isn't that it writes code. It's that some work no longer requires you to be present.

<p class="lead">Which brings us to the most under-discussed part of this whole thing.</p>

<!--
THE STRONGEST SEAM IN THE TALK. Slow delivery.
The flaw becomes the transition — don't rush past it.
Analogy: it did what a competent new hire does on day one with no onboarding —
made a reasonable guess from surrounding code.
The unwritten convention is in three people's heads and one Slack thread from March.
CLOSE: the moment work doesn't require you present, everything you WOULD have said
in the moment has to exist somewhere else, in writing, where it can be loaded.
-->

---

# The Context Supply Chain

<p class="lead">How each surface actually consumes configuration.</p>

---

## The Gap

Everybody has seen a custom instructions file.

**Far fewer people can tell you what actually gets loaded** when you type a prompt in:

- the CLI
- agent mode in the IDE
- the cloud agent

<p class="big">That resolution order is the difference between config that works everywhere and config that mysteriously works on your machine only.</p>

<p class="small">Deliberate constraint for this section: we're talking about how surfaces <em>consume</em> these artifacts, not what goes inside them.</p>

<!--
1:00 → 1:13 · 13 min. Your most differentiated block.
STATE THE CONSTRAINT OUT LOUD: we are not opening a single one of these files.
"Here's what good instructions look like" has a hundred blog posts —
most of you have written better ones than I would.
What nobody covers is HOW EACH SURFACE CONSUMES THEM. That's the section.
-->

---

## The Artifacts — Purpose Only

| Artifact | Purpose | Scope |
|---|---|---|
| **Repo-wide instructions** | Baseline conventions every interaction inherits | Repo |
| **Path-scoped instructions** | Rules that apply only to matching files | Glob |
| **Prompt files** | Reusable, invocable task templates | Repo / user |
| **Custom agents** | Persona + tool restrictions for a mode of work | Repo / user |
| **Skills** | Packaged domain procedures, loaded on demand | Repo / user / plugin |
| **MCP servers** | Live access to systems outside the repo | Anywhere |

<p class="small">One line each. We are not opening any of these files today.</p>

<!--
Vocabulary only. ONE LINE EACH, fast.
Flag path-scoped as underused — it comes back in principle #3.
-->

---

## The Consumption Matrix

**Which surface reads what?**

| | IDE | CLI | Cloud agent | Code review | dotcom / app |
|---|---|---|---|---|---|
| Repo instructions | | | | | |
| Path-scoped | | | | | |
| Prompt files | | | | | |
| Custom agents | | | | | |
| Skills | | | | | |
| MCP | | | | | |

<p class="small">Built live from my own setup the week of this talk. This matrix moves fast — verify yours before you trust mine.</p>

<!--
*** PREP: FILL THIS IN THE WEEK OF THE TALK, FROM VERIFIED BEHAVIOR. ***
Do not present a cell you haven't personally tested.
If uncertain, SAY "I haven't verified this one" — far better than being
confidently wrong on your most authoritative slide.

Two things to point out while walking it:
1. Coverage isn't uniform. Put a critical convention in a surface-specific artifact
   and you've created a class of engineer for whom your standards silently don't apply.
2. This matrix MOVES. Re-verification is the operating advice, not a disclaimer.
-->

---

## Same Prompt. Same Repo. Two Surfaces.

<span class="demo">LIVE DEMO</span>

Different outputs — **because of what each one loaded.**

Then: show the loaded-context indicator in each.

> Mechanism, not magic.

<!--
*** THE MONEY SHOT OF THE BLOCK. REHEARSE HARDEST. NEVER CUT. ***
Same prompt, same repo, two surfaces → different outputs → THEN reveal why.
The point: it isn't randomness or temperature. They loaded different things
before they ever saw my prompt.
Close: "once you can see that, you can debug it. Before you can see it,
it just feels like the tool is inconsistent."
-->

---

## Three Principles

**1. Write for the lowest common denominator surface**
Config that only works in one surface fragments your org. Universal conventions go where everything reads them.

**2. Instructions are a code artifact**
Reviewed. Versioned. And they rot. A stale instruction file is worse than a stale README — it actively misleads an agent that trusts it.

**3. More context is not better context**
Everything loaded competes for attention and costs tokens. Selective beats comprehensive.

<p class="small">A 400-line instructions file is usually someone's monument to a problem they solved once.</p>

<!--
#2 why it's worse than a stale README: a stale README misleads a HUMAN who'll
   probably notice. A stale instruction file misleads an AGENT with no independent
   basis for doubt, which will confidently propagate it across forty files.
#3 deliver the "monument" line lighter. Somebody hit a problem once, added forty lines,
   and now every interaction in that repo pays for it forever. "Half of it is archaeology."
-->

---

## Tie It Back

Remember the "when not to use it" list?

<p class="big">Half of those failure modes get better when the context supply chain is healthy.</p>

The tool didn't change.

**What it could see did.**

<!--
WHY this section came AFTER the failure modes.
Walk back through: "can't articulate done" → better when conventions are written down.
"codebase is the wrong teacher" → EXACTLY what instructions are for; you can mark
patterns deprecated explicitly.
Agent not knowing standards → not a capability gap, an UNWRITTEN-KNOWLEDGE gap.
SHOULD BE AT 1:13 LEAVING THIS SLIDE.
-->

---

# What Effective Implementation Looks Like

<p class="lead">Seats are not adoption.</p>

---

## The Rollout You've Probably Seen

1. Buy licenses
2. Send an email with a link
3. Put "AI adoption" on a slide
4. Wonder in six months why usage is a flat line at tab completion

<p class="big">Installing the app is table stakes. It is not the project.</p>

<!--
1:13 · Deliver the four steps deadpan. Let them recognize themselves.
THEN be generous: nobody involved is lazy. There's a genuine misconception
that the hard part was procurement.
-->

---

## Four Layers. Most Orgs Do One.

| Layer | What it is | Who owns it |
|---|---|---|
| **1 — Access** | Licenses, policy, approved surfaces, governance | Procurement / security |
| **2 — Context** | The supply chain, built deliberately | Platform |
| **3 — Workflow** | Copilot *in the path of work* | Eng leadership |
| **4 — Craft** | The practices separating 10% from 40% | The team, socially |

> Layer 1 is necessary, not sufficient. Do it fast and stop congratulating yourself for it.

<!--
Name all four, then spend your time on layers 2 and 3 — that's where the money is.
-->

---

## Layer 2 — Context

- Repo instructions in your top repos
- MCP servers for your critical internal systems
- Curated org knowledge

This is **platform work** with a real backlog, a real owner, and a real maintenance burden.

<p class="big">If nobody owns it, it doesn't exist.</p>

<!--
Be blunt: this is PLATFORM WORK. Backlog, maintenance burden, an owner with a NAME.
The failure pattern: "we should write instructions files" — everyone agrees,
nobody's accountable. Six months later there are three files, two are wrong,
and nobody trusts any of them.
-->

---

## Layer 3 — Workflow

The layer that moves the needle. The layer everyone skips.

Copilot has to be **in the path of work**, not adjacent to it:

- Code review runs on PRs *by default*, not when someone remembers
- Issue templates that produce **agent-ready** issues
- CI failures that route somewhere useful
- Prompt files for genuinely repetitive work — release notes, migrations, boilerplate
- Team norms: what gets delegated async vs. done live

<!--
THE LAYER THAT MOVES THE NEEDLE. Everyone skips it — it needs process change, not purchase.
Key distinction: ADJACENT = available if people remember and feel motivated.
              IN THE PATH = happens whether anyone remembers or not.
On review: "if it's opt-in, you've built a tool for the people who least need it."
On issues: three words and a screenshot is useless to an agent — and to a new hire.
On norms: most teams have no shared answer, so everyone guesses.
          The guessing is where the inconsistency comes from.
-->

---

## Layer 4 — Craft

The difference between a team getting 10% and a team getting 40%:

- Prompt and context discipline
- Knowing when to start a fresh session
- **Knowing when to stop and do it yourself**

> This spreads socially, not through training decks.

**Budget for it:** pairing, demos, an internal channel where people post what actually worked.

<!--
*** CUT CANDIDATE #4 *** — if behind, compress to one sentence.
Hardest of the three: knowing when to STOP and do it yourself.
Key claim: never seen a lunch-and-learn move this needle.
It spreads socially — somebody watches somebody and says "wait, how did you do that?"
So pairing time isn't culture fluff, it's the DELIVERY MECHANISM for the highest-value layer.
-->

---

## You Cannot Roll This Out Uniformly

Because your people don't work uniformly.

- The PM and the staff engineer needed **different surfaces**
- Different onboarding
- Different definitions of success

<p class="big">A single rollout plan optimized for the median developer will underserve both ends.</p>

> Segment by how people work. Your advanced users are your seed crystals. Your **dev-adjacent** roles are your biggest untapped population.

<!--
This is WHY the middle of the talk was structured around personas — call that back.
PM's win condition = better-decomposed backlog.
Staff engineer's = a twelve-repo change that didn't break anything.
The ENDS are where your leverage is: advanced users seed layer 4,
dev-adjacent roles are the untapped population.
-->

---

## One Concrete Recommendation

Find the two or three teams already using this hard.

**Make them visible.**

Let adoption spread laterally.

<p class="lead">Mandates produce compliance. Demonstrated leverage produces adoption.</p>

<!--
They exist in your org RIGHT NOW, quietly getting more done and not telling anyone
because nobody asked.
Kicker: mandates and leverage look identical on a dashboard for about a quarter,
then diverge permanently.
SHOULD BE AT 1:22 LEAVING THIS SLIDE.
-->

---

# Measuring What Matters

<p class="lead">Let me talk you out of a metric first.</p>

---

## The Two Worst Metrics in This Space

<p class="big">Acceptance rate.<br/>Lines of AI-generated code.</p>

- Most reported
- Least useful
- They tell you the tool is **on**
- They tell you nothing about whether it's **working**

> Worse: the moment lines-generated hits a dashboard, you've told your engineers what you reward. They will deliver it.

<!--
1:22 · Open by TAKING SOMETHING AWAY.
Acceptance rate: high might mean suggestions are great. Might mean people stopped
reading them carefully. Opposite situations, IDENTICAL NUMBERS.
Lines-of-AI-code is worse than useless — actively harmful.
You WILL get more lines of code. Enthusiastically. Not the same as more value,
and by the time you notice, the codebase is full of it.
-->

---

## The Three Questions the Business Actually Asks

**1. Are we delivering more value, faster?**
Lead time, throughput, cycle time on work that matters

**2. Are we delivering it safely?**
Change failure rate, defect escape, security findings, review depth

**3. Is it worth what we're paying?**
Cost per unit of outcome, adoption *depth*, where value concentrates

<p class="big">If a metric doesn't answer one of these three — delete it.</p>

<!--
DELETE, not "deprioritize."
Kicker: if your dashboard has fourteen metrics and four answer these questions,
you have ten metrics costing you attention and buying you nothing.
-->

---

## Reading Them Honestly

**On question 1:** look for *shape* changes, not averages. The biggest real effect is usually that **the slow tail gets shorter**.

**On question 2:** these are non-negotiable companions. If speed went up and safety went down, you didn't get faster — you moved work downstream where it costs more.

**On question 3:** value is rarely evenly distributed. That's a **finding**, not a failure.

<!--
Q1: the real effect isn't a faster median — it's tasks that took three days
    because someone was STUCK now taking four hours. Small wobble in the mean. Not small.
Q2: speed up + failure rate up = you didn't get faster, you took out a LOAN.
Q3: two teams getting enormous benefit, six getting little — tells you where to look
    and what to replicate. Most orgs average it away and learn nothing.
-->

---

## Two Principles

**Measure the system, not the individual.**
Individual AI-usage metrics destroy trust faster than any efficiency gain justifies — and they don't survive contact with reality anyway. Team and org level only.

**Pair every quantitative metric with a qualitative one.**
DevEx surveys tell you *why* the numbers moved months before you could infer it.

> The usage API tells you what happened. Your engineers tell you what it means.

<!--
Individual metrics: destroy trust faster than any efficiency gain could justify,
AND they don't work — they don't survive contact with how differently work is shaped.
Team and org level. That's it.
Close: you need both, and only ONE of them is on a dashboard.
-->

---

## Be Careful With the Word "Productivity"

Most of what teams actually gain isn't more output per hour.

<p class="big">It's less time stuck.</p>

- Less time on boilerplate
- Less time lost in an unfamiliar codebase
- Less *"I know this is a two-line fix, I just don't know which two lines"*

> That shows up as **reduced variance and shorter tails** long before it shows up in a velocity chart.

<p class="lead">Measure only the average and you will miss the win and conclude it didn't work.</p>

<!--
MOST REPEATABLE LINE FOR THEIR LEADERSHIP. Slow.
The specific misery: "I know this is a two-line fix, I just don't know WHICH two lines."
Shows up as REDUCED VARIANCE and SHORTER TAILS long before a velocity chart moves.
The failure mode to avoid: orgs that measured only the average, concluded it didn't work,
and walked away from something that was genuinely helping them. I've watched it happen.
-->

---

## Three Takeaways

**1. Route work to the right surface**
Most "Copilot doesn't work for this" is a routing mistake, not a capability limit

**2. Context is the product**
The gap between teams isn't which model they're on — it's what their tools can see

**3. Adoption is a workflow problem, not a license problem**
Seats are layer one of four

---

<!-- _class: lead -->

# The interesting question stopped being<br/>*"can AI write this code."*

<p class="big">It's "where does this work belong,<br/>and can I tell if it's right?"</p>

<p class="lead">Everything else is implementation detail.</p>

<!--
PAUSE BEFORE THIS SLIDE. Let the room settle. Then deliver it clean.
Then: "Thank you." Stop talking.
-->

---

## Questions

Things worth asking your own org this week:

- Which surface is our team **not** using that they should be?
- What's the highest-value internal system Copilot currently **can't see**?
- Is our code review agent running by default, or by memory?
- What's the one metric on our dashboard that answers none of the three questions?
- Which team is already getting 40%, and why is nobody else watching them?

<p class="small">Backup close: "Pick one workflow. Pick the right surface. Give it the context it needs. Measure the tail, not the average."</p>

<!--
Leave this slide up for the whole Q&A. It gives people something to think about
if nobody wants to go first.
"Happy to take anything — including the uncomfortable ones. Especially those."

LIKELY Qs (full answers in the script appendix):
 blind acceptance · juniors + learning path · MCP security review
 realistic ROI · does this replace developers · keeping instructions from rotting

PUNT LINE for pricing/licensing/roadmap:
"Whatever I tell you today will be wrong by next quarter. Grab me after."
-->
