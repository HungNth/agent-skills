# OpenSpec Delivery: Pi + AGY and OMP + AGY

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
