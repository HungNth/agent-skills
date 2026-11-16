# Codex-led AGY delivery through Herdr Core

Status: ready-for-agent

## Problem Statement

The user plans features with Codex in Herdr App, but the repository's delivery workflow does not match the desired runtime. The existing delivery skill assumes OMP, uses the retired `herdr` interface, runs in the main checkout, and delegates substantive review to another AGY agent. The generic implementation skill would let the lead agent write product code directly. There is also no versioned Herdr template or portable installer that reliably launches AGY with the required model.

The user needs one recoverable workflow in which planning stays with Codex, approved tickets are stored locally, AGY performs all product-code edits, and Codex monitors, reviews, accepts, commits, and reports each ticket through Herdr Core without automatically integrating the finished feature.

## Solution

Make `ship-with-agy` the delivery entrypoint for an approved local Markdown ticket set. Codex remains the Lead Agent and acceptance authority. It proves its Herdr identity, creates or resumes one isolated Delivery Worktree, computes the Ticket Frontier, and launches a fresh AGY Implementation Agent for one ticket at a time through a versioned Herdr template pinned to Gemini 4 Hydrogen High.

Each Implementation Agent receives one ticket, its semantic scope and acceptance criteria, the exact working directory, restrictions, and the parent terminal address. Codex treats worker reports as evidence to inspect, reviews the actual candidate, runs the declared verification, returns defects to the same worker within a bounded remediation loop, and commits only accepted work. Approved planning files remain immutable, and ticket-referenced commits form the completion ledger.

Provide safe PowerShell and POSIX shell installers for the versioned Herdr template. Remove obsolete OMP and legacy Herdr guidance so repository instructions and the delivery skill describe one workflow. At final closeout, Codex verifies the aggregate delivery and reports the result without pushing, merging, deleting the worktree, or changing the approved plan.

## User Stories

1. As a feature owner, I want to start from `grill-with-docs`, so that domain language and architectural decisions are settled before delivery.
2. As a feature owner, I want specifications and tickets stored as local Markdown, so that planning does not depend on GitHub Issues.
3. As a feature owner, I want one canonical specification and ticket set, so that delivery never reconciles duplicate planning artifacts.
4. As a feature owner, I want implementation requests routed to `ship-with-agy`, so that the generic implementation skill does not cause Codex to write product code.
5. As a feature owner, I want delivery to start only after explicit approval of the ticket breakdown, so that AGY never implements unsettled requirements.
6. As a feature owner, I want Codex to prove it is running under Herdr Core, so that monitoring and recovery are available before delegation starts.
7. As a feature owner, I want delivery to fail closed when Herdr identity or the required template is unavailable, so that it never silently falls back to an unobservable AGY process.
8. As a Windows user, I want a PowerShell installer for the AGY template, so that setup is reproducible on my current machine.
9. As a macOS or Linux user, I want a POSIX shell installer for the same template, so that the workflow remains portable.
10. As a user with an existing Herdr template, I want installers to refuse unexpected overwrites, so that local customizations are not destroyed without explicit force.
11. As a feature owner, I want AGY pinned to `gemini-4-hydrogen-high`, so that every implementation ticket uses the approved model and effort level.
12. As a feature owner, I want one Delivery Worktree per feature, so that product changes remain isolated from my primary checkout.
13. As a feature owner, I want branch and worktree names derived from the local spec identity, so that an existing delivery can be recognized and resumed deterministically.
14. As a feature owner, I want tickets executed serially in dependency order, so that accepted changes accumulate without parallel merge conflicts.
15. As a feature owner, I want a fresh Implementation Agent for each ticket, so that unrelated ticket context does not leak between workers.
16. As a Lead Agent, I want every Implementation Agent to receive one bounded ticket and an exact working directory, so that the candidate has clear provenance.
17. As a Lead Agent, I want workers to report `STARTED`, `BLOCKED`, and `DONE` through Herdr Core, so that progress and intervention needs remain visible in Herdr App.
18. As a feature owner, I want Codex to inspect the actual diff rather than trust a `DONE` report, so that acceptance is based on repository evidence.
19. As a feature owner, I want Codex to check acceptance criteria, declared tests, scope, security, regressions, and candidate stability, so that incomplete or unsafe work is rejected.
20. As a feature owner, I want implementation defects returned to the same worker with a bounded retry count, so that remediation is focused and cannot loop forever.
21. As a feature owner, I want each accepted ticket committed with its canonical local ticket reference, so that completion can be reconstructed from Git history without mutable orchestration state.
22. As a feature owner, I want blocked or interrupted deliveries preserved, so that worktrees, diffs, and relevant Herdr terminals remain available for diagnosis.
23. As a feature owner, I want ambiguous dirty candidates to stop delivery, so that Codex never assigns unknown changes to the wrong ticket.
24. As a feature owner, I want final verification across the entire delivery, so that individually accepted tickets are also checked as an integrated feature.
25. As a feature owner, I want the final report to include accepted tickets, commits, verification evidence, remediation counts, changed files, tracker state, and risks, so that I can decide whether to integrate.
26. As a feature owner, I want push, merge, worktree removal, and other integration actions to require separate direction, so that delivery does not alter shared history automatically.
27. As a maintainer, I want obsolete OMP and legacy Herdr instructions removed, so that agents encounter one authoritative workflow.
28. As a maintainer, I want long-running commands and AGY sessions managed through Herdr Core, so that Codex remains reachable while work continues.

