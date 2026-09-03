## Dry-run delivery target

- **Change:** `add-search`
- **Store:** none specified; use the active/default OpenSpec planning root
- **State:** `ready`
- **Execution:** none—this describes the workflow only and does not run commands or modify files
- **Superpowers:** not required by this delivery workflow

Before launching AGY, I would resolve authoritative values rather than infer paths:

```text
openspec status --change add-search --json
openspec instructions apply --change add-search --json
openspec validate add-search --type change --strict --no-interactive
```

From those results I would retain `schemaName`, `planningHome`, `changeRoot`, `actionContext`, apply state, task list, `contextFiles`, and the dynamic apply instruction. Every `contextFiles` path would be read before delegation.

I would also confirm `HERDR_ENV=1`, CLI availability, authentication, repository root, and working-tree safety. Pre-existing changes would be allowed only inside the resolved `changeRoot`; unrelated dirty paths would stop delivery. Canonical lint, typecheck, test, build, and behavioral-smoke commands would be discovered from repository instructions and manifests before prompting AGY.

## Worker launch

I would first inspect the current Herdr topology and existing agents, using separate CLI operations:

```text
herdr pane current --current
herdr pane layout --current
herdr agent list
```

The worker would normally be named:

```text
agy-add-search
```

If that name already existed, I would add a short suffix. I would not reuse an unrelated worker or create a workspace, tab, worktree, or alternate cwd.

Using the absolute repository root returned by:

```text
git rev-parse --show-toplevel
```

I would choose the split according to current pane geometry:

- wide pane → `right`
- otherwise → `down`

For example:

```text
herdr pane split --current --direction right --cwd <absolute-repository-root> --no-focus
```

I would parse the new pane ID from `.result.pane.pane_id`, then start AGY:

```text
herdr agent start agy-add-search --kind agy --pane <new-pane-id>
```

The user’s pane retains focus. The implementation request would be passed as one argument:

```text
herdr agent prompt agy-add-search <complete-brief> --wait --timeout 3600000
```

## Complete AGY implementation brief

Before sending, placeholders for context, paths, and project commands would be replaced with the literal values discovered by OMP. The brief would be:

```xml
<task>
Implement the approved OpenSpec change: add-search.
Use the selected store: none.

Run OpenSpec status and apply instructions for exactly the add-search change
in the default selected planning root.

Read every path returned in contextFiles, including the approved proposal,
specs, design, tasks, and any action-context files. Follow the dynamic apply
instruction returned by OpenSpec.

Implement every remaining approved task until all tasks are complete or you
are blocked.
</task>

<scope>
Treat the approved OpenSpec proposal, specifications, design, task list,
schema, resolved roots, and action context as authoritative.

Work only in the resolved repository root and against the resolved
add-search change.

Do not create another plan.
Do not redesign the approved change.
Do not broaden requirements or implementation scope.
Do not perform unrelated refactoring, cleanup, dependency upgrades, or
formatting.
Do not create another workspace, tab, branch, worktree, or repository clone.
Do not overwrite or remove pre-existing user work.
Do not commit.
Do not deploy or publish.
Do not synchronize OpenSpec delta specifications.
Do not archive the OpenSpec change.

Update only the implementation files and the task-completion markers required
by the OpenSpec apply workflow.
</scope>

<verification_loop>
Run the following exact project commands discovered by OMP, from the resolved
absolute repository root, and fix failures caused by this delivery:

Lint:
<literal canonical lint command or explicitly “not defined by project”>

Typecheck:
<literal canonical typecheck command or explicitly “not defined by project”>

Tests:
<literal canonical test command or commands>

Build:
<literal canonical build command or explicitly “not defined by project”>

Behavioral smoke:
<literal smallest relevant command or scenario for the changed search surface>

Do not substitute guessed commands or omit a defined gate.

Review the complete working tree, including tracked, staged, and untracked
files. Confirm it contains only changes intended for add-search.

Do not weaken tests to make checks pass. Do not skip, disable, delete, or
relax assertions covering required behavior.
</verification_loop>

<decision_safety>
Stop and report rather than proceeding if the work requires any of the
following:

- credentials or authentication decisions
- destructive operations
- deleting or overwriting user work
- permission escalation
- deployment or publishing
- a new requirement or product decision
- a design decision not settled by the approved OpenSpec artifacts
- resolution of a conflict between approved artifacts
- scope expansion
- branch, workspace, or worktree topology changes
- any action that cannot safely be attributed to add-search

Do not guess, silently select an option, or auto-approve a protected decision.
Safe mechanical implementation choices may be made only within the approved
design and requirements.
</decision_safety>

<report>
At completion, provide a concise but complete report containing:

1. work completed
2. files touched
3. task-by-task OpenSpec progress and completion markers
4. every verification command actually run
5. exact outcome of each lint, typecheck, test, build, and smoke check
6. deviations from the approved artifacts, if any
7. blockers, if any
8. remaining risks or concerns
9. confirmation that no commit, spec synchronization, or archive was performed
</report>
```

