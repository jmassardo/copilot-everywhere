# Copilot Everywhere — 90 Minute Session Plan

> Working title options:
> - **"Copilot Everywhere: Picking the Right Surface for the Right Work"**
> - **"Beyond the Editor: Copilot as a Workflow, Not a Tool"**
> - **"Meet Developers Where They Are"**

**Format:** 90 minutes, ~72 min content / 10 min Q&A / 8 min slip buffer
**Audience:** Mixed experience, skewing advanced. Developers, platform leads, PMs.
**Promise to the audience:** Leave knowing *which mode fits which workflow*, and how to roll it out to people who work differently from each other.

---

## Structural devices

Three things that carry the whole talk. Set them up early.

### 1. The cold-open agent task (minute 3)
Assign a real issue in your demo repo to the cloud coding agent on camera, in the first five minutes. Say out loud: *"We'll check on that around minute 60."* Then move on.

Why it works: it proves asynchrony without explaining asynchrony, it gives the room a reason to stay, and it buys you a guaranteed-interesting payoff later. Pick an issue that's real but low-risk — a test gap, a doc fix with code changes, a small refactor.

**Fallback:** have a completed PR from the same issue already open in another tab. If the live run stalls, cut to it.

### 2. The Surface/Work matrix
One slide, referenced repeatedly. Every demo should end with you pointing at a cell on it. This is your anti-sales-pitch device — it's a *decision tool*, not a feature list.

|  | Synchronous | Asynchronous |
|---|---|---|
| **You hold the context** | IDE inline/chat, CLI | — |
| **Repo holds the context** | dotcom chat, Copilot app | Coding agent, code review |
| **Org holds the context** | Spaces / knowledge bases | Agent + org instructions |

### 3. The running example
Use **one repository** for every demo. Different surface, same codebase. This is what makes the "consistency" claim land — the audience watches context carry across surfaces instead of hearing you assert that it does.

Pick a repo with: a real test suite, some CI, at least one MCP-able external dependency, and enough mess to be believable.

---

## Agenda with timings

| Time | Block | Minutes |
|---|---|---|
| 0:00 | Cold open + framing | 6 |
| 0:06 | What Copilot actually is (mental model) | 7 |
| 0:13 | When *not* to reach for it | 8 |
| 0:21 | Surface map — rapid fire | 9 |
| 0:30 | Personas + deep demos | 26 |
| 0:56 | Cold-open payoff | 4 |
| 1:00 | The context supply chain | 13 |
| 1:13 | What effective implementation looks like | 9 |
| 1:22 | Measuring what matters | 6 |
| 1:28 | Close | 2 |
| 1:30 | Q&A | — |

Q&A runs past the hour if the room stays. Don't promise it inside the 90.

---

# Block-by-block talk track

## 0:00 — Cold open + framing (6 min)

**Do this first, before any slides.** Share screen on github.com, open a real issue, assign it to the coding agent, walk away from it.

> "That's going to run while we talk. We'll come back to it. I want you to notice that I didn't open an editor to start it."

Then the framing slide.

**Talk track:**

The pitch you've heard is "Copilot is an AI pair programmer." That was true in 2022 and it's now the least interesting thing about it. A pair programmer sits next to you. What's actually happened is that Copilot stopped requiring you to be sitting anywhere in particular.

Today it shows up in your editor, in your terminal, in a browser tab, in a pull request review, on your phone, and increasingly *without you present at all*. Same underlying capability, radically different ergonomics — and the ergonomics are the whole ballgame. Choosing the wrong surface for a task is the single most common reason people conclude "this doesn't work for my workflow."

So this session is not a feature tour. It's a *routing* problem. Given a piece of work, where should it go?

**Set expectations explicitly:**
- Demos are live against a real repo. Some will be imperfect. That's the point.
- If you're advanced: the customization and measurement blocks are where your value is.
- If you're new: the persona block is where yours is.

---

## 0:06 — What Copilot actually is (7 min)

Resist defining Copilot by its features. Define it by its three variables.

**The mental model slide — every Copilot interaction is three things:**

