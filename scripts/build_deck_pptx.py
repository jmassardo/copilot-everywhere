#!/usr/bin/env python3
"""Build the "Copilot Everywhere" deck into the corporate GitHub PowerPoint template.

Marp's own --pptx export rasterizes each slide to an image, which discards the
template entirely. This maps the deck's content onto real template layouts and
placeholders so the result is editable, on-brand, and carries speaker notes.

Usage:
    python scripts/build_deck_pptx.py [--template PATH] [--out PATH]
"""

from __future__ import annotations

import argparse
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.util import Pt

REPO = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = Path.home() / "Downloads" / "2026 GitHub Presentation Template.potx"
DEFAULT_OUT = REPO / "talk" / "copilot-everywhere.pptx"

# Layout indices in the 2026 GitHub Presentation Template.
L_AGENDA = 6
L_SECTION = 7
L_STATEMENT = 8
L_TITLE_CONTENT = 23
L_TITLE_SUBTITLE = 24
L_TWO_STATEMENTS = 25
L_THREE_STATEMENTS = 26
L_THANKYOU = 43

# Placeholder idx maps, per layout.
PH = {
    L_AGENDA: {"numbers": 11, "items": 12},
    L_SECTION: {"title": 11},
    L_STATEMENT: {"title": 11},
    L_TITLE_CONTENT: {"title": 33, "body": 1, "eyebrow": 32},
    L_TITLE_SUBTITLE: {"title": 33, "body": 1, "eyebrow": 32},
    L_TWO_STATEMENTS: {
        "title": 39,
        "eyebrow": 32,
        "heads": [22, 36],
        "descs": [23, 37],
    },
    L_THREE_STATEMENTS: {
        "title": 45,
        "eyebrow": 32,
        "heads": [36, 39, 42],
        "descs": [37, 40, 43],
    },
}


def open_template(path: Path) -> Presentation:
    """python-pptx rejects the .potx content type, so rewrite it in a temp copy."""
    if path.suffix.lower() != ".potx":
        return Presentation(str(path))

    tmp = Path(tempfile.mkdtemp()) / "template.pptx"
    template_ct = "application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"
    presentation_ct = "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"

    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.replace(template_ct.encode(), presentation_ct.encode())
            dst.writestr(item, data)

    return Presentation(str(tmp))


def strip_slides(prs: Presentation) -> None:
    """Remove the template's sample slides, keeping masters and layouts."""
    id_list = prs.slides._sldIdLst
    rel_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    for slide_id in list(id_list):
        prs.part.drop_rel(slide_id.get(rel_ns))
        id_list.remove(slide_id)


def placeholder(slide, idx):
    for shape in slide.placeholders:
        if shape.placeholder_format.idx == idx:
            return shape
    return None


def set_text(slide, idx, value, size=None):
    """Fill a placeholder. Lists become bullets; '>' prefix marks an emphasis line."""
    shape = placeholder(slide, idx)
    if shape is None or value is None:
        return

    lines = value if isinstance(value, list) else [value]
    frame = shape.text_frame
    frame.word_wrap = True

    for i, line in enumerate(lines):
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        emphasis = line.startswith("> ")
        indent = line.startswith("    ")
        text = line[2:] if emphasis else line.strip()
        para.level = 1 if indent else 0

        # **bold** segments become real bold runs.
        for chunk in re.split(r"(\*\*[^*]+\*\*)", text):
            if not chunk:
                continue
            run = para.add_run()
            if chunk.startswith("**") and chunk.endswith("**"):
                run.text = chunk[2:-2]
                run.font.bold = True
            else:
                run.text = chunk
            if size:
                run.font.size = Pt(size)
            if emphasis:
                run.font.italic = True


def add_table(slide, rows, left, top, width, height, font_size=11):
    cols = len(rows[0])
    shape = slide.shapes.add_table(len(rows), cols, left, top, width, height)
    table = shape.table

    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.text = ""
            frame = cell.text_frame
            frame.word_wrap = True
            para = frame.paragraphs[0]
            for chunk in re.split(r"(\*\*[^*]+\*\*)", str(value)):
                if not chunk:
                    continue
                run = para.add_run()
                if chunk.startswith("**") and chunk.endswith("**"):
                    run.text = chunk[2:-2]
                    run.font.bold = True
                else:
                    run.text = chunk
                run.font.size = Pt(font_size)
                if r == 0:
                    run.font.bold = True
    return shape


def drop_empty_placeholders(slide) -> None:
    """Remove unfilled placeholders so prompt text never leaks into the deck."""
    for shape in list(slide.placeholders):
        empty = not shape.has_text_frame or not shape.text_frame.text.strip()
        if empty:
            shape._element.getparent().remove(shape._element)