## Implementation Decisions

- The planning sequence is `grill-with-docs`, `to-spec`, `to-tickets`, explicit user approval, then `ship-with-agy`.
- `ship-with-agy` is the only delivery entrypoint. Repository guidance routes requests such as implement, ship, execute, continue, or finish to it when an approved ticket set exists.
- The installed generic implementation skill remains unchanged. It is not a compatibility layer or alternate path for this workflow.
- Local Markdown is the sole tracker. One feature directory contains one specification and one file per ticket, with dependency edges and triage state recorded in those files.
- Approved specifications and tickets become immutable during delivery. Accepted commits include the repository-relative ticket reference and form the durable completion ledger.
- Codex is the Lead Agent. It owns orchestration, substantive review, Ticket Acceptance, administrative commits, recovery decisions, final verification, and user reporting.
- AGY is the Implementation Agent and the only role allowed to edit product code or tests. It never commits, pushes, merges, changes planning artifacts, delegates, or starts subagents.
- No separate AGY verifier is used. Codex directly reviews each candidate and retains final acceptance authority.
- Delivery requires a recognized Herdr Core parent terminal running Codex without daemon mode. Missing or unprovable identity, a missing template, or a blocked readiness prompt stops delivery without direct-AGY fallback.
- The versioned implementer template launches interactive AGY in edit-accepting mode with `gemini-4-hydrogen-high`. The template contains stable role constraints; ticket-specific scope is supplied in the first launch task.
- The template is distributed with the skill and installed into the platform-specific Herdr template directory by PowerShell and POSIX shell installers.
- Installers are idempotent when contents match, refuse a conflicting installed template by default, and replace it only through an explicit force option.
- A new delivery records a clean Delivery Base, creates one feature branch and one sibling Delivery Worktree, and executes all tickets there serially.
- Delivery identity is derived from the local feature slug. If the expected branch or worktree already exists, the workflow enters recovery checks instead of deleting it or inventing a second identity.
- Before every ticket, Codex recomputes the ordered Ticket Frontier from explicit blocker edges and selects the first runnable ticket.
- Every ticket gets a uniquely named, fresh Implementation Agent in the Delivery Worktree. The first task is included in the Herdr launch and contains the ticket reference, acceptance criteria, semantic allowed scope, restrictions, verification commands, and explicit parent address.
- Workers report `STARTED`, `BLOCKED`, and `DONE`. Long reports may be written to a file and reported by path. Codex reads the actual result and terminal state rather than inferring success from status words.
- Codex never auto-answers permission, trust, or protected-decision prompts. A blocked worker requiring human authority stops for user action.
- Ticket Acceptance requires inspection of staged, unstaged, and untracked changes; conformance to the ticket and repository standards; passing declared checks; no blocking quality, security, regression, or scope findings; and an unchanged candidate during review.
- Codex may run deterministic verification and administrative Git operations, but it does not edit candidate files or run source-mutating fixers. Any tracked mutation during review invalidates the candidate.
- Implementation defects return to the same Implementation Agent with exact evidence. At most three remediation prompts are allowed, with earlier termination when the same blocker repeats without measurable progress.
- After Ticket Acceptance, Codex stages only the accepted candidate, commits it with the canonical local ticket reference, and removes only the accepted ticket's Herdr terminal.
- On failure or ambiguity, Codex preserves the Delivery Worktree and workflow-created terminals. It never stashes, resets, cleans, switches away, or deletes unaccepted work.
- Recovery reconstructs state from the named worktree, Git history, local ticket references, the current diff, and live Herdr transcripts. A dirty candidate resumes only when it can be attributed to exactly one unfinished ticket.
- Final closeout runs authoritative full verification from a clean committed delivery branch and reviews the aggregate delivery against the specification.
- Final closeout reports evidence but does not push, merge, delete the worktree, or alter the approved plan.
- Obsolete OMP-specific and retired Herdr workflow documents are removed rather than maintained as compatibility paths.
- Herdr App remains the human observation and takeover surface. This feature does not modify Herdr App or Herdr Core.

