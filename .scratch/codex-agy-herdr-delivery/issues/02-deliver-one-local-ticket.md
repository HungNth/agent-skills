# 02: Deliver one local ticket through Codex and Herdr

**Parent specification:** `../spec.md`

**What to build:** Enable Codex to take one approved local Markdown ticket from a clean Delivery Base through an isolated Delivery Worktree, a fresh AGY Implementation Agent, evidence-backed Ticket Acceptance, an accepted commit, and worker cleanup.

**Blocked by:** 01: Install the AGY Implementation Agent template safely.

**Status:** ready-for-agent

## Allowed scope

The single-ticket happy path, including conductor preflight, local tracker resolution, worktree creation, worker briefing, candidate review, verification, commit, and accepted-worker cleanup. Recovery, bounded remediation, multiple tickets, and final feature closeout belong to later tickets.

## Acceptance criteria

- [ ] Delivery starts only from an explicitly approved local specification and ticket.
- [ ] Preflight proves the current Codex parent through Herdr Core, confirms no-daemon operation, verifies the installed template, and fails closed without direct AGY fallback.
- [ ] A new delivery records a clean Delivery Base and creates the deterministic feature branch and sibling Delivery Worktree without stashing, resetting, cleaning, or discarding existing work.
- [ ] The first runnable local ticket is resolved from its canonical repository-relative reference.
- [ ] Codex launches one uniquely named, fresh Implementation Agent in the Delivery Worktree with the first task included at launch.
- [ ] The task contains the parent and ticket references, semantic scope, acceptance criteria, verification requirements, restrictions, exact working directory, and explicit parent terminal address.
- [ ] Codex observes `STARTED`, `BLOCKED`, or `DONE` through Herdr Core and inspects the actual report and repository state.
- [ ] A `DONE` report does not count as acceptance without diff inspection, declared verification, scope review, security and regression review, and a stable candidate.
- [ ] Codex does not edit product code, tests, or candidate files during review.
- [ ] An accepted candidate is committed with its canonical local ticket reference while the approved planning files remain unchanged.
- [ ] Only the accepted ticket's workflow-created terminal is killed and removed after the commit.
- [ ] No push, merge, worktree removal, branch removal, or unrelated tracker mutation occurs.
- [ ] The repository's skill validator passes.

## Testing seam

Exercise the workflow at the Herdr, Git, and filesystem boundary in a disposable Git repository using the real installed template and one harmless local ticket.

## Demo path

Launch a real `gemini-4-hydrogen-high` Implementation Agent through Herdr Core, make one harmless change in the disposable repository, receive its report, review the diff, create the accepted ticket-referenced commit, and clean up only that worker terminal.

## Expected deliverables

A Codex-led single-ticket delivery path, updated conductor and worker prompt contracts, and recorded live-smoke evidence.
