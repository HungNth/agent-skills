---
name: openspec-agy-delivery
description: Deliver an explicitly approved OpenSpec change by having OMP orchestrate Antigravity CLI (AGY) workers through Herdr via task-by-task and concurrent scheduling, evaluate diffs and verification results, and gate archive. Use only when the current agent is OMP and the user asks to implement, apply, ship, or deliver an approved OpenSpec change through AGY or Antigravity. Never use inside an AGY implementation worker, during explore or proposal work, before separate post-planning approval, or for small tasks the user wants OMP to implement directly.
compatibility: Requires OMP running inside Herdr with the herdr, agy, openspec, and git CLIs installed; AGY must be authenticated. Supports native Windows, macOS, and Linux hosts supported by those tools.
---

# OpenSpec AGY Delivery

Deliver one approved OpenSpec change end to end. OpenSpec artifacts define the work; OMP plans and evaluates; AGY implements, verifies, and archives under OMP orchestration and gating; Herdr owns terminal and agent lifecycle.

## Agent-role preflight

This is an OMP orchestration workflow, never an AGY implementation workflow. Before any OpenSpec command or Herdr mutation, confirm that the current runtime identifies this agent as OMP and that `HERDR_ENV` is `1`. Skill availability, repository location, or an implementation request does not prove the OMP role.

If the current agent is AGY or cannot confirm that it is OMP, stop without splitting a pane, starting or prompting an agent, or running the delivery lifecycle. Reply with the exact literal skill name `openspec-apply-change` as the required workflow for the named change; do not replace it with a path, link label, or generic `SKILL.md`. State that `openspec-agy-delivery` is OMP-owned.

## Approval boundary

Planning authorization never authorizes implementation. Planning must be completed first using `openspec-explore` or `openspec-propose`. Start this delivery workflow only after the planning workflow has stopped and the user sends a separate request to deliver a named approved change.

That delivery request authorizes:

- task DAG dependency analysis and scheduling (sequential default, concurrent only when preconditions hold)
- implementation of assigned tasks via `openspec-apply-change` (sequential or concurrent)
- up to three bounded remediation rounds per task or verification failure
- AGY execution of verification and archiving upon explicit OMP gatekeeper authorization

It never authorizes credentials, destructive operations, permission escalation, deployment, publishing, requirement decisions, or scope expansion. Stop and ask the user for any of those.

## Cross-platform command rule

Run each CLI operation separately through the host command tool and parse returned JSON directly. Treat command examples as argument sequences, not shell programs. Use host-native quoting and environment access; do not require a POSIX shell, inline shell functions, pipelines, heredocs, or command substitution. A host-native multiline string literal is acceptable only when it is passed as one CLI argument rather than executed as a shell program.

Use resolved absolute paths when a command accepts a cwd. Never infer OpenSpec locations from conventional directory names.

## Ownership

- **OpenSpec:** proposal, specs, design, implementation tasks, schema, roots, and action context. OpenSpec alone decides the task list, task artifact path(s), apply state, and progress.
- **AGY:** scoped implementation through `openspec-apply-change` for the assigned task IDs only, verification execution through `openspec-verify-change`, and archive execution through `openspec-archive-change` upon explicit OMP authorization. AGY never commits, merges, branches, picks a non-default archive option, or invokes this delivery skill.
- **Herdr:** pane layout, process launch, agent identity, lifecycle state, and transcript access.
- **OMP:** preflight, pre-dispatch task DAG analysis, worker briefs, task dispatching (sequential or concurrent), diff and patch integration, verification evaluation (including an independent targeted smoke check), remediation decisions, and archive gating.

## 1. Resolve the change and root

If the user names a standalone store, resolve it before listing or selecting changes:

1. Run `openspec store list --json` and resolve its registered id.
2. Add `--store <id>` to every applicable OpenSpec command for the rest of this delivery.
3. Include the selected store id in the AGY brief and every verification, remediation, and archive handoff.

Then resolve exactly one change inside the selected planning root. If ambiguous, run `openspec list --json [--store <id>]` and ask the user to choose from that result.

Announce the selected change and store, if any.

Run:

```text
openspec status --change <change> --json [--store <id>]
openspec instructions apply --change <change> --json [--store <id>]
openspec validate <change> --type change --strict --no-interactive [--store <id>]
```

Use the returned `schemaName`, `planningHome`, `changeRoot`, `actionContext`, apply `state`, `contextFiles`, task list, and dynamic instruction as authoritative.

- The task list and the task artifact path(s) come from `openspec instructions apply --json`. Treat the `tasks` artifact path under `contextFiles` as the only task file. For the project's default `spec-driven` schema this resolves to `tasks.md`; for custom schemas it may resolve to a different file. Never hardcode, alias, or fall back to a literal `tasks.md` when the schema reports a different path.
- `blocked`: stop before starting AGY and report the missing planning prerequisite.
- `all_done`: skip AGY implementation, start (or reuse) a lifecycle AGY worker, and proceed to verification.
- `ready`: read every path under `contextFiles`, then continue.

Apply relevant runtime `context` and compatible `operationGuidance`. They do not override explicit user choices, CLI state, resolved paths, or built-in workflow contracts.

## 2. Check prerequisites and protect user work

Confirm all of the following before delegation:

1. The agent-role preflight confirmed OMP, and OMP is inside Herdr with `HERDR_ENV=1`.
2. `herdr --help`, `agy help`, `agy models`, `openspec --help`, and `git --version` succeed.
3. AGY is authenticated. Resolve the repository root with `git rev-parse --show-toplevel` and keep the returned absolute path for every cwd-sensitive Herdr operation.
4. The selected change is valid; apply state is `ready`, `all_done`, or `blocked`. Start implementation AGY only for `ready`. Start a lifecycle verification worker for `all_done`. Stop for `blocked`.
5. The working tree can be attributed safely.

Inspect tracked, staged, and untracked changes. On a fresh delivery, pre-existing changes may remain only inside the selected `changeRoot`. If unrelated paths are already dirty, stop and list them; never clean, reset, stash, switch branches, or overwrite user work.

When explicitly continuing a partial delivery, treat existing implementation edits as baseline only when repository evidence ties them to the same selected change. If attribution is uncertain, stop.

Discover the project's exact lint, typecheck, test, build, and behavioral smoke commands from root `AGENTS.md`, repository instructions, documentation, and manifests. Do not ask AGY to guess them.

## 3. Plan worker topology from the task DAG

OMP reads the task list from `openspec instructions apply --json` (never from a literal file name) and constructs the DAG:

1. Identify sequential dependencies: tasks that share base schemas, interfaces, or outputs from earlier tasks.
2. Identify independent root tasks: tasks that modify disjoint files, separate modules, or isolated documentation and do not depend on each other.

Then select the topology with this state machine:

- `apply state == "blocked"` → STOP. No pane mutation, no agent start, no prompt. Report the missing planning prerequisite.
- `apply state == "all_done"` → SKIP implementation. Start or reuse a single lifecycle AGY worker rooted at the primary tree. Do not create detached worktrees. Proceed directly to the verification phase (Section 7).
- `apply state == "ready"`:
  - If the primary tree is dirty with paths outside the attributable baseline → STOP. Report the conflicting paths.
  - If the selected change's repo-local artifacts are not committed at HEAD (uncommitted `changeRoot` content), or worker-side probe later fails, or task independence cannot be established → use the SEQUENTIAL topology below.
  - Otherwise, when independent root tasks exist and no more than three concurrent panes are needed → MAY use the CONCURRENT topology (Section 5).

Topology choice is OMP's judgment; never ask the implementer to pick. Sequential is the default. Concurrency is an optimization layered on top.

## 4. Start the primary worker through Herdr

Follow the installed `herdr` skill. Inspect the current pane and layout:

```text
herdr pane current --current
herdr pane layout --current
herdr agent list
```

Derive a valid worker name matching `[a-z][a-z0-9_-]{0,31}` (e.g., `agy-<change>`). Split the pane right if wide, otherwise split down:

```text
herdr pane split --current --direction <right|down> --cwd <repository-root> --no-focus
herdr agent start <worker-name> --kind agy --pane <pane-id> -- --model gemini-3.8-flash-high --effort high
```

