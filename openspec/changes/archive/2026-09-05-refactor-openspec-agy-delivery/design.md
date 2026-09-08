## Context

See `proposal.md` for motivation and `specs/openspec-agy-delivery/spec.md` for requirements.

The current `openspec-agy-delivery` handles delivery as a monolithic block: OMP launches a single AGY worker in Herdr, instructs it to apply all tasks at once, then OMP directly executes verification and archiving. The current concurrent path is unsafe: it asks AGY not to commit while OMP integrates with `git merge`, and detached worktrees do not carry repo-local OpenSpec artifacts or uncommitted implementation edits, so concurrent dispatches can race on `.git/index.lock` or silently drop work.

The refactored workflow enables:

1. Schema-driven task discovery by OMP and AGY (`openspec instructions apply --json`).
2. Safe, fallback-aware scheduling: single primary worker by default; concurrent only when isolation/integration preconditions hold; otherwise sequential.
3. Patch-based concurrent integration with no commits, no merges, no branches from AGY.
4. Assigned-task apply semantics shared by every `openspec-apply-change` install so OMP can dispatch individual task IDs without AGY absorbing the rest of the list.
5. AGY-executed verification with OMP gatekeeping and an explicit targeted smoke run on the primary tree.
6. AGY-executed archive only after every gate passes, with `Sync now (recommended)` pinned in the prompt.
7. Byte-identical canonical and `.agents` mirror skills; repeatable evals live alongside the skill and remain tracked in git.

## Goals / Non-Goals

**Goals:**
- Provide a clear, executable protocol for OMP to evaluate the schema-reported task list, choose a safe topology, dispatch tasks, integrate results, verify, and archive.
- Support multi-pane Herdr orchestration where independent tasks run in parallel across detached `git worktree`s integrated via binary patches, with safe fallback to the single-worker path.
- Enforce OMP diff and transcript inspection and task acceptance before advancing to subsequent tasks.
- Allow AGY to execute verification and archiving commands only after explicit OMP authorization, with prompts that pin required choices (e.g., `Sync now (recommended)`).
- Keep the canonical skill (`skills/openspec-agy-delivery/SKILL.md`), the project installation (`.agents/skills/openspec-agy-delivery/SKILL.md`), and `AGENTS.md` strictly synchronized.
- Ship repeatable evals at `skills/openspec-agy-delivery/evals/evals.json` that cover both the revised and prior behavior, runnable by the skill-creator workflow.

**Non-Goals:**
- Merging the planning phase into the delivery skill (planning remains separate via `openspec-explore` / `openspec-propose`).
- Autonomous, ungated execution by AGY (AGY never decides to skip tasks, ignore test failures, pick a non-default archive option, or archive without OMP authorization).
- Replacing standard git commands with proprietary branching tools or committing on AGY's behalf.
- Hardcoding the task artifact to `tasks.md`. Schemas may report a different file; both OMP and AGY follow the CLI.

## Decisions

### 1. Schema-Driven Task Source

OMP and AGY both derive the task list and task artifact path(s) from the `contextFiles`, `progress`, and `tasks` fields returned by `openspec instructions apply --change <change> --json [--store <id>]`.

- The apply contract never assumes `tasks.md`; it reads whatever artifact path the schema reports for the `tasks` artifact ID. For the project's default `spec-driven` schema this resolves to `tasks.md`; for custom schemas it may resolve to e.g. `implementation.md`.
- The task IDs and descriptions used in worker briefs come from the same JSON response, so worker prompts and OMP evaluation use one source of truth.

*Alternative considered*: Hardcoding `tasks.md` for the spec-driven schema. Rejected because the main capability spec already requires following the schema-reported file, and hardcoding would silently break custom-schema deliveries.

### 2. Safe Topology Selection

OMP picks a topology from the task DAG before dispatching workers. The state machine is:

```
apply state == "blocked"          → STOP, report missing planning prerequisite.
apply state == "all_done"         → SKIP implementation; start a lifecycle AGY worker for verification; do not create detached worktrees.
apply state == "ready"            → continue.
  selected change has uncommitted artifacts or implementation edits
                                 → treat as baseline if attributable to the change; otherwise STOP and ask.
  independent root tasks present, primary tree clean, changeRoot committed at HEAD
                                 → CONCURRENT topology (Section 3).
  otherwise                     → SEQUENTIAL topology (Section 4).
```

Topology choice is OMP's judgment, not a user prompt; safety wins over speed.

*Alternative considered*: Always concurrent when the DAG allows it. Rejected because it would race user work, fail patch precheck, or drop change artifacts.

### 3. Concurrent Topology With Patch-Based Integration

Preconditions (all must hold):

1. The primary working tree is clean: `git status --short` is empty except for the selected `changeRoot` and any explicitly attributed implementation edits that OMP chose to carry as baseline.
2. The selected change's repo-local artifacts are committed at HEAD; if they are not, OMP does not copy or guess artifact paths — the workflow falls back to sequential.
3. The selected tasks are independent root tasks (no shared file paths or sequential dependencies).
4. There are at most 3 concurrent panes at any moment.

Per independent task OMP:

1. Picks an absolute worktree path under the repo (e.g., `<repo>/.worktrees/<task-id>`).
2. Runs `git worktree add --detach <absolute-worktree-path> <base-commit>` from the primary tree.
3. Inside the worktree, runs `openspec status --change <change> --json [--store <id>]` and `openspec instructions apply --change <change> --json [--store <id>]`. The probe MUST return the same change/store, `state: "ready"`, and the same task IDs OMP planned for. Otherwise OMP removes the worktree and falls the whole stage back to sequential.
4. Spawns a dedicated AGY worker in a Herdr pane rooted at that worktree (see Section 5).

Worker completion, OMP integration:

1. After the worker settles with status `idle` or `done`, OMP inspects `git status --short`, `git diff HEAD`, staged content, and each untracked file in the worktree.
2. OMP decides which paths are approved implementation edits. OMP never includes `tasks` artifact paths, `openspec/changes/<change>/...` planning artifacts, or other OMP-owned files in the integration set.
3. OMP stages new files for patch export with `git add -N -- <paths>` in the worktree (still inside the detached worktree — never in the primary tree).
4. OMP exports a binary patch scoped to the approved implementation paths:
   `git diff HEAD --binary --output=<absolute-patch-path> -- <approved-implementation-paths>`.
5. OMP switches to the primary tree and runs `git apply --check <absolute-patch-path>`, then `git apply <absolute-patch-path>`. If `--check` fails, OMP stops, keeps the worktree and patch for investigation, and does not edit the primary tree.
6. OMP reviews the resulting primary-tree diff, updates the assigned task's `- [x]` marker in the schema-reported task artifact in the primary tree, and removes the worktree with `git worktree remove --force <absolute-worktree-path>` and deletes the patch file.

No `git merge`, no branch creation, no commit from AGY, no branch left behind.

*Alternative considered*: `git merge` of a delivery branch per worker. Rejected because the main capability spec forbids AGY commits, and merge conflicts force user-attended resolution.

### 4. Sequential Topology

OMP uses a single primary worker rooted at the primary working tree. The task DAG runs top-down; OMP prompts one assigned task at a time and reviews the primary tree between steps. Sequential is the default; concurrency is an optimization layered on top.

### 5. Worker Lifecycle and Status Handling

OMP launches workers through the `herdr` skill. Worker name pattern: `[a-z][a-z0-9_-]{0,31}` (e.g., `agy-<change>`).

