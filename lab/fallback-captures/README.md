# Lab fallback captures

Facilitator-ready screenshots for the twelve saved-output checkpoints in
[`../facilitator-guide.md`](../facilitator-guide.md).

Open [`walkthrough.md`](walkthrough.md) for the presentation order, review
questions, and the point at which each capture should replace unavailable live
tooling.

Each persona directory contains:

- presentation-ready macOS Terminal screenshots;
- the concise text frame used to create each screenshot; and
- evidence labels that match the corresponding lab exercise.

These are fallback review artifacts, not model answers to distribute at the
start of the lab. Use them only when live tooling is unavailable or an exercise
reaches its timebox. Participants should still inspect the evidence, identify
limitations, and make the persona-owned decision.

The captures contain only synthetic application data. Recreate a screenshot
from its frame with:

```bash
./replay-frame.sh engineer/frame-01-api-reproduction.txt \
  "Engineer lab — API reproduction"
```