If the user requested a specific model or provider, substitute that model from `agy models`. Otherwise, default to `gemini-3.8-flash-high` with `--effort high`. The default model must appear in `agy models`; if it does not, stop and report the missing prerequisite.

For the sequential topology, the primary worker is the only worker. For the concurrent topology, start additional workers as Section 5 describes after detached worktrees pass probe.

## 5. Concurrent topology (only when preconditions hold)

Preconditions (all must hold before OMP creates a detached worktree):

1. The primary tree is clean except for attributable baseline inside the selected `changeRoot`.
2. The selected change's repo-local artifacts are committed at HEAD. If they are not committed, fall back to sequential; never copy artifacts into a worktree.
3. The candidate tasks are independent root tasks (no shared file paths, no sequential dependency).
4. At most three concurrent panes in flight.

Per independent root task OMP:

1. Pick an absolute worktree path under the repo (e.g., `<repo>/.worktrees/<task-id>`).
2. From the primary tree, run `git worktree add --detach <absolute-worktree-path> <base-commit>`. Use a detached worktree (no branch).
3. Inside the worktree, run `openspec status --change <change> --json [--store <id>]` and `openspec instructions apply --change <change> --json [--store <id>]`. The probe MUST return the same change/store, `state: "ready"`, and the same task IDs OMP planned for. If probe fails, run `git worktree remove --force <absolute-worktree-path>` and convert the entire stage to sequential before starting any concurrent worker. Do not retry the probe, do not copy artifacts, do not guess paths.
4. Spawn the worker in its own Herdr pane rooted at the worktree:
   ```text
   herdr pane split --pane <parent-pane-id> --direction <right|down> --cwd <worktree-path> --no-focus
   herdr agent start <worker-name>-<task-id> --kind agy --pane <pane-id> -- --model gemini-3.8-flash-high --effort high
   ```

After the primary tree accepts the first patch (Section 6) and OMP updates the first task marker, do not create additional worktrees. Remaining tasks run on the single primary worker so subsequent tasks see the accepted baseline.

## 6. Dispatch tasks and integrate results

OMP drives every dispatch and integration step. AGY never commits, merges, branches, or picks a non-default archive option.

### 6.1 Sequential dispatch (and post-baseline dispatch)

For each task OMP assigns, send exactly one prompt per turn. Do not stack tasks.

Worker prompt template:

```xml
<role>
You are the AGY implementation worker, not the OMP delivery orchestrator.
Use the workflow named exactly openspec-apply-change for the named change; do not describe it only as SKILL.md.
Never invoke openspec-agy-delivery or create another AGY worker.
Never commit, merge, create a branch, or archive without explicit OMP authorization.
</role>
<task>
Implement only this assigned task: <task-id> - <task-description>.
Change: <change>. Store: <store-id or none>.
Read root AGENTS.md for project rules.
Mark the assigned task checkbox - [x] in the schema-reported task artifact upon completion.
Do not modify unrelated tasks or their markers. Even when OpenSpec still reports state: ready, stop after the assigned task.
Run task-specific verification if available. Report overall remaining progress.
</task>
```

Send via:

```text
herdr agent prompt <worker-name> <task-prompt> --wait --timeout 3600000
```

After the prompt returns, read `.result.agent.status`. Worker status state machine:

- `idle` or `done`: OMP reviews the transcript, the worker's tree change, and the schema-reported task artifact before advancing.
- `blocked`: OMP reads the transcript, replies with mechanical input only (no scope expansion), and re-prompts. If the same blocker repeats three times for the same task, OMP halts that task without marking it complete.
- `unknown`: OMP keeps inspecting or waits for the worker to settle. No advancement.
- Timeout or command error: OMP inspects the worker, the recent transcript, and the worktree (if any) before deciding to retry. The same blocker repeating three times for one task halts that task without marking it complete.

When the sequential topology is active, OMP reviews the primary tree directly (`git diff`, `git status --short`) and updates the schema-reported task artifact in place.

### 6.2 Concurrent integration (no commits, no merges, no branches)

For each accepted concurrent worker result, in the worktree:

1. OMP inspects `git status --short`, `git diff HEAD`, staged content, and each untracked file.
2. OMP decides which paths are approved implementation edits. Excluded from the integration set: the schema-reported task artifact, planning artifacts under `openspec/changes/<change>/`, and any OMP-owned file.
3. OMP stages new files for patch export with `git add -N -- <paths>` (still inside the detached worktree — never in the primary tree).
4. OMP exports the binary patch scoped to the approved implementation paths:
   `git diff HEAD --binary --output=<absolute-patch-path> -- <approved-implementation-paths>`.
5. OMP switches to the primary tree and runs `git apply --check <absolute-patch-path>`, then `git apply <absolute-patch-path>`. If `--check` fails, OMP stops, keeps the worktree and patch file for investigation, does not modify the primary tree, and reports the exact blocker.
6. OMP reviews the resulting primary-tree diff, updates the schema-reported task artifact in the primary tree (`- [x]` for the assigned task), then `git worktree remove --force <absolute-worktree-path>` and deletes the patch file.

No `git merge`. No branch creation. No commit from AGY. No branch left behind. After the first accepted patch, OMP does not create new worktrees for the remaining tasks.

### 6.3 Remediation budget

Up to three remediation rounds per task. After three rounds without progress or when the same blocker repeats, OMP keeps the working tree untouched and surfaces the blocker to the user.

## 7. Verification phase

After every implementation task is integrated into the primary tree (or when `apply state == "all_done"` skips implementation):

1. Instruct the lifecycle AGY worker to execute `openspec-verify-change` and every canonical lint/typecheck/test/build command OMP discovered in Section 2:

```xml
<verification_task>
All implementation tasks are complete and integrated in the primary tree.
Execute openspec-verify-change for change: <change> [--store <id>].
Run the canonical project verification commands:
<commands discovered by OMP>
Report full verification findings and command results.
Do not archive; OMP evaluates verification first.
</verification_task>
```

Send via:

```text
herdr agent prompt <worker-name> <verification-prompt> --wait --timeout 3600000
```

2. OMP evaluates:
   - The raw AGY transcript and exit outcomes.
   - The complete primary-tree change (tracked, staged, untracked).
   - Reject weakened, skipped, or disabled tests.
   - Run the smallest behaviorally relevant smoke check on the primary tree (not delegated to AGY).

3. Remediation: OMP sends a concrete delta prompt. AGY runs every blocking command again. OMP re-reviews the diff and re-runs targeted smoke. Up to three rounds; the same blocker repeating or three rounds failing halts without archive.

## 8. Archive phase

Only when every gate passes:

1. OMP prompts the worker with an archive prompt that pins `Sync now (recommended)` and forbids AGY from choosing any other option:

```xml
<archive_task>
Verification has passed and archive is authorized for change: <change> [--store <id>].
Execute openspec-archive-change for change: <change>.
When archive-change asks whether to sync specs to main specs, choose "Sync now (recommended)".
Do not choose any other option.
Report the archive outcome.
</archive_task>
```

Send via:

```text
herdr agent prompt <worker-name> <archive-prompt> --wait --timeout 3600000
```

2. After AGY archives, OMP confirms:
   - The original `changeRoot` no longer exists.
   - The archive path exists under `openspec/changes/archive/`.
   - Main specs in `openspec/specs/` reflect the delta.
3. OMP runs both validators and confirms zero errors:
   ```text
   openspec validate --specs --strict --no-interactive [--store <id>]
   openspec validate --archived --strict --no-interactive [--store <id>]
   ```
4. Only after every confirmation holds, OMP reports success.

If any gate remains unresolved, OMP does not authorize archive, the change stays active, and OMP reports why archive was blocked.

## 9. Report the delivery outcome

Summarize the delivery:

- change name, schema, store, and worker topology (sequential or concurrent) with the reason for the choice
- tasks implemented, the schema-reported task artifact path, and per-task evaluation outcome
- remediation rounds used (if any)
- verification results, project checks, and OMP's independent targeted smoke
- archive confirmation: original changeRoot gone, archive path present, main spec synced, both `openspec validate` calls passed
