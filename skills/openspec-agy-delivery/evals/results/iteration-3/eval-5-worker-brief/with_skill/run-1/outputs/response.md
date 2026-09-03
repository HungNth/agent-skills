This is a dry-run description only. I would not execute commands, split panes, start agents, or modify files. The absence of Superpowers skills does not block delivery because those skills are supplemental.

## 1. Preflight and change resolution

Given the supplied evaluation facts, I would confirm:

- Current agent role: OMP
- Runtime: inside Herdr with `HERDR_ENV=1`
- Separate post-planning approval exists for delivery of `add-search`
- Change state: `ready`
- Required CLIs and AGY authentication: available

Because no standalone OpenSpec store was named, the selected store would be **none**. In a live delivery, I would still obtain authoritative metadata by running each operation separately:

```text
openspec status --change add-search --json
openspec instructions apply --change add-search --json
openspec validate add-search --type change --strict --no-interactive
```

I would use the returned `schemaName`, `planningHome`, `changeRoot`, `actionContext`, `contextFiles`, tasks, state, and dynamic apply instruction rather than assuming conventional paths.

Before delegation, I would also:

1. Resolve the absolute repository root with `git rev-parse --show-toplevel`.
2. Inspect staged, tracked, and untracked changes.
3. Stop if any pre-existing changes outside the selected `changeRoot` cannot safely be attributed to this delivery.
4. Read every returned `contextFiles` path.
5. Read root `AGENTS.md`, repository instructions, documentation, and manifests.
6. Discover the project’s exact lint, typecheck, test, build, and behavioral smoke commands. AGY would not be asked to guess them.

## 2. Worker launch

I would inspect Herdr before changing its layout:

```text
herdr pane current --current
herdr pane layout --current
herdr agent list
```

I would derive a valid, unused worker name such as:

```text
agy-add-search
```

The name must match `[a-z][a-z0-9_-]{0,31}`. If it collided, I would add a short suffix.

Using the current pane geometry:

- Split **right** if the current pane is wide.
- Otherwise split **down**.

The dry-run launch sequence would be:

```text
herdr pane split --current --direction <right|down> --cwd <absolute-repository-root> --no-focus
```

I would read the new pane ID from `.result.pane.pane_id`, then start AGY in that pane:

```text
herdr agent start agy-add-search --kind agy --pane <pane-id> -- --model gemini-3.8-flash-high --effort high
```

This uses:

- A dedicated worker
- The existing repository working tree
- The resolved repository root as its cwd
- No new tab, worktree, workspace, or alternate checkout
- The default `gemini-3.8-flash-high` model with high reasoning effort
- No focus change for the user

I would then send the brief as one argument and wait up to one hour:

```text
herdr agent prompt agy-add-search <brief> --wait --timeout 3600000
```

## 3. Complete implementation brief

The brief would be self-contained and would include the project commands discovered by OMP verbatim:

```xml
<role>
You are the AGY implementation worker, not the OMP delivery orchestrator.
Use the workflow named exactly openspec-apply-change for the named change;
do not describe it only as SKILL.md.
Never invoke openspec-agy-delivery or create another AGY worker.
</role>

<task>
Implement the approved OpenSpec change: add-search.
Use the selected store: none.

Read root AGENTS.md and all applicable repository instructions for shared
project policy.

Run OpenSpec status and apply instructions for the exact change add-search,
with no standalone store selected.

Use the schema, planning home, change root, action context, apply state,
contextFiles, task list, and dynamic apply instruction returned by OpenSpec
as authoritative.

Read every path returned in contextFiles and follow the dynamic apply
instruction.

Implement every remaining approved task until all tasks are complete or
you encounter a blocker.
</task>

<scope>
Treat the approved proposal, specs, design, implementation tasks, and
action context as authoritative.

Do not create a second plan.
Do not redesign the approved change.
Do not broaden scope.
Do not perform unrelated refactoring, cleanup, dependency updates, or
formatting churn.
Do not make requirement decisions that are not already resolved by the
approved artifacts.

Update only the task-completion markers required by the apply workflow.

Do not commit.
Do not synchronize delta specs into the main specs.
Do not archive the change.
OMP owns independent verification, remediation decisions, spec
synchronization, archive, and any separately requested commit.
</scope>

<verification_loop>
Run and fix failures from these exact project commands before finishing:

Lint:
<exact lint command discovered by OMP>

Typecheck:
<exact typecheck command discovered by OMP>

Tests:
<exact test command or commands discovered by OMP>

Build:
<exact build command discovered by OMP>

Behavioral smoke:
<exact smallest relevant smoke command or procedure discovered by OMP>

Do not substitute guessed commands for these commands.
Do not weaken, skip, disable, or remove tests to obtain a passing result.

After implementation and checks, inspect the complete working tree,
including staged and untracked files, and confirm that it contains only
changes intended for delivery of add-search.
</verification_loop>

<decision_safety>
Stop and report rather than proceeding if the work requires any of the
following:

- credentials or secrets
- a destructive operation
- permission escalation
- deployment
- publishing
- a new or unresolved requirement decision
- a conflict between approved design or specification artifacts
- scope expansion

Do not guess, silently choose, or auto-approve any such decision.
Do not reset, clean, stash, switch branches, overwrite unrelated user work,
or otherwise destroy or conceal existing changes.
</decision_safety>

<report>
End with a complete report containing:

1. Work completed
2. Files touched
3. OpenSpec task progress and completion-marker updates
4. Every exact check command run and its observed outcome
5. Behavioral smoke outcome
6. Deviations from the approved artifacts or instructions
7. Blockers
8. Remaining concerns
9. Confirmation that no commit, spec synchronization, or archive was done
</report>
```