def build_slide(prs: Presentation, spec: dict):
    layout_idx = spec["layout"]
    slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])
    keys = PH.get(layout_idx, {})

    if "eyebrow" in keys and spec.get("eyebrow"):
        set_text(slide, keys["eyebrow"], spec["eyebrow"])
    if "title" in keys and spec.get("title"):
        set_text(slide, keys["title"], spec["title"])
    if "body" in keys and spec.get("body"):
        set_text(slide, keys["body"], spec["body"], size=spec.get("body_size"))

    if layout_idx == L_AGENDA:
        items = spec["items"]
        set_text(slide, keys["numbers"], [f"{i:02d}" for i in range(1, len(items) + 1)])
        set_text(slide, keys["items"], items)

    if layout_idx in (L_TWO_STATEMENTS, L_THREE_STATEMENTS):
        for i, (head, desc) in enumerate(spec["statements"]):
            set_text(slide, keys["heads"][i], head)
            set_text(slide, keys["descs"][i], desc)

    table = spec.get("table")
    if table:
        anchor = placeholder(slide, keys.get("body", -1))
        if anchor is not None:
            left, top, width, height = anchor.left, anchor.top, anchor.width, anchor.height
            anchor._element.getparent().remove(anchor._element)
        else:
            from pptx.util import Inches

            left, top, width, height = Inches(0.9), Inches(2.2), Inches(11.5), Inches(4.2)
        add_table(slide, table, left, top, width, height, spec.get("table_font", 11))

    drop_empty_placeholders(slide)

    if spec.get("notes"):
        slide.notes_slide.notes_text_frame.text = spec["notes"].strip()

    return slide


