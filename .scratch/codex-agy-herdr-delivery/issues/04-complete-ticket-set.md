# 04: Complete a ticket set and make the workflow authoritative

**Parent specification:** `../spec.md`

**What to build:** Extend the accepted single-ticket workflow across an entire dependency graph, perform final feature closeout, report the completed delivery, and leave one authoritative Codex-led workflow in the repository.

**Blocked by:** 03: Recover and remediate an unfinished ticket.

**Status:** ready-for-agent

## Allowed scope

Ticket Frontier advancement, fresh-worker sequencing, completion-ledger reconstruction, final verification and reporting, repository routing guidance, removal of obsolete OMP and retired Herdr paths, and final skill validation. Do not add parallel delivery or automatic integration.

## Acceptance criteria

- [ ] Codex recomputes the ordered Ticket Frontier before every ticket and selects only a ticket whose explicit blockers have accepted commits.
- [ ] Every ticket receives a fresh Implementation Agent; an agent is reused only for remediation of its own ticket.
- [ ] Approved specification and ticket files remain immutable throughout delivery.
- [ ] Accepted ticket commits with canonical local references form the only completion ledger; no progress or orchestration state files are introduced.
- [ ] The next ticket cannot start until the current ticket has an accepted commit and its worker has been cleaned up.
- [ ] After every ticket is accepted, Codex runs authoritative full verification from a clean committed delivery branch and reviews the aggregate diff against the parent specification.
- [ ] Final closeout handles a narrow attributable implementation defect through bounded same-ticket remediation and stops for cross-ticket design or requirement gaps.
- [ ] The final report lists the parent specification, tickets in execution order, commit for each ticket, remediation counts, verification evidence, changed files, tracker state, remaining risks, and preserved branch and worktree state.
- [ ] Final closeout does not push, merge, rebase, deploy, remove the branch or worktree, or change approved planning files.
- [ ] Repository guidance routes approved implementation requests to `ship-with-agy`, describes Codex as Lead Agent and AGY as Implementation Agent, and names local Markdown as the tracker.
- [ ] Obsolete OMP-specific guidance and retired `herdr` workflow documentation are removed rather than retained as compatibility paths.
- [ ] The generic implementation skill remains unchanged.
- [ ] The repository's skill validator and diff checks pass with no unrelated user changes modified.

## Testing seam

Validate the complete skill as one external workflow: resolve a multi-ticket local dependency graph from ticket-referenced commits, advance it serially, run final closeout, and compare the final report and repository state with the approved specification.

## Demo path

Replay a small local ticket graph through the completed workflow or its accepted smoke evidence, demonstrate deterministic frontier advancement and final closeout, then show the authoritative repository guidance and absence of legacy workflow paths.

## Expected deliverables

A complete serial local-ticket delivery workflow, final closeout and reporting contracts, authoritative repository guidance, legacy-path removal, and passing package validation.
