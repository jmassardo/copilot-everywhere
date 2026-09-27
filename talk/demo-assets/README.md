# Demo Assets

These files support the four persona demos without creating a second copy of
the Orders Service.

## GitHub issues

Create issues from the Markdown files in `issues/` before the talk. Keep a
completed fallback pull request for the two cloud-agent tasks.

## Platform fallback

The normal demo creates the repository instructions and `Orders API Maintainer`
live with Copilot. `origin/demo/platform-customization` is the fallback if live
generation fails or runs long.

Before the talk, confirm the branch contains:

- `.github/copilot-instructions.md`
- `.github/agents/orders-api-maintainer.agent.md`
- `.github/agents/orders-data-investigator.agent.md`

Keep the branch open on GitHub so the files can be shown without switching the
local workspace.

## Reset

- Remove the two customization files generated during the live Platform demo.
- Do not merge the fallback pull requests.
- Rebuild `sample-app/data/orders.db`.
- Keep the fallback branch separate from `main`.