1. **Context** — what it can see (your open file, your repo, your org's knowledge, live systems via MCP)
2. **Autonomy** — how far it runs before checking in (completion → chat → agent → fully async)
3. **Surface** — where you meet it, which determines the first two more than people realize

> "The surfaces aren't different products. They're different default settings on those first two dials."

**Why this framing matters for this room:** it makes the rest of the talk predictive rather than descriptive. Once you know a surface's context scope and autonomy ceiling, you can reason about tasks you've never tried.

**Quick calibration on autonomy levels** (name them, you'll reuse the vocabulary all talk):

| Level | What it does | You are... |
|---|---|---|
| Completion | Predicts the next edit | Driving |
| Chat / Ask | Answers, you apply | Driving |
| Edit | Proposes multi-file diffs | Approving |
| Agent | Plans, edits, runs, iterates | Supervising |
| Async agent | Same, without you in the loop | Reviewing |

Say plainly: **most teams are stuck at levels 1–2 and think that's the product.** The delta in value between level 2 and level 4 is larger than the delta between no Copilot and level 2.

---

## 0:13 — When *not* to reach for it (8 min)

This is your credibility block. Be specific and opinionated. Vague disclaimers ("always review the output!") read as legal boilerplate. Named failure modes read as experience.

**Frame it as a cost model, not a rule list:**

> "Every Copilot interaction costs you two things: tokens, and the review effort to verify what came back. The tool is a bad deal whenever verification costs more than doing it yourself."

**Six places where verification cost exceeds the work.** Pick 4–5 to say out loud, leave all six on the slide.

1. **Work where you can't articulate "done."** If you can't write the acceptance criteria, the agent can't hit them, and you'll burn more time in review loops than you'd have spent thinking. *Fix: use Copilot to draft the criteria first, in a separate session, then start over.*

2. **Load-bearing decisions with long half-lives.** Schema design, auth models, public API contracts, service boundaries. Not because the model can't reason about them — it reasons about them fine — but because a plausible-sounding wrong answer here costs you eighteen months. Use it as a challenger, not an author.

3. **Anything where the codebase is the wrong teacher.** The agent pattern-matches your existing code. If your repo is full of the pattern you're trying to get away from, you're paying it to entrench the thing you're fixing. *This is the one that bites platform teams hardest.*

4. **Debugging where you haven't reproduced the bug.** Agents are excellent at fixing a failing test and terrible at finding out why prod is weird at 3am. Get to a reproduction first, then hand it over. Reproduction is the human's job.

5. **Genuinely novel work with no prior art.** Not "new to you" — new to the world. Rare, but when you're there, the tool is a fluent, confident distraction.

6. **Compliance-critical output you can't attribute.** If you'd have to explain the provenance of a given line to an auditor, know your org's policy before, not after.

**The nuance that earns the advanced room:**

> "Notice that none of those are 'Copilot isn't smart enough.' They're all about *where the verification burden lands*. That's a workflow design problem, and it's solvable. Most of what looks like a model limitation is actually a routing mistake."

Land the reframe: the question isn't "can Copilot do this?" It's "**can I cheaply tell whether it did it right?**" Cheap verification — a test suite, a type checker, a linter, a repro case — is what converts a risky task into a safe one. **Teams with strong verification infrastructure can safely give Copilot dramatically more autonomy.** That's the real prerequisite nobody talks about, and it's a good foreshadow of the implementation block.

---

## 0:21 — Surface map, rapid fire (9 min)

**Do not linger here.** One slide, then ~60–90 seconds of live motion per surface. You are establishing existence and ergonomics only. Depth comes in the persona block.

For each: *what it sees*, *how far it runs*, *the one thing it's uniquely good at*.

| Surface | Sees | Autonomy | Uniquely good at |
|---|---|---|---|
| **IDE — inline & chat** | Open files, workspace | Low–mid | Tight loops where you already have the context loaded |
| **IDE — agent mode** | Workspace, terminal, tools | High | Multi-file changes you want to watch happen |
| **CLI** | Filesystem, shell, MCP | High | Anything that isn't one repo in one editor — multi-repo, scripting, piping, headless |
| **Coding agent (cloud)** | Repo, CI, issue context | Async | Work you want to *delegate* and review as a PR |
| **Code review** | The diff + repo context | Async | First-pass review consistency; catching the boring stuff before a human looks |
| **github.com chat** | Repos, issues, PRs, org knowledge | Low–mid | Questions about code you haven't cloned |
| **Copilot app** | Repos, issues, your work | Mid | Triage, backlog work, and thinking away from a keyboard |
| **Spaces / knowledge** | Curated context you define | — | Making org-specific context reusable across all of the above |

**The line to say here:**

> "The CLI and the cloud agent are the powerhouses — that's where the leverage is. But the reason this matters at an org level isn't the powerhouses. It's that the person who only ever opens a browser and the person who lives in tmux are getting the same assistant with the same context. Consistency across surfaces is the feature. Everything else is packaging."

**Rapid-fire demo order** (~90 sec each, three only — resist doing all eight):
1. CLI: one command, non-trivial result
2. github.com chat: ask a question about a repo you have not cloned
3. Code review: open a PR that already has agent comments on it

The rest get covered organically in the persona block. Say so.

---

## 0:30 — Personas + deep demos (26 min)

**Open with the persona slide, then go one at a time.** ~6 minutes each for four personas. This is the heart of the talk.

For each persona use the same three-beat structure — it builds a rhythm the audience can follow:
**Beat 1:** the job they're actually trying to do (30 sec)
**Beat 2:** live demo (3–4 min)
**Beat 3:** point at the matrix, name the surface and *why* (1 min)

---

### Persona 1 — Senior / staff engineer
*Surfaces: CLI + code review*

**The job:** Changes that span more repos than you can hold in your head, in an environment where you already know exactly what you want.

**Demo A:** A cross-cutting change across multiple repos from the terminal — a dependency upgrade with API breakage, or applying a lint rule and fixing the fallout. Show it running, show it using the test suite as its own feedback signal.

**Optional beat:** Piping. `git diff | copilot -p "..."`. Composability is the CLI's real superpower and it's what earns the terminal-dwellers in the room.

**Demo B:** Push the change, open a PR, show the agent review on it. **The continuity is the point** — this is the change you just made, not a separate example. Show what it caught and, honestly, what it missed.

Frame review as *triage, not judgment*: a first pass so humans spend attention on design instead of nitpicks. The unglamorous argument is that review latency is usually the largest single chunk of dead time in a delivery pipeline and nobody optimizes it because it's nobody's job.

**Why this surface:** You have the context, you don't need a UI, and the work escapes a single workspace. The CLI is the only surface where Copilot composes with the rest of your tooling.

**The routing beat worth saying out loud:** the same person doing the same piece of work moved cells on the matrix the moment it went from "I'm doing this" to "someone should check this."

---

### Persona 2 — Platform / developer experience lead
*Surfaces: MCP + org-level configuration*

**The job:** Making the other 200 engineers faster without sitting next to each of them. This person's output is *leverage*, not code.

**Demo:** Wire up an MCP server live and show Copilot reaching a system it couldn't see thirty seconds ago — observability data, an internal service catalog, a ticketing system, your cloud provider. Then run a task that could not have been done without it.

**The advanced beat:** Show that the *same* MCP config and the *same* instructions now apply in the IDE, the CLI, and the cloud agent. Platform teams build context once and it propagates.

**Why this surface:** MCP is where "Copilot knows our codebase" becomes "Copilot knows our *company*." For a platform audience this is the highest-leverage thing in the entire product.

---

### Persona 3 — Product manager / business analyst
*Surfaces: Copilot app + github.com*

**The job:** Turning a fuzzy idea into a backlog that engineers don't hate.

This is the persona most likely to be underserved in the room, and the one where you can most easily surprise people. Do not apologize for it or treat it as the "non-technical" slot — the framing is **dev-adjacent**, and it's a deliberate word choice worth making explicit on stage.

**Demo:** Start from a real spec or a messy doc. Decompose into an epic with issues. Show it *reading the actual codebase* to inform the breakdown — that's the part that separates this from any generic AI writing tool.

> "The difference between this and pasting your spec into a chatbot is that this one has read the code. It knows that thing you're asking for touches the billing service, because it can see the billing service."

**The advanced beat:** Create the issues, then assign one straight to the coding agent. A PM just opened a PR without writing code. Let that sit for a second — for a lot of rooms this is the moment the talk lands.

**Why this surface:** No local environment, no clone, no terminal. The barrier to entry is a browser or a phone, and the context is still real.

---

### Persona 4 — DBA / analytics engineer / data scientist
*Surfaces: github.com + CLI + SQL*

**Put this one last deliberately. It complicates everything the first three established, and that's its job.**

**The job:** A schema you didn't design, data you didn't generate, queries somebody wrote in a hurry three years ago before leaving.

**Demo — three beats:**
1. **Read the schema on github.com.** No clone, no database connection. "Explain this data model and what could go wrong at query time."
2. **The money mismatch.** Ask it to compare the schema against the application's models. The warehouse stores money as a float; the app uses integer cents. **Neither codebase knows.** This bug is invisible from inside either one — it's only visible from a vantage point that reads both at once.
3. **`EXPLAIN QUERY PLAN`.** The output says `SEARCH o USING AUTOMATIC COVERING INDEX` — SQLite announcing it had to build a throwaway index at runtime because the schema didn't provide one. Add the index; the N+1 shape goes from ~0.96s to ~0.009s.

> "The database has been filing a bug report against itself for three years and nobody read it."

**Then the turn — this is the most intellectually honest moment in the talk:**

> "Every other persona today had a test suite. This one doesn't. A wrong query doesn't throw an exception. It returns a confident, plausible, correctly-formatted, completely wrong number — and that number goes into a dashboard somebody makes a decision from. Software fails loudly. Analysis fails quietly, and then gets presented to leadership."

Apply the earlier thesis honestly and it gives an uncomfortable answer: **where verification is expensive or absent, you get *less* autonomy, not more** — no matter how good the model gets.

Be explicit that this isn't a walk-back. It's the thesis applied to a discipline where the answer comes out different. Land the practical upshot:

> "The highest-value thing a data team can build right now isn't a prompt library. It's reconciliation checks. Those are what make everything else safe to hand off."

**Why this persona:** it's the one that proves the framework is a framework and not a sales pitch. If anyone in the room does data work, this is the moment they decide you're worth listening to — because everyone else sells them the opposite.

---

**Close the block with the honest caveat:**

> "Four personas, and every one of them used a different surface for the same underlying capability. That's not fragmentation — that's the tool meeting each of them where they already work. But notice something else: every demo depended on Copilot knowing things specific to *this* repo and *this* org. That's not free. That's the next section."

---

## 0:56 — Cold-open payoff (4 min)

Go back to the agent task from minute 3.

Review the PR *live and critically*. Don't perform delight. Point at what's good, point at what you'd change, and if it got something wrong, **say so and explain why that's a fixable context problem rather than a model problem** — which sets up the next block perfectly.

> "It's been working the whole time we've been talking. I didn't supervise it. That's the actual shift — not that it writes code, but that some work no longer requires you to be present. And look at where it went wrong: it didn't know our convention for X. That's not the model being dumb. That's me not telling it."

---

## 1:00 — The context supply chain (13 min)

Your differentiated block. **Stay disciplined: this is about how each surface *consumes and resolves* configuration, not about what goes inside the files.** Say that constraint out loud so the room knows you're skipping content deliberately.

**Opening frame:**

> "Everybody's seen a custom instructions file. Fewer people can tell you what actually gets loaded when you type a prompt in the CLI versus agent mode in the IDE versus the cloud agent. That resolution order is the difference between configuration that works everywhere and configuration that mysteriously works on your machine only."

**The mechanism slide — five artifact types, one line each on *purpose*:**

| Artifact | Purpose | Scope |
|---|---|---|
| Repo-wide instructions | Baseline conventions every interaction inherits | Repo |
| Path-scoped instructions | Rules that apply only to matching files | Glob |
| Prompt files | Reusable, invocable task templates | Repo / user |
| Custom agents | Persona + tool restrictions for a mode of work | Repo / user |
| Skills | Packaged domain procedures loaded on demand | Repo / user / plugin |
| MCP servers | Live access to systems outside the repo | Anywhere |

Then move immediately to the part they came for.

**The consumption matrix — which surface reads what:**

Build this live from your own setup rather than trusting a slide you made three weeks ago; the support matrix moves fast. Verify each cell before you present.

| | IDE | CLI | Cloud agent | Code review | dotcom / app |
|---|---|---|---|---|---|
| Repo instructions | | | | | |
| Path-scoped | | | | | |
| Prompt files | | | | | |
| Custom agents | | | | | |
| Skills | | | | | |
| MCP | | | | | |

**Demo — the money shot of this block:** same prompt, same repo, two surfaces. Show the outputs differing *because of what each one loaded*. Then show the loaded-context indicator in each so it's mechanism, not magic.

**Three principles to land:**

1. **Write for the lowest common denominator surface.** Configuration that only works in one surface fragments your org. Put universal conventions where everything reads them; put surface-specific tuning in surface-specific files.
2. **Instructions are a code artifact.** They're reviewed, versioned, and they rot. Treat a stale instruction file like a stale README — because it's worse: it actively misleads an agent that trusts it.
3. **More context is not better context.** Everything you load competes for attention and costs tokens. The skill is *selective* loading — path-scoped rules and on-demand skills beat one enormous always-on file. Say the quiet part: a 400-line instructions file is usually someone's monument to a problem they solved once.

**Tie it back:**

> "Remember the 'when not to use it' list? Half of those failure modes get better when the context supply chain is healthy. The tool didn't change. What it could see did."

---

## 1:13 — What effective implementation looks like (9 min)

**Open with the failure mode**, because everyone in the room has lived it:

> "The most common rollout is: buy licenses, send an email with a link, put 'AI adoption' on a slide, and then wonder in six months why usage is a flat line at 'tab completion.' Seats aren't adoption. Installing the app is table stakes — it's not the project."

**The four layers.** Most orgs do layer 1 and stop.

**1. Access** — licenses, policy, approved surfaces, data governance. Necessary, not sufficient. Do it fast and stop congratulating yourself for it.

**2. Context** — the supply chain from the last block, built deliberately. Repo instructions in your top repos. MCP servers for your critical internal systems. This is platform work with a real backlog, an owner, and a maintenance burden. *If nobody owns it, it doesn't exist.*

**3. Workflow** — the layer that actually moves the needle and the one everyone skips. Copilot has to be *in the path of work*, not adjacent to it:
   - Code review runs on PRs by default, not when someone remembers
   - Issue templates that produce agent-ready issues
   - CI failures that route somewhere useful
   - Prompt files for your genuinely repetitive tasks (release notes, migrations, boilerplate services)
   - Team norms on what gets delegated async vs. done live

**4. Craft** — the practices that separate a team getting 10% from a team getting 40%. Prompt and context discipline, knowing when to start a fresh session, knowing when to *stop* and do it yourself. This spreads socially, not through training decks. **Budget for it: pairing, demos, an internal channel where people post what worked.**

**The organizational point, stated plainly:**

> "You cannot roll this out uniformly, because your people don't work uniformly. The PM and the staff engineer in our demos needed completely different surfaces, different onboarding, and different definitions of success. A single rollout plan optimized for the median developer will underserve both ends. Segment by how people work — which, conveniently, is what the persona exercise was for."

**One concrete recommendation to leave them with:** find the two or three teams already using it hard, make them visible, and let adoption spread laterally. Mandates produce compliance; demonstrated leverage produces adoption.

---

## 1:22 — Measuring what matters (6 min)

**Open by taking something away:**

> "I want to talk you out of a metric. Acceptance rate and lines-of-AI-code are the two most reported and least useful numbers in this space. They tell you the tool is on. They tell you nothing about whether it's working. Worse, the moment you put lines-generated on a dashboard, you've told your engineers what you reward — and they'll deliver it."

**The three questions the business actually asks.** Every metric you keep must answer one of these; anything that doesn't, delete.

**1. Are we delivering more value, faster?**
Lead time for changes, throughput, cycle time on the work that matters. Look for *shape* changes, not just averages — the biggest real effect is usually that the slow tail gets shorter.

**2. Are we delivering it safely?**
Change failure rate, defect escape rate, security findings, review depth. Non-negotiable companion metrics. If speed went up and this got worse, you didn't get faster — you moved the work downstream where it costs more.

**3. Is it worth what we're paying?**
Cost per unit of outcome, adoption *depth* (not seat count), where the value concentrates. You'll usually find it's not evenly distributed — that's a finding, not a failure.

**Two measurement principles worth stating:**

- **Measure the system, not the individual.** Individual productivity metrics on AI usage destroy trust faster than any efficiency gain justifies, and they don't survive contact with reality anyway. Team and org level only.
- **Pair every quantitative metric with a qualitative one.** Developer experience surveys will tell you *why* the numbers moved months before you could infer it from the numbers themselves. The usage API tells you what happened; your engineers tell you what it means.

**The honest close on productivity:**

> "Be careful with the word 'productivity.' Most of what teams actually gain isn't more output per hour — it's less time stuck. Less time on the boilerplate, the unfamiliar codebase, the 'I know this is a two-line fix, I just don't know which two lines.' That shows up as reduced variance and shorter tails before it ever shows up as a bigger number in a velocity chart. If you measure only the average, you will miss the win and conclude it didn't work."

---

## 1:28 — Close (2 min)

Three takeaways, mapped to the audience segments. No summary slide of everything. Say these and stop.

1. **Route work to the right surface.** Most "Copilot doesn't work for this" is a routing mistake, not a capability limit.
2. **Context is the product.** The gap between teams isn't which model they're on — it's what their tools can see.
3. **Adoption is a workflow problem, not a license problem.** Seats are layer one of four.

**Closing line option:**

> "The interesting question stopped being 'can AI write this code.' It's 'where does this work belong, and can I tell if it's right?' Everything else is implementation detail."

---

# Demo prep checklist

**Environment**
- [ ] Demo repo — real tests, real CI, some mess, safe to change publicly
- [ ] Everything authenticated *before* you present. All surfaces. Including the phone.
- [ ] Terminal font 18pt+, high contrast, prompt shortened, scrollback cleared
- [ ] Notifications off — OS, Slack, email, calendar. All of them.
- [ ] Second browser profile with no personal tabs or bookmarks
- [ ] MCP servers verified working *today*, not last week
- [ ] Network fallback: phone hotspot tested

**Per-demo fallbacks** — for every single demo, have a pre-recorded clip or screenshot ready. Non-negotiable for the cold-open agent task.

**Timing rehearsal**
- [ ] Full dry run with a timer. Note actual times per block.
- [ ] Identify your cut list in advance: which persona and which rapid-fire demos drop if you're 10 minutes behind at the halfway mark. Decide *now*, not on stage.
- [ ] Rehearse the recovery line for a failed demo. Something like: *"That's a real failure and it's a useful one — here's what it's telling us."* Then move.

**Content verification** — the support matrix changes constantly:
- [ ] Re-verify the consumption matrix against current behavior the week of the talk
- [ ] Re-verify surface names and availability
- [ ] Check nothing you're demoing has shipped a breaking UI change

---

# Cut list (if you're running long)

In order of what to drop first:
1. Rapid-fire demo #3 (code review) — it reappears in persona 4 anyway
2. Persona 4's second path — you were only doing one
3. The autonomy-levels table in the mental model block — talk it instead of showing it
4. Implementation layer 4 (craft) — compress to one sentence

**Never cut:** the "when not to" block, the context supply chain demo, or the cold-open payoff. Those three are why an advanced audience stays.
