# OpenSpec Delivery: Pi + AGY and OMP + AGY

=======

# AGENTS.md

- Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current requirements. Avoid speculative abstractions, configuration, and indirection .
- Grow the system in layers. Start from the smallest version that works end to end, and add each new capability on top of a product that already works. Never trade a working product for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.
- Study how established products solve the problem before designing a solution. Adopt their proven patterns and conventions rather than inventing an approach from scratch.

## Output style

The reader has ADHD. Shape every response so it can be acted on:

1. Lead with the answer or next action: command, path, or snippet first.
2. Number multi-step work; one bounded action per step.
3. End with one next action doable in under two minutes.
4. Finish the current issue before raising a new one.
5. Restate progress each turn ("step 3 of 5 done").
6. Give time estimates in concrete units, never "a bit".
7. After a change, show what now works.
8. Errors: state location, cause, and fix. No drama.
9. Cap lists at 5 items.
10. No preamble, no recaps, no closers.

Exceptions: explain fully when asked to explain. Confirm before destructive actions. After three failed fixes, stop and name the doubtful assumption. If the request is ambiguous, ask one short question.

# OMP + OpenSpec Development Workflow

This repository supports two delivery workflows. Every agent follows the shared rules; each orchestrator additionally follows its own section and must read its exact delivery skill before starting a delivery.

## Shared rules

- OpenSpec owns requirements, specifications, design, tasks, and change history. Never create a second plan alongside an active OpenSpec change.
- Planning workflows (`/opsx-explore`, `/opsx-propose`) authorize planning only. Implementation starts only on a separate, explicit request to deliver a named approved change.
- Read current OpenSpec status, apply instructions, and every context file before delegating or deciding; never assume repository-relative artifact paths.
- Keep work scoped to the approved change. Do not silently absorb scope, weaken or skip tests, or interpret requirements. Stop for user guidance on credentials, destructive actions, permission escalation, deployment, publishing, requirement or design decisions, and model escalation.
- Worker reports are claims. Accept work only from fresh diffs, checks, and verification evidence; never mark a task complete without its stated verification passing.
- An AGY worker performs only its assigned atomic workflow. It never starts another delivery, creates workers or panes, or invokes an orchestration skill.

## Pi + AGY: pi-openspec-agy-delivery

Pi coordinates dependency-aware parallel AGY workers per `skills/pi-openspec-agy-delivery/SKILL.md`:

- Pi owns planning, dependency scheduling, review, acceptance, and integration; Pi never writes implementation code during delivery.
- AGY performs apply, fresh read-only verification (`--mode plan`), spec sync, and archive in separately authorized stages, each after Pi accepts the preceding gate.
- Independent tasks run in parallel waves with a default maximum of three workers; every concurrent writer gets its own branch, external worktree, and Herdr pane.
- Pi accepts integrated work, then a single AGY integration worker updates authoritative task markers; parallel lanes report candidate completion only.
- Pi creates local planning and lane commits (`delivery/<change>` when starting from the default branch) and never pushes or merges into the default branch.
- Remediation continues while progress is measurable and stops after two consecutive rounds without progress. Cleanup is success-only and non-force; failures preserve every resource for resumption.

## OMP + AGY: openspec-agy-delivery

OMP coordinates the AGY delivery per `skills/openspec-agy-delivery/SKILL.md`:

- OMP owns planning and synthesis, diff review, `/opsx-verify`, fresh project checks, remediation decisions, spec synchronization, and archive; AGY implements the approved tasks and updates task completion markers.
- Delivery uses one AGY worker on the attributed existing working tree by default; any alternate topology requires explicit user authorization.
- OMP commits nothing without a separate user request. Remediation is bounded at three failed rounds and stops earlier when the same blocker repeats without progress.
- On failure, preserve the working tree and report; after archive or termination, optionally close the worker pane.
- OMP-only aids: `scout` for broad repository exploration, `librarian` for external research, `sonic` for mechanical edits. Keep architectural and acceptance decisions with the main agent, and use the `reviewer` agent for substantial changes.
