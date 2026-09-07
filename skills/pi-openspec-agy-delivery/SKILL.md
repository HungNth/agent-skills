---
name: pi-openspec-agy-delivery
description: Deliver an explicitly approved OpenSpec change by having Pi coordinate dependency-aware parallel Antigravity CLI (AGY) workers through Herdr in isolated worktrees, then supervise fresh read-only verification, spec synchronization, and archive. Use only when the current agent is Pi and the user explicitly requests post-planning delivery of a named approved OpenSpec change. Never use inside an AGY worker, under OMP, during initial exploration or proposal planning workflows, before separate post-planning approval, or for ad-hoc coding tasks.
compatibility: Requires Pi running inside Herdr (HERDR_ENV=1) with herdr, agy, openspec, and git CLIs installed; AGY authenticated with gemini-3.8-flash-high available. Supports native Windows, macOS, and Linux hosts.
---

# Pi + OpenSpec AGY Delivery

Deliver one approved OpenSpec change end to end using Pi as orchestrator and AGY workers for execution. Pi derives a conservative task dependency graph, schedules ready work in parallel waves across dedicated git worktrees and Herdr panes, reviews and integrates accepted local commits, supervises fresh read-only verification, and gates spec synchronization and archive.

## Agent-Role Preflight & Fail-Closed Guard

This is a Pi-owned orchestration workflow, never an AGY implementation worker or OMP orchestrator workflow. Before executing any OpenSpec command, git operation, or Herdr mutation, verify that the active harness context identifies the current agent as Pi and that `HERDR_ENV` is `1`. Skill availability, repository location, or an implementation prompt does not establish the Pi role. Do not rely solely on inherited environment variables that child AGY processes might share.

Route on role detection strictly before mutating delivery state, branches, worktrees, panes, or child agents:
- **Confirmed AGY role**: Stop immediately before creating branches, worktrees, Herdr panes, or child agents. Reply with the exact literal skill name `openspec-apply-change` as the required workflow for the assigned change; do not replace it with a path, link label, or generic filename. State that `pi-openspec-agy-delivery` is Pi-owned. AGY workers must never recursively spawn workers, create Herdr panes, or orchestrate deliveries.
- **Confirmed OMP role**: Refuse orchestration immediately and direct OMP to `openspec-agy-delivery`.
- **Unknown or unconfirmed agent role**: Fail closed immediately before any mutation. Report the inability to confirm that the current agent is Pi in Herdr, and stop without assuming or pretending the caller is AGY.
- Stop before creating branches, worktrees, panes, or AGY workers for all negative trigger cases.

## Post-Planning Approval Boundary

Planning authorization never authorizes implementation. Exploration and proposal workflows (`/opsx-explore`, `/opsx-propose`) authorize planning only; Pi must stop after planning artifacts are complete without starting AGY workers, creating delivery branches, or editing project files. Implementation begins only when the user sends a separate, explicit request naming an approved OpenSpec change for delivery through Pi and AGY.

The delivery request authorizes:
- Local planning checkpoint and accepted lane commits on the integration branch
- Dedicated per-lane branches, worktrees, and background Herdr AGY workers
- AGY implementation and bounded progress-aware remediation
- Authoritative task marker updates by a single AGY integration worker
- Fresh read-only AGY verification cycles in `--mode plan`
- Separately prompted AGY spec synchronization and archive
- Success-only non-force cleanup of workflow-created resources

Strictly prohibited actions (never authorized):
- Credentials, production tokens, or secret requests
- Remote git operations: `git push`, remote fetch, or remote PR creation
- Deployment, staging upload, or package publishing
- Permission bypass, sandbox escape, or automatic model escalation beyond `gemini-3.8-flash-high`
- Destructive cleanup: `git worktree remove --force`, `git branch -D`, `git clean -fdx`, or `git reset --hard`
- Requirement interpretations, design deviations, or scope expansion

If any protected decision arises, Pi must halt immediately, preserve delivery state, and prompt the user.

## Cross-Platform Command Execution

