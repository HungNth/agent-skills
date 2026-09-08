## 1. Artifact Correction

- [ ] 1.1 Update `openspec/changes/refactor-openspec-agy-delivery/proposal.md` so the impact list includes `openspec-apply-change` (`.gemini`, `.agents`, `.omp`), the tracked `evals/evals.json` definition, and `.gitignore`; preserve the DAG, task-level gating, and AGY-executed verify+archive objectives; describe concurrency as a conditional capability, not a universal requirement.

- [ ] 1.2 Replace the concurrency decisions in `openspec/changes/refactor-openspec-agy-delivery/design.md` with the concrete state machine: schema-reported task source, single-worker default, detached worktrees only when worker-side probe confirms the same change/store with `state: ready` and matching task IDs, patch-based integration with no commits, and concurrent fallback to sequential.

- [ ] 1.3 Rewrite the delta spec `openspec/changes/refactor-openspec-agy-delivery/specs/openspec-agy-delivery/spec.md` to require schema-reported task artifacts (no literal `tasks.md`), to allow concurrent independent tasks only when isolation/integration preconditions hold, to add the assigned-task apply semantics, the `all_done` lifecycle-worker path, worker `blocked`/`unknown`/timeout handling, the concurrent fallback, and patch-apply failure handling, and to update the `Verification failures use bounded remediation` requirement so AGY runs gates while OMP runs targeted smoke.

## 2. Apply Contract Update

- [ ] 2.1 Update `.gemini/skills/openspec-apply-change/SKILL.md` to accept an optional set of assigned task IDs from the orchestrator, cross-check IDs against the schema-reported task list, implement only the assigned tasks when assignment is supplied, and read the task artifact from the schema-reported path instead of hardcoding `tasks.md`.

- [ ] 2.2 Update `.agents/skills/openspec-apply-change/SKILL.md` to mirror the assigned-task semantics using its platform-specific invocation spelling, keeping the file consistent with `.gemini` aside from platform differences.

- [ ] 2.3 Update `.omp/skills/openspec-apply-change/SKILL.md` to mirror the assigned-task semantics using its platform-specific invocation spelling, keeping the file consistent with `.gemini` aside from platform differences.

## 3. Delivery Skill Implementation

- [ ] 3.1 Rewrite `skills/openspec-agy-delivery/SKILL.md` so every reference to `tasks.md` becomes a schema-reported task artifact path, the sequential loop dispatches one assigned task at a time, the concurrent loop creates detached worktrees only when preconditions hold, worker integration uses binary patches with no `git merge` and no commit, and the `all_done` lifecycle creates a worker that runs verification.

- [ ] 3.2 Synchronize the canonical skill to `.agents/skills/openspec-agy-delivery/SKILL.md` and confirm byte-identical via `cmp`.

## 4. Policy and Install Copies

- [ ] 4.1 Update `AGENTS.md` to state the new contract: OMP owns DAG, diff/patch integration, independent targeted smoke, and gates; AGY owns assigned apply tasks, command execution, and authorized archive; concurrency is allowed only when preconditions hold and falls back to sequential otherwise.

- [ ] 4.2 Update `.gitignore` to keep `skills/openspec-agy-delivery-workspace/` ignored but unignore `skills/openspec-agy-delivery/evals/evals.json` so the tracked repeatable eval definitions ship with the skill package.

## 5. Evaluations

- [ ] 5.1 Snapshot the current refactor `skills/openspec-agy-delivery/SKILL.md` and `.gemini/skills/openspec-apply-change/SKILL.md` to `skills/openspec-agy-delivery-workspace/refactor-baseline/` so every baseline run receives both and every revised run receives the canonical delivery skill plus the revised `.gemini` apply skill.

- [ ] 5.2 Author `skills/openspec-agy-delivery/evals/evals.json` per `.agents/skills/skill-creator/references/schemas.md` covering: custom schema + assigned subset, two dependent tasks sequential, two independent root tasks with detached worktrees and patch integration, uncommitted changeRoot fallback, post-sequential stage fallback, `all_done` lifecycle worker, verification failure/remediation/archive gate, AGY-role recursive-delivery rejection, and default model launch.

- [ ] 5.3 Run baseline and revised pairs in parallel via the skill-creator workflow, passing the matching skill files to each run, grading objective assertions, persisting iteration-4 results in `skills/openspec-agy-delivery-workspace/iteration-4/`, aggregating with `python3 .agents/skills/skill-creator/scripts/aggregate_benchmark.py skills/openspec-agy-delivery-workspace/iteration-4 --skill-name openspec-agy-delivery`, and generating the static review with `python3 .agents/skills/skill-creator/eval-viewer/generate_review.py skills/openspec-agy-delivery-workspace/iteration-4 --skill-name openspec-agy-delivery --benchmark skills/openspec-agy-delivery-workspace/iteration-4/benchmark.json --previous-workspace skills/openspec-agy-delivery-workspace/iteration-3 --static skills/openspec-agy-delivery-workspace/iteration-4/static`.

## 6. Final Validation

- [ ] 6.1 Run `openspec validate refactor-openspec-agy-delivery --type change --strict --no-interactive` and confirm zero errors.

- [ ] 6.2 Run `cmp skills/openspec-agy-delivery/SKILL.md .agents/skills/openspec-agy-delivery/SKILL.md` and confirm exit 0 with no output.

- [ ] 6.3 Run `agy models` and confirm `gemini-3.8-flash-high` is present for the default worker launch.

- [ ] 6.4 Run the quick_validate structural check on both `skills/openspec-agy-delivery` and `.agents/skills/openspec-agy-delivery` via `.agents/skills/skill-creator/scripts/quick_validate.py` and confirm `Skill is valid!` for both. If pip cannot install PyYAML, mark this task unverified, do not mark complete, and do not archive.
