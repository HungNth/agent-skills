## ADDED Requirements

### Requirement: Task source comes from OpenSpec apply instructions
The delivery workflow and the AGY apply contract SHALL derive the task list and task artifact path(s) from `openspec instructions apply --json` instead of assuming `tasks.md` or any other literal path.

#### Scenario: Spec-driven schema
- **WHEN** the selected change uses the default spec-driven schema
- **THEN** the workflow reads the `tasks` artifact path reported under `contextFiles` (typically `tasks.md`) and uses the same JSON task list for both OMP dispatch and AGY implementation

#### Scenario: Custom schema
- **WHEN** the selected change uses a schema whose task artifact is not `tasks.md`
- **THEN** the workflow follows the file path the schema reports and does not substitute, alias, or hardcode a different path

### Requirement: OMP evaluates dependencies and schedules delivery with safe concurrency fallback
OMP SHALL evaluate task dependencies from the schema-reported task list, schedule dependent tasks sequentially on a single primary worker, and MAY schedule independent tasks concurrently only when isolation/integration preconditions hold. Concurrency is an optimization; the single-worker path is the default.

#### Scenario: Tasks have dependencies
- **WHEN** tasks share base schemas, interfaces, or sequential outputs
- **THEN** OMP dispatches them sequentially on the primary worker and evaluates each task's diff and completion marker before dispatching the next

#### Scenario: Tasks are independent and topology preconditions hold
- **WHEN** independent root tasks exist, the primary tree is clean except for attributable change-root edits, repo-local change artifacts are committed at HEAD, and no more than three concurrent panes are needed
- **THEN** OMP MAY dispatch them concurrently on detached `git worktree`s integrated by binary patch; otherwise OMP falls back to the single-worker path

#### Scenario: Concurrency preconditions fail
- **WHEN** the primary tree is dirty, change artifacts are not committed, worker-side OpenSpec probe does not return the same change/store with `state: ready` and the same task IDs, or independence cannot be established
- **THEN** OMP removes the worktree (if created), falls the entire stage back to sequential, and never copies or guesses artifact paths into a worktree

### Requirement: Concurrent integration is patch-based and creates no commits
Concurrent worker results SHALL be integrated into the primary tree through a binary patch that is applied and verified before the worktree is removed. AGY SHALL NOT commit, merge, or create branches on the primary tree.

#### Scenario: Patch precheck passes
- **WHEN** OMP exports `git diff HEAD --binary --output=<patch> -- <approved-implementation-paths>` from the worktree and runs `git apply --check <patch>` in the primary tree
- **THEN** OMP runs `git apply <patch>`, reviews the resulting diff, updates the task marker in the primary tree, then `git worktree remove --force <path>` and deletes the patch file

#### Scenario: Patch precheck fails
- **WHEN** `git apply --check` reports any error
- **THEN** OMP keeps the worktree and patch file for investigation, does not modify the primary tree, and stops with the exact blocker

#### Scenario: Integration includes only approved implementation paths
- **WHEN** OMP selects which paths to integrate
- **THEN** the selected paths exclude the schema-reported task artifact, the planning artifacts under `openspec/changes/<change>/`, and any OMP-owned file

### Requirement: Concurrent scheduling stops after the first accepted implementation edit
After the primary tree accepts any implementation edit from a concurrent worker, OMP SHALL NOT create additional detached worktrees; remaining stages run on the single primary worker so subsequent tasks see the accepted baseline.

#### Scenario: Stage baseline captured
- **WHEN** OMP has applied at least one approved patch and updated at least one task marker in the primary tree
- **THEN** OMP does not create new worktrees for the remaining tasks and continues with the single primary worker

### Requirement: Worker status drives OMP progression
OMP SHALL read the worker's `result.agent.status` after each prompt and SHALL NOT advance to the next task or gate until the worker reports `idle` or `done`. Other statuses are diagnostic signals.

#### Scenario: Worker reports idle or done
- **WHEN** the AGY worker settles with status `idle` or `done`
- **THEN** OMP reviews the transcript, the working-tree change, and the task marker; this is the only state that authorizes advancement