Execute each CLI operation separately through the host command tool and parse returned JSON directly. Treat commands as argument sequences, not shell scripts. Use host-native quoting and environment access. Do not require a POSIX shell, inline shell functions, pipelines (`|`), heredocs, command substitution (`$()`), or `jq`. No scheduler service or helper runtime is required. Always pass cwds as resolved absolute paths. Never assume conventional repository-relative OpenSpec paths.

## Ownership Split

- **OpenSpec**: Proposal, specs, design, tasks, schema, planning root, change root, and action context.
- **AGY Implementer**: Scoped implementation within assigned worktree, candidate task completion claims, and targeted lane checks. Never commits, merges, pushes, spawns workers, syncs specs, or archives.
- **AGY Integration Worker**: Verifies integrated code, updates authoritative task markers on the integration branch, and resolves mechanical integration conflicts.
- **AGY Verifier**: Dedicated read-only verifier in `--mode plan` executing `openspec-verify-change`. Never edits files, commits, or transitions to a writer role.
- **AGY Lifecycle Worker**: Write-capable worker executing separately prompted `openspec-sync-specs` and `openspec-archive-change`.
- **Herdr**: Terminal panes, agent process launch, lifecycle status, and transcript access.
- **Pi Orchestrator**: Dependency DAG construction, wave scheduling, worktree/branch/pane lifecycle, lane briefs, diff inspection, test integrity review, local commits, topological integration, independent project gates, stage authorization, remediation decisions, and success-only cleanup. Pi NEVER edits implementation code.

## 1. Resolve Change, Sticky Store & Planning State

If the user specifies a standalone store or the work resides in one:
1. Run `openspec store list --json` and verify the registered store ID.
2. Treat `--store <id>` as sticky across all applicable OpenSpec CLI commands (`status`, `instructions`, `validate`, `show`, `archive`, `list`).
3. Propagate `--store <id>` to every atomic skill and handoff (implementation, verification, spec synchronization, archive), ensuring each worker executes its OpenSpec commands with the sticky store flag.

Resolve exactly one change in the selected planning root. If ambiguous, run `openspec list --json [--store <id>]` and prompt the user to choose. Announce the selected change and store.

Run authoritative OpenSpec commands and parse their separate payloads:
```text
openspec status --change <change> --json [--store <id>]
openspec instructions apply --change <change> --json [--store <id>]
openspec validate <change> --type change --strict --no-interactive [--store <id>]
```

Separate field ownership across returned JSON outputs (do not treat as a single merged payload):
- **From `openspec status` JSON**: Extract `schemaName`, `planningHome`, `changeRoot`, `artifactPaths`, and `actionContext` to establish workflow schema, repository/store roots, and allowed edit paths.
- **From `openspec instructions apply` JSON**: Extract apply `state`, `contextFiles` (artifact ID to concrete file paths), `progress`, `tasks` checklist, dynamic `instruction`, required project `context`, and advisory `operationGuidance`.

Route on apply `state`:
- `blocked`: Stop before creating workers and report the missing planning prerequisites.
- `all_done`: Skip implementation and proceed directly to independent verification.
- `ready`: Read every file path listed in `contextFiles`.

Apply runtime `context` as required project input, and consider compatible `operationGuidance`. Neither overrides user decisions, CLI state, or workflow contracts.

## 2. Prerequisites, Continuation & Dirty-Tree Preflight

Verify all prerequisites before delegation:
1. Active harness identifies Pi, running in Herdr with `HERDR_ENV=1`.
2. `herdr --help`, `agy help`, `agy models`, `openspec --help`, and `git --version` succeed. Confirm `gemini-3.8-flash-high` is available in `agy models`.
3. AGY authentication is active. Resolve the repository root: `git rev-parse --show-toplevel`.
4. OpenSpec apply state is `ready` (or `all_done`).
5. Continuation and reconstruction check: When starting or resuming delivery, inspect current OpenSpec status, local integration/lane branches (`git branch --list`), active worktrees (`git worktree list`), active Herdr agents (`herdr agent list`), commit ancestry (`git log --oneline`), and dirty paths (`git status --porcelain`). Reuse an existing branch, worktree, or worker only when repository evidence ties it conclusively to this exact change and delivery; otherwise stop or derive a collision-safe name. Never overwrite or rebind an existing unrelated ref, path, or agent.
6. Dirty-tree attribution check: Run `git status --porcelain`. On a fresh delivery, pre-existing uncommitted changes may exist only within the approved change's `changeRoot`. If any unattributable tracked, staged, or untracked changes exist, stop immediately and report them. Never clean, reset, stash, switch branches, or overwrite user work.
7. Discover project gates: Identify exact lint, typecheck, test, build, and behavioral smoke check commands from `AGENTS.md`, documentation, and manifests. Do not ask AGY to guess them.

