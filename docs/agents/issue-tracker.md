# Issue tracker: GitHub

Specs and tickets live in GitHub Issues at `Hungnth/agent-skills`.
Use `gh` with `--repo Hungnth/agent-skills`; the Git remote uses an SSH
alias, so do not rely on automatic repository inference.

## Issue operations

- Create: `gh issue create --repo Hungnth/agent-skills --title "<title>" --body-file "<body-file>"`
- Read: `gh issue view <number> --repo Hungnth/agent-skills --json number,title,body,labels,state,comments`
- List: `gh issue list --repo Hungnth/agent-skills --state open --json number,title,body,labels`
- Comment: `gh issue comment <number> --repo Hungnth/agent-skills --body-file "<body-file>"`
- Labels: `gh issue edit <number> --repo Hungnth/agent-skills --add-label "<label>"` or `--remove-label "<label>"`
- Close: `gh issue close <number> --repo Hungnth/agent-skills --comment "<resolution>"`

“Publish to the issue tracker” means create a GitHub issue.
“Fetch the relevant ticket” means read its body, labels, state, and comments.
Use canonical issue URLs in cross-agent handoffs.

Read `docs/agents/triage-labels.md` when assigning triage roles.
Follow the active delivery workflow's acceptance gate before closing tickets.

## Pull requests as a triage surface

**PRs as a request surface: no.**

## Wayfinding operations

For `/wayfinder`, the map is one issue labelled `wayfinder:map`.
Its body holds Notes, Decisions-so-far, and Fog.

Link child tickets as GitHub sub-issues using `gh api`. Where sub-issues
are unavailable, list children in the map's task list and put
`Part of #<map>` in each child body.

Label children `wayfinder:<type>`, where type is `research`, `prototype`,
`grilling`, or `task`.

Represent blockers with native GitHub issue dependencies:

`gh api --method POST repos/Hungnth/agent-skills/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-database-id>`

Get the database ID with:

`gh api repos/Hungnth/agent-skills/issues/<blocker> --jq .id`

Use the database ID, not the issue number or node ID. Where native
dependencies are unavailable, record `Blocked by: #<n>, #<n>` in the
child body. A ticket is unblocked when every blocker is closed.

For the frontier, inspect the map's open children and exclude assigned
tickets or tickets with open blockers. Select the first remaining child
in map order.

Claim with `gh issue edit <number> --repo Hungnth/agent-skills --add-assignee @me`.
Resolve by commenting with the result, closing the child, and adding a
concise result plus link to the map's Decisions-so-far.
