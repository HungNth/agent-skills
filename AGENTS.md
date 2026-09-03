# OMP + OpenSpec Development Workflow

Sections prefixed `OMP-only` apply only to the OMP orchestrator. AGY implementation workers must not invoke OMP worker kinds or delegation rules; they follow the shared `OpenSpec AGY delivery` section and their approved OpenSpec apply context.

## Responsibility split

OpenSpec owns feature requirements, specifications, design artifacts, task
tracking, and change history.

OMP owns execution, model routing, subagent delegation, implementation,
integration, and verification.

Do not create a second OMP Plan Mode plan for a change already being managed
through OpenSpec unless the user explicitly asks for a separate tactical
investigation.

## OMP-only: Main-agent responsibility

The main agent is the orchestrator.

The main agent owns:

- understanding the user's goal;
- architectural decisions;
- decomposition and cross-task contracts;
- integration of delegated results;
- final verification;
- deciding whether the implementation satisfies the OpenSpec artifacts.

Do not delegate the top-level architecture decision to a generic task worker.

## OMP-only: Repository exploration

Use `scout` for broad codebase discovery, file mapping, dependency tracing,
and read-only investigation.

Use `librarian` for external libraries, framework APIs, package behavior,
and source-backed external research.

Avoid spending the main agent's context reading large numbers of files when
a scout can return a compressed map.

## OMP-only: OpenSpec planning

During OpenSpec explore/propose/new/continue/ff workflows, do not modify
project implementation code.

Use scouts or librarians when research is needed.

The main agent should synthesize findings and own the final proposal,
specification, design, and task decomposition.

## OMP-only: OpenSpec implementation orchestration

During OpenSpec apply:

1. Read the selected change's proposal, specs, design, and tasks first.
2. Establish shared interfaces and dependencies before delegation.
3. Follow the selected implementation workflow. A specifically approved delivery workflow may assign implementation to AGY; otherwise delegate independent work to general `task` workers.
4. Use `sonic` only for mechanical, low-judgment edits or data collection.
5. Keep tightly coupled or architectural work with the main agent when delegation would add more coordination cost than value.
6. Do not run repository-wide lint, test, or build commands independently in every worker.
7. Integrate delegated results in the main agent.
8. Run final targeted verification once integration is complete.

## OpenSpec AGY delivery

`openspec-agy-delivery` is an OMP orchestration workflow. An AGY implementation worker must use `openspec-apply-change` and must never invoke the delivery workflow or create another AGY worker.

For the default single-worker delivery, use the existing repository working tree only after the dirty-tree attribution preflight passes. Create a worktree only when the user explicitly authorizes one or an approved concurrent-worker topology requires it.

Herdr, AGY, OpenSpec, git, and AGY authentication are delivery prerequisites. Additional TDD, debugging, review, verification, or worktree skills are optional aids; when unavailable, follow the equivalent explicit project and delivery rules.

## OMP-only: Review

For substantial changes, use the `reviewer` agent after implementation and
before considering the change complete.

The main agent is responsible for evaluating reviewer findings and applying
or delegating fixes.

## OMP-only: Cost policy

Prefer specialized workers for high-volume implementation and exploration.
Reserve the main reasoning model for architecture, integration, ambiguous
decisions, and final correctness judgments.
