# Copilot Everywhere — Full Presentation Script

**Runtime:** 90 minutes (~72 content / 10 Q&A / 8 buffer)
**Companion deck:** `copilot-everywhere.marp.md`
**Companion plan:** `copilot-everywhere-90min-plan.md`

---

## How to use this script

Prose in normal text is **written to be said out loud**. It's not a summary of what to say — it's the words. Read it aloud during rehearsal, then deliver it from the beats rather than reciting.

- **[STAGE]** — what you're doing, not saying
- **[SLIDE n]** — advance the deck
- **[DEMO]** — leave the deck, go live
- *Italics in brackets* — delivery notes, pacing, emphasis
- **CUT IF BEHIND** — drop this if you're running long

Timings are cumulative and assume you start on time. If you start late, take it out of the rapid-fire block, not out of Q&A.

---

# BLOCK 0 — Cold Open
**0:00–0:06 · 6 minutes**

[STAGE: Do not show the title slide yet. Start on a browser, github.com, your demo repo's issue list. Screen already shared before you speak.]

Good morning. Before I introduce myself or show you a single slide, I want to start something.

[STAGE: Open a real issue in your demo repo. Read the title out loud.]

This is a real issue in a real repository. It's small but it's not fake — it needs a change in a couple of files and it needs the tests to still pass.

I'm going to hand it to Copilot's coding agent.

[STAGE: Assign the issue to Copilot. Let the audience watch the click.]

That's it. That's the whole interaction. It's going to go read the repo, make a plan, write the code, run the tests, and open a pull request. It'll take somewhere between five and fifteen minutes.

We're going to come back to it around minute sixty.

*[Pause. Let that land. Do not oversell it.]*

I want you to notice one specific thing about what just happened, and it's not that AI wrote code. You've all seen AI write code.

**I never opened an editor.**

I wasn't in a terminal. I wasn't in an IDE. I'm not going to sit here and watch it work. And in about an hour, there's going to be a pull request waiting for me that I had almost no involvement in producing.

*[Beat.]*

That's a different thing than what most people mean when they say "AI coding assistant." And that gap — between what people think this is and what it's actually become — is what the next ninety minutes are about.

[SLIDE 1 — Title]

I'm Jenna. Let's talk about Copilot everywhere.

[SLIDE 2 — "First, a delegation"]

That slide is just a bookmark so we remember to come back to it. Moving on.

---

# BLOCK 1 — The Mental Model
**0:06–0:13 · 7 minutes**

[SLIDE 3 — The pitch you've already heard]

Here's the pitch you've heard, probably more than once: *Copilot is an AI pair programmer.*

That was a genuinely useful description in 2022. Today it's the least interesting thing about it, and I'd argue it's actively holding teams back.

Because think about what a pair programmer is. A pair programmer sits next to you. That's the defining characteristic — co-presence. Two people, one problem, same moment in time.

[SLIDE 4 — So this isn't a feature tour]

What's actually happened over the last couple of years is that Copilot stopped requiring you to be sitting anywhere in particular.

It shows up in your editor. It shows up in your terminal. It shows up in a browser tab, in a pull request, on your phone. And increasingly — as we just demonstrated — it shows up **without you present at all.**

Same underlying capability in all of those places. Radically different ergonomics.

And here's the thing I want to convince you of early, because everything else depends on it: **the ergonomics are the whole ballgame.**

*[Slow down here.]*

The single most common reason I hear someone say "yeah, we tried Copilot, it doesn't really work for our workflow" — it's almost never a capability problem. It's that they took a piece of work and put it in front of the wrong surface. They tried to do a twelve-repo migration in an IDE chat window. They tried to do a two-line fix with a full agent. They asked a question about a repository they'd never cloned while sitting in an editor that had never seen it.

So this session is not a feature tour. I'm not going to walk you through a product catalog.

This is a **routing** problem. You have a piece of work. Where should it go?

[SLIDE 5 — Session flow]

Here's where we're headed.

We'll start with a mental model — three dials, not eight products. Then we'll spend real time on when *not* to reach for this, because I think that's where credibility lives. Then the surface map, four personas with live demos, and then the three sections I think are most valuable if you're already using this heavily: how context actually gets loaded, what a real implementation looks like beyond licenses, and how to measure it without lying to yourself.

Two housekeeping notes.

One: the demos are live, against a real repository. Some of them will be imperfect. **That's deliberate.** If I show you eight flawless demos, I've shown you a commercial, and you'll correctly discount everything I say.

Two: this room has a wide range of experience. If you're brand new, the persona block in the middle is your section. If you've been running this hard for a year, the context and measurement blocks at the end are where your value is. Everybody should stay for the "when not to" part.

[SLIDE 6 — Every interaction is three things]

Let's build the model.

I want you to stop thinking about Copilot as a set of features and start thinking about it as three dials. Every single interaction you have with it — every one — is some setting of these three.

**Context.** What can it see? Just the file you have open? Your whole workspace? Your organization's internal documentation? Your production monitoring system?

**Autonomy.** How far does it run before it checks in with you? Does it finish your line, or does it go make eleven file changes and run the test suite twice?

**Surface.** Where do you meet it — and this is the part people underestimate, because **the surface largely determines the first two.**

*[Point at the slide.]*

That's the reframe. The surfaces aren't different products that happen to share a name. They're different **default settings** on context and autonomy.

Why does that matter to you practically? Because it makes this predictive instead of descriptive. Once you know a given surface's context scope and its autonomy ceiling, you can reason correctly about tasks you have *never tried on it*. You don't need me to enumerate use cases. You can derive them.

[SLIDE 7 — The autonomy ladder]

Quick calibration on that middle dial, because I'm going to use this vocabulary for the rest of the talk.

**Level one, completion.** It predicts your next edit. You're driving.

**Level two, chat.** You ask, it answers, you decide what to do with the answer. You're still driving.

**Level three, edit.** It proposes changes across multiple files. Now you're approving rather than driving.

**Level four, agent.** It plans, it edits, it runs commands, it reads the output, it iterates. You're supervising.

**Level five, async agent.** Same as four — without you in the loop. You're reviewing a finished artifact.

**CUT IF BEHIND:** *talk this table rather than showing it — say the five levels in one sentence each and move to slide 8.*

[SLIDE 8 — Where most teams actually live]

Now here's the uncomfortable part.

Most teams — most organizations I talk to — are living at levels one and two. Tab completion and a chat window. And they think **that's the product.** They've evaluated Copilot, they've formed an opinion, and their opinion is based on maybe thirty percent of what's there.

I want to be precise about the size of this gap, because it's easy to hand-wave.

The jump from *no Copilot* to *level two* is real. It's a genuine improvement. Nobody's disputing it.

But the jump from *level two* to *level four* is **bigger**. And most organizations have never made it.

*[Beat.]*

So if you're sitting there and your adoption dashboard shows a nice flat line at "suggestions accepted," I'd gently suggest you haven't found the product yet. You've found the on-ramp.

---

# BLOCK 2 — When *Not* to Reach For It
**0:13–0:21 · 8 minutes**

[SLIDE 9 — Section header: When not to reach for it]

Okay. Before I show you a single additional capability, I want to spend eight minutes on when you shouldn't use this.

I'm doing this early and I'm doing it on purpose. Partly because it's the right thing to do. But mostly because I think you can't trust anybody's advice about a tool until you've heard them describe its limits specifically.

[SLIDE 10 — It's a cost model]

And I want to frame it as a cost model rather than a list of rules, because rules don't generalize and cost models do.

Every interaction you have with Copilot costs you two things.

The first is tokens — compute, money, latency. That one's obvious and it's mostly not the interesting one.

The second is **the review effort required to verify what came back.** And that's the one that actually determines whether this is worth doing.

*[Slow, clear.]*

So here's the whole rule, and everything else is a corollary: **the tool is a bad deal whenever verification costs more than doing it yourself.**

That's it. Not "AI is bad at hard things." Not "don't use it for important code." Just: what does it cost you to find out if it's right?

[SLIDE 11 — Six places, part 1]

Let me give you six places where, in my experience, verification cost exceeds the work.

**One. Work where you can't articulate what "done" means.**

If you cannot write the acceptance criteria, the agent cannot hit them. What actually happens is you get something back, you look at it, you go "no, not quite," you nudge it, you get something else back, and you burn forty minutes in a loop you could have short-circuited by spending five minutes thinking first.

The fix here is not "don't use it." The fix is to use it *differently*: open a separate session, use it to help you draft the acceptance criteria, and then **start over** with a clean context and a clear target.

**Two. Load-bearing decisions with long half-lives.**

Schema design. Auth models. Public API contracts. Service boundaries.

And I want to be careful here, because the naive version of this point is wrong. It's not that the model can't reason about these things — it reasons about them fine, often better than the average whiteboard session.

The problem is asymmetry. A plausible-sounding wrong answer about your service boundaries costs you eighteen months. And "plausible-sounding" is exactly what these systems are best at. Use it as a *challenger* — "here's my design, attack it" — not as an author.

**Three. Work where your codebase is the wrong teacher.**

This one's sneaky and it hits platform teams hardest.

The agent pattern-matches against your existing code. That's usually a feature. But if your repository is full of the exact pattern you are trying to get *away* from, you are now paying a machine to lovingly propagate the thing you're trying to kill.

*[Beat.]*

You've hired a very fast, very confident junior engineer who has read only your worst code and assumed it was intentional.

[SLIDE 12 — Six places, part 2]

**Four. Debugging something you haven't reproduced.**

Agents are outstanding at fixing a failing test. They are genuinely bad at "production is behaving strangely at 3am and I don't know why."

The difference is that a failing test is a *specification of wrongness*. Vague production weirdness isn't. So: get to a reproduction first. **Reproduction is the human's job.** Once you have it, hand it over and go get coffee.

**Five. Genuinely novel work.**

And I mean genuinely — not "new to me," not "new to this team." New to the world. This is rare. Most of us go years between encountering it. But when you're actually there, at the edge of the known, you have a fluent, confident, extremely articulate distraction.

**Six. Compliance-critical output you can't attribute.**

If you would have to explain the provenance of a specific line to an auditor, know your organization's policy **before** you generate it, not after. This is a five-minute conversation with your legal team that some of you have been avoiding for a year.

[SLIDE 13 — Notice what's missing]

Now. *[Pause.]* Look back at those six.

**Not one of them is "the model isn't smart enough."**

Every single one is about *where the verification burden lands.* Whether you can cheaply tell if the output is correct.

And that's important, because "the model isn't smart enough" is not a problem you can solve. You just wait for a better model. But **where the verification burden lands is a workflow design problem.** And workflow design problems are solvable. By you. This quarter.

*[Land it.]*

Which means most of what looks like a model limitation is actually a routing mistake.

[SLIDE 14 — The real question]

So the question to carry for the rest of this talk is not "can Copilot do this?"

It's: **"can I cheaply tell whether it did it right?"**

And when you ask it that way, something useful falls out. Cheap verification has a name, and you already own it. It's your test suite. Your type checker. Your linter. A reproduction case. Your CI pipeline.

Those things are what convert a risky task into a safe one.

*[This is the important line. Slow down.]*

Which means: **teams with strong verification infrastructure can safely give Copilot dramatically more autonomy than teams without it.**

That's the prerequisite almost nobody talks about. Everybody's asking which model is best. Almost nobody's asking whether their test suite is good enough to let an agent run unsupervised. Those are the same question wearing different clothes.

Hold onto that. It comes back in the implementation section.

---

# BLOCK 3 — The Surface Map
**0:21–0:30 · 9 minutes**

[SLIDE 15 — Section header: The surface map]

Alright. Nine minutes on what actually exists. I'm going fast here on purpose — I'm establishing that these things exist and roughly how they feel. The depth comes in the persona block right after.

[SLIDE 16 — The routing matrix]

This is the slide I'm going to keep pointing back at, so let's read it properly once.

Two axes. Across the top: is the work **synchronous** — you're there, waiting — or **asynchronous** — you've handed it off?

Down the side: **who holds the context?** Is it in your head and your open editor? Is it in the repository? Or does it live at the organizational level — your internal docs, your conventions, your systems?

*[Walk the cells briefly.]*

You in the driver's seat with the context loaded, working synchronously — that's your IDE and your CLI. Repo-level context, asynchronous — that's the coding agent and code review. Org-level context — that's where knowledge bases and org-wide configuration come in.

Notice the empty cell: *you* hold the context, asynchronously. That doesn't work, because if the context is only in your head, you can't hand it off. Which is a nice little preview of the entire context section later.

After every demo today I'm going to point at a cell on this. That's the actual takeaway of this talk — not the features, the routing.

[SLIDE 17 — What each surface is uniquely good at]

Here's the full inventory. I'm not reading this table to you. It's in the deck, you'll get the deck.

What I want you to notice is the last column: what is each one *uniquely* good at. Not "what can it do" — almost all of them can do almost everything, badly. What's it uniquely good at.

*[Hit four or five, fast.]*

**IDE inline and chat** — tight loops where you already have the context loaded in your head and in your tabs.

**CLI** — anything that isn't one repository in one editor.

**Coding agent** — work you want to *delegate* and then review as a pull request.

**Code review** — first-pass consistency. Catching the boring stuff before a human spends attention on it.

**github.com chat** — questions about code you haven't cloned. Which, if you work at any reasonably large company, is most of the code.

[SLIDE 18 — The part that actually matters]

Now, the honest version of this.

The CLI and the cloud coding agent are the powerhouses. If you're an individual engineer trying to get maximum leverage, that's where it is. Not close.

**But that's not why this matters at an organizational level.**

*[Slow down.]*

The reason this matters to a platform lead or a VP is that the person who only ever opens a browser and the person who lives in a tmux session are getting **the same assistant with the same context.**

The PM writing an epic and the staff engineer doing a cross-repo refactor are drawing on the same understanding of your codebase.

That consistency across surfaces is the feature. Everything else is packaging.

[SLIDE 19 — Rapid fire]

Three quick ones. Ninety seconds each. Then we go deep.

[DEMO 1 — CLI · ~90 sec]

> **Setup:** terminal already open, clean scrollback, in the demo repo.
> **Goal:** one command, non-trivial result. Not "write me a function."
> **Narrate:** what you're asking for, and specifically what it's *reading* to answer.
> **Land on:** "notice that never left the terminal, and never needed an editor."

[DEMO 2 — github.com chat · ~90 sec]

> **Setup:** browser, a repo you have genuinely never cloned. Say so out loud.
> **Goal:** ask a real architectural question about that repo and get a grounded answer.
> **Land on:** "zero setup. No clone, no environment, no IDE. This is the surface your dev-adjacent folks can actually reach."

[DEMO 3 — Code review · ~90 sec]

> **Setup:** a PR with agent review comments already posted.
> **Goal:** scroll the comments. Point at one good catch. Point at one thing it missed.
> **Land on:** "we'll come back to this properly in persona four."
>
> **CUT IF BEHIND:** drop this one. It reappears later anyway.

[STAGE: Return to deck.]

Those were three of eight. The other five you'll see in context over the next twenty-five minutes, which is a much better way to see them.

---

# BLOCK 4 — Four Personas
**0:30–0:56 · 26 minutes**

[SLIDE 20 — Section header: Four personas]

Here's the structure of this block, so you know what you're in for.

Four personas. Four different surfaces. And critically — **one codebase.** Same repository every single time. Because the claim I just made, that the consistency is the feature, is a claim I should demonstrate rather than assert.

[SLIDE 21 — Who we're following]

Same three beats for each one. What's the job they're *actually* trying to do — not the feature, the job. Then a live demo. Then we go back to the matrix and I tell you which cell and why.

One note on the last one. I've put the data person last on purpose, because that persona is going to **complicate** everything I tell you in the first three. Hold that thought.

---

## Persona 1 — Senior / Staff Engineer
**~6 minutes**

[SLIDE 22 — Persona 1]

First one's the easiest for this room.

**The job:** you have a change that spans more repositories than you can hold in your head at once. And crucially — you already know exactly what you want. You're not exploring. You don't need help thinking. You need help *typing*, across twelve places, without making a mistake in the ninth one.

This is the CLI's home turf.

[DEMO 4 — CLI cross-repo change · ~4 min]

> **Setup:** multiple repos available locally. Terminal at 18pt+.
> **Task:** a dependency upgrade with real API breakage, or applying a lint rule and fixing the fallout.
> **Critical beat:** show it *running the test suite* and using the failures as its own feedback signal. Narrate that explicitly — "it just failed, and it's reading its own failure."
>
> **The advanced beat — pick ONE:**
> - Piping. `git log --oneline -20 | copilot -p "..."`. This is the one that earns the terminal people.
> - A custom agent scoped to this task
> - Running headless inside a script
>
> **Fallback:** pre-recorded clip of the same run.

[STAGE: Back to deck, or stay on slide 22.]

So — why this surface.

You already had the context. You didn't need a UI to help you think. And the work escaped a single workspace, which immediately disqualifies anything editor-shaped.

But the real reason, and the thing I want the terminal people in this room to hear: **the CLI is the only surface where Copilot composes with the rest of your tooling.** It has standard input and standard output. It goes in a pipe. It goes in a script. It goes in a loop. Everything else is a destination; this one's a component.

*[Point at matrix.]* Top left. You hold the context, synchronous.

*[Beat — transition, don't treat this as a new topic.]*

But I'm not done with this persona, because making the change is only half of what this person's day looks like. The other half is **what happens when they try to ship it.**

[DEMO 5 — Agent review on the same PR · ~2 min]

> **Setup:** push the branch from demo 4, open a PR, agent review has already run.
> The continuity matters — this is *the change we just made*, not a different example.
>
> - Point at a genuine catch, something a human would plausibly miss
> - **Point at something it missed.** Out loud.
>
> **Fallback:** a PR from the same change, already reviewed, in another tab.

[STAGE: On the review comments.]

The framing I'd push for here: this is **triage, not judgment.**

It is not reviewing your code. It's doing the first pass so that when a human shows up, they're spending attention on design and correctness instead of "you forgot a null check" and "this variable name is misleading."

*[Point at the miss.]*

And it missed that. Which I'd rather show you than hide, because the version of this talk where the review catches everything is a version you'd correctly distrust.

I'd argue this is the fastest ROI available to most teams, for an unglamorous reason: **review latency is usually the largest single chunk of dead time in your delivery pipeline, and nobody's optimizing it because it's nobody's job.**

*[Point at matrix.]* And notice this one moved — middle row, right column. Same person, same piece of work, **different cell.** The routing changed the moment the work went from "I'm doing this" to "someone should check this."

---

## Persona 2 — Platform / DevEx Lead
**~6 minutes**

[SLIDE 23 — Persona 2]

Second persona. If you're in this role, this is your section.

**The job:** making the other two hundred engineers faster without sitting next to each of them. Your output isn't code. Your output is **leverage.**

And the single highest-leverage thing available to you right now is MCP — because it's the mechanism by which Copilot stops being limited to what's in the repository.

[DEMO 6 — MCP wire-up · ~4 min]

> **Setup:** an MCP server you can connect live. Observability, service catalog, ticketing, cloud provider — whatever's real for your demo.
> **Beat 1:** ask a question it *cannot* answer. Let it fail or hedge.
> **Beat 2:** wire up the server. Live.
> **Beat 3:** same question. Now it answers.
> **Beat 4 — the advanced one:** show that the same configuration now applies in the IDE, the CLI, *and* the cloud agent. Build once, propagates everywhere.
>
> **Fallback:** this is your highest-risk demo. Have a recording.

[STAGE: Back to deck.]

That transition — from "I can't see that" to "here's the answer" — took thirty seconds of configuration. And it applies to every surface simultaneously.

Here's why I think this is the most important thing in the product for a platform audience.

*[Slow.]*

MCP is where **"Copilot knows our codebase"** becomes **"Copilot knows our company."**

Your codebase is maybe forty percent of the context an engineer needs to do their job. The rest is: what's currently broken, who owns this service, what did we decide in that design review, what's the actual state of production. None of that is in the repo. All of it is in systems that MCP can reach.

*[Point at matrix.]* This one's the bottom row — org-level context. And it's the row most organizations have completely empty.

---

## Persona 3 — Product Manager / Business Analyst
**~6 minutes**

[SLIDE 24 — Persona 3]

Third persona, and I want to set this up carefully because it's the one most likely to get dismissed in a room like this.

**The job:** turning a fuzzy idea into a backlog that engineers don't hate.

*[Beat.]*

And a word choice, because I think it matters: I don't call these roles "non-technical." I call them **dev-adjacent.**

*[Beat.]*

"Non-technical" defines a person by what they aren't, and it's usually wrong anyway — the PM who knows exactly which service a request lands in is technical, they just don't commit. Dev-adjacent says something more accurate: you work *next to* the code, you're affected by it, you shape it — you're just not the one merging it.

And that distinction turns out to be operationally useful, not just polite. Dev-adjacent people need real context about the codebase. They just need to reach it without a clone and a build environment.

So — decomposing an ambiguous requirement into well-scoped work is genuinely hard, most people are bad at it, and when it's done badly it costs your engineering org more than any refactor.

[DEMO 7 — Spec to backlog · ~4 min]

> **Setup:** Copilot app or github.com. A real, messy spec or doc.
> **Beat 1:** decompose into an epic with issues.
> **Beat 2 — THE critical one:** show it referencing the *actual codebase* in the breakdown. Point at the specific line where it names a real service or file.
> **Beat 3 — the advanced beat:** create the issues, then assign one straight to the coding agent.
>
> **Fallback:** screenshots of each beat.

[STAGE: On beat 2, say this.]

*[Point at the screen.]*

**This** is the difference between what you just watched and pasting your spec into a general-purpose chatbot.

This one has read the code.

It knows the thing you're asking for touches the billing service — because it can see the billing service. It knows there's already a half-finished implementation of something similar, because it found it. That's not a writing tool. That's a tool that has the same context your engineers have.

[SLIDE 24, advanced beat]

And then — watch this.

[STAGE: Assign a generated issue to the coding agent.]

*[Pause. Let it sit.]*

A product manager just opened a pull request. Without writing code. Without cloning anything. Without opening an editor.

*[Beat.]*

I'm not claiming that PR is going to be perfect, or that it merges without review. It won't and it shouldn't. But the distance between "I have an idea" and "there is code to react to" just collapsed from a sprint to a coffee break — and for a lot of organizations, *that specific gap* is the actual bottleneck. Not typing speed.

*[Point at matrix.]* Middle row — repo holds the context. And it spans both columns, sync and async, which is unusual.

Why this surface: no local environment. No clone. No terminal. The barrier to entry is a browser or a phone — and the context is still completely real.

---

## Persona 4 — DBA / Analytics Engineer
**~6 minutes**

[SLIDE 25 — Persona 4]

Last persona, and I saved it for last deliberately, because this one **complicates everything I've told you so far.**

**The job:** you own a schema you didn't design, data you didn't generate, and a set of queries somebody wrote in a hurry three years ago before they left the company.

[DEMO 8 — Schema, mismatch, query plan · ~4 min]

> **Beat 1 — dotcom chat, no clone, no DB connection:**
> "Read this schema. Explain the data model and what could go wrong at query time."
>
> **Beat 2 — the money mismatch. This is the one.**
> "Compare the schema with the application's models. Where do they disagree?"
> Warehouse stores money as a float. Application uses integer cents.
>
> **Beat 3 — `EXPLAIN QUERY PLAN`:**
> Output says `SEARCH o USING AUTOMATIC COVERING INDEX`.
> Add the index. The N+1 shape goes from ~0.96s to ~0.009s.
>
> **Fallback:** screenshots of all three beats.

[STAGE: On beat 2.]

*[Slow down here.]*

The warehouse stores money as a floating-point number. The application uses integer cents. Somebody, somewhere, is doing a lossy conversion — and **neither codebase knows.**

You cannot see this bug from inside the application. You cannot see it from inside the database. It is only visible from a vantage point that can read both at once.

*[Beat.]*

That's not a clever AI trick. That's just what happens when the thing helping you isn't confined to the file you have open.

[STAGE: On beat 3.]

And look at what the database just told us. `AUTOMATIC COVERING INDEX`. SQLite is saying, in plain language, *"I had to build an index at runtime, every single time you ran this, because your schema didn't give me one."*

The database has been filing a bug report against itself for three years and nobody read it.

[SLIDE 26 — The persona that breaks the pattern]

Now. Here's why this persona is last.

*[Slow. This is the most intellectually honest moment in the talk.]*

Every other persona today had a test suite. Run it, get the truth in one second. That's what made it safe to hand an agent a twelve-repo refactor.

**This person doesn't have that.**

A wrong query doesn't throw an exception. It doesn't turn CI red. It returns a **number.** A confident, plausible, correctly-formatted, completely wrong number — and that number goes into a dashboard that somebody makes a decision from.

Software fails loudly. **Analysis fails quietly, and then gets presented to leadership.**

*[Beat.]*

So go back to what I told you forty minutes ago: cheap verification is what buys autonomy.

Apply it honestly here, and it gives you an uncomfortable answer. **Where verification is expensive or absent — which is most of data work — you get *less* autonomy. Not more.** No matter how good the model gets.

I want to be clear that I'm not walking back the thesis. I'm applying it. And the practical upshot is the useful part:

> The highest-value thing a data team can build right now is not a prompt library. It's **reconciliation checks.** Those are what make everything else safe to hand off.

*[Point at matrix.]* And this persona doesn't sit in one cell — dotcom for reading the schema, CLI for the query work. Which is the whole argument about routing, one more time.

---

[SLIDE 27 — What just happened]

Okay. Step back.

Four personas. Four completely different surfaces. **One underlying capability**, one codebase.

That's not fragmentation. That's the tool meeting each of those people where they already work — which is the only kind of adoption that actually sticks, because it doesn't ask anyone to change their habits before they've seen value.

But I want you to notice something else about those four demos.

*[Beat. This is the pivot into the second half of the talk.]*

**Every single one of them depended on Copilot knowing things specific to *this* repository and *this* organization.**

The cross-repo refactor needed to know our conventions. The MCP demo was *entirely* about external context. The PM demo only worked because it could read the actual services. The review demo only caught what it caught because it knew what our code is supposed to look like.

None of that is free. None of that arrived in the box.

*[Beat.]*

And that's the next section. But first —

---

# BLOCK 5 — The Cold Open, Revisited
**0:56–1:00 · 4 minutes**

[SLIDE 28 — The cold open revisited]

Let's go see what happened to that issue.

[DEMO 9 — Review the agent's PR · ~3 min]

> **Critical delivery note: do NOT perform delight.** No "wow, look at that!" The room will smell it instantly and you'll lose everything you built in the "when not to" block.
>
> Review it the way you'd review a colleague's PR:
> - Read the description
> - Look at the diff honestly
> - Name one thing that's good and *why*
> - **Name one thing you'd change**
> - Check whether the tests actually pass
>
> **Fallback:** a completed PR from the same issue, already open in another tab.

[STAGE: While reviewing.]

So this has been running the entire time we've been talking. About fifty-five minutes. I didn't supervise it. I didn't check on it. I gave it an issue and went and did something else.

*[On the diff:]*

This part's good — and here's specifically why. *[Name it. Be concrete.]*

This part I'd change. *[Name it.]*

[SLIDE 29 — What the agent got wrong]

And I want to dwell on that second one for a second, because it's the most useful thing in this whole talk.

*[Slow.]*

It didn't know our convention for that.

**That is not the model being dumb.**

**That is me not telling it.**

*[Beat.]*

Nobody wrote that convention down anywhere the agent could reach. It's in three people's heads and one Slack thread from last March. The agent did exactly what a competent new hire would do on day one with no onboarding: it made a reasonable guess based on the surrounding code.

So the shift here isn't that it writes code. It's that **some work no longer requires you to be present.** And the moment work doesn't require you to be present, everything you *would* have said in the moment has to exist somewhere else, in writing, where it can be loaded.

Which brings us to the most under-discussed part of this entire space.

---

# BLOCK 6 — The Context Supply Chain
**1:00–1:13 · 13 minutes**

[SLIDE 30 — Section header: The context supply chain]

[SLIDE 31 — The gap]

Here's my honest read on where the collective knowledge is right now.

Everybody in this room has seen a custom instructions file. It's the first thing anyone does. You write some conventions down, you commit it, you feel good.

**Far fewer people can tell me what actually gets loaded** when they type a prompt into the CLI, versus agent mode in an IDE, versus the cloud coding agent running on its own.

*[Beat.]*

And that resolution order — what's read, by which surface, in what precedence — is the difference between configuration that works everywhere and configuration that mysteriously only works on your machine.

I want to be explicit about a constraint I'm putting on this section, because it's the opposite of how this topic usually gets covered.

**I am not going to open a single one of these files.** We're not doing "here's what good instructions look like." There are a hundred blog posts about that, and honestly most of you have written better ones than I would.

What almost nobody covers — and what actually determines whether your configuration works — is **how each surface consumes these artifacts.** That's the whole section.

[SLIDE 32 — The artifacts, purpose only]

Six things. One line each. Purpose and scope only.

**Repo-wide instructions.** Baseline conventions that every interaction inherits. Repo scope.

**Path-scoped instructions.** Rules that only apply to files matching a pattern. Glob scope. This one's underused and we'll come back to it.

**Prompt files.** Reusable task templates you explicitly invoke.

**Custom agents.** A persona plus a set of tool restrictions, for a particular mode of work.

**Skills.** Packaged domain procedures, loaded on demand rather than always-on.

**MCP servers.** Live access to systems outside the repository.

That's the vocabulary. Now the part you came for.

[SLIDE 33 — The consumption matrix]

Which surface reads what.

*[Walk through your actual matrix — built the week of the talk.]*

> **PREP NOTE:** Fill this in from your own verified setup within a week of delivery. Do not present cells you haven't personally tested. If a cell is uncertain, say "I haven't verified this one" — that's far better than being confidently wrong on your most authoritative slide.

Two things to notice as I walk this.

First — the coverage isn't uniform. Some artifacts are read by everything. Some are surface-specific. If you put a critical convention in a surface-specific artifact, you've just created a class of engineer for whom your standards silently don't apply.

Second — this matrix moves. Fast. What I'm showing you is verified as of this week. If you're watching a recording of this, go check it yourself. That's not a disclaimer, that's the actual operating advice: **this is a thing you re-verify, not a thing you learn once.**

[DEMO 10 — Same prompt, two surfaces · ~3 min]

> **This is the money shot of the block. Rehearse it hardest.**
>
> - Same prompt. Same repository. Two surfaces.
> - Outputs differ.
> - Then reveal *why*: show the loaded-context indicator in each.
>
> **Land on:** "mechanism, not magic."

[STAGE: Back to deck.]

Same words. Same repo. Different answers. And the reason isn't randomness or temperature — it's that those two surfaces loaded different things before they saw my prompt.

Once you can see that, you can debug it. Before you can see it, it just feels like the tool is inconsistent.

[SLIDE 34 — Three principles]

Three things I'd take from this.

**One: write for the lowest common denominator surface.**

If your configuration only works in one surface, you've fragmented your organization along a line nobody chose. Universal conventions go where *everything* reads them. Surface-specific tuning goes in surface-specific files, and you should be able to justify why each one is surface-specific.

**Two: instructions are a code artifact.**

They get reviewed. They get versioned. And — this is the part people miss — **they rot.**

A stale instruction file is worse than a stale README. A stale README misleads a human, who will probably notice something's off. A stale instruction file misleads an agent that has no independent basis for doubting it and will confidently propagate the mistake across forty files.

**Three: more context is not better context.**

Everything you load competes for attention and costs tokens. The skill here is *selective* loading — path-scoped rules that fire only when relevant, skills that load on demand — not one enormous always-on file.

*[Lighter delivery.]*

I'll say the quiet part. A four-hundred-line instructions file is usually a monument. Somebody hit a problem once, added forty lines to make sure it never happened again, and now every single interaction in that repository pays for it forever. Go read yours. Half of it is archaeology.

[SLIDE 35 — Tie it back]

And here's why I put this section after the failure modes instead of before.

Go back to those six places where verification costs too much.

**Half of them get better when the context supply chain is healthy.**

"You can't articulate done" — better when your conventions are written down. "The codebase is the wrong teacher" — that's *exactly* what instructions are for; you can explicitly tell it which patterns are deprecated. The agent not knowing your standards — that's not a capability gap, that's an unwritten-knowledge gap.

*[Land it.]*

The tool didn't change.

**What it could see did.**

---

# BLOCK 7 — Effective Implementation
**1:13–1:22 · 9 minutes**

[SLIDE 36 — Section header]

[SLIDE 37 — The rollout you've probably seen]

Let me describe a rollout. Tell me if it sounds familiar.

Step one: buy licenses. Step two: send an email with a link to the docs. Step three: put "AI adoption" on a slide for the leadership review. Step four: six months later, wonder why the usage dashboard is a flat line at tab completion.

*[Beat.]*

I've watched this happen at a lot of companies and I don't think anybody involved is being lazy. I think there's a genuine misconception that the hard part was procurement.

**Installing the app is table stakes. It is not the project.**

[SLIDE 38 — Four layers]

Four layers. Most organizations do the first one and stop.

**Layer one: access.** Licenses, policy, which surfaces are approved, data governance. This is real work and it has to happen. It is also not a strategy. Do it quickly and stop congratulating yourself for it.

**Layer two: context.** Everything we just spent thirteen minutes on, built deliberately.

**Layer three: workflow.** Getting this into the actual path of work.

**Layer four: craft.** The practices that separate a team getting ten percent from a team getting forty.

Let me take the middle two, because those are where the money is.

[SLIDE 39 — Layer 2, context]

Layer two. Repo instructions in your highest-traffic repositories. MCP servers pointed at your critical internal systems. Curated org knowledge.

I want to be blunt about what this is: **it's platform work.** It has a backlog. It has a maintenance burden. It needs an owner with a name.

*[Beat.]*

And I'll put it more strongly than that. **If nobody owns it, it doesn't exist.**

I've seen a dozen orgs where "we should write instructions files" was a good idea that everyone agreed with and no one was accountable for. Six months later there are three instruction files, two of them are wrong, and nobody trusts any of them.

[SLIDE 40 — Layer 3, workflow]

Layer three is the one that actually moves the needle, and it's the one everybody skips — because it requires changing process rather than buying something.

The principle: **Copilot has to be in the path of work, not adjacent to it.**

Adjacent means it's available and people remember to use it when they're feeling motivated. In the path means it happens whether anyone remembers or not.

Concretely:

Code review runs on pull requests **by default** — not when a reviewer thinks to ask for it. If it's opt-in, you've built a tool for the people who least need it.

Issue templates that produce **agent-ready** issues. If your issues are three words and a screenshot, no agent is going to do anything useful with them — and neither is a new hire, incidentally.

CI failures that route somewhere useful instead of into a notification nobody reads.

Prompt files for the work that's genuinely repetitive. Release notes. Migrations. The seventeenth boilerplate service.

And team norms about what gets delegated asynchronously versus done live — because right now most teams have no shared answer to that, so everyone guesses, and the guessing is where the inconsistency comes from.

[SLIDE 41 — Layer 4, craft]

Layer four. This is the difference between teams getting ten percent and teams getting forty, and it's almost entirely tacit.

Prompt and context discipline. Knowing when to abandon a session and start fresh instead of arguing with a context window that's gone sideways. And — the hardest one — **knowing when to stop and just do it yourself.**

*[Beat.]*

Here's the thing about layer four: it does not spread through training decks. I have never once seen a lunch-and-learn move this needle. It spreads socially. Somebody sits next to somebody else, watches them work, and says "wait, how did you do that?"

So budget for it. Pairing time. Internal demos. A channel where people post what actually worked this week. That's not culture fluff — that's the actual delivery mechanism for the highest-value layer.

[SLIDE 42 — You cannot roll this out uniformly]

One more organizational point, and it's the reason I structured the middle of this talk around personas.

**You cannot roll this out uniformly, because your people do not work uniformly.**

The PM and the staff engineer in our demos needed different surfaces, different onboarding, and different definitions of success. The PM's win condition was a better-decomposed backlog. The staff engineer's was a twelve-repo change that didn't break anything.

If you build one rollout plan optimized for the median developer, you will underserve both ends of your distribution — and the ends are where your leverage is. The advanced users are your layer-four seed crystals. The dev-adjacent roles are your biggest untapped population.

Segment by how people work. Which is exactly what that persona exercise was for.

[SLIDE 43 — One concrete recommendation]

If you take one operational thing from this section:

Find the two or three teams already using this hard. They exist. They're in your org right now, quietly getting a lot more done and not telling anyone because nobody asked.

**Make them visible.** Have them demo. Publish what they did.

Let adoption spread laterally instead of vertically.

*[Beat.]*

Mandates produce compliance. Demonstrated leverage produces adoption. Those look identical on a dashboard for about a quarter and then diverge permanently.

---

# BLOCK 8 — Measuring What Matters
**1:22–1:28 · 6 minutes**

[SLIDE 44 — Section header]

Last section, and I want to start by talking you out of something.

[SLIDE 45 — The two worst metrics]

**Acceptance rate. Lines of AI-generated code.**

These are the two most-reported and least-useful numbers in this entire space.

Here's the problem with both: they tell you the tool is **on**. They tell you nothing whatsoever about whether it's **working**.

A high acceptance rate might mean the suggestions are great. It might also mean your engineers have stopped reading them carefully. Those are opposite situations and they produce identical numbers.

*[Beat.]*

And lines-of-AI-code is worse than useless, because it's not just uninformative — it's **actively harmful.**

The moment you put "lines of AI-generated code" on a dashboard that anyone's performance is judged against, you have told your engineering organization what you reward.

And they will deliver it. Enthusiastically. You will get more lines of code. That is not the same thing as getting more value, and by the time you notice the difference, you've got a codebase full of it.

[SLIDE 46 — The three questions]

So here's the filter I'd use instead.

There are exactly three questions your business is actually asking. Every metric you keep has to answer one of them. Anything that doesn't — delete it. Not "deprioritize." Delete.

**One. Are we delivering more value, faster?**

Lead time for changes. Throughput. Cycle time on the work that actually matters.

**Two. Are we delivering it safely?**

Change failure rate. Defect escape rate. Security findings. Review depth.

**Three. Is it worth what we're paying?**

Cost per unit of outcome. Adoption *depth* — not seat count. Where the value is concentrating.

*[Point at the slide.]*

That's the whole list. If your dashboard has fourteen metrics on it and four of them answer these questions, you have ten metrics that are costing you attention and buying you nothing.

[SLIDE 47 — Reading them honestly]

Three notes on reading these without fooling yourself.

**On question one:** look for changes in *shape*, not changes in average. The biggest real effect I see is not that the median task gets faster. It's that **the slow tail gets shorter** — the tasks that used to take three days because someone was stuck now take four hours. If you're only watching the mean, that's a small wobble. It's not a small wobble.

**On question two:** these are non-negotiable companion metrics, not optional extras. If your speed went up and your change failure rate went up with it, **you did not get faster.** You moved work downstream to where it costs more. That's not a productivity gain, that's a loan.

**On question three:** value is almost never evenly distributed. You'll find two teams getting enormous benefit and six getting very little. That's a **finding**, not a failure — it tells you exactly where to look and what to replicate. Most orgs average it away and learn nothing.

[SLIDE 48 — Two principles]

Two principles I'd hold firmly.

**Measure the system, not the individual.**

Individual-level AI usage metrics destroy trust faster than any efficiency gain could possibly justify. And practically, they don't even work — they don't survive contact with the reality of how differently people's work is shaped. Team and org level. That's it.

**Pair every quantitative metric with a qualitative one.**

Your developer experience survey will tell you *why* the numbers moved months before you could possibly infer it from the numbers themselves.

*[Land it.]*

The usage API tells you what happened. Your engineers tell you what it means. You need both, and only one of them is on a dashboard.

[SLIDE 49 — Be careful with "productivity"]

Last thing in this section, and it's the one I'd most like you to repeat to your leadership.

Be careful with the word "productivity."

Most of what teams actually gain from this is not more output per hour.

*[Slow.]*

**It's less time stuck.**

Less time on boilerplate you've written forty times. Less time lost in an unfamiliar part of the codebase. Less of that specific, miserable experience of *"I know this is a two-line fix, I just don't know which two lines."*

That shows up as **reduced variance and shorter tails** long, long before it shows up as a bigger number in a velocity chart.

Which means — and this is the failure mode I'd most like you to avoid — if you measure only the average, you will miss the win entirely and conclude it didn't work. I have watched organizations do exactly that and walk away from something that was genuinely helping them.

---

# BLOCK 9 — Close
**1:28–1:30 · 2 minutes**

[SLIDE 50 — Three takeaways]

Three things.

**One. Route work to the right surface.** Most of the time when somebody says "Copilot doesn't work for this," it's a routing mistake, not a capability limit. The work went to the wrong place.

**Two. Context is the product.** The gap between the team getting ten percent and the team getting forty percent is almost never which model they're on. It's what their tools can see.

**Three. Adoption is a workflow problem, not a license problem.** Seats are layer one of four.

[SLIDE 51 — Closing line]

*[Pause before this. Let the room settle.]*

The interesting question stopped being "can AI write this code."

It's **"where does this work belong, and can I tell if it's right?"**

Everything else is implementation detail.

*[Beat.]*

Thank you.

[SLIDE 52 — Questions]

I've got some questions up there that are worth asking your own organization this week, whether or not anybody has one for me.

Happy to take anything — including the uncomfortable ones. Especially those.

---

# Appendix A — Timing checkpoints

Check the clock at these three points. If you're behind, cut from the list below — **decide now, not on stage.**

| Checkpoint | Should be at | If you're behind |
|---|---|---|
| End of "when not to" | **0:21** | Cut rapid-fire demo 3 |
| End of personas | **0:56** | Cut demo 5 (the review beat in persona 1); compress persona 4 to beats 2 and 3 |
| End of context supply chain | **1:13** | Cut implementation layer 4 to one sentence |

**Cut order:**
1. Rapid-fire demo 3 (code review) — persona 1 does this properly later
2. The autonomy ladder table — talk it instead of showing it
3. Demo 5, the review beat in persona 1 — only if rapid-fire demo 3 survived
4. Persona 4's beat 1 (schema explanation) — go straight to the money mismatch
5. Implementation layer 4 — compress to one sentence

**Never cut:** the "when not to" block, demo 10 (same prompt / two surfaces), the cold-open payoff, or slide 26 ("the persona that breaks the pattern"). Those four are why an advanced audience stays.

---

# Appendix B — Recovery lines

**A demo fails outright:**
> "That's a real failure, and honestly it's a useful one. Here's what it's telling us — *[name the actual cause: context, permissions, a flaky tool]*. That's the exact category of problem we're going to talk about in the context section."
>
> Then switch to the fallback. Do not debug on stage. **Ever.** You get one sentence, then you move.

**The agent produces something wrong or mediocre:**
> "Good — I'd rather show you this than a rehearsed win. Look at *why* it's wrong: it didn't have X. That's fixable, and it's fixable by me, not by waiting for a better model."

**Network dies:**
> "This is why every one of these has a recording. Give me five seconds."
>
> [Switch to hotspot in the background while the clip plays.]

**Someone challenges a claim mid-talk:**
> "That's fair, and I might be wrong about that — let me take it at the end so I can give you a real answer instead of a fast one."
>
> Write it down visibly. Actually come back to it.

**You're asked about pricing, licensing tiers, or a roadmap item:**
> "I'm going to punt on that — not because it's secret, but because whatever I tell you today will be wrong by next quarter. Grab me after and I'll point you at the source of truth."

---

# Appendix C — Likely questions

**"How do we stop people from just accepting everything blindly?"**
You mostly don't solve this with policy — you solve it with verification infrastructure. If your tests and CI are good enough to catch a bad change, blind acceptance is survivable. If they aren't, you had that problem before Copilot; it's just faster now.

**"What about junior engineers? Are we hollowing out the learning path?"**
Real concern, and I don't think anyone has fully solved it. The version I believe: the danger isn't that juniors use it, it's that they use it at level four autonomy before they can evaluate level four output. Pair the autonomy ladder to the experience ladder deliberately.

**"How do you handle the security review for MCP servers?"**
Treat each one like a new integration with production data access — because that's what it is. Scope the permissions, audit what it can reach, and don't let individual engineers wire up arbitrary servers against internal systems without review. This is a genuine platform responsibility.

**"What's the realistic ROI number?"**
I'd distrust anybody who gives you one. The honest answer is that it varies enormously by team, and that variance is the most useful signal you have. Measure your own, at team level, against the three questions.

**"Does this replace developers?"**
Not the answer people expect: it changes what the bottleneck is. When producing code gets cheaper, deciding *what* to build and verifying *whether it's right* become the scarce skills. Most orgs are not staffed for that shift yet.

**"How do we keep instructions files from rotting?"**
Same way you keep anything from rotting: ownership plus a trigger. Put them in CODEOWNERS. Review them when the thing they describe changes. And periodically delete aggressively — most rot is accumulation, not decay.