## 3. Local Integration Branch & Planning Checkpoint

Resolve the repository default branch from local git evidence (e.g. `git symbolic-ref refs/remotes/origin/HEAD` stripped of prefix, or `git config init.defaultBranch`), falling back to `main` or `master` only when no default reference exists. Inspect current branch with `git branch --show-current`.
- **If on the resolved default branch**: Create and check out a local integration branch before committing:
  ```text
  git checkout -b delivery/<change>
  ```
- **If already on a safe non-default feature branch** (e.g. `feature/auth-prep`): Use it directly as the integration branch.

Idempotent planning checkpoint:
- Inspect whether the approved planning artifacts under `changeRoot` are already committed in the integration branch history (`git diff --quiet HEAD -- <planning-artifact-paths>`). If already committed and unchanged, reuse that existing checkpoint idempotently without creating an empty or duplicate commit.
- Otherwise, stage ONLY the complete planning artifacts returned under `changeRoot`:
  ```text
  git add <planning-artifact-paths>
  ```
  Create a local planning checkpoint commit on the integration branch:
  ```text
  git commit -m "chore(spec): planning checkpoint for <change>"
  ```
- Partial continuation attribution: When continuing a partial delivery, existing uncommitted or committed implementation edits may be kept as baseline only after evidence review confirms they attribute to the same change and delivery. If attribution is uncertain, stop.
- Never stage unrelated files. Maintain the local-only boundary: no `git push`, remote tracking, or default-branch merges.

## 4. Build Conservative Dependency Graph & Wave Partitioning

Construct a directed acyclic graph (DAG) of tasks from:
1. Explicit task descriptions, numbering, and dependencies in the tasks artifact.
2. Architectural relationships and module contracts in `design.md` and specs.
3. Code symbols, module boundaries, produced schemas, fixtures, and interfaces.
4. Target file paths and overlapping edit surfaces.

Partition tasks into topological waves:
- **Independent tasks**: Non-overlapping file paths, no shared mutable contracts, and no producer-consumer relationship -> schedule in parallel in the same wave.
- **Dependent tasks**: Tasks consuming schemas, interfaces, fixtures, or components produced by upstream tasks -> schedule in a subsequent wave, executable only after upstream dependencies are integrated on the integration branch.
- **Uncertain dependencies**: When tasks touch shared migration runners (e.g. `src/db/migrate.ts`), shared registries, or overlapping modules where independence cannot be proven safe -> serialize into separate waves. Refuse to guess independence.

Calculate active concurrency:
- Default active worker limit: `min(3, ready lanes)`.
- User-specified limit N (e.g. N=2 or N=5): Use `min(N, ready lanes)`. The user limit acts as an upper bound and may exceed 3; Pi may still reduce concurrency for dependency safety, resource constraints, build contention, or Herdr geometry.

## 5. Per-Lane Worktree, Herdr Pane & AGY Startup

For each ready lane in the wave:
1. Derive a sanitized lane identifier (e.g. `lane-collector`, `lane-validator`, or `lane-1`). Sanitize branch, worktree, and agent names to valid alphanumeric/hyphen/underscore tokens.
2. Collision check: Check for collisions against existing local branches (`git branch --list`), worktrees (`git worktree list`), and active Herdr agents (`herdr agent list`). If an unrelated resource matches, stop or derive a collision-safe name. Never overwrite an existing ref, path, or agent.
3. Herdr agent naming: Herdr agent names must match `[a-z][a-z0-9_-]{0,31}` (up to 32 characters). Truncate the base name (e.g. `agy-<change>-<lane>`) if needed and append a short unique suffix to remain within the 32-character limit and avoid collisions.
4. Create dedicated lane branch from current integration HEAD:
   ```text
   git branch agy/<change>/<lane> HEAD
   ```
