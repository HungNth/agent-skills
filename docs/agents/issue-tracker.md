# Issue tracker: GitHub

The Matt Pocock workflow in [AGENTS.md](../../AGENTS.md) tracks specs and tickets in [HungNth/agent-skills](https://github.com/HungNth/agent-skills/issues). Use GitHub issue URLs as canonical references. The separately distributed [ship-with-agy skill](../../skills/ship-with-agy/SKILL.md) defines its own tracker contract.

## Conventions

Use `gh` and pass `-R github.com/HungNth/agent-skills` to issue, label, and PR commands because the checkout uses an SSH host alias. Verify the target with `gh repo view github.com/HungNth/agent-skills --json nameWithOwner,hasIssuesEnabled`.

- **Publish the spec** with `gh issue create --title "<title>" --body-file <file>`.
- **Publish approved tickets** in dependency order. Use `gh issue create --parent <spec> --title "<title>" --body-file <file> --label ready-for-agent`. Add `--blocked-by <number>,<number>` when the ticket has blockers. To link existing issues, use `gh issue edit <spec> --add-sub-issue <ticket>` and `gh issue edit <ticket> --add-blocked-by <blocker>`.
- **Fetch a spec or ticket** with `gh issue view <number> --json number,title,body,state,labels,comments,url,parent,subIssues,blockedBy`. A blocker is satisfied when its issue is closed or when it has passed acceptance and is integrated on the same delivery branch, as described in `AGENTS.md`.
- **Triage** with `gh issue list --state open --label <label>` and `gh issue edit <number> --add-label <label>` or `--remove-label <label>`. Use the mapping in [triage-labels.md](triage-labels.md).
- **Comment or close** with `gh issue comment <number> --body-file <file>` and `gh issue close <number>`. Post the explanation as a comment before closing when the workflow calls for one.

## Delivery completion

Approved spec and ticket requirements are immutable during delivery. An accepted ticket commit must include `Ticket: <issue-url>` in its message or body to record local acceptance.

With ship approval, use `Closes #<ticket>` in the PR for each delivered ticket. Include `Closes #<spec>` once the PR completes all remaining work under that spec. After merge, verify issue states and close any delivered issues GitHub left open.

## Pull requests as a triage surface

**PRs as a request surface: no.** Set to `yes` if external PRs should enter `/triage`. When enabled, use `gh pr view`, `gh pr diff`, `gh pr comment`, `gh pr edit`, and `gh pr close` for PRs. Resolve ambiguous numbers before writing because issues and PRs share a number space.

## Wayfinding operations

For `/wayfinder`, the map is an issue labelled `wayfinder:map`. Its tickets are GitHub sub-issues with native dependencies and one label from `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`.

- Read the map's `subIssues` and each child's `blockedBy`, `state`, and `assignees` with `gh issue view`. The frontier is the first open, unassigned child in map order whose blockers are all closed.
- Claim the child with `gh issue edit <number> --add-assignee @me`.
- Resolve it by posting the answer as an issue comment, closing the child, and adding its title, link, and one-line decision to the map's **Decisions so far**.
