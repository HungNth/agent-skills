---
name: omp-plan-agy-delivery
description: Execute an explicitly approved Oh My Pi plan by having OMP control one Antigravity CLI worker through Herdr, independently review the resulting diff and verification, and send concrete fixes back to the same worker until completion or the bounded retry stop. Use when the current agent is OMP, plan mode has ended, and the user asks to implement, execute, ship, or continue an OMP plan through AGY or Antigravity. Never use inside AGY, during plan authoring, without an approved plan file, or when the user wants OMP to implement directly.
compatibility: Requires OMP running inside Herdr with HERDR_ENV=1 and the herdr, agy, and git CLIs installed; AGY must be authenticated. Supports native Windows, macOS, and Linux hosts supported by those tools.
---

# OMP Plan AGY Delivery

Execute one approved Oh My Pi plan file end to end. The plan file is the only specification: AGY implements it, Herdr owns terminal and agent lifecycle, OMP owns judgment, independent review, verification, and remediation. This skill has no dependency on any planning or specification system — it reads only the OMP plan file and never creates a second plan.

## Agent-role preflight

This is an OMP orchestration workflow, never an AGY implementation workflow. Before any Herdr mutation, confirm every check:

1. The current runtime identifies this agent as OMP. Skill availability, repository location, or an implementation request does not prove the role.
2. `HERDR_ENV` is `1`: this agent runs inside a Herdr-managed pane.
3. Plan mode has ended. A turn that is authoring, revising, or approving a plan never triggers this skill.
4. The request asks to execute, implement, ship, or continue an approved plan and names an approved plan file. A request that only asks to write or edit a plan is plan authoring.

Fail closed before every Herdr mutation when any check fails, and say which check failed.

If the current agent is AGY or cannot confirm that it is OMP, stop. Split no pane, start or prompt no agent, and run no delivery step. Reply that `omp-plan-agy-delivery` is OMP-owned and orchestration belongs to the OMP session.

## Plan resolution gate

Resolve the explicit plan path before any delegation:

1. Run `git rev-parse --show-toplevel` and keep the absolute root for the whole delivery.
2. Resolve the user-supplied plan path against that root. The file must exist inside the root; reject a path outside it.
3. The basename must end with `-plan.md` (the OMP plan convention, e.g. `plans/add-cache-plan.md`).
4. Read the plan file and require the canonical OMP plan structure:
   - `## Context`
   - an ordered `## Approach` — the task sequence AGY must execute
   - `## Verification`
   - optional `## Critical files & anchors` and `## Assumptions & contingencies`
5. Require decision-completeness: no placeholder (`TODO`, `TBD`, open questions), every Approach step names exact target files/symbols, and Verification lists commands or scenarios with expected observable output. If a plan command no longer exists or repository state makes the plan no longer decision-complete, stop and ask the user to fix the plan instead of letting the worker guess.

The plan file is immutable for the whole delivery: the skill and AGY never modify it in any state. No `spec.md`, `tasks.md`, checkbox file, state comment, or progress file is required or created.

## Cross-platform command rule

Run each CLI operation separately through the host command tool and parse returned JSON directly. Treat command examples as argument sequences, not shell programs: no POSIX-only pipelines, heredocs, command substitution, or `jq`. Use host-native quoting and pass multiline text as one CLI argument. Use resolved absolute paths for every cwd-sensitive operation.

## Preflight toolchain and protecting user work

Confirm before delegation:

1. `herdr --help`, the relevant `herdr pane` and `herdr agent` group help, `agy help`, and `git --version` succeed.
2. `agy models` succeeds — that proves authentication. Use it only to validate a model or effort override the user explicitly named; if the override is not in the list, stop before starting the agent, with no fallback or escalation. With no user override, pass no model or effort arguments and let AGY use its configured default.
3. Read root project guidance and manifests (`AGENTS.md`, README, package manifests) and confirm every command in the plan's Verification section is still valid for this project.
4. Working tree attribution:
   - Fresh delivery: continue only when the working tree is clean except the plan file itself. If anything else is changed, staged, or untracked, stop and list it; never stash, reset, clean, or switch branches.
   - `continue` request: accept existing edits as baseline only when every changed, staged, or untracked path is confidently attributable to this plan. If attribution is uncertain, stop and list the paths.

Credentials, destructive actions, permission bypass, deployment, publishing, requirement or design changes, scope expansion, and model escalation are protected decisions: stop and return them to the user.

## Start one AGY worker through Herdr

Follow the installed `herdr` skill. Inspect the calling pane and live agents:

```text
herdr pane current --current
herdr pane layout --current
herdr agent list
```

Split one sibling pane in the current tab: a wide pane splits right, otherwise down. Preserve the repository root and the user's focus:

```text
herdr pane split --current --direction <right|down> --cwd <git-root> --no-focus
```

Read the new pane id from `.result.pane.pane_id`.

Derive the worker name from the plan slug, matching `[a-z][a-z0-9_-]{0,31}` (for example `agy-add-cache`); add a short numeric suffix on collision. Then start AGY:

```text
herdr agent start <worker> --kind agy --pane <pane-id>
```

Pass native AGY arguments only after `--`, and only for an override the user named and `agy models` validated. Do not create a workspace, tab, worktree, or alternate cwd: one AGY worker executes the whole plan in the existing checkout. Never split the plan across multiple workers or use parallel scheduling.

## Send one self-contained implementation brief

AGY has a separate conversation and sees nothing of this one. Compose one brief and send it once:

```text
herdr agent prompt <worker> <brief> --wait --timeout 3600000
```

The brief must contain:

```xml
<role>
You are the AGY implementation worker, not the OMP orchestrator.
Never invoke omp-plan-agy-delivery, create another worker or pane, or delegate further.
</role>

<approved_plan>
Approved plan: <plan-path>. Read the file before editing; it is read-only reference.
The ordered Approach steps are your task sequence. Follow every step with its
exact target files/symbols, plus Critical files, Assumptions, and acceptance
conditions from the plan.
</approved_plan>

<scope>
Execute all Approach steps top to bottom in the existing checkout.
The plan file is immutable; do not modify it.
No unrelated refactor or cleanup. Do not commit; OMP owns git history.
</scope>

<verification_loop>
Run and fix failures from these exact plan commands/scenarios before reporting:
<exact Verification commands with their expected observable output>
</verification_loop>

<decision_safety>
Stop instead of interpreting a requirement, changing design, or exceeding scope.
Protected decisions: credentials, destructive actions, permission bypass,
deployment, publishing, requirement or design changes, scope expansion.
</decision_safety>

<report>
End with: completed steps, behavior changed, files touched, exact check outputs,
deviations, blockers, and remaining concerns.
</report>
```

## Handle the settled worker state

Read `.result.agent.status` from the prompt response:

- `idle` or `done`: collect the report and go to independent review.
- `blocked`: inspect `herdr agent get` and `herdr agent read`; answer only safe mechanical prompts; escalate protected decisions to the user.
- `unknown`, timeout, or command error: not completion evidence. Inspect the transcript and the complete working tree before deciding whether to retry.

Read the transcript with `herdr agent read <worker> --source recent-unwrapped --lines 200`. If the report is incomplete (an alternate-screen agent may not keep it in scrollback), ask the idle worker to write its full report to a temporary Markdown file and reply with only the path, then read the file directly.

## Review independently — claims are not evidence

The worker report is a claim, never completion evidence:

1. Inspect the complete cumulative tree: staged (`git diff --cached`), unstaged, and untracked files. Untracked files are the worker's new files; no diff shows their contents.
2. Review edits to existing tests first. A weakened assertion, an added skip, a disabled or deleted test is a blocking finding: the gate measures less than it did before the run until it is resolved.
3. Compare the diff against every Approach step and its target paths/symbols: scope shortfall, scope creep, and quiet judgment calls are all findings.
4. Re-run every command and scenario in the plan's `## Verification` verbatim from OMP and read the output.
5. Exercise the smallest real-surface smoke for the changed behavior.
6. For a substantial diff, use the `reviewer` subagent when available; OMP still owns acceptance.

## Remediate in the same conversation

On any failed gate, send one delta prompt to the same worker conversation:

```text
herdr agent prompt <worker> <delta-findings> --wait --timeout 3600000
```

The delta prompt must name exact files, failing output, the plan clause, and the expected outcome, and must prohibit redesign and scope expansion.

After every remediation round, repeat the full review: complete diff, test-integrity check, every Verification command, and the smoke scenario. The initial implementation prompt is not a retry; one delivery invocation allows at most three remediation prompts. Stop earlier when the same blocker repeats without measurable progress. When stopping, keep the checkout and the worker conversation for the user to inspect. A later `continue` request is a new delivery invocation: re-run the attribution preflight over all existing edits, and reuse the old conversation only when Herdr proves it is the same worker; otherwise start a new worker with the full plan and the current diff context.

## End state: git history never changes by itself

Never run `git add` or `git commit`. Commit happens only when the user separately requests it. Only on success may the pane this workflow created be closed (`herdr pane close <pane-id>`) to free resources; on failure or interruption keep the pane and the working tree.

## Report the outcome

On success, report: plan path and title, worker state, major files or components changed, remediation rounds used, the exact fresh Verification commands and smoke outputs, and that no commit was made. On failure or stop, report the exact blocker, the preserved working-tree and worker-conversation state, and one concrete action for the user.