## 4. Settled worker handling

After the prompt returned, I would inspect `.result.agent.status`:

- `idle` or `done`: collect the report and begin independent verification.
- `blocked`: inspect the agent and transcript. I could answer only safe, mechanical questions; protected decisions would go back to the user.
- `unknown`: inspect and wait because this is not completion evidence.
- Timeout or command error: inspect agent state, terminal output, and the working tree before retrying.

I would read the recent transcript with:

```text
herdr agent read agy-add-search --source recent-unwrapped --lines 200
```

If the report were incomplete, I would ask the same idle worker to write a full report to a temporary Markdown file and reply only with its path, then read that file directly.

## 5. Exact independent OMP verification

The worker’s report would be treated only as a claim. OMP would independently perform all of the following.

### A. Inspect the complete working tree

I would inspect:

- Unstaged tracked changes
- Staged changes
- Untracked files
- The complete diff, not merely the worker’s file list
- Task-marker edits under the resolved `changeRoot`
- Existing tests modified by the worker

I would block delivery if tests had been weakened, including:

- Reduced or removed assertions
- Skipped or disabled tests
- Narrowed test coverage that hides a failure
- Changed fixtures that make an invalid behavior pass
- Suppressed lint, type, or runtime errors without approved justification

I would also confirm that no unrelated user files were modified and that there was no commit, spec synchronization, or archive.

### B. Compare implementation with all approved context

I would reread and compare the implementation against every authoritative path returned in `contextFiles`, including the applicable:

- Proposal
- Delta specifications
- Design
- Task list
- Action context
- Dynamic apply instruction

I would verify each required task against repository evidence rather than trusting its checkbox. A checked task without its required implementation or test evidence would remain incomplete.

### C. Run OpenSpec verification

OMP would invoke the installed verification workflow for the exact change:

```text
/opsx-verify add-search
```

This verification would use the same selected planning root and store selection—here, no standalone store.

Any **CRITICAL** OpenSpec finding would block archive. Warnings and suggestions would be reported and would block only if they reveal missing required behavior or another failed gate.

### D. Rerun canonical project gates from OMP

From the resolved repository root, OMP—not AGY—would freshly rerun the exact commands discovered before delegation:

```text
<exact lint command>
<exact typecheck command>
<exact test command or commands>
<exact build command>
```

These would be clean, fresh executions after the worker had settled. The worker’s reported results would not substitute for them.

Any required command failure would block delivery and archive.

### E. Exercise the changed behavior directly

OMP would run the smallest relevant real-surface smoke scenario for search, as determined from the approved requirements and repository instructions. It would test the actual affected interface rather than only an internal helper—for example, the real CLI command, HTTP endpoint, UI flow, or library entry point used by the project.

The smoke verification would establish the approved behavior, including relevant success and failure or empty-result behavior required by `add-search`. I would not invent additional requirements beyond the approved artifacts.

A failed smoke scenario would block archive even if unit tests passed.

### F. Determine the verification result

Archive would remain blocked if any of these existed:

- A CRITICAL `/opsx-verify` finding
- An incomplete required task
- A task marker that does not match implementation evidence
- A weakened, skipped, or disabled test
- A failed lint, typecheck, test, or build command
- A failed behavioral smoke scenario
- Unattributed or unrelated working-tree changes
- An unresolved credential, destructive, permission, deployment, publishing, requirement, design, or scope decision

## 6. Remediation if verification fails

Concrete findings would be sent to the **same** `agy-add-search` conversation. The prompt would identify:

- Exact files and lines or components at issue
- Exact failed commands and relevant output
- Exact OpenSpec findings
- Expected approved behavior
- Required outcome

It would explicitly prohibit redesign, new planning, and scope expansion.

After each remediation round, OMP would again:

1. Inspect the complete working tree and diff.
2. Rerun `/opsx-verify add-search`.
3. Rerun all required project gates, including previously failed commands.
4. Rerun the behavioral smoke scenario.

At most three failed remediation rounds are authorized. If the same blocker repeated without progress, I would stop earlier, preserve the working tree, skip archive, and report the concrete user action needed.

Only after every blocking gate passed would OMP perform recommended spec synchronization and archive through the `openspec-archive-change` workflow. AGY would never synchronize, archive, or commit.