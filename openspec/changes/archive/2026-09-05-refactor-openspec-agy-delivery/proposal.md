## Why

The current `openspec-agy-delivery` workflow delegates implementation as a single coarse-grained execution block where AGY applies all tasks at once, while OMP independently runs verify, spec synchronization, and archive.

This model has limitations:
1. It does not support task-by-task iterative review, allowing errors to accumulate across multiple tasks before OMP detects them.
2. It cannot parallelize independent tasks across multiple AGY worker panes in Herdr to accelerate delivery.
3. It prevents AGY from executing the standard `openspec-verify-change` and `openspec-archive-change` workflows, placing all verification execution burden on OMP rather than having OMP act as an evaluator and gatekeeper.
4. The concurrent path is unsafe as written: AGY is forbidden from committing while OMP integrates via `git merge`, and detached worktrees do not inherit repo-local change artifacts or uncommitted implementation edits, so concurrent dispatches can silently corrupt user work.
5. `openspec-apply-change` does not honor an orchestrator-supplied task assignment; it iterates the full pending task list, which conflicts with task-by-task dispatch and breaks the assignment boundary the delivery workflow depends on.

By refactoring the workflow, OMP retains ownership of planning (`openspec-explore` / `openspec-propose`), pre-dispatch task DAG analysis, worker briefs, scheduling (sequential by default, concurrent only when isolation/integration preconditions hold), diff and patch integration, targeted independent smoke verification, and archive gating. AGY owns scoped implementation of assigned tasks (`openspec-apply-change`), verification execution (`openspec-verify-change`), and authorized archive execution (`openspec-archive-change`).

## What Changes

- **OMP Planning Separation**: Explicitly preserve planning as an upfront stage owned by OMP using `openspec-explore` and `openspec-propose`.
- **Schema-Driven Task Source**: OMP and AGY both derive the task list and task artifact path(s) from `openspec instructions apply --json` instead of literal `tasks.md`. The task file is whatever the schema reports under `contextFiles` (for spec-driven, the path is `tasks.md`; for custom schemas, it is the file the schema names).
- **Pre-Dispatch Dependency Analysis**: OMP analyzes task dependencies into a DAG (sequential vs independent tasks) using the schema-reported task list.
- **Scheduling With Safe Concurrency Fallback**:
  - Sequential tasks run on a single primary AGY worker with OMP reviewing diffs and transcripts between tasks.
  - Independent tasks MAY run concurrently across detached worktrees, but only when isolation/integration preconditions hold; otherwise the workflow falls back to sequential without asking.
- **Patch-Based Concurrent Integration (No Commits)**: Concurrent worker results return to the primary tree as binary patches for approved implementation paths; the primary tree runs `git apply --check` then `git apply`, updates task markers itself, and removes the worktree. No `git merge`, no branch, no commit from AGY.
- **Continuous OMP Evaluation**: OMP evaluates each task's diff and completion status before advancing to subsequent tasks.
- **Assigned-Task Apply Contract**: `openspec-apply-change` accepts an optional orchestrator-supplied set of assigned task IDs and implements only those IDs, even when other pending tasks exist. Without assignment the apply contract behaves as before.
- **AGY-Executed Verification & Lifecycle Archive Under OMP Gates**:
  - OMP instructs an AGY worker to execute `openspec-verify-change` and the canonical project lint/typecheck/test/build/smoke commands OMP discovered. OMP evaluates the transcript, the complete primary diff (tracked, staged, untracked), and runs its own targeted smoke check.
  - When every gate passes, OMP authorizes archive with a prompt that pins `Sync now (recommended)` and forbids AGY from picking another option.
  - After archive, OMP verifies the archive path exists, the change root is gone, the main spec reflects the delta, and runs `openspec validate --specs --strict --no-interactive` and `openspec validate --archived --strict --no-interactive`.
- **Agent Roles and Coordination Policy**: Update `AGENTS.md` and skill instructions to define this cooperative orchestration contract.

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `openspec-agy-delivery`: Update requirements to cover schema-reported task source, task-by-task DAG scheduling, safe concurrent scheduling with detached worktrees and patch-based integration (no commit), AGY-Executed verification and authorized archive, and assignment-aware `openspec-apply-change`.

## Impact

- Affected skill files:
  - `skills/openspec-agy-delivery/SKILL.md` (canonical, end-to-end executable flow)
  - `.agents/skills/openspec-agy-delivery/SKILL.md` (kept byte-identical to the canonical)
  - `.agents/skills/openspec-agy-delivery/evals/evals.json` (new, tracked repeatable evals per the main capability spec)
  - `.gemini/skills/openspec-apply-change/SKILL.md`, `.agents/skills/openspec-apply-change/SKILL.md`, `.omp/skills/openspec-apply-change/SKILL.md` (assigned-task semantics)
- Affected guidelines: `AGENTS.md` (revised orchestration contract)
- Affected ignore rules: `.gitignore` (unignore `skills/openspec-agy-delivery/evals/evals.json` while keeping `skills/openspec-agy-delivery-workspace/` ignored as evaluation scratch)
- Runtime dependencies: `herdr`, `agy`, `openspec`, `git` (with `git worktree` support)
