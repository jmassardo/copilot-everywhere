# Setup and Baseline

Complete installation before the lab. The first 10 minutes are for verification,
not package troubleshooting.

## Requirements by track

| Track | Required |
|---|---|
| Engineer | VS Code with Copilot chat, agent mode, multiple sessions; GitHub access |
| Platform | VS Code with agent mode and custom-agent support; GitHub access |
| Product | Browser, GitHub account, Copilot on GitHub or Copilot app |
| Data | VS Code with agent mode, Python, SQLite client |

Cloud coding agent access is strongly recommended for Engineer and Product.
Facilitators provide completed fallback pull requests when it is unavailable or
does not finish within the lab.

## Repository setup

```bash
git clone https://github.com/jmassardo/copilot-everywhere.git
cd copilot-everywhere/sample-app

python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Windows PowerShell equivalents:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Fork the repository if your track needs to create issues, push branches, or
delegate to a cloud coding agent.

## Verify the baseline

From `sample-app/`:

```bash
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
```

Expected:

```text
13 passed
All checks passed!
```

This baseline is intentionally green **and still contains a customer-isolation
defect**. One lab objective is learning why a passing suite can verify the wrong
thing. Do not “repair” `store.list_orders` during setup.

## Data track

```bash
.venv/bin/python data/build_db.py
sqlite3 data/orders.db "SELECT COUNT(*) FROM orders;"
```

Expected order count: `50000`.

The database is deterministic and disposable. Rebuild it at any time with the
same command.

## Copilot verification

Before class:

- Open the repository in VS Code.
- Start two separate chat sessions and confirm both remain available.
- Confirm you can select Ask/Plan and Agent modes.
- If available, confirm the cloud coding agent can be assigned an issue in your
  fork.
- Platform attendees: confirm custom agents and repository instructions are
  supported by your editor version.
- Product attendees: confirm Copilot can answer a repository-grounded question
  in the browser.

## Track starting points

| Track | Start with |
|---|---|
| Engineer | `INCIDENT-4552` in `FEEDBACK.md`; green baseline |
| Platform | Conflicting router conventions; no Copilot customization |
| Product | Entire raw `FEEDBACK.md`; no pre-triaged backlog |
| Data | Freshly generated `orders.db`; unchanged `schema.sql` |

## Safety

- Work on a branch, never `main`.
- Use only the synthetic sample app or an authorized repository.
- Never connect lab agents to production systems.
- Never give a data agent write access until reconciliation is captured.
- Do not merge exercise pull requests into the shared student baseline.

## Ready checklist

- [ ] Correct persona track selected.
- [ ] Repository or fork available.
- [ ] Two VS Code chat sessions can run independently where required.
- [ ] Agent picker works.
- [ ] Baseline shows 13 passing tests and clean Ruff.
- [ ] Cloud agent availability known, or fallback plan accepted.
- [ ] Data track database contains 50,000 orders.
- [ ] Working branch is not `main`.
