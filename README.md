# Copilot Everywhere

Talk and hands-on lab materials for **"Copilot Everywhere: picking the right surface for the right work."**

The argument: GitHub Copilot isn't one tool, it's the same capability with different defaults on **context** and **autonomy**, exposed through different surfaces. Most "Copilot doesn't work for this" complaints are routing mistakes, not capability limits.

---

## Contents

| Path | What it is |
|---|---|
| [`talk/`](talk/) | 90-minute session: deck, full script, session plan |
| [`lab/`](lab/) | 90-minute hands-on lab: syllabus, setup, four exercises, facilitator guide |
| [`sample-app/`](sample-app/) | FastAPI service with deliberately seeded flaws — the lab workbench |
| [`scripts/`](scripts/) | Deck build tooling |

The talk and the lab each stand alone. Run either, or both back to back for a half day.

---

## The talk

**[`talk/`](talk/)** — 90 minutes, ~72 content / 10 Q&A / 8 buffer.

| File | Use |
|---|---|
| [`copilot-everywhere.marp.md`](talk/copilot-everywhere.marp.md) | Source deck (Marp), presenter notes embedded |
| [`copilot-everywhere.marp.html`](talk/copilot-everywhere.marp.html) | Rendered deck — press **P** for presenter view |
| [`copilot-everywhere.pptx`](talk/copilot-everywhere.pptx) | Corporate-template build, speaker notes included |
| [`script.md`](talk/script.md) | Full verbatim script with stage directions and recovery lines |
| [`session-plan.md`](talk/session-plan.md) | Structure, demo prep checklist, cut list |

### Rebuilding the deck

```bash
# HTML
marp talk/copilot-everywhere.marp.md --html -o talk/copilot-everywhere.marp.html

# PowerPoint, against the corporate template
pip install python-pptx
python scripts/build_deck_pptx.py
```

The PPTX build maps content onto real template layouts and placeholders, so the output is editable and on-brand. Marp's own `--pptx` export rasterizes slides to images and discards the template — don't use it.

> **Two decks, one message.** The Marp and PowerPoint versions are built from separate sources and can drift. Treat the PPTX as canonical if you're required to present from it.

---

## The lab

**[`lab/`](lab/)** — 90 minutes, four exercises, one per persona. Start at the [syllabus](lab/README.md).

| Exercise | Persona | Surface |
|---|---|---|
| [1](lab/exercises/01-staff-engineer-cli.md) | Senior / staff engineer | CLI |
| [2](lab/exercises/02-platform-context.md) | Platform / DevEx lead | Context configuration + MCP |
| [3](lab/exercises/03-dev-adjacent-backlog.md) | Dev-adjacent (PM / BA) | github.com + coding agent |
| [4](lab/exercises/04-maintainer-review.md) | Maintainer / reviewer | Code review |

Every exercise works against the included [sample app](sample-app/) **or** the student's own repository.

Exercises are ordered deliberately: exercise 2 produces the configuration that 3 and 4 consume, so students watch their own context work change the agent's output.

Facilitators: [facilitator-guide.md](lab/facilitator-guide.md).

---

## The through-line

Both halves argue the same thing from different directions:

1. **Route work to the right surface.** Most failures are routing mistakes.
2. **Context is the product.** The gap between teams isn't which model they're on — it's what their tools can see.
3. **Cheap verification buys autonomy.** Teams with fast, trustworthy tests can safely delegate far more, using the identical tool.
4. **Adoption is a workflow problem, not a license problem.** Seats are layer one of four.

---

## Adapting this

Fork it. The parts most worth keeping when you do:

- The **routing matrix** — it turns a feature tour into a decision tool
- The **"when not to" block** — it's where credibility with a senior audience comes from
- The sample app's **seams 1 and 4** — ambiguous convention and untested module with a real bug carry most of the lab's weight
- Exercise 2's **before/after** — the only part that makes context resolution visible rather than asserted

Re-verify the context consumption matrix before every delivery. Support for these artifacts changes fast enough that a slide you made a month ago will have a wrong cell.

---

## License

MIT. See [LICENSE](LICENSE).