## Worker settlement and report collection

I would inspect `.result.agent.status` from the prompt response:

- `idle` or `done`: collect the report and verify independently.
- `blocked`: inspect the worker and transcript; answer only safe mechanical questions and escalate protected decisions.
- `unknown`: inspect and wait for a known state; it is not completion evidence.
- timeout or command error: inspect the agent, terminal output, and working tree before deciding whether a retry is safe.

The transcript would be read with:

```text
herdr agent read agy-add-search --source recent-unwrapped --lines 200
```

If the transcript lacked a complete report, I would ask the same idle worker to write its report to a temporary Markdown file and reply only with that path. I would then read that file directly.

## Independent OMP verification

AGY’s report would be treated only as a claim. OMP would perform all of the following from the resolved repository root.

### 1. Inspect the complete working tree

I would inspect:

- tracked modifications
- staged modifications
- untracked files
- deletions and renames
- task-marker edits
- all changed tests

Representative separate Git operations would include:

```text
git status --porcelain=v1 --untracked-files=all
git diff
git diff --cached
```

I would compare the resulting path set with the approved `add-search` scope and the pre-delegation baseline.

Blocking findings include:

- unrelated files changed
- unexplained generated artifacts
- overwriting pre-existing user work
- test skips or disabled tests
- deleted coverage for required behavior
- weakened assertions
- implementation outside approved scope
- unapproved dependency or configuration changes

### 2. Compare implementation with every approved artifact

I would reread every resolved `contextFiles` path and verify:

- each approved task is implemented
- required task markers are complete
- implementation matches the proposal and specifications
- design constraints were followed
- action-context requirements were respected
- no extra requirement or behavior was introduced
- no required error case, compatibility condition, or acceptance scenario was omitted

I would refresh OpenSpec state rather than trust task markers alone:

```text
openspec status --change add-search --json
openspec instructions apply --change add-search --json
openspec validate add-search --type change --strict --no-interactive
```

Any incomplete required task or invalid change blocks archive.

### 3. Run formal OpenSpec verification

In OMP, I would invoke the installed verification workflow for the exact change:

```text
/opsx-verify add-search
```

Because no standalone store is selected, no `--store` value is added. If a store had been resolved, that same store ID would be used here and in every later handoff.

A **CRITICAL** OpenSpec finding blocks delivery. Warnings and suggestions would be reported and would block only if they reveal missing required behavior or another failed gate.

### 4. Rerun canonical project checks freshly

OMP—not AGY—would rerun every canonical command discovered before delegation, individually and from the absolute repository root:

1. lint
2. typecheck
3. complete relevant test suite
4. build
5. any repository-mandated validation command

I would record each exact command, exit status, and material output. AGY’s earlier successful results would not substitute for these fresh runs.

If a category is genuinely absent from the project, I would report it as “not defined by project,” based on repository evidence rather than guessing a command.

### 5. Exercise the real search behavior

I would run the smallest relevant behavioral smoke scenario on the actual changed surface, not merely a mocked helper. Depending on the approved artifacts, that would verify applicable cases such as:

- entering a query through the real UI, CLI, or API surface
- receiving expected matching results
- handling no-result input correctly
- preserving required filtering, ordering, or pagination
- handling empty or malformed input as specified
- confirming existing non-search behavior remains usable

The precise smoke procedure would come from the approved specs and the project’s documented run commands. A failed or unexercisable required smoke scenario blocks archive.

## Remediation if verification fails

Concrete findings would be sent to the same `agy-add-search` conversation. The prompt would name:

- exact files
- exact failed commands and outputs
- exact OpenSpec findings
- required task or behavior
- expected corrected outcome
- prohibition on redesign or scope expansion

For example:

```text
herdr agent prompt agy-add-search <delta-findings> --wait --timeout 3600000
```

After each remediation round, OMP would repeat:

1. complete working-tree and test-diff inspection
2. `/opsx-verify add-search`
3. all failed and mandatory project checks
4. the behavioral smoke scenario

At most three failed remediation rounds are authorized. A repeated blocker without progress would stop earlier. The working tree would be preserved, and no archive would occur.

## Completion gate

Only after all checks pass would OMP—not AGY—perform recommended specification synchronization and archive through the installed OpenSpec archive workflow. Archive requires:

- worker settled successfully, or implementation was already complete
- every required task complete
- no CRITICAL `/opsx-verify` finding
- fresh lint/typecheck/test/build gates passing
- behavioral smoke passing
- no weakened tests
- no unresolved protected decision

No commit would be created unless the user separately requested one.