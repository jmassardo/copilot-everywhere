# Demo captures

Offline fallback assets for the four persona demos in [`../Demos.md`](../Demos.md).

For the complete presenter sequence and narration, open
[`offline-walkthrough.md`](offline-walkthrough.md).

Each persona directory contains:

- `*-01-terminal.png` through `*-03-terminal.png`: real macOS Terminal window
  screenshots presenting the key demo beats.
- `*-04-live-copilot-cli.png`: a real, resumed GitHub Copilot CLI session.
- `*-browser-*.png`: real GitHub pages captured in Safari or an authenticated
  Chrome window for issue, pull-request, feedback, and delegation moments.
- `*-copilot-app-*.png`: real GitHub Copilot desktop app output grounded in
  this repository.
- `frame-*.txt`: the concise terminal text used for the presentation captures.
- `*-terminal.txt`: raw output captured from the corresponding command or
  Copilot CLI run.
- `*-session.md`: exported Copilot CLI session details.

## Suggested order

| Persona | First | Second | Third | Optional live UI |
|---|---|---|---|---|
| Engineer | Green CI and reproduced leak | Investigation | Red/green fix | `engineer-04-live-copilot-cli.png` |
| Platform | Ambiguous conventions | Durable customization | Agent stops for policy | `platform-04-live-copilot-cli.png` |
| Product | Evidence triage | Issue #5 audit | Issue #6 human decision | `product-04-live-copilot-cli.png` |
| Data | Read-only boundary | Before/after query plan | NULL-semantics stop | `data-04-live-copilot-cli.png` |

## Browser and Copilot App captures

| Persona | Capture | Purpose |
|---|---|---|
| Engineer | `engineer-05-browser-issue-2.png` | Customer-isolation incident and acceptance criteria |
| Platform | `platform-05-browser-pr-9.png` | Review of asynchronous UTC timestamp work |
| Product | `product-05-browser-issue-5.png` | Clean issue and acceptance-criteria view |
| Product | `product-06-browser-feedback.png` | Raw, untriaged feedback queue |
| Product | `product-07-browser-issue-6.png` | Blocked refund-contract decision |
| Product | `product-08-copilot-app-triage.png` | Repository-grounded Copilot App classification with citations |
| Product | `product-10-browser-delegate-issue-5.png` | Authenticated issue view with **Assign to Agent** |
| Data | `data-05-browser-issue-8.png` | `needs-human` and `status:blocked` semantic stop |

The terminal screenshots use synthetic application data only. The recorded
flows were run in an isolated worktree; rehearsal-only source and database
changes were reset afterward.
