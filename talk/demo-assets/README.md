# Demo Assets

These files support the four persona demos without creating a second copy of
the Orders Service.

## GitHub issues

Create issues from the Markdown files in `issues/` before the talk. Keep a
completed fallback pull request for the two cloud-agent tasks.

## Platform branch

Create a branch from the demo baseline, then copy:

```bash
mkdir -p .github/agents
cp talk/demo-assets/platform/copilot-instructions.md .github/copilot-instructions.md
cp talk/demo-assets/platform/*.agent.md .github/agents/
```

Open this branch only for the Platform and Data demos. The baseline remains
unconfigured so the before/after behavior is real.

Use VS Code's Agent Customizations editor to confirm each agent appears and to
review the available tool list for the installed editor version.

## Reset

- Return local source changes to the prepared baseline branch.
- Do not merge the fallback pull requests.
- Rebuild `sample-app/data/orders.db`.
- Keep the Platform customization files only on the prepared branch.