5. Allocate dedicated git worktree rooted at the lane branch:
   - Worktree path definition: Define the worktree path strictly outside the repository working directory, using a resolved sibling worktree root (e.g. `<repo-parent>/<repo-name>-worktrees/agy-<change>-<lane>`) or another user-approved external path. Never create lane worktrees inside the parent repository checkout.
   - Collision-check the resolved absolute filesystem path against existing disk directories and `git worktree list` before creation.
   - Create worktree:
     ```text
     git worktree add <worktree-path> agy/<change>/<lane>
     ```
   - No two active writers ever share a worktree or working directory.
6. Allocate a dedicated background Herdr pane rooted at `<worktree-path>`:
   ```text
   herdr pane split --current --direction <right|down> --cwd <worktree-path> --no-focus
   ```
   Parse `.result.pane.pane_id` directly from the split response JSON to obtain `<pane-id>`.
7. Launch AGY implementation worker in the pane using the extracted `<pane-id>` with explicit model and reasoning effort:
   ```text
   herdr agent start <worker-name> --kind agy --pane <pane-id> -- --model gemini-3.8-flash-high --effort high
   ```

## 6. Implementation Brief & Worker Supervision

Send a self-contained brief to each lane worker via:
```text
herdr agent prompt <worker-name> <brief> --wait --timeout 3600000
```

Format the brief with explicit boundaries:
```xml
<role>
You are the AGY implementation worker, not the Pi orchestrator.
Use the workflow named exactly openspec-apply-change for your assigned tasks.
Never invoke pi-openspec-agy-delivery or openspec-agy-delivery, and never create child workers.
</role>

<task>
Implement assigned tasks: <assigned-task-ids> for change: <change>.
Store: <store-id or none>.
Read root AGENTS.md for shared project conventions.
Run OpenSpec status and apply instructions for this change and store.
Read every contextFiles path and implement assigned tasks.
</task>

<scope>
Allowed files and interfaces: <lane-owned-paths>.
Do not modify unassigned tasks, shared contracts, or planning artifacts.
Do not commit changes; leave implementation in the working tree for Pi review.
</scope>

<verification_loop>
Run and fix failures from these targeted lane checks before finishing:
<targeted-commands>
</verification_loop>

<decision_safety>
Stop and report any credential request, destructive action, permission escalation,
deployment, requirement ambiguity, or scope change. Do not auto-approve.
</decision_safety>

<report>
Report completed work, touched files, passing checks, blockers, and concerns.
</report>
```

Monitor settled worker status from `.result.agent.status`:
- `blocked`: Inspect transcript via `herdr agent read <worker-name> --source recent-unwrapped --lines 200`. Answer safe mechanical prompts; escalate protected decisions to user.
- `idle` or `done`: Treat completion report as a candidate claim; proceed to Pi review.
- Crash or timeout: Inspect partial work (tracked, staged, untracked) in `<worktree-path>`. Resume the same conversation when safe, or start a replacement worker on the preserved lane.

## 7. Pi Acceptance Review, Local Commits & Integration

AGY reports are candidate claims, not authoritative completion evidence.