#### Scenario: Worker reports blocked
- **WHEN** the worker reports `blocked`
- **THEN** OMP reads the transcript, replies with mechanical input only (no scope expansion), and re-prompts; if the same blocker repeats three times for one task, OMP halts that task without marking it complete

#### Scenario: Worker status is unknown or times out
- **WHEN** the worker reports `unknown`, times out, or returns a command error
- **THEN** OMP inspects the worker, the transcript, and the worktree (if any) before deciding to retry; OMP does not advance

### Requirement: AGY apply contract accepts an optional orchestrator assignment
The `openspec-apply-change` skill SHALL accept an optional set of `assigned task IDs` from the orchestrator and SHALL implement only those IDs, even when other pending tasks exist in the same change. Without assignment, the existing full-pending-task loop is preserved.

#### Scenario: Orchestrator supplies assigned task IDs
- **WHEN** OMP passes assigned task IDs and a selected change/store
- **THEN** the apply contract cross-checks each ID against the schema-reported task list, rejects missing, already-complete, or out-of-change IDs as blockers, implements only the assigned tasks, marks only their checkboxes complete, and reports overall remaining progress even when OpenSpec still reports `ready`

#### Scenario: No assignment is supplied
- **WHEN** OMP does not supply assigned task IDs
- **THEN** the apply contract preserves its original behavior and iterates all pending tasks

#### Scenario: Task artifact path
- **WHEN** the apply contract reads the task artifact
- **THEN** it uses the path the schema reports under `contextFiles` and does not hardcode, alias, or fall back to `tasks.md` for any other schema

### Requirement: All-done state still creates a lifecycle AGY worker
When `openspec instructions apply` reports `state: all_done`, OMP SHALL skip implementation but SHALL still start (or reuse) an AGY worker to execute `openspec-verify-change` and the canonical lint/typecheck/test/build commands. State `blocked` stops OMP before any pane mutation.

#### Scenario: Apply state is all_done
- **WHEN** OpenSpec reports `state: all_done`
- **THEN** OMP does not prompt AGY to implement, but starts a lifecycle AGY worker that executes verification; OMP independently runs a targeted smoke check on the primary tree

#### Scenario: Apply state is blocked
- **WHEN** OpenSpec reports `state: blocked`
- **THEN** OMP stops before any Herdr pane mutation, agent start, or prompt and reports the missing planning prerequisite

### Requirement: Verification is bounded remediation with OMP independent smoke
After implementation tasks are integrated, OMP SHALL instruct AGY to execute `openspec-verify-change` and the canonical lint/typecheck/test/build commands OMP discovered, and OMP SHALL run a smallest behaviorally relevant smoke check on the primary tree independently. Weakened, skipped, or disabled tests are forbidden.

#### Scenario: AGY executes verification
- **WHEN** OMP instructs the lifecycle AGY worker to run verification
- **THEN** OMP reviews the raw transcript, exit outcomes, and the complete primary diff (tracked, staged, untracked) and rejects any weakened, skipped, or disabled test

#### Scenario: Remediation succeeds within three rounds
- **WHEN** AGY fixes the reported findings within three rounds and re-runs every blocking command
- **THEN** OMP reviews the new diff and re-runs the targeted smoke before authorizing archive

#### Scenario: Remediation remains unsuccessful
- **WHEN** three rounds fail or the same unresolved blocker repeats without progress
- **THEN** OMP halts, preserves the primary tree, and refuses archive authorization

### Requirement: Archive prompt pins Sync now (recommended)
OMP SHALL authorize `openspec-archive-change` only after every gate passes and SHALL send an archive prompt that explicitly names `Sync now (recommended)` and forbids AGY from choosing any other option.

#### Scenario: All gates pass
- **WHEN** implementation is complete, `openspec-verify-change` reports zero CRITICAL findings, every canonical check and OMP's targeted smoke pass, and no protected decision remains
- **THEN** OMP prompts AGY with the pinned archive prompt, AGY executes `openspec-archive-change`, and OMP confirms the original `changeRoot` is gone, the archive path exists, the main spec reflects the delta, and `openspec validate --specs --strict --no-interactive [--store <id>]` plus `openspec validate --archived --strict --no-interactive [--store <id>]` pass

