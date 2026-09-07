# OMP + OpenSpec Development Workflow

Sections prefixed `OMP-only` apply only to the OMP orchestrator. AGY implementation workers must not invoke OMP worker kinds or delegation rules; they follow the applicable delivery policy (`OpenSpec AGY delivery` for OMP or `Pi + OpenSpec AGY delivery: pi-openspec-agy-delivery` for Pi) and their approved OpenSpec apply context.

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

## Pi + OpenSpec AGY delivery: pi-openspec-agy-delivery

`pi-openspec-agy-delivery` is a Pi-owned orchestration workflow. An AGY implementation worker must use its assigned atomic OpenSpec workflow (`openspec-apply-change`, `openspec-verify-change`, `openspec-sync-specs`, or `openspec-archive-change`) and must never invoke `pi-openspec-agy-delivery` or `openspec-agy-delivery`, create another worker, or orchestrate deliveries.

### Hard post-planning approval
Planning workflows (`/opsx-explore`, `/opsx-propose`) authorize planning only. Pi must stop after planning artifacts are complete without starting AGY workers or modifying implementation files. Implementation begins only when the user explicitly requests delivery of a named, approved OpenSpec change through `pi-openspec-agy-delivery`.

### One writer per branch/worktree/pane
Every concurrently active AGY implementation writer must be isolated in its own dedicated git branch (`agy/<change>/<lane>`), clean git worktree, and Herdr pane. No two active writers ever share a working tree or pane.

### Dependency-aware parallel waves with default maximum three
Pi builds a conservative task dependency graph from approved artifacts, interfaces, modules, and repository evidence. Execution runs in topological waves branching from the latest accepted integration commit. Uncertain dependencies are serialized rather than guessed as parallel. Concurrency is capped at a default maximum of three workers (`min(3, ready lanes)`); an explicit user concurrency limit acts as an upper bound.

### Pi acceptance and local-only integration commits
Pi owns diff inspection, test-integrity review, rerunning targeted and full project gates, and acceptance. Pi integrates accepted lanes in dependency order using local commits on the integration branch. Pi never modifies implementation code itself. Mechanical integration conflicts are delegated to a single AGY integration worker; contract-changing conflicts halt for user planning clarification.
Authoritative task completion markers on the integration branch are owned by Pi and updated by an AGY integration worker only after accepted code is integrated and verified; parallel implementation lanes report candidate completion but do not modify authoritative task markers.

### AGY ownership of atomic OpenSpec workflows
AGY performs all post-planning OpenSpec operations under Pi's gated supervision: implementation via `openspec-apply-change`, verification via `openspec-verify-change`, synchronization via `openspec-sync-specs`, and archive via `openspec-archive-change`. Each stage is prompted separately after preceding gates pass.

### Fresh read-only verification
Every verification cycle must run in a fresh AGY conversation started with `--mode plan`, `gemini-3.8-flash-high`, and `--effort high`. The verifier has no write authority, cannot modify files, and cannot transition into a writer role. The verifier evaluates completeness, correctness, coherence, task state, and test integrity. The verifier's report is advisory evidence and never replaces Pi's independent project gates. Any remediation modifying implementation triggers a new fresh read-only verification cycle.

### Safe local integration branch and no-push boundary
Delivery creates local orchestration checkpoints and accepted lane commits only. If delivery starts on the default branch, Pi creates a local `delivery/<change>` integration branch before committing the planning checkpoint. Delivery results remain on the local integration branch without pushing to remotes, force-pushing, rebasing, opening pull requests, or merging into the default branch.

### Progress-aware remediation
Pi automatically retries actionable AGY failures without an arbitrary fixed round cap as long as measurable progress occurs (reducing failing tests, clearing blocking issues, or completing behavior). If the same blocker persists across two consecutive rounds without progress, Pi halts and reports the blocker for user action. Pi immediately stops for user guidance on protected decisions (credentials, destructive actions, permission escalation, deployment, publishing, requirement/design decisions, scope changes, model escalation). In case of worker crashes or timeouts, partial work is inspected and preserved before resuming or replacing workers.

### Failure preservation and success-only cleanup
On failure, user interruption, or unresolved blockers, Pi preserves all worker conversations, Herdr panes, branches, worktrees, local commits, partial changes, and diagnostic evidence for inspection and resumption. Only after complete success across all stages (implementation, verification, synchronization, archive, and final audit pass), Pi cleans workflow-created idle panes, clean lane worktrees, and fully integrated lane branches using non-force operations. The integration branch is always retained. Any resource refusing non-force removal is reported and preserved intact.