For each completed lane:
1. **Diff and untracked file inspection**: Inspect the complete lane worktree. Review modified tracked files with `git -C <worktree-path> diff`. Check `git -C <worktree-path> status --porcelain` to identify untracked files and explicitly inspect/read their contents, as `git diff` omits untracked files entirely. Verify all additions and edits stay strictly within assigned scope and no existing tests are weakened, skipped, or deleted.
2. **Task marker isolation**: Authoritative task markers are strictly single-writer and updated only on the integration branch. Lane workers must never edit `tasks.md`. If a lane worker edits authoritative `tasks.md` (e.g. `- [x] 1.1`), Pi must reject the lane and instruct the same AGY worker to revert that lane-local marker edit before acceptance. Pi never silently edits or reverts worker files itself; once the worker restores scope, Pi stages only accepted implementation paths for the local lane commit.
3. **Targeted checks**: Pi independently reruns required targeted checks inside `<worktree-path>`.
4. **Lane acceptance**:
   - If review fails: Send exact delta findings to the same AGY conversation; refuse integration until checks pass.
   - If review passes: Pi creates a local commit for accepted code on the lane branch:
     ```text
     git -C <worktree-path> add <changed-files>
     git -C <worktree-path> commit -m "feat(<scope>): implement <lane>"
     ```
     Pi creates the commit; AGY never runs `git commit`.
5. **Topological integration**: Pi integrates accepted lane commits into the integration branch in topological/dependency order (not worker completion order) via `git cherry-pick <commit>` or fast-forward merge. Pi NEVER edits implementation code itself.
6. **Conflict handling**:
   - Mechanical conflicts: Assign to a single AGY integration worker on the integration branch; Pi reviews the resolution.
   - Contract-changing conflicts: Stop delivery and request user planning clarification.
7. **Authoritative task markers**: After accepted lane code is integrated, a single AGY integration worker on the integration branch verifies integrated behavior and updates only the corresponding task markers in the tasks artifact.

## 8. Integrated Project Gates & Fresh Read-Only Verification

After all implementation waves are integrated on the integration branch:
1. **Independent project gates**: Pi runs repository-wide gates on the integrated branch: lint, typecheck, test suite, build, and behavioral smoke check. These run once on the integrated tree.
2. **Fresh read-only AGY verifier**:
   - Allocate a fresh background Herdr pane rooted at the repository root:
     ```text
     herdr pane split --current --direction <right|down> --cwd <repository-root> --no-focus
     ```
     Parse `.result.pane.pane_id` from the split response JSON to obtain `<pane-id>`.
   - Launch a brand-new AGY verifier in read-only mode using the extracted `<pane-id>`:
     ```text
     herdr agent start <verifier-name> --kind agy --pane <pane-id> -- --mode plan --model gemini-3.8-flash-high --effort high
     ```
     `--mode plan` ensures read-only mode. The verifier has no write authority, cannot modify files or commit, and never transitions to a writer role.
   - Prompt the fresh AGY verifier to invoke the exact skill `openspec-verify-change` (passing the change name and sticky `--store <id>` when applicable). The verifier obtains planning context using `openspec status --change <change> --json` and `openspec instructions apply --change <change> --json`, reads all context files, and evaluates completeness, correctness, coherence, task state, scenario coverage, and test integrity without editing project files.
   - Verifier findings are advisory evidence and never replace Pi's independent project gates.
   - If verifier reports a CRITICAL finding or Pi project gates fail: Route exact findings back to the responsible AGY lane or integration worker for remediation.
   - Every remediation modifying implementation code triggers a BRAND-NEW fresh read-only AGY verifier session (avoiding self-review and anchoring bias).

## 9. Remediation Loop, Resumption & Protected Stops

- **Progress-aware retries**: Automatically retry actionable AGY failures without an arbitrary round limit as long as measurable progress occurs (reducing failing tests, clearing blocking issues, or completing behavior).
- **Two-round stagnation stop**: If the identical blocker persists across two consecutive rounds without measurable progress, Pi STOPS automatic retries, preserves all delivery state, and reports the blocker and required user action.
- **Protected decision stops**: Halt immediately if an AGY worker requests credentials, destructive actions, permission escalation, deployment, publishing, requirement interpretations, scope changes, or model escalation beyond `gemini-3.8-flash-high`. Never auto-approve.
- **Partial-work recovery**: On crash or timeout, inspect and preserve partial tracked, staged, and untracked work before resuming or replacing workers.
- **Later-session recovery & ground-truth reconstruction**: When delivery resumes in a new or restarted Pi session, never trust a prior prose report, unverified summary, or candidate claims alone. Pi must:
  1. Re-run OpenSpec status and strict validation to discover current authoritative state.
  2. Inspect authoritative task markers in `tasks.md` and commit ancestry on the integration branch (`git log --oneline`) to reconstruct which lanes were legitimately accepted.
  3. Re-run independent project gates (lint, typecheck, tests, build) on the integration branch to verify that integrated code remains intact before continuing waves, verification, spec sync, or archive.