def slides() -> list[dict]:
    """The deck, in order. Mirrors talk/copilot-everywhere.marp.md."""
    return [
        {
            "layout": L_TITLE_SUBTITLE,
            "title": "Copilot Everywhere",
            "body": "Picking the right surface for the right work",
            "notes": """0:00 - DO NOT START HERE. Cold open first, on a browser, before any slide.
Assign the issue live, then land on: "I never opened an editor."
Only after that beat, advance to this title slide and introduce yourself.
TOTAL BUDGET: 72 min content / 10 Q&A / 8 buffer.""",
        },
        {
            "layout": L_STATEMENT,
            "title": "I'm assigning a real issue to the coding agent right now. We'll come back to it around minute 60.",
            "notes": """LIVE DEMO already happened before this slide.
This slide is just a bookmark. Say "we'll come back to it" and MOVE ON.
Do not linger.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "The pitch you've already heard",
            "body": [
                '"Copilot is an AI pair programmer."',
                "True in 2022",
                "Now the least interesting thing about it",
                "**A pair programmer sits next to you**",
                "> Copilot stopped requiring you to be sitting anywhere in particular.",
            ],
            "notes": """0:06 - Key beat: a pair programmer SITS NEXT TO YOU. Co-presence is the defining trait.
That's the thing that broke.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "So this isn't a feature tour",
            "body": [
                "Same capability. Radically different ergonomics.",
                "Your editor",
                "Your terminal",
                "A browser tab",
                "A pull request",
                "Your phone",
                "**Increasingly: without you present at all**",
                "> This is a routing problem. Given a piece of work - where should it go?",
            ],
            "notes": """SLOW DOWN. This is the thesis of the whole talk.
Routing mistakes: 12-repo migration in an IDE chat window. Two-line fix with a full agent.
Question about a repo you never cloned, asked in an editor.""",
        },
        {
            "layout": L_AGENDA,
            "items": [
                "The mental model: three dials, not eight products",
                "When not to reach for it",
                "The surface map",
                "Four personas, four surfaces, one codebase",
                "The context supply chain",
                "What effective implementation looks like",
                "Measuring what the business cares about",
            ],
            "notes": """Two housekeeping notes, say both out loud:
1. Live demos WILL be imperfect - deliberate. Eight flawless demos = a commercial.
2. Wide room: new folks -> persona block. Veterans -> context + measurement blocks.
   Everyone stays for "when not to." """,
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Every interaction is three things",
            "eyebrow": "The mental model",
            "table": [
                ["Dial", "Question it answers"],
                ["Context", "What can it see?"],
                ["Autonomy", "How far does it run before checking in?"],
                ["Surface", "Where do you meet it?"],
            ],
            "table_font": 14,
            "notes": """The reframe: surfaces aren't different products, they're different DEFAULTS
on context + autonomy.
Why it matters: makes the model PREDICTIVE, not descriptive.
They can derive use cases without me enumerating them.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "The autonomy ladder",
            "table": [
                ["Level", "What it does", "You are..."],
                ["1 - Completion", "Predicts the next edit", "Driving"],
                ["2 - Chat / Ask", "Answers, you apply", "Driving"],
                ["3 - Edit", "Proposes multi-file diffs", "Approving"],
                ["4 - Agent", "Plans, edits, runs, iterates", "Supervising"],
                ["5 - Async agent", "Same, without you in the loop", "Reviewing"],
            ],
            "table_font": 13,
            "notes": """Vocabulary I reuse all talk. One sentence per level, fast.
*** CUT CANDIDATE #2 *** - if behind, talk these five levels aloud and skip ahead.""",
        },
        {
            "layout": L_STATEMENT,
            "title": "Most teams live at levels 1 and 2. And they think that's the product.",
            "notes": """Be precise about the gap size - don't hand-wave:
  no Copilot -> L2 = real
  L2 -> L4 = BIGGER, and most orgs never made it
Close: "you haven't found the product. You've found the on-ramp." """,
        },
        {
            "layout": L_SECTION,
            "title": "When not to reach for it",
            "notes": """0:13 -> 0:21 - 8 min. NEVER CUT THIS BLOCK.
Why early + on purpose: you can't trust anyone's advice about a tool
until you've heard them describe its limits specifically.""",
        },
        {
            "layout": L_STATEMENT,
            "title": "The tool is a bad deal whenever verification costs more than doing it yourself.",
            "notes": """Why a cost model and not rules: rules don't generalize, cost models do.
Token cost = obvious + boring. VERIFICATION cost = the one that decides.
Deliver the bottom line slowly. Everything after is a corollary.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Where verification costs too much",
            "eyebrow": "1 of 2",
            "body": [
                "**1. Work where you can't articulate \"done\"**",
                "    No acceptance criteria, no target, endless review loops",
                "**2. Load-bearing decisions with long half-lives**",
                "    Schema design, auth models, public APIs, service boundaries",
                "    A plausible-sounding wrong answer here costs you 18 months",
                "**3. When the codebase is the wrong teacher**",
                "    It pattern-matches your existing code, including the pattern you're escaping",
            ],
            "body_size": 16,
            "notes": """#1 fix isn't "don't use it" - use a SEPARATE session to draft criteria, then START OVER.
#2 the naive version is wrong. It reasons fine. The problem is ASYMMETRY -
   plausible-sounding is exactly what it's best at. Challenger, not author.
#3 hits platform teams hardest. Punchline: "a very fast, very confident junior who has
   read only your worst code and assumed it was intentional." """,
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Where verification costs too much",
            "eyebrow": "2 of 2",
            "body": [
                "**4. Debugging you haven't reproduced**",
                "    Excellent at fixing a failing test. Terrible at \"prod is weird at 3am.\"",
                "    Reproduction is the human's job",
                "**5. Genuinely novel work**",
                "    Not \"new to you\" - new to the world. Rare, but it becomes a confident distraction",
                "**6. Compliance-critical output you can't attribute**",
                "    Know the policy before, not after",
            ],
            "body_size": 16,
            "notes": """#4 a failing test is a SPECIFICATION OF WRONGNESS. Vague prod weirdness isn't.
#5 genuinely novel = new to the WORLD, not new to you. Rare.
#6 five-minute conversation with legal that some of you have avoided for a year.""",
        },
        {
            "layout": L_STATEMENT,
            "title": "None of those are \"the model isn't smart enough.\" They're about where the verification burden lands.",
            "notes": """PAUSE before this. Let them look back at the six.
The pivot: "not smart enough" is unsolvable - you just wait for a better model.
"Where verification lands" is a WORKFLOW DESIGN problem. Solvable. By you. This quarter.
Land: most of what looks like a model limitation is a routing mistake.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "The real question",
            "body": [
                "Not: \"Can Copilot do this?\"",
                "**\"Can I cheaply tell whether it did it right?\"**",
                "Cheap verification is what converts a risky task into a safe one:",
                "    Test suite · Type checker · Linter · Repro case · CI",
                "> Teams with strong verification infrastructure can safely give Copilot dramatically more autonomy.",
            ],
            "notes": """MOST IMPORTANT LINE IN THE FIRST HALF. Slow way down.
Cheap verification already has a name and you own it.
Kicker: "Everybody's asking which model is best. Almost nobody's asking whether their
test suite is good enough to let an agent run unsupervised. Same question, different clothes."
FORESHADOW: this returns in the implementation block.""",
        },
        {
            "layout": L_SECTION,
            "title": "The surface map",
            "notes": "0:21 - Nine minutes. Existence and ergonomics only. Depth comes in the persona block.",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "The routing matrix",
            "table": [
                ["", "Synchronous", "Asynchronous"],
                ["You hold the context", "IDE inline / chat, CLI", "--"],
                ["Repo holds the context", "dotcom chat, Copilot app", "Coding agent, code review"],
                ["Org holds the context", "Spaces / knowledge bases", "Agent + org instructions"],
            ],
            "table_font": 13,
            "notes": """Read this matrix properly ONCE. It's the spine of the talk.
Call out the EMPTY cell: you hold context + async = impossible.
If it's only in your head you can't hand it off. -> previews the context section.
Point back at this after EVERY demo.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "What each surface is uniquely good at",
            "table": [
                ["Surface", "Sees", "Autonomy", "Uniquely good at"],
                ["IDE - inline & chat", "Open files, workspace", "Low-mid", "Tight loops, context already loaded"],
                ["IDE - agent mode", "Workspace, terminal, tools", "High", "Multi-file changes you want to watch"],
                ["CLI", "Filesystem, shell, MCP", "High", "Anything that isn't one repo in one editor"],
                ["Coding agent", "Repo, CI, issue context", "Async", "Work you delegate and review as a PR"],
                ["Code review", "Diff + repo context", "Async", "First-pass consistency on the boring stuff"],
                ["github.com chat", "Repos, issues, PRs, org", "Low-mid", "Code you haven't cloned"],
                ["Copilot app", "Repos, issues, your work", "Mid", "Triage away from a keyboard"],
                ["Spaces / knowledge", "Curated context", "--", "Reusable org context across all of the above"],
            ],
            "table_font": 10,
            "notes": """DO NOT READ THIS TABLE. Point at the LAST COLUMN only.
Not "what can it do" (everything, badly) - what is it UNIQUELY good at.
Hit 4-5 rows fast, then move. They get the deck.""",
        },
        {
            "layout": L_STATEMENT,
            "title": "The browser-only person and the tmux person get the same assistant with the same context.",
            "notes": """Concede first: CLI + cloud agent ARE the powerhouses. Don't undersell them.
THEN pivot - that's not why it matters at org scale.
Consistency across surfaces is the feature. Everything else is packaging.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Rapid fire",
            "eyebrow": "Live demo",
            "body": [
                "**CLI** - one command, non-trivial result",
                "**github.com chat** - a question about a repo I never cloned",
                "**Code review** - a PR that already has agent comments",
                "> The other five surfaces get covered inside the persona demos. On purpose.",
            ],
            "notes": """~90 SEC EACH. Hard stop. Three only.
1 CLI -> "never left the terminal, never needed an editor"
2 dotcom -> say out loud you've never cloned it. "Zero setup. Dev-adjacent folks reach this."
3 review -> *** CUT CANDIDATE #1 *** reappears in persona 4 anyway
SHOULD BE AT 0:30 LEAVING THIS SLIDE.""",
        },
        {
            "layout": L_SECTION,
            "title": "Four personas",
            "notes": """0:30 -> 0:56 - 26 min - ~6 min each. THE HEART OF THE TALK.
Same repo every time - because "consistency is the feature" should be
DEMONSTRATED, not asserted.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Who we're following",
            "table": [
                ["Persona", "Core job", "Surface"],
                ["Senior / staff engineer", "Changes bigger than one repo", "CLI + code review"],
                ["Platform / DevEx lead", "Making 200 other people faster", "MCP + org config"],
                ["Product manager / BA (dev-adjacent)", "Fuzzy idea to backlog engineers don't hate", "Copilot app + dotcom"],
                ["DBA / analytics engineer", "A schema you didn't design", "dotcom + CLI + SQL"],
            ],
            "table_font": 12,
            "notes": """The three beats build a rhythm. Keep them strict.
Beat 1 = the JOB, not the feature (30 sec)
Beat 2 = live demo (3-4 min)
Beat 3 = point at the matrix cell + why (1 min)""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Persona 1: senior / staff engineer",
            "eyebrow": "Surface: CLI + code review",
            "body": [
                "**The job:** changes spanning more repos than you can hold in your head, where you already know exactly what you want.",
                "**Demo A:** cross-repo change from the terminal, tests as the feedback signal",
                "**Demo B:** push it, then agent review on the resulting PR - what it caught, and what it missed",
                "> The CLI is the only surface where Copilot composes with the rest of your tooling.",
            ],
            "notes": """TWO DEMOS - one workflow, not two topics. Make the change, then review it.

DEMO A: cross-repo dep upgrade w/ real API breakage. Terminal 18pt+.
CRITICAL BEAT - narrate the test suite as its OWN feedback signal:
  "it just failed, and it's reading its own failure."
Optional: piping. git diff | copilot -p "..." earns the terminal people.

DEMO B: MUST point at something the review MISSED, out loud.
Framing: TRIAGE, not judgment.
Review latency is the biggest chunk of dead time in most pipelines and
nobody optimizes it because it's nobody's job.

*** CUT CANDIDATE #3 *** - drop DEMO B if behind; rapid-fire already showed review.
Matrix: TOP LEFT for the change, MIDDLE-RIGHT for the review. Say both -
same person, same work, DIFFERENT CELL once it becomes 'someone should check this.'""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Persona 2: platform / DevEx lead",
            "eyebrow": "Surface: MCP + org config",
            "body": [
                "**The job:** making the other 200 engineers faster without sitting next to each of them. Output is leverage, not code.",
                "**Demo:** wire up an MCP server live - Copilot reaches a system it couldn't see 30 seconds ago",
                "**Advanced beat:** the same config now applies in the IDE, the CLI, and the cloud agent",
                "> MCP is where \"Copilot knows our codebase\" becomes \"Copilot knows our company.\"",
            ],
            "notes": """HIGHEST-RISK DEMO. Have the recording ready.
Four beats: ask something it CAN'T answer -> wire up live -> same question, now answered
-> show same config applies in IDE + CLI + cloud agent.
The argument: your codebase is ~40% of the context an engineer needs.
The rest - what's broken, who owns this, what we decided, state of prod - is NOT in the repo.
Matrix: BOTTOM ROW. The row most orgs have completely empty.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Persona 3: product manager / BA",
            "eyebrow": "Dev-adjacent, not non-technical",
            "body": [
                "**The job:** turning a fuzzy idea into a backlog engineers don't hate.",
                "**Demo:** messy spec to epic to issues, informed by the actual codebase",
                "**Advanced beat:** assign one of those issues straight to the coding agent",
                "> The difference from a general chatbot is that this one has read the code.",
            ],
            "notes": """Set up the TERM deliberately: not "non-technical" - DEV-ADJACENT.
"Non-technical" defines someone by what they aren't, and it's usually wrong.
The PM who knows which service a request lands in IS technical - they just don't commit.
Operational payoff: dev-adjacent people need REAL codebase context;
they just need to reach it without a clone and a build env.

DEMO beat 2 is the money beat - point at the line naming a REAL service.
After assigning to the agent: PAUSE. Then caveat honestly - that PR won't be perfect
and shouldn't merge unreviewed. Overclaiming here undoes the "when not to" credibility.
Real point: idea -> code-to-react-to collapsed from a sprint to a coffee break.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Persona 4: DBA / analytics engineer",
            "eyebrow": "Surface: dotcom + CLI + SQL",
            "body": [
                "**The job:** a schema you didn't design, data you didn't generate, queries somebody wrote in a hurry before they left.",
                "**Demo:** read an inherited schema on dotcom, find where the warehouse and the app disagree about money, then EXPLAIN QUERY PLAN",
                "> The warehouse stores money as a float. The app uses integer cents. Neither codebase knows.",
            ],
            "notes": """THIS PERSONA COMPLICATES THE THESIS ON PURPOSE. Don't rush to the twist.

Beat 1: dotcom chat, "explain this schema" - no clone, no DB connection.
Beat 2: THE MONEY MISMATCH. Warehouse REAL vs app integer cents.
  Invisible from inside EITHER codebase. Only visible from a vantage point
  that reads both at once.
Beat 3: EXPLAIN QUERY PLAN -> "SEARCH o USING AUTOMATIC COVERING INDEX"
  SQLite announcing it built a throwaway index because the schema didn't
  provide one. "The database has been filing a bug report against itself
  for three years and nobody read it."
  Add the index: N+1 shape 0.96s -> 0.009s. ~100x.

*** CUT CANDIDATE #4 *** - drop beat 1 if behind, go straight to the mismatch.""",
        },
        {
            "layout": L_STATEMENT,
            "title": "A wrong query doesn't throw. It returns a plausible number.",
            "notes": """NEVER CUT. The most intellectually honest slide in the talk. Slow.

Setup: "Every other persona today had a test suite. This one doesn't."
Software fails LOUDLY. Analysis fails QUIETLY, then gets presented to leadership.

Apply the earlier thesis honestly:
  Where verification is expensive or absent - which is most of data work -
  you get LESS autonomy. Not more. No matter how good the model gets.

This is NOT a walk-back. It's the thesis applied to a discipline where the
answer comes out different. If someone in the room does data work, this is
the moment they decide you're worth listening to - because everyone else
sells them the opposite.

Practical upshot, say it out loud:
'The highest-value thing a data team can build right now isn't a prompt
library. It's reconciliation checks. Those are what make everything else
safe to hand off.'""",
        },
        {
            "layout": L_STATEMENT,
            "title": "Every demo depended on Copilot knowing things specific to this repo and this org. That's not free.",
            "notes": """THE PIVOT INTO THE SECOND HALF. Beat before the last line.
Walk it back through all four:
  refactor needed our conventions - MCP was ENTIRELY external context
  PM demo only worked because it could read real services
  review only caught what it caught because it knew what our code should look like
None of that arrived in the box.""",
        },
        {
            "layout": L_SECTION,
            "title": "The cold open, revisited",
            "notes": """0:56 - NEVER CUT.
*** DO NOT PERFORM DELIGHT. *** No "wow, look at that!"
The room will smell it and you'll spend all the credibility from "when not to."
Review it like a colleague's PR: read description, read diff honestly,
name ONE thing that's good and WHY, name ONE thing you'd change, check tests pass.
Fallback: completed PR from the same issue, already open in another tab.""",
        },
        {
            "layout": L_STATEMENT,
            "title": "It didn't know our convention. That is not the model being dumb. That is me not telling it.",
            "notes": """THE STRONGEST SEAM IN THE TALK. Slow delivery.
The flaw becomes the transition - don't rush past it.
Analogy: it did what a competent new hire does on day one with no onboarding -
made a reasonable guess from surrounding code.
The unwritten convention is in three people's heads and one Slack thread from March.
CLOSE: the moment work doesn't require you present, everything you WOULD have said
in the moment has to exist somewhere else, in writing, where it can be loaded.""",
        },
        {
            "layout": L_SECTION,
            "title": "The context supply chain",
            "notes": """1:00 -> 1:13 - 13 min. Your most differentiated block.
STATE THE CONSTRAINT OUT LOUD: we are not opening a single one of these files.
What nobody covers is HOW EACH SURFACE CONSUMES THEM. That's the section.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "The gap",
            "body": [
                "Everybody has seen a custom instructions file.",
                "**Far fewer people can tell you what actually gets loaded** when you type a prompt in:",
                "    the CLI",
                "    agent mode in the IDE",
                "    the cloud agent",
                "> That resolution order is the difference between config that works everywhere and config that mysteriously works on your machine only.",
            ],
            "notes": """"Here's what good instructions look like" has a hundred blog posts -
most of you have written better ones than I would.
Say the constraint out loud: we are not opening a single one of these files.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "The artifacts, purpose only",
            "table": [
                ["Artifact", "Purpose", "Scope"],
                ["Repo-wide instructions", "Baseline conventions every interaction inherits", "Repo"],
                ["Path-scoped instructions", "Rules that apply only to matching files", "Glob"],
                ["Prompt files", "Reusable, invocable task templates", "Repo / user"],
                ["Custom agents", "Persona + tool restrictions for a mode of work", "Repo / user"],
                ["Skills", "Packaged domain procedures, loaded on demand", "Repo / user"],
                ["MCP servers", "Live access to systems outside the repo", "Anywhere"],
            ],
            "table_font": 11,
            "notes": """Vocabulary only. ONE LINE EACH, fast.
Flag path-scoped as underused - it comes back in principle #3.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "The consumption matrix",
            "eyebrow": "Which surface reads what",
            "table": [
                ["", "IDE", "CLI", "Cloud agent", "Code review", "dotcom / app"],
                ["Repo instructions", "", "", "", "", ""],
                ["Path-scoped", "", "", "", "", ""],
                ["Prompt files", "", "", "", "", ""],
                ["Custom agents", "", "", "", "", ""],
                ["Skills", "", "", "", "", ""],
                ["MCP", "", "", "", "", ""],
            ],
            "table_font": 11,
            "notes": """*** PREP: FILL THIS IN THE WEEK OF THE TALK, FROM VERIFIED BEHAVIOR. ***
Do not present a cell you haven't personally tested.
If uncertain, SAY "I haven't verified this one" - far better than being
confidently wrong on your most authoritative slide.

Two things to point out while walking it:
1. Coverage isn't uniform. Put a critical convention in a surface-specific artifact
   and you've created a class of engineer for whom your standards silently don't apply.
2. This matrix MOVES. Re-verification is the operating advice, not a disclaimer.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Same prompt. Same repo. Two surfaces.",
            "eyebrow": "Live demo",
            "body": [
                "Different outputs - **because of what each one loaded.**",
                "Then: show the loaded-context indicator in each.",
                "> Mechanism, not magic.",
            ],
            "notes": """*** THE MONEY SHOT OF THE BLOCK. REHEARSE HARDEST. NEVER CUT. ***
The point: it isn't randomness or temperature. They loaded different things
before they ever saw my prompt.
Close: "once you can see that, you can debug it. Before you can see it,
it just feels like the tool is inconsistent." """,
        },
        {
            "layout": L_THREE_STATEMENTS,
            "title": "Three principles",
            "statements": [
                (
                    "Write for the lowest common denominator surface",
                    "Config that only works in one surface fragments your org.",
                ),
                (
                    "Instructions are a code artifact",
                    "Reviewed, versioned, and they rot. A stale instruction file misleads an agent that trusts it.",
                ),
                (
                    "More context is not better context",
                    "Everything loaded competes for attention. Selective beats comprehensive.",
                ),
            ],
            "notes": """#2 why it's worse than a stale README: a stale README misleads a HUMAN who'll
   probably notice. A stale instruction file misleads an AGENT with no independent
   basis for doubt, which confidently propagates it across forty files.
#3 deliver the "monument" line lighter: somebody hit a problem once, added forty lines,
   and now every interaction in that repo pays for it forever. "Half of it is archaeology." """,
        },
        {
            "layout": L_STATEMENT,
            "title": "The tool didn't change. What it could see did.",
            "notes": """WHY this section came AFTER the failure modes.
"can't articulate done" -> better when conventions are written down.
"codebase is the wrong teacher" -> EXACTLY what instructions are for.
Agent not knowing standards -> not a capability gap, an UNWRITTEN-KNOWLEDGE gap.
SHOULD BE AT 1:13 LEAVING THIS SLIDE.""",
        },
        {
            "layout": L_SECTION,
            "title": "What effective implementation looks like",
            "notes": "1:13 - Seats are not adoption.",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "The rollout you've probably seen",
            "body": [
                "Buy licenses",
                "Send an email with a link",
                "Put \"AI adoption\" on a slide",
                "Wonder in six months why usage is a flat line at tab completion",
                "> Installing the app is table stakes. It is not the project.",
            ],
            "notes": """Deliver the four steps deadpan. Let them recognize themselves.
THEN be generous: nobody involved is lazy. There's a genuine misconception
that the hard part was procurement.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Four layers. Most orgs do one.",
            "table": [
                ["Layer", "What it is", "Who owns it"],
                ["1 - Access", "Licenses, policy, approved surfaces, governance", "Procurement / security"],
                ["2 - Context", "The supply chain, built deliberately", "Platform"],
                ["3 - Workflow", "Copilot in the path of work", "Eng leadership"],
                ["4 - Craft", "The practices separating 10% from 40%", "The team, socially"],
            ],
            "table_font": 12,
            "notes": """Name all four, then spend your time on layers 2 and 3 - that's where the money is.
Layer 1 is necessary, not sufficient. Do it fast and stop congratulating yourself.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Layer 2: context",
            "body": [
                "Repo instructions in your top repos",
                "MCP servers for your critical internal systems",
                "Curated org knowledge",
                "This is **platform work** with a real backlog, a real owner, and a real maintenance burden.",
                "> If nobody owns it, it doesn't exist.",
            ],
            "notes": """Be blunt: this is PLATFORM WORK. Backlog, maintenance burden, an owner with a NAME.
The failure pattern: "we should write instructions files" - everyone agrees,
nobody's accountable. Six months later there are three files, two are wrong,
and nobody trusts any of them.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Layer 3: workflow",
            "body": [
                "The layer that moves the needle. The layer everyone skips.",
                "Code review runs on PRs **by default**, not when someone remembers",
                "Issue templates that produce **agent-ready** issues",
                "CI failures that route somewhere useful",
                "Prompt files for genuinely repetitive work",
                "Team norms: what gets delegated async vs. done live",
            ],
            "notes": """Key distinction: ADJACENT = available if people remember and feel motivated.
              IN THE PATH = happens whether anyone remembers or not.
On review: "if it's opt-in, you've built a tool for the people who least need it."
On issues: three words and a screenshot is useless to an agent - and to a new hire.
On norms: most teams have no shared answer, so everyone guesses.
          The guessing is where the inconsistency comes from.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Layer 4: craft",
            "body": [
                "The difference between a team getting 10% and a team getting 40%:",
                "Prompt and context discipline",
                "Knowing when to start a fresh session",
                "**Knowing when to stop and do it yourself**",
                "> This spreads socially, not through training decks. Budget for pairing and demos.",
            ],
            "notes": """*** CUT CANDIDATE #4 *** - if behind, compress to one sentence.
Key claim: never seen a lunch-and-learn move this needle.
It spreads socially - somebody watches somebody and says "wait, how did you do that?"
So pairing time isn't culture fluff, it's the DELIVERY MECHANISM for the
highest-value layer.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "You cannot roll this out uniformly",
            "body": [
                "Because your people don't work uniformly.",
                "The PM and the staff engineer needed **different surfaces**",
                "Different onboarding",
                "Different definitions of success",
                "> A single rollout plan optimized for the median developer will underserve both ends.",
            ],
            "notes": """This is WHY the middle of the talk was structured around personas - call that back.
PM's win condition = better-decomposed backlog.
Staff engineer's = a twelve-repo change that didn't break anything.
The ENDS are where your leverage is: advanced users seed layer 4,
dev-adjacent roles are the untapped population.""",
        },
        {
            "layout": L_STATEMENT,
            "title": "Mandates produce compliance. Demonstrated leverage produces adoption.",
            "notes": """Find the two or three teams already using this hard. Make them visible.
They exist in your org RIGHT NOW, quietly getting more done and not telling anyone
because nobody asked.
Kicker: mandates and leverage look identical on a dashboard for about a quarter,
then diverge permanently.
SHOULD BE AT 1:22 LEAVING THIS SLIDE.""",
        },
        {
            "layout": L_SECTION,
            "title": "Measuring what matters",
            "notes": "1:22 - Open by TAKING SOMETHING AWAY.",
        },
        {
            "layout": L_STATEMENT,
            "title": "Acceptance rate and lines of AI-generated code tell you the tool is on. Not that it's working.",
            "notes": """Acceptance rate: high might mean suggestions are great. Might mean people stopped
reading them carefully. Opposite situations, IDENTICAL NUMBERS.
Lines-of-AI-code is worse than useless - actively harmful.
The moment it hits a dashboard you've told your engineers what you reward.
You WILL get more lines of code. Enthusiastically. Not the same as more value,
and by the time you notice, the codebase is full of it.""",
        },
        {
            "layout": L_THREE_STATEMENTS,
            "title": "The three questions the business asks",
            "statements": [
                (
                    "Are we delivering more value, faster?",
                    "Lead time, throughput, cycle time on work that matters.",
                ),
                (
                    "Are we delivering it safely?",
                    "Change failure rate, defect escape, security findings, review depth.",
                ),
                (
                    "Is it worth what we're paying?",
                    "Cost per unit of outcome, adoption depth, where value concentrates.",
                ),
            ],
            "notes": """If a metric doesn't answer one of these three - DELETE it. Not "deprioritize."
Kicker: if your dashboard has fourteen metrics and four answer these questions,
you have ten metrics costing you attention and buying you nothing.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Reading them honestly",
            "body": [
                "**On question 1:** look for shape changes, not averages. The slow tail gets shorter.",
                "**On question 2:** if speed went up and safety went down, you didn't get faster. You moved work downstream where it costs more.",
                "**On question 3:** value is rarely evenly distributed. That's a finding, not a failure.",
            ],
            "notes": """Q1: the real effect isn't a faster median - it's tasks that took three days
    because someone was STUCK now taking four hours. Small wobble in the mean. Not small.
Q2: speed up + failure rate up = you took out a LOAN.
Q3: two teams getting enormous benefit, six getting little - tells you where to look
    and what to replicate. Most orgs average it away and learn nothing.""",
        },
        {
            "layout": L_TWO_STATEMENTS,
            "title": "Two principles",
            "statements": [
                (
                    "Measure the system, not the individual",
                    "Individual AI-usage metrics destroy trust faster than any efficiency gain justifies.",
                ),
                (
                    "Pair every quantitative metric with a qualitative one",
                    "DevEx surveys tell you why the numbers moved months before you could infer it.",
                ),
            ],
            "notes": """Individual metrics don't even work - they don't survive contact with how
differently people's work is shaped. Team and org level. That's it.
Close: "The usage API tells you what happened. Your engineers tell you what it means."
You need both, and only ONE of them is on a dashboard.""",
        },
        {
            "layout": L_STATEMENT,
            "title": "Most of what teams gain isn't more output per hour. It's less time stuck.",
            "notes": """MOST REPEATABLE LINE FOR THEIR LEADERSHIP. Slow.
The specific misery: "I know this is a two-line fix, I just don't know WHICH two lines."
Shows up as REDUCED VARIANCE and SHORTER TAILS long before a velocity chart moves.
The failure mode to avoid: orgs that measured only the average, concluded it didn't work,
and walked away from something that was genuinely helping them. I've watched it happen.""",
        },
        {
            "layout": L_THREE_STATEMENTS,
            "title": "Three takeaways",
            "statements": [
                (
                    "Route work to the right surface",
                    "Most \"Copilot doesn't work for this\" is a routing mistake, not a capability limit.",
                ),
                (
                    "Context is the product",
                    "The gap between teams isn't which model they're on. It's what their tools can see.",
                ),
                (
                    "Adoption is a workflow problem",
                    "Not a license problem. Seats are layer one of four.",
                ),
            ],
            "notes": "Three things, mapped to the audience segments. No summary slide of everything.",
        },
        {
            "layout": L_STATEMENT,
            "title": "The question stopped being \"can AI write this code.\" It's \"where does this work belong, and can I tell if it's right?\"",
            "notes": """PAUSE BEFORE THIS SLIDE. Let the room settle. Then deliver it clean.
Then: "Everything else is implementation detail. Thank you." Stop talking.""",
        },
        {
            "layout": L_TITLE_CONTENT,
            "title": "Questions",
            "body": [
                "Which surface is our team **not** using that they should be?",
                "What's the highest-value internal system Copilot currently **can't see**?",
                "Is our code review agent running by default, or by memory?",
                "What's the one metric on our dashboard that answers none of the three questions?",
                "Which team is already getting 40%, and why is nobody else watching them?",
            ],
            "notes": """Leave this slide up for the whole Q&A.
"Happy to take anything - including the uncomfortable ones. Especially those."

LIKELY Qs (full answers in the script appendix):
 blind acceptance - juniors + learning path - MCP security review
 realistic ROI - does this replace developers - keeping instructions from rotting

PUNT LINE for pricing/licensing/roadmap:
"Whatever I tell you today will be wrong by next quarter. Grab me after."

Backup close: "Pick one workflow. Pick the right surface. Give it the context it needs.
Measure the tail, not the average." """,
        },
        {"layout": L_THANKYOU, "notes": "Leave up while packing down."},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    if not args.template.exists():
        raise SystemExit(f"Template not found: {args.template}")

    prs = open_template(args.template)
    strip_slides(prs)

    specs = slides()
    for spec in specs:
        build_slide(prs, spec)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(args.out))
    print(f"Wrote {args.out} ({len(specs)} slides)")


if __name__ == "__main__":
    main()
