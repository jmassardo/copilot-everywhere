#!/usr/bin/env python3

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "copilot-everywhere-persona-labs.pptx"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

BG = RGBColor(0x0D, 0x11, 0x17)
PANEL = RGBColor(0x16, 0x1B, 0x22)
PANEL_ALT = RGBColor(0x20, 0x26, 0x2C)
BORDER = RGBColor(0x30, 0x36, 0x3D)
TEXT = RGBColor(0xF0, 0xF6, 0xFC)
MUTED = RGBColor(0xB0, 0xBA, 0xC3)
GREEN = RGBColor(0x5E, 0xEC, 0x83)
GREEN_SOFT = RGBColor(0xBE, 0xFF, 0xD0)
BLUE = RGBColor(0x2F, 0x94, 0xFF)
PURPLE = RGBColor(0xB8, 0x70, 0xFF)
ORANGE = RGBColor(0xD2, 0x99, 0x22)
RED = RGBColor(0xF8, 0x51, 0x49)

TITLE_FONT = "Mona Sans Display"
BODY_FONT = "Mona Sans"
MONO_FONT = "SFMono-Regular"


def set_background(slide, color=BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text(
    slide,
    text,
    x,
    y,
    w,
    h,
    *,
    size=24,
    color=TEXT,
    bold=False,
    font=BODY_FONT,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
    margin=0,
):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    frame.word_wrap = True
    paragraph = frame.paragraphs[0]
    paragraph.text = text
    paragraph.alignment = align
    paragraph.font.name = font
    paragraph.font.size = Pt(size)
    paragraph.font.bold = bold
    paragraph.font.color.rgb = color
    return shape


def add_box(
    slide,
    x,
    y,
    w,
    h,
    *,
    fill=PANEL,
    line=BORDER,
    radius=True,
    line_width=1,
):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(
        shape_type, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(line_width)
    return shape


def add_footer(slide, number):
    add_text(
        slide,
        "GitHub Copilot  /  Persona Labs",
        0.45,
        7.10,
        4.2,
        0.20,
        size=10,
        color=MUTED,
    )
    add_text(
        slide,
        str(number),
        12.45,
        7.08,
        0.42,
        0.22,
        size=10,
        color=MUTED,
        align=PP_ALIGN.RIGHT,
    )


def add_kicker(slide, text, color=GREEN):
    add_text(
        slide,
        text.upper(),
        0.60,
        0.38,
        7.0,
        0.28,
        size=12,
        color=color,
        bold=True,
    )


def add_title(slide, title, subtitle=None, *, color=TEXT):
    long_title = len(title) > 50
    add_text(
        slide,
        title,
        0.58,
        0.72,
        12.15,
        0.98 if long_title else 0.72,
        size=30 if long_title else 34,
        color=color,
        bold=True,
        font=TITLE_FONT,
    )
    if subtitle:
        add_text(
            slide,
            subtitle,
            0.60,
            1.72 if long_title else 1.46,
            11.9,
            0.38 if long_title else 0.55,
            size=18,
            color=MUTED,
        )


def add_paragraphs(
    slide,
    paragraphs,
    x,
    y,
    w,
    h,
    *,
    size=20,
    color=TEXT,
    bullet_color=GREEN,
    spacing=8,
):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = 0
    frame.margin_right = 0
    frame.margin_top = 0
    frame.margin_bottom = 0
    for index, item in enumerate(paragraphs):
        if isinstance(item, tuple):
            label, body = item
            text = f"{label}  {body}"
        else:
            label = None
            text = item
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = text
        paragraph.level = 0
        paragraph.space_after = Pt(spacing)
        paragraph.font.name = BODY_FONT
        paragraph.font.size = Pt(size)
        paragraph.font.color.rgb = color
        if label:
            paragraph.runs[0].font.bold = True
            paragraph.runs[0].font.color.rgb = bullet_color
    return shape


def add_step_cards(slide, steps, *, y=2.22, card_h=0.92):
    gap = 0.12
    for index, step in enumerate(steps, 1):
        top = y + (index - 1) * (card_h + gap)
        add_box(slide, 0.65, top, 12.02, card_h, fill=PANEL)
        add_box(
            slide,
            0.85,
            top + 0.18,
            0.52,
            0.52,
            fill=GREEN,
            line=GREEN,
        )
        add_text(
            slide,
            str(index),
            0.85,
            top + 0.19,
            0.52,
            0.48,
            size=18,
            color=BG,
            bold=True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_text(
            slide,
            step,
            1.58,
            top + 0.16,
            10.65,
            0.58,
            size=18,
            color=TEXT,
            valign=MSO_ANCHOR.MIDDLE,
        )


def add_checkpoint(slide, text, *, x=0.65, y=6.22, w=12.02, color=GREEN):
    add_box(slide, x, y, w, 0.62, fill=PANEL_ALT, line=color)
    add_text(
        slide,
        f"CHECKPOINT  {text}",
        x + 0.22,
        y + 0.13,
        w - 0.44,
        0.34,
        size=14,
        color=color,
        bold=True,
        valign=MSO_ANCHOR.MIDDLE,
    )


def add_image_contain(slide, image_path, x, y, w, h):
    add_box(slide, x, y, w, h, fill=RGBColor(0, 0, 0), line=BORDER)
    with Image.open(image_path) as image:
        image_ratio = image.width / image.height
    box_ratio = w / h
    if image_ratio > box_ratio:
        image_w = w - 0.08
        image_h = image_w / image_ratio
    else:
        image_h = h - 0.08
        image_w = image_h * image_ratio
    left = x + (w - image_w) / 2
    top = y + (h - image_h) / 2
    slide.shapes.add_picture(
        str(image_path),
        Inches(left),
        Inches(top),
        width=Inches(image_w),
        height=Inches(image_h),
    )


def add_badge(slide, text, x, y, *, color=GREEN, width=1.55):
    add_box(slide, x, y, width, 0.36, fill=PANEL_ALT, line=color)
    add_text(
        slide,
        text,
        x,
        y + 0.04,
        width,
        0.25,
        size=10,
        color=color,
        bold=True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )


def new_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    return slide


def add_standard_slide(prs, number, kicker, title, subtitle=None):
    slide = new_slide(prs)
    add_kicker(slide, kicker)
    add_title(slide, title, subtitle)
    add_footer(slide, number)
    return slide


def add_section_slide(prs, number, persona, role, question, arc, accent):
    slide = new_slide(prs)
    add_text(
        slide,
        persona,
        0.68,
        0.56,
        8.2,
        1.0,
        size=48,
        color=accent,
        bold=True,
        font=TITLE_FONT,
    )
    add_text(slide, role, 0.72, 1.60, 8.5, 0.42, size=18, color=MUTED)
    add_box(slide, 0.72, 2.25, 11.9, 1.35, fill=PANEL, line=accent)
    add_text(
        slide,
        question,
        1.02,
        2.43,
        11.25,
        0.98,
        size=28,
        color=TEXT,
        bold=True,
        font=TITLE_FONT,
        valign=MSO_ANCHOR.MIDDLE,
    )
    labels = ["START", "BUILD", "FINISH"]
    for index, item in enumerate(arc):
        left = 0.72 + index * 4.06
        add_text(
            slide,
            labels[index],
            left,
            4.15,
            3.55,
            0.24,
            size=11,
            color=accent,
            bold=True,
        )
        add_text(
            slide,
            item,
            left,
            4.48,
            3.55,
            1.05,
            size=22,
            color=TEXT,
            bold=True,
        )
    add_text(
        slide,
        "Five connected exercises. Preserve each artifact for the next step.",
        0.72,
        6.28,
        11.7,
        0.40,
        size=16,
        color=MUTED,
    )
    add_footer(slide, number)
    return slide


def add_exercise_slide(
    prs,
    number,
    persona,
    exercise,
    minutes,
    title,
    objective,
    steps,
    checkpoint,
    *,
    accent=GREEN,
    image=None,
    facilitator_cue=None,
):
    slide = add_standard_slide(
        prs,
        number,
        f"{persona}  /  exercise {exercise}",
        title,
        objective,
    )
    add_badge(slide, f"{minutes} MIN", 11.10, 0.34, color=accent, width=1.46)
    if image:
        add_box(slide, 0.65, 2.18, 5.02, 3.72, fill=PANEL)
        add_text(
            slide,
            "DO",
            0.92,
            2.45,
            0.55,
            0.24,
            size=11,
            color=accent,
            bold=True,
        )
        y = 2.78
        for index, step in enumerate(steps, 1):
            add_text(
                slide,
                f"{index}.",
                0.92,
                y,
                0.32,
                0.42,
                size=17,
                color=accent,
                bold=True,
            )
            add_text(
                slide,
                step,
                1.28,
                y,
                4.00,
                0.63,
                size=16,
                color=TEXT,
            )
            y += 0.78
        add_image_contain(slide, ROOT / image, 5.92, 2.18, 6.75, 3.72)
        add_checkpoint(slide, checkpoint, y=6.08)
    else:
        add_step_cards(slide, steps)
        add_checkpoint(slide, checkpoint)
    if facilitator_cue:
        add_text(
            slide,
            f"FACILITATOR CUE  {facilitator_cue}",
            0.70,
            6.82,
            11.75,
            0.22,
            size=10,
            color=MUTED,
        )
    return slide


def build_deck():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    prs.core_properties.title = "Copilot Everywhere — Persona Labs"
    prs.core_properties.subject = "Facilitator walkthrough for the persona labs"
    prs.core_properties.author = "Jenna Massardo"
    prs.core_properties.keywords = "GitHub Copilot, labs, personas, facilitator"

    slide = new_slide(prs)
    add_text(
        slide,
        "GitHub Copilot",
        0.72,
        0.55,
        4.0,
        0.35,
        size=14,
        color=GREEN,
        bold=True,
    )
    add_text(
        slide,
        "Copilot Everywhere",
        0.72,
        1.48,
        11.8,
        0.88,
        size=50,
        color=TEXT,
        bold=True,
        font=TITLE_FONT,
    )
    add_text(
        slide,
        "Persona Labs",
        0.72,
        2.38,
        11.8,
        0.88,
        size=50,
        color=GREEN,
        bold=True,
        font=TITLE_FONT,
    )
    add_text(
        slide,
        "Choose one role. Complete one connected workflow. Bring back evidence.",
        0.76,
        3.55,
        10.8,
        0.55,
        size=22,
        color=MUTED,
    )
    add_box(slide, 0.76, 5.05, 11.72, 1.22, fill=PANEL, line=GREEN)
    add_text(
        slide,
        "90 minutes  /  synthetic Orders Service  /  four persona tracks",
        1.06,
        5.38,
        11.1,
        0.42,
        size=22,
        color=GREEN_SOFT,
        bold=True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_footer(slide, 1)

    slide = add_standard_slide(
        prs,
        2,
        "The lab promise",
        "This is not a prompt collection",
        "Each track follows one piece of work from evidence to a defensible outcome.",
    )
    add_step_cards(
        slide,
        [
            "Investigate before increasing autonomy.",
            "Keep independent questions in independent sessions.",
            "Delegate only when scope and verification are explicit.",
            "Review at the level your persona actually owns.",
        ],
        y=2.18,
        card_h=0.82,
    )
    add_checkpoint(
        slide,
        "A green agent summary is not evidence. Point to the test, diff, plan, criterion, or reconciliation.",
        y=6.15,
    )

    slide = add_standard_slide(
        prs,
        3,
        "Shared scenario",
        "One Orders Service. Several kinds of uncertainty.",
        "Every track sees the same repository and backlog through a different responsibility.",
    )
    scenario_cards = [
        ("CUSTOMER", "Cross-customer order exposure escaped green CI.", RED),
        ("PRICING", "Exact boundaries and penny reconciliation disagree.", ORANGE),
        ("PLATFORM", "API conventions conflict and refund policy is missing.", PURPLE),
        ("DATA", "The replica is slow, inconsistent, and ambiguous.", BLUE),
    ]
    for index, (label, body, color) in enumerate(scenario_cards):
        left = 0.65 + (index % 2) * 6.10
        top = 2.28 + (index // 2) * 1.75
        add_box(slide, left, top, 5.92, 1.48, fill=PANEL, line=color)
        add_text(slide, label, left + 0.24, top + 0.19, 1.6, 0.24, size=11, color=color, bold=True)
        add_text(slide, body, left + 0.24, top + 0.52, 5.38, 0.72, size=17, color=TEXT, bold=True)

    slide = add_standard_slide(
        prs,
        4,
        "Choose your track",
        "Pick the responsibility you want to practice",
        "The tracks run in parallel and converge for a shared debrief.",
    )
    tracks = [
        ("ENGINEER", "Parallel investigation, red/green verification, handoff", GREEN),
        ("PLATFORM", "Instructions, custom agents, scoped guidance", PURPLE),
        ("PRODUCT", "Evidence, issue design, delegation, acceptance", ORANGE),
        ("DATA", "Read-only analysis, reconciliation, bounded change", BLUE),
    ]
    for index, (name, body, color) in enumerate(tracks):
        left = 0.65 + (index % 2) * 6.10
        top = 2.18 + (index // 2) * 1.82
        add_box(slide, left, top, 5.92, 1.55, fill=PANEL, line=color)
        add_text(slide, name, left + 0.26, top + 0.20, 2.15, 0.30, size=14, color=color, bold=True)
        add_text(slide, body, left + 0.26, top + 0.58, 5.32, 0.72, size=17, color=TEXT, bold=True)

    slide = add_standard_slide(
        prs,
        5,
        "Timing",
        "One connected 90-minute workflow",
        "Setup should be complete before the first exercise whenever possible.",
    )
    timeline = [
        ("0:00", "Setup + seating", "10 min"),
        ("0:10", "Exercise 1", "15 min"),
        ("0:25", "Exercise 2", "20 min"),
        ("0:45", "Exercise 3", "15 min"),
        ("1:00", "Exercise 4", "15 min"),
        ("1:15", "Exercise 5", "10 min"),
        ("1:25", "Shared debrief", "10 min"),
    ]
    for index, (clock, activity, duration) in enumerate(timeline):
        top = 2.04 + index * 0.63
        add_text(slide, clock, 0.72, top, 1.1, 0.34, size=16, color=GREEN, bold=True)
        add_text(slide, activity, 2.05, top, 6.8, 0.34, size=18, color=TEXT, bold=True)
        add_text(slide, duration, 10.72, top, 1.45, 0.34, size=16, color=MUTED, align=PP_ALIGN.RIGHT)

    slide = add_standard_slide(
        prs,
        6,
        "Operating rules",
        "Protect the lab before you protect the schedule",
        "These constraints apply to every persona and every Copilot surface.",
    )
    add_step_cards(
        slide,
        [
            "Work on a branch or fork — never directly on main.",
            "Use synthetic data and non-production systems only.",
            "Start read-only when the problem is not understood.",
            "Do not merge exercise pull requests into the shared baseline.",
        ],
        y=2.20,
        card_h=0.82,
    )
    add_checkpoint(slide, "If the baseline is dirty or surprising, move to the prepared clean branch.", y=6.15)

    slide = add_standard_slide(
        prs,
        7,
        "Working with Copilot",
        "Choose the mode that matches the uncertainty",
        "The same assistant can investigate, implement, or review — but those are different jobs.",
    )
    modes = [
        ("ASK / PLAN", "Read, trace, compare, cite. No edits.", BLUE),
        ("AGENT", "Edit and run commands after the contract is clear.", GREEN),
        ("CUSTOM AGENT", "Add durable role boundaries and stop conditions.", PURPLE),
        ("CLOUD AGENT", "Run independent, bounded work asynchronously.", ORANGE),
    ]
    for index, (name, body, color) in enumerate(modes):
        left = 0.65 + index * 3.05
        add_box(slide, left, 2.28, 2.83, 2.32, fill=PANEL, line=color)
        add_text(slide, name, left + 0.18, 2.55, 2.45, 0.48, size=14, color=color, bold=True)
        add_text(slide, body, left + 0.18, 3.16, 2.45, 1.15, size=16, color=TEXT, bold=True)
    add_checkpoint(slide, "Start a fresh session when the job, permissions, or evidence boundary changes.", y=5.76)

    slide = add_standard_slide(
        prs,
        8,
        "What each track brings back",
        "The debrief is artifact-first",
        "Bring one reusable piece of evidence — not a story about how helpful the model felt.",
    )
    outputs = [
        ("ENGINEER", "Ownership regression test + compact handoff", GREEN),
        ("PLATFORM", "A rule that demonstrably changed behavior", PURPLE),
        ("PRODUCT", "A criterion tied to evidence — or a deliberate stop", ORANGE),
        ("DATA", "A plan change or a question the data cannot answer", BLUE),
    ]
    for index, (name, body, color) in enumerate(outputs):
        top = 2.18 + index * 0.92
        add_box(slide, 0.72, top, 11.86, 0.72, fill=PANEL, line=BORDER)
        add_text(slide, name, 0.98, top + 0.18, 1.60, 0.28, size=12, color=color, bold=True)
        add_text(slide, body, 2.72, top + 0.15, 9.32, 0.34, size=19, color=TEXT, bold=True)

    add_section_slide(
        prs,
        9,
        "Engineer",
        "Senior / Staff Engineer",
        "How do we fix a serious defect without widening the change?",
        ["Reproduce + bound", "Red before green", "Review + hand off"],
        GREEN,
    )
    add_exercise_slide(
        prs,
        10,
        "Engineer",
        1,
        15,
        "Triage with two independent sessions",
        "Reproduce the symptom and assess blast radius without sharing assumptions.",
        [
            "Start a read-only API reproduction session.",
            "Start a separate blast-radius session immediately.",
            "Reconcile broad claims against exact call-path evidence.",
        ],
        "API reproduction + missing ownership invariant + bounded blast-radius statement.",
        accent=GREEN,
        image="fallback-captures/engineer/engineer-02-blast-radius.png",
        facilitator_cue="Reject edits. Ask which path is proven affected versus merely related.",
    )
    add_exercise_slide(
        prs,
        11,
        "Engineer",
        2,
        20,
        "Strengthen verification before fixing",
        "Make the ownership invariant fail at the API boundary before authorizing production edits.",
        [
            "Turn the reproduction into a test specification.",
            "Allow test edits only and inspect the focused red result.",
            "Authorize the smallest predicate fix, then run focused, full, and Ruff.",
        ],
        "The failure is customer ownership — not a typo, fixture, or import error.",
        accent=GREEN,
        image="fallback-captures/engineer/engineer-03-red-test.png",
        facilitator_cue="Do not manufacture red by changing expectations.",
    )
    add_exercise_slide(
        prs,
        12,
        "Engineer",
        3,
        15,
        "Delegate independent maintenance work",
        "Practice asynchronous delegation without blocking incident response.",
        [
            "Open or create the timezone-aware UTC issue.",
            "Confirm it does not touch the incident files or contract.",
            "Assign the cloud coding agent, record the link, and leave the page.",
            "Continue incident work instead of polling.",
        ],
        "Independent work is running with explicit scope and verification.",
        accent=GREEN,
        facilitator_cue="Use the prepared timestamp PR if assignment is unavailable.",
    )
    add_exercise_slide(
        prs,
        13,
        "Engineer",
        4,
        15,
        "Practice an evidence-only handoff",
        "Give a fresh reviewer enough evidence to decide without the full chat transcript.",
        [
            "Assemble reproduction, root cause, red/green test, diff, and remaining risk.",
            "Start a fresh reviewer session with only that packet.",
            "Compare its decision with your own review of the diff.",
            "Remove claims that cannot be traced to evidence.",
        ],
        "A reviewer can decide scope and correctness from the compact packet.",
        accent=GREEN,
        facilitator_cue="The handoff should preserve evidence, not conversation history.",
    )
    add_exercise_slide(
        prs,
        14,
        "Engineer",
        5,
        10,
        "Review the asynchronous result",
        "Review the timestamp change against its own acceptance criteria.",
        [
            "Open the live or fallback pull request.",
            "Map each criterion to diff or check evidence.",
            "Confirm timezone-aware UTC, stable API fields, and no unrelated changes.",
        ],
        "Leave an accept-or-revise decision grounded in acceptance evidence.",
        accent=GREEN,
        image="fallback-captures/engineer/engineer-04-green-verification.png",
        facilitator_cue="Green checks prove mechanics; compatibility still needs review.",
    )

    add_section_slide(
        prs,
        15,
        "Platform",
        "Platform / Developer Experience Lead",
        "How do we make safe behavior repeatable across future agent work?",
        ["Expose ambiguity", "Encode boundaries", "Prove scope"],
        PURPLE,
    )
    add_exercise_slide(
        prs,
        16,
        "Platform",
        1,
        15,
        "Audit whether the repository is agent-ready",
        "Observe what a normal agent assumes when policy and conventions are incomplete.",
        [
            "Ask for a refund endpoint plan without supplying refund rules.",
            "Record every assumption and its repository evidence.",
            "Classify conflict, missing policy, and durable standards.",
        ],
        "A gap list separates what can be encoded from what humans must decide.",
        accent=PURPLE,
        image="fallback-captures/platform/platform-01-refund-assumptions.png",
        facilitator_cue="For every plausible rule, ask which file or decision establishes it.",
    )
    add_exercise_slide(
        prs,
        17,
        "Platform",
        2,
        15,
        "Write and prove repository-wide instructions",
        "Encode short, durable engineering standards and prove they alter a fresh session.",
        [
            "Create .github/copilot-instructions.md at the repository root.",
            "Keep standards; remove style filler and invented product policy.",
            "Start a fresh session and verify the file is active.",
            "Record one measurable behavior change.",
        ],
        "The file is successful only if a fresh session behaves differently.",
        accent=PURPLE,
        facilitator_cue="Placement matters: repository root, not sample-app/.github.",
    )
    add_exercise_slide(
        prs,
        18,
        "Platform",
        3,
        20,
        "Build and test a bounded custom agent",
        "Define role, permitted scope, verification, and explicit stop conditions.",
        [
            "Create the Orders API Maintainer workspace agent.",
            "Test a missing-decision refund request.",
            "Test a prohibited dependency / CI request.",
            "Test a permitted existing-contract test plan.",
        ],
        "The same agent stops, refuses, and proceeds for the right reasons.",
        accent=PURPLE,
        image="fallback-captures/platform/platform-02-custom-agent-stop.png",
        facilitator_cue="A long persona description is not a substitute for boundaries.",
    )
    add_exercise_slide(
        prs,
        19,
        "Platform",
        4,
        15,
        "Add and verify path-scoped guidance",
        "Apply test-specific practices only when test files are actually in scope.",
        [
            "Create tests.instructions.md with sample-app/tests/** scope.",
            "Run a focused test-generation task and inspect active context.",
            "Run a README-only planning task in a fresh session.",
        ],
        "Test guidance activates for tests and stays absent from unrelated work.",
        accent=PURPLE,
        image="fallback-captures/platform/platform-03-scoped-instructions.png",
        facilitator_cue="Prove both activation and non-activation.",
    )
    add_exercise_slide(
        prs,
        20,
        "Platform",
        5,
        10,
        "Improve the paved road using asynchronous work",
        "Use a real pull-request observation to justify one durable improvement.",
        [
            "Review the timestamp PR through the platform lens.",
            "Identify one recurring gap — not a one-off detail.",
            "Revise the correct customization layer.",
            "Retest the rule and record rollout telemetry.",
        ],
        "One evidence-driven improvement is tested and ready for controlled rollout.",
        accent=PURPLE,
        facilitator_cue="Reject vague 'be careful' language and policy the platform team does not own.",
    )

    add_section_slide(
        prs,
        21,
        "Product",
        "Product / Dev-Adjacent",
        "How do we delegate delivery without delegating product judgment?",
        ["Map evidence", "Separate decisions", "Accept outcomes"],
        ORANGE,
    )
    add_exercise_slide(
        prs,
        22,
        "Product",
        1,
        15,
        "Build an evidence-grounded demand map",
        "Separate customer problems, requested solutions, technical risks, and uncertainty.",
        [
            "Map every FEEDBACK.md source item exactly once.",
            "Ground each theme in repository evidence.",
            "Verify at least three citations yourself.",
        ],
        "Every source is represented; reports, code facts, and unknowns stay distinct.",
        accent=ORANGE,
        image="fallback-captures/product/product-01-demand-map.png",
        facilitator_cue="Do not rank yet, and do not merge the penny complaint with exact boundaries.",
    )
    add_exercise_slide(
        prs,
        23,
        "Product",
        2,
        15,
        "Separate objective defects from human decisions",
        "Classify work by whether correct behavior is already knowable and verifiable.",
        [
            "Classify each theme: objective, product, contract, or discovery.",
            "Score impact, urgency, and decision readiness separately.",
            "Add at least one explicit piece of human business context.",
            "Choose one agent-ready item and one decision item.",
        ],
        "The final ranking distinguishes evidence from human judgment.",
        accent=ORANGE,
        facilitator_cue="Demand evidence does not define refund behavior.",
    )
    add_exercise_slide(
        prs,
        24,
        "Product",
        3,
        20,
        "Write one delegatable issue and one decision issue",
        "Make the two issue types intentionally different.",
        [
            "Draft the exact discount-boundary defect with six observable outcomes.",
            "Audit it for hidden decisions and scope creep.",
            "Draft a refund decision issue with owners and open questions.",
            "Keep implementation explicitly blocked.",
        ],
        "One issue can be tested now; the other organizes a decision without pretending it is made.",
        accent=ORANGE,
        facilitator_cue="The lab teaches issue quality, not backlog volume.",
    )
    add_exercise_slide(
        prs,
        25,
        "Product",
        4,
        15,
        "Delegate without waiting",
        "Send objective work asynchronously and continue useful human-owned work.",
        [
            "Perform the final readiness check on the boundary issue.",
            "Assign only the objective defect to the cloud agent.",
            "Improve the refund decision record while delivery runs.",
            "Check status once near the end.",
        ],
        "Objective work is running; the unresolved decision remains human-owned.",
        accent=ORANGE,
        facilitator_cue="If the task is not ready, use the prepared PR — do not spend the lab polling.",
    )
    add_exercise_slide(
        prs,
        26,
        "Product",
        5,
        10,
        "Accept or reject against customer outcomes",
        "Review the live or fallback pull request as a product owner, not a Python reviewer.",
        [
            "Read issue, summary, changed files, checks, then acceptance map.",
            "Verify all six threshold outcomes and protected non-goals.",
            "Leave an accept-or-revise decision with missing evidence named.",
        ],
        "Every acceptance criterion maps to observable evidence.",
        accent=ORANGE,
        image="fallback-captures/product/product-02-acceptance-matrix.png",
        facilitator_cue="Do not approve because the agent says all criteria pass.",
    )

    add_section_slide(
        prs,
        27,
        "Data",
        "DBA / Analytics Engineer / Data Scientist",
        "How do we make one defensible change without hiding data risk?",
        ["Enforce read-only", "Reconcile + change", "Stop at semantics"],
        BLUE,
    )
    add_exercise_slide(
        prs,
        28,
        "Data",
        1,
        15,
        "Establish a read-only investigation mode",
        "Prove the session can inspect the replica without modifying schema or data.",
        [
            "Set PRAGMA query_only = ON and verify it returns 1.",
            "Allow only SELECT, PRAGMA, and EXPLAIN QUERY PLAN.",
            "Deliberately attempt CREATE INDEX and observe the write failure.",
            "Review each risk with evidence, query, result, and limitation.",
        ],
        "The write guard is demonstrated and the evidence table remains read-only.",
        accent=BLUE,
        facilitator_cue="A failed write is the successful safety demonstration.",
    )
    add_exercise_slide(
        prs,
        29,
        "Data",
        2,
        20,
        "Run independent quality and performance investigations",
        "Prevent one plausible symptom from becoming an unsupported explanation for another.",
        [
            "Start a data-quality session with row-count evidence.",
            "Start a separate query-performance session with the unchanged dashboard query.",
            "Confirm the automatic covering index manually.",
            "Compare reports without merging their causal stories.",
        ],
        "Two independent reports: quality counts and plan evidence; no data changed.",
        accent=BLUE,
        facilitator_cue="Ask for the query that connects two symptoms before accepting causation.",
    )
    add_exercise_slide(
        prs,
        30,
        "Data",
        3,
        15,
        "Build reconciliation before allowing repair",
        "Create one repeatable control row before any database write.",
        [
            "Use scalar subqueries for counts and orphan checks.",
            "Compute order dollars directly from orders — no fan-out joins.",
            "Run the identical statement twice and record units and limitations.",
        ],
        "Two identical one-row baselines are ready for the write-capable session.",
        accent=BLUE,
        image="fallback-captures/data/data-01-reconciliation.png",
        facilitator_cue="The baseline detects selected changes; it does not prove every row is correct.",
    )
    add_exercise_slide(
        prs,
        31,
        "Data",
        4,
        15,
        "Make one bounded performance change",
        "Approve only the index supported by the captured plan.",
        [
            "Re-run reconciliation and stop if it differs.",
            "Create only idx_orders_customer_id.",
            "Re-run the unchanged query plan and reconciliation.",
            "Compare timing without requiring a fixed speedup.",
        ],
        "The named index replaces the automatic index and every control is unchanged.",
        accent=BLUE,
        image="fallback-captures/data/data-02-query-plans.png",
        facilitator_cue="Reject speculative indexes, cleanup, constraints, or query rewrites.",
    )
    add_exercise_slide(
        prs,
        32,
        "Data",
        5,
        10,
        "Write the decision memo the data requires",
        "Stop when stored columns cannot distinguish meaning for every affected row.",
        [
            "Investigate NULL discount correlations without turning them into facts.",
            "Identify the missing provenance field.",
            "Name the pipeline owner and proposed future contract.",
            "Document unsafe analyses and restore the disposable database.",
        ],
        "Unknown meaning, human owner, and required contract change are explicit.",
        accent=BLUE,
        image="fallback-captures/data/data-03-semantic-stop.png",
        facilitator_cue="Ask which stored field records why the value is NULL.",
    )

    slide = add_standard_slide(
        prs,
        33,
        "Fallback protocol",
        "Preserve the exercise — not the outage",
        "The capture package replaces unavailable execution, not participant review.",
    )
    add_step_cards(
        slide,
        [
            "State the capability or timing limit plainly.",
            "Open the matching saved capture or prepared pull request.",
            "Keep the participant in the reviewer / decision-maker role.",
            "Ask what the evidence proves, what it cannot prove, and what happens next.",
        ],
        y=2.18,
        card_h=0.82,
    )
    add_checkpoint(slide, "Do not let participants spend lab time polling or debugging unrelated setup.", y=6.15)

    slide = add_standard_slide(
        prs,
        34,
        "Shared debrief",
        "Bring one artifact. Explain one autonomy decision.",
        "The tracks are different; the reasoning pattern should be recognizable.",
    )
    questions = [
        "Which session or agent did you choose first — and why?",
        "What ran concurrently without creating merge or reasoning conflict?",
        "What evidence let you increase autonomy?",
        "Where did the agent need to stop for a human decision?",
        "Which artifact would your team reuse on Monday?",
    ]
    add_step_cards(slide, questions, y=2.03, card_h=0.70)

    slide = add_standard_slide(
        prs,
        35,
        "Artifact gallery",
        "Show the work, not the vibes",
        "Each artifact should make a future decision cheaper.",
    )
    gallery = [
        ("ENGINEER", "Test + handoff", GREEN),
        ("PLATFORM", "Instruction + proof", PURPLE),
        ("PRODUCT", "Criterion + evidence", ORANGE),
        ("DATA", "Plan or semantic stop", BLUE),
    ]
    for index, (label, body, color) in enumerate(gallery):
        left = 0.70 + index * 3.08
        add_box(slide, left, 2.35, 2.82, 2.45, fill=PANEL, line=color)
        add_text(slide, label, left + 0.18, 2.62, 2.42, 0.28, size=12, color=color, bold=True)
        add_text(slide, body, left + 0.18, 3.20, 2.42, 1.05, size=21, color=TEXT, bold=True)
    add_checkpoint(slide, "Reusable evidence is the bridge from a successful lab to a better operating system.", y=5.55)

    slide = new_slide(prs)
    add_text(
        slide,
        "Route the work.",
        0.75,
        1.15,
        11.85,
        0.80,
        size=48,
        color=TEXT,
        bold=True,
        font=TITLE_FONT,
        align=PP_ALIGN.CENTER,
    )
    add_text(
        slide,
        "Make the context visible.",
        0.75,
        2.18,
        11.85,
        0.80,
        size=48,
        color=TEXT,
        bold=True,
        font=TITLE_FONT,
        align=PP_ALIGN.CENTER,
    )
    add_text(
        slide,
        "Increase autonomy only when verification gets cheaper.",
        0.75,
        3.22,
        11.85,
        0.88,
        size=40,
        color=GREEN,
        bold=True,
        font=TITLE_FONT,
        align=PP_ALIGN.CENTER,
    )
    add_box(slide, 2.12, 5.20, 9.10, 0.92, fill=PANEL, line=GREEN)
    add_text(
        slide,
        "Now choose a track and start with evidence.",
        2.30,
        5.44,
        8.74,
        0.38,
        size=22,
        color=GREEN_SOFT,
        bold=True,
        align=PP_ALIGN.CENTER,
    )
    add_footer(slide, 36)

    prs.save(OUTPUT)
    return OUTPUT, len(prs.slides)


if __name__ == "__main__":
    output, slide_count = build_deck()
    print(f"Wrote {output} ({slide_count} slides)")