## 10. Separately Prompted Spec Synchronization & Archive

Spec synchronization and archive are strictly separate serial stages with independent prompt gates. Never issue a combined sync-and-archive prompt to AGY.

### Stage 1: Spec Synchronization
- Authorized only after implementation verification and Pi project gates pass.
- Allocate a dedicated background Herdr pane rooted at the repository root, parse `.result.pane.pane_id` from the split response JSON to obtain `<pane-id>`, and start or prompt a write-capable AGY lifecycle worker in `<pane-id>` to invoke the exact skill `openspec-sync-specs` (passing the change name and sticky `--store <id>` when applicable). The worker obtains context using `openspec status --change <change> --json` and `openspec instructions specs --change <change> --json`, performs an agent-driven intelligent merge of delta specs into main specs, and preserves unaffected requirements.
- Pi validates the result:
  - Compare updated main specs against change delta specs.
  - Run strict specs validation:
    ```text
    openspec validate --specs --strict --no-interactive [--store <id>]
    ```
- If sync diverges, fails, or produces validation errors: Withhold archive authorization, preserve state, and send exact mismatch findings back to the AGY lifecycle worker.

### Stage 2: Change Archive
- Authorized only after spec synchronization passes validation and all gates remain green.
- Send a separate archive prompt to the AGY lifecycle worker to execute the exact skill `openspec-archive-change` (passing the change name and sticky `--store <id>` when applicable). The worker may use the supported optional `openspec instructions archive --change <change> --json` lookup for runtime context and guidance, verify artifact/task completion, and move the change directory to `archive/`.
- Final Archive Audit: Pi independently confirms:
  1. The active change is removed from `changesDir`.
  2. The archive directory and metadata exist in archived changes.
  3. Main specs remain valid under strict validation.
  4. Working tree contains no unexpected modifications.

## 11. Success-Only Non-Force Cleanup & Failure Preservation

- **On failure, blocker, or user interruption**: Preserve ALL delivery resources intact.
  - Keep all Herdr panes, worker conversations, lane branches (`agy/<change>/*`), worktrees, local commits, partial changes, and logs available for resumption and audit.
  - Never run destructive or forced commands (`git worktree remove --force`, `git branch -D`, `git clean -fdx`, `git reset --hard`).
- **On complete success** (implementation, fresh verification, spec sync, archive, and final audit all pass):
  - Clean only workflow-created resources using non-force operations:
    - Close workflow-created idle panes: `herdr pane close <pane-id>`
    - Remove clean lane worktrees: `git worktree remove <worktree-path>` (without `--force`)
    - Delete fully integrated lane branches: `git branch -d agy/<change>/<lane>` (non-force `-d`, never `-D`)
  - Retain the verified local integration branch intact (`delivery/<change>` or feature branch) for user review.
  - If any resource refuses non-force removal, retain and report it intact rather than forcing cleanup.

## 12. Outcome Reporting

- **Success Report**:
  - Change name, schema, and store (if applicable)
  - Integration branch name and commit history
  - Wave breakdown, per-lane branches, worktrees, and AGY worker names
  - Accepted commits integrated in topological order
  - Independent Pi gate outcomes and fresh read-only verification results
  - Spec synchronization and archive audit outcomes
  - Summary of cleaned workflow-created resources and preserved integration branch
- **Blocked / Interrupted Report**:
  - Exact blocker or reason for pause (stagnation, protected decision, failed gate)
  - Completed and pending task lanes
  - Preserved Herdr panes, worker conversations, worktree locations, and branch names
  - Failing command outputs and error logs
  - Concrete single action or decision required from user to resume