## Testing Decisions

- Tests verify externally observable behavior at the CLI and Git boundaries rather than wording or internal prompt structure.
- The existing skill validator is the prior-art structural check and must pass for the completed delivery skill.
- Installer contract tests use temporary platform config directories. Both installers must cover fresh installation, idempotent reinstallation, conflict refusal, and explicit forced replacement without touching the user's active template directory.
- A live delivery smoke test uses a disposable Git repository, the installed template, Herdr Core, and a real interactive AGY session pinned to `gemini-4-hydrogen-high`. The smoke task makes one harmless change and verifies reporting, diff visibility, Codex review, an accepted commit, and terminal cleanup.
- The live smoke test does not push, merge, or operate on GitHub Issues.
- Repository diff checks confirm that verification does not mutate tracked candidate files and that unrelated pre-existing work is preserved.
- No unit tests are added solely for prose. New executable installer behavior must be covered through its black-box contract test.

## Out of Scope

- Parallel ticket execution or one worktree per ticket.
- Remote Herdr machines.
- Automatic model selection, effort escalation, or models other than `gemini-4-hydrogen-high`.
- Direct AGY execution when Herdr Core preflight fails.
- A second AGY reviewer or verifier role.
- Changes to Herdr App, Herdr Core, Codex CLI, or AGY CLI themselves.
- Automatic installation or overwrite of global Herdr templates during delivery.
- GitHub Issues, pull requests, or another remote tracker as planning storage.
- Automatic push, merge, rebase, deployment, parent-spec closure, worktree deletion, or branch deletion.
- Backward compatibility for OMP-specific or retired `herdr` commands.
- Duplicate feature plans under another documentation tree.

## Further Notes

- The model identifier verified from the installed AGY CLI is `gemini-4-hydrogen-high`; `geminmi-4-hydrogen` and `gemini-4-hydrogen` are not valid complete identifiers.
- The installed Herdr Core manual requires background interactive agent launches, first-task delivery at launch time, readiness inspection before resend, and explicit child cleanup after acceptance.
- The live AGY smoke test consumes a real model invocation and requires an authenticated AGY installation.
- Existing unrelated user changes, including the current README modification, must remain untouched.