- Default model is `gemini-3.8-flash-high` with `--effort high`. Substitutions only when the user names a model and `agy models` lists it.
- After each prompt, OMP reads `.result.agent.status`. The state machine is:
  - `idle` or `done` → OMP reviews transcript and tree; this is the only state that authorizes advancement.
  - `blocked` → OMP reads the transcript, responds only with mechanical input (no scope expansion), and re-prompts.
  - `unknown` → OMP keeps inspecting or waits for the worker to settle; no advancement.
  - Timeout / command error → OMP inspects the worker, the recent transcript, and the worktree before deciding to retry. The same blocker repeating three times for a single task halts that task without marking it complete.
- Per-task remediation budget: up to 3 rounds. After that, OMP keeps the tree untouched and surfaces the blocker to the user.

### 6. Verification Phase

After every implementation task is integrated into the primary tree:

1. OMP instructs the primary AGY worker to execute `openspec-verify-change` and the canonical lint/typecheck/test/build commands OMP discovered.
2. OMP reads the raw AGY transcript, exit outcomes, and the complete primary diff (tracked, staged, untracked).
3. OMP rejects weakened, skipped, or disabled tests.
4. OMP runs the smallest behaviorally relevant smoke check directly on the primary tree (not delegated to AGY).
5. Remediation: OMP sends a concrete delta prompt; AGY runs every blocking command again; OMP reviews diff and smoke. Up to 3 rounds; the same blocker repeating twice or three rounds failing halts without archive.

### 7. Archive Phase

Only when every gate passes:

1. OMP prompts the worker with an archive prompt that pins `Sync now (recommended)` and forbids AGY from picking another option. The prompt names the change and the selected store.
2. AGY executes `openspec-archive-change` and reports back.
3. OMP confirms the original `changeRoot` is gone, the archive path exists, and the main spec reflects the delta.
4. OMP runs `openspec validate --specs --strict --no-interactive [--store <id>]` and `openspec validate --archived --strict --no-interactive [--store <id>]`.
5. OMP reports success only when all four confirmations hold.

### 8. Apply Contract: Assigned-Task Boundary

Every install of `openspec-apply-change` (`.gemini`, `.agents`, `.omp`) accepts an optional `assigned task IDs` parameter from the orchestrator:

- AGY cross-checks each ID against the schema-reported task list. Missing, already-complete, or out-of-change IDs are blockers.
- With assignment, AGY implements and marks complete only the assigned tasks and reports the overall remaining progress even when OpenSpec still reports `ready`.
- Without assignment, the existing full-pending-task loop is preserved.
- The task artifact path is always the schema-reported path (typically `tasks.md` for `spec-driven`); no alias, no hardcoded fallback, no compatibility path.

## Risks / Trade-offs

- **[Risk]** Patch export fails to capture binary or intent-to-add content.
  → **Mitigation**: Use `git add -N` for new files and `git diff HEAD --binary` so both staged modifications and new untracked files travel through the patch.
- **[Risk]** AGY runs `git merge` or commits despite the contract.
  → **Mitigation**: Worker briefs forbid both; OMP inspects every primary-tree diff for unintended commits or merges before advancing.
- **[Risk]** Worker probe inside a detached worktree does not see repo-local change artifacts.
  → **Mitigation**: Probe failure removes the worktree and falls the stage back to sequential; OMP never copies artifacts into a worktree.
- **[Risk]** `openspec-apply-change` ignores the assigned-task boundary.
  → **Mitigation**: Assigning only IDs that OMP wants implemented, and reading the worker's reported remaining progress before advancing, makes drift visible immediately.
- **[Risk]** Archive prompt defaults to "Skip" and silently drops spec sync.
  → **Mitigation**: The OMP archive prompt explicitly pins `Sync now (recommended)`; OMP re-runs `openspec validate --specs` afterwards to detect any drift.
- **[Risk]** `skills/openspec-agy-delivery-workspace/` leaks into git.
  → **Mitigation**: `.gitignore` ignores the directory but unignores `skills/openspec-agy-delivery/evals/evals.json`, so only the eval definitions are tracked.

## Open Questions

None. The remaining unknowns belong in the apply-state and probe responses at runtime, not in this design.