#### Scenario: A blocking gate remains
- **WHEN** any required gate or decision remains unresolved
- **THEN** OMP does not authorize archive, the change remains active, and the workflow reports why archive was blocked

### Requirement: Evaluations ship with the skill package
The skill package SHALL include `evals/evals.json` whose repeatable cases cover the revised behavior and the previously-broken behavior so the running revision can be distinguished from the prior one. The file SHALL be tracked in git while evaluation scratch under `skills/openspec-agy-delivery-workspace/` SHALL remain ignored.

#### Scenario: Revised skill runs against new cases
- **WHEN** the evaluation suite runs against the revised skill
- **THEN** every case that targets the new behavior passes and the previously-broken cases (commit/merge in concurrent path, missing worktree context, missing assigned-task boundary, broken `all_done` lifecycle) fail

#### Scenario: Eval definitions are tracked but scratch is not
- **WHEN** `git status` inspects the skill package
- **THEN** `skills/openspec-agy-delivery/evals/evals.json` is tracked and `skills/openspec-agy-delivery-workspace/` is ignored

## MODIFIED Requirements

### Requirement: AGY follows the approved OpenSpec apply contract
The AGY worker SHALL implement only the tasks OMP assigns via the apply contract, update required task completion markers, run implementation-time checks, and return structured reports for OMP evaluation. The AGY worker SHALL NOT commit, merge, branch, or archive without explicit OMP authorization.

#### Scenario: Apply state is ready with assigned task IDs
- **WHEN** OpenSpec reports remaining implementation tasks and OMP supplies an assigned task subset
- **THEN** AGY reads every reported context file, implements and marks complete only the assigned tasks, runs implementation-time checks, and reports overall remaining progress even when OpenSpec still reports `ready`

#### Scenario: Apply state is blocked
- **WHEN** OpenSpec reports that required planning artifacts are missing or the apply workflow is blocked
- **THEN** the delivery workflow stops without asking AGY to invent missing plans or requirements

#### Scenario: Apply state is ready
- **WHEN** OpenSpec reports remaining implementation tasks
- **THEN** AGY reads every reported context file, implements the remaining tasks, updates required completion markers, runs implementation-time checks, and returns a structured report

#### Scenario: Worker encounters a protected decision
- **WHEN** implementation requires a credential, destructive action, permission escalation, deployment, publishing, requirement decision, or scope expansion
- **THEN** AGY stops and OMP presents the blocker to the user instead of guessing or auto-approving it

### Requirement: Verification failures use bounded remediation
When verification fails, AGY SHALL execute the bounded remediation rounds and re-run every blocking command; OMP SHALL re-run targeted verification on the primary tree after each round.

#### Scenario: Remediation succeeds
- **WHEN** AGY fixes the reported findings within the allowed rounds and re-runs every blocking command
- **THEN** OMP re-runs `openspec-verify-change`, the canonical project verification, and a targeted smoke check on the primary tree before continuing

#### Scenario: Remediation remains unsuccessful
- **WHEN** three remediation rounds fail or the same unresolved blocker repeats without progress
- **THEN** the workflow stops, preserves the working tree, and reports the remaining findings without archiving

### Requirement: Archive is owned and gated by OMP
OMP SHALL gate and authorize archive, AGY SHALL execute `openspec-archive-change` only after an explicit OMP archive prompt that pins `Sync now (recommended)`, and OMP SHALL verify the archive outcome before reporting success.

#### Scenario: Every blocking gate passes
- **WHEN** implementation is complete, `openspec-verify-change` has no CRITICAL findings, every canonical check and OMP's targeted smoke pass, and no protected decision remains
- **THEN** OMP prompts AGY with the pinned archive prompt, AGY executes `openspec-archive-change`, and OMP confirms the archive path, the synced main spec, and the two `openspec validate` calls

#### Scenario: A blocking gate remains
- **WHEN** any required gate or decision remains unresolved
- **THEN** OMP does not authorize archive, the change remains active, and the workflow reports why archive was blocked
