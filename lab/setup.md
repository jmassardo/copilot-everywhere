# Setup and Baseline

Complete installation before the lab. The first 10 minutes are for verification,
not package troubleshooting.

## Requirements by track

| Track | Required |
|---|---|
| Engineer | VS Code with Copilot chat, agent mode, multiple sessions; GitHub access; Python 3.12 |
| Platform | VS Code with agent mode and custom-agent support; GitHub access; Python 3.12 |
| Product | Browser, GitHub account, Copilot on GitHub or Copilot app |
| Data | VS Code with agent mode, Python 3.12, SQLite client |

Cloud coding agent access is strongly recommended for Engineer and Product.
Facilitators provide completed fallback pull requests when it is unavailable or
does not finish within the lab.

## Install and verify Python

Use **Python 3.12** for the lab. The lab environment has not been validated with
Python 3.13 on Windows 11.

Check the interpreter before creating the virtual environment:

macOS or Linux:

```bash
python3.12 --version
```

Windows PowerShell:

```powershell
py -3.12 --version
```

Expected:

```text
Python 3.12.x
```

If the command is not found, install Python 3.12 from
[python.org](https://www.python.org/downloads/) and select **Add python.exe to
PATH** in the Windows installer. Close and reopen VS Code after installation,
then rerun the version command.

## Repository and virtual-environment setup

The presentation deck and saved captures make a full clone unnecessarily large
for conference Wi-Fi. Participants should use this shallow sparse clone, which
downloads only the lab instructions and sample application:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/jmassardo/copilot-everywhere.git
cd copilot-everywhere
git sparse-checkout set lab sample-app
cd sample-app

python3.12 -m venv .venv
.venv/bin/python --version
.venv/bin/python -m pip install -r requirements.txt
```

The clone and sparse-checkout commands are the same in Windows PowerShell.
Then run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The version check must print:

```text
Python 3.12.x
```

If it reports another version, remove only the `sample-app/.venv` directory and
recreate it with the Python 3.12 command above. Installing Python 3.12 does not
change an existing virtual environment.

If Git does not support the sparse-clone options or the clone stalls, do not
retry a full clone on the conference network. Ask the facilitator for a
prepared local copy and continue.

Use a fork or training repository if your track needs to push branches or
delegate to a cloud coding agent. The Engineer track uses a prepared timestamp
issue and does not require students to create an issue.

## Verify the baseline

From `sample-app/`:

```bash
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
```

Expected:

```text
13 passed
All checks passed!
```

This baseline is intentionally green **and still contains a customer-isolation
defect**. One lab objective is learning why a passing suite can verify the wrong
thing. Do not “repair” `store.list_orders` during setup.

### If setup still fails

Do not spend the lab debugging Python installation problems. Copy the command
you ran and its complete terminal output, give both to the facilitator, and use
the prepared baseline or pair with someone whose environment works. Continue
the track with that environment. Use the expected output below as a reference,
not as a result from your machine:

```text
13 passed
All checks passed!
```

On Windows, include the output of these diagnostics:

```powershell
py -0p
py -3.12 --version
.\.venv\Scripts\python.exe --version
```

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
- Confirm Agent mode is available.
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
- [ ] Python 3.12 is installed for Engineer, Platform, and Data tracks.
- [ ] Repository or fork available.
- [ ] Two VS Code chat sessions can run independently where required.
- [ ] Agent picker works.
- [ ] Baseline shows 13 passing tests and clean Ruff.
- [ ] Cloud agent availability known, or fallback plan accepted.
- [ ] Data track database contains 50,000 orders.
- [ ] Working branch is not `main`.
