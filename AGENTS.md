## Engineering

Apply these principles within the assigned role and approved scope. During ticket delivery, treat the approved spec and tickets as settled requirements; report gaps for a planning decision before changing them.

- Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current requirements. Avoid speculative abstractions, configuration, and indirection.
- Grow the system in layers. Start from the smallest version that works end to end, and add each new capability on top of a product that already works. Never trade a working product for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.
- Study how established products solve the problem before designing a solution. Adopt their proven patterns and conventions rather than inventing an approach from scratch.
- Before creating, changing, or reviewing UI, read [DESIGN.md](./DESIGN.md) for the project's visual and interaction direction; update it alongside deliberate changes to shared design decisions.

## Agent Development Workflow

This project uses Matt Pocock Skills for planning and delivery.

### Planning Workflow

Follow this sequence for non-trivial feature work.

```text
grill-with-docs
→ to-spec
→ to-tickets
→ delivery approval
→ implement / implement-spec
→ code-review and commit
→ PR, merge, cleanup, and sync when authorized to ship
```

Keep requirement discovery, specification, and ticket decomposition in the primary OMP context. Use `grill-me` when persistent domain documentation is outside the requested scope.

Publish the parent spec on GitHub and agree on how to test the behavior. Publish the approved ticket breakdown as sub-issues with native dependencies. Follow [issue-tracker.md](docs/agents/issue-tracker.md) for GitHub operations.

### Delivery Approval

- **Approve implementation.** Explicit approval to implement the named spec and tickets authorizes a feature or integration branch, implementation, verification, review, and local commits within that scope.
- **Approve and ship.** Explicit approval to ship also authorizes pushing the feature branch, opening a PR, merging it once the branch requirements pass, resolving delivered issues, cleaning up branches and worktrees created for the delivery, and synchronizing the local target branch.

Continue through the approved steps without asking again. Approval of a planning draft and the `ready-for-agent` label indicate readiness for delivery approval. For work outside an approved delivery, get explicit approval before committing. Get a planning decision before changing approved requirements.

### Delivery Workflow

1. **Start.** Pin the latest remote target commit and branch from it before editing. Use an isolated worktree when the existing checkout contains unrelated work. Use `implement` for a ticket or `implement-spec` for a set of tickets on one integration branch. Start tickets with closed blockers. For tickets sharing one integration branch, a blocker is satisfied once its acceptance checks pass and its work is integrated, even while its issue is open.
2. **Review and commit.** Verify the ticket acceptance criteria and run `code-review` for Standards and Spec. For a pre-commit review, stage the scoped changes and review `git diff --cached <base-sha>`. For committed work, review the branch diff against the pinned base. Fix findings, rerun the affected checks, and commit only the reviewed, in-scope changes.
3. **Publish and merge.** With ship approval, push the feature branch and open or update a PR with verification evidence. Use closing references for the tickets delivered by the PR. Include the parent spec when the PR completes all of its remaining work. Merge the reviewed head after the target branch's required checks and approvals pass. Verify the merge and close delivered issues that GitHub leaves open.
4. **Clean up and sync.** Remove the delivery branches and worktrees after verifying the merge and checking for local work to preserve. Fetch the target and fast-forward the local checkout when it is clean and can fast-forward. If it has divergent commits or uncommitted work, preserve them and report what needs a decision. Report the PR, merge commit, issue states, and local sync status.

### Git Commits

- Format all commit messages according to [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/): `<type>[scope]: <description>`.
- Valid types include `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, and `chore`.
- Use lower-case types and scopes; write imperative, concise descriptions without trailing periods.
- Use `!` or a `BREAKING CHANGE:` footer only when introducing breaking changes.

### Ticket Design

Tickets should be self-contained vertical slices and include, where applicable:

- required behavior;
- acceptance criteria;
- testing seam;
- demo path;
- dependencies/blockers;
- parent specification.

Do not turn tickets into implementation scripts with unnecessary file paths or line numbers.

## Output style

The reader has ADHD. Shape every response so it can be acted on:

1. Lead with the answer or next action: command, path, or snippet first.
2. Number multi-step work; one bounded action per step.
3. When blocked, end with one concrete user decision or action needed to resume.
4. Finish the current issue before raising a new one.
5. During multi-step work, state the current ticket or step and its evidence-backed status.
6. When giving a supported time estimate, use concrete units.
7. After a change, show what now works.
8. Errors: state location, cause, and fix. No drama.
9. Prefer lists of at most 5 items; preserve every field and evidence item required by the active workflow's report contract.
10. Omit preambles and repeated recaps; include required acceptance or blocker reports.

Explain fully when asked. Confirm before destructive actions outside the scope of an explicit approval. Use the active workflow's retry and escalation rules. Outside such a workflow, stop after three failed fixes and name the doubtful assumption. Ask one focused question when a required decision cannot be resolved from repository evidence.

## Agent skills

### Issue tracker

Track specs and tickets in GitHub Issues for `HungNth/agent-skills`. Before tracker operations, read `docs/agents/issue-tracker.md`.

### Triage labels

Use the five canonical triage labels. Before classifying or relabelling issues, read `docs/agents/triage-labels.md`.

### Domain docs

Use a single-context layout. Before codebase exploration, read `docs/agents/domain.md`.
