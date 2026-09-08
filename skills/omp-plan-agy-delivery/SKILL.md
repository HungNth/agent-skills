---
name: omp-plan-agy-delivery
description: "Execute an explicitly approved Oh My Pi plan by having OMP orchestrate AGY workers through Herdr: one AGY implementer executes the plan, then for each verification round a fresh AGY verifier in a new sibling pane independently reviews changes and reruns verification in read-only plan mode. OMP inspects evidence, decides acceptance, and routes remediation deltas back to the implementer until completion or the bounded retry stop. OMP never implements, reviews code, or runs verification checks itself. Use when the current agent is OMP, plan mode has ended, and the user asks to implement, execute, ship, or continue an OMP plan through AGY or Antigravity. Never use inside AGY, during plan authoring, without an approved plan file, or when the user wants OMP to implement directly."
compatibility: Requires OMP running inside Herdr with HERDR_ENV=1 and the herdr, agy, and git CLIs installed; AGY must be authenticated. Supports native Windows, macOS, and Linux hosts supported by those tools.
---

# OMP Plan AGY Delivery

Execute one approved Oh My Pi plan file end to end. The plan file is the only specification: AGY workers implement and verify it, Herdr owns terminal and agent lifecycle, and OMP strictly orchestrates — reading artifacts and evidence, deciding acceptance, and routing remediation. OMP does NOT implement code, perform substantive code review itself, execute project Verification (tests/build/lint), run smoke tests, or substitute built-in reviewer subagents. One AGY implementer performs all implementation and self-checks. For each verification round, a fresh AGY verifier in a new sibling pane independently verifies the candidate in read-only plan mode. This serialized two-role topology (one implementer plus one fresh verifier per verification round in the same checkout, with no concurrent writers) is the sole exception to the one-worker rule. This skill has no dependency on any planning or specification system — it reads only the OMP plan file and never creates a second plan.

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

The plan file is immutable for the whole delivery: the skill and AGY workers never modify it in any state. No `spec.md`, `tasks.md`, checkbox file, state comment, or progress file is required or created.

## Cross-platform command rule

Run each CLI operation separately through the host command tool and parse returned JSON directly. Treat command examples as argument sequences, not shell programs: no POSIX-only pipelines, heredocs, command substitution, or `jq`. Use host-native quoting and pass multiline text as one CLI argument (in PowerShell, use here-strings `@' ... '@` or ensure multiline XML arguments are properly quoted to avoid shell redirection interpretation). Use resolved absolute paths for every cwd-sensitive operation.

## Preflight toolchain and protecting user work

Confirm before delegation:

1. CLI checks:
   - `herdr --help`, `agy help`, and `git --version` succeed (exit code 0).
   - The installed `herdr pane` and `herdr agent` group discovery commands print valid help output but exit with status 2 in the installed Herdr CLI because no subcommand was specified. Accept that specific help-only outcome; NEVER whitelist exit 2 for control commands (where exit 2 indicates invalid CLI syntax and exit 1 indicates server errors).
2. Model and effort validation:
   - `agy models` validates requested model IDs (e.g. `gemini-3.8-flash-high`). It does NOT validate effort levels. Do not overclaim that model listing proves generation permissions or quota.
   - To validate effort overrides, use `agy help`, which documents supported `--effort low|medium|high` separately. Valid values are `low`, `medium`, and `high`.
   - With no user override, pass no model or effort arguments and let AGY use its configured defaults.
   - If a user-requested model or effort override is invalid, stop before starting any agent, with no fallback or escalation.
3. Read root project guidance and manifests (`AGENTS.md`, README, package manifests) and confirm every command in the plan's Verification section is still valid for this project.
4. Working tree attribution:
   - Fresh delivery: continue only when the working tree is clean except the plan file itself. If anything else is changed, staged, or untracked, stop and list it; never stash, reset, clean, or switch branches.
   - `continue` request: accept existing edits as baseline only when every changed, staged, or untracked path is confidently attributable to this plan. If attribution is uncertain, stop and list the paths.

Credentials, destructive actions, permission bypass, deployment, publishing, requirement or design changes, scope expansion, and model escalation are protected decisions: stop and return them to the user.

## Start the AGY implementer through Herdr

Follow the installed `herdr` skill. Inspect the calling pane and live agents:

```text
herdr pane current --current
herdr pane layout --current
herdr agent list
```

Split one sibling pane in the current tab: a wide pane splits right, otherwise down. Avoid repeated same-direction splits that create unusably narrow columns or short rows. Preserve the repository root and the user's focus:

```text
herdr pane split --current --direction <right|down> --cwd <git-root> --no-focus
```

Read the new pane id from `.result.pane.pane_id`.

Derive the implementer name from the plan slug, matching `[a-z][a-z0-9_-]{0,31}` (for example `agy-add-cache`). Herdr agent names must not exceed 32 characters: truncate the slug if needed (e.g. up to 24 characters) before prepending `agy-` and adding a short numeric suffix on collision. Then start AGY:

```text
herdr agent start <implementer> --kind agy --pane <pane-id> [-- <validated-user-overrides>]
```

Pass native AGY arguments only after `--`, and only for overrides the user explicitly named and preflight validated.

A successful `agent start` returns only after Herdr detects AGY and considers it ready for input. If startup returns `agent_not_ready` (e.g. AGY is showing an interactive first-run notice or prompt), or if the agent enters a `blocked` state:
- Inspect with `herdr agent get <implementer>` and `herdr agent read <implementer>`.
- Ask the user before answering! Never auto-approve or send automated keys like `y enter`.
- Wait until the agent reaches `idle` (`herdr agent wait <implementer> --timeout 30000`) before prompting it.

Do not create a workspace, tab, worktree, or alternate cwd: one AGY implementer executes the whole plan in the existing checkout. Never split the plan across multiple implementation workers or use parallel writers.

## Send one self-contained implementation brief

AGY has a separate conversation and sees nothing of this one. Compose one brief and send it once:

```text
herdr agent prompt <implementer> <brief> --wait --timeout 3600000
```

The brief must contain:

```xml
<role>
You are the AGY implementation worker, not the OMP orchestrator or verifier.
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

<self_verification>
Run and fix failures from these exact plan commands/scenarios before reporting:
<exact Verification commands with their expected observable output>
</self_verification>

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

## Handle the settled implementer state

Read `.result.agent.status` from the prompt response:

- `idle` or `done`: require target `idle` or `done` before proceeding, ensuring the active turn is complete and not mistaken for new completion. Collect the report and proceed to independent verification.
- `blocked`: inspect `herdr agent get` and `herdr agent read`. Note that `herdr agent prompt` will fail with `agent_blocked` when an agent is waiting at an approval or question dialog; inspect the UI and ask the user before answering; never auto-approve or send automated keys like `y enter`.
- `agent_prompt_stalled`, `unknown`, timeout, or command error: never prove completion. Do not resend prompts blindly. Inspect the pane with `herdr pane read <pane-id> --source recent-unwrapped` and transcript with `herdr agent read <implementer>`. Buffered Enter recovery applies ONLY when positively observing an unsent brief resting unsubmitted at an ordinary input prompt (not an approval or question UI); otherwise escalate ambiguity to the user.

Read the transcript with `herdr agent read <implementer> --source recent-unwrapped --lines 200`. If the report is incomplete (an alternate-screen agent may not keep it in scrollback), ask the idle worker to write its full report to a temporary Markdown file and reply with only the path, then read the file directly.

## Independent verification by a fresh AGY verifier

The implementer report is a claim, never completion evidence. OMP strictly orchestrates and does NOT implement, perform substantive code review itself, execute project Verification (tests/build/lint), run smoke tests, or substitute built-in reviewer subagents. Administrative Herdr/Git inspection and evidence reading remain OMP duties.

For each verification round, OMP coordinates verification using a FRESH AGY verifier in a NEW sibling Herdr pane. This serialized two-role topology (one implementer plus one fresh verifier per verification round, same checkout, no concurrent writers) is the explicit exception to the one-worker rule. The existing implementation pane remains completely idle while the verifier runs. Stop immediately on any unattributable concurrent changes.

Verifier read-only rules: no source, test, or plan edits; no fixes; no staging or commits. Build/test artifacts may be generated by approved checks; no destructive cleanup. If plan mode or permissions cannot execute a required check, the verifier must report `BLOCKED`; never switch modes, bypass permissions, or pretend `PASS`.

### Create the verifier pane and agent

1. Inspect CURRENT layout afresh:
   ```text
   herdr pane current --current
   herdr pane layout --current
   ```
   Choose `right` if the pane is wide, otherwise `down`, avoiding repeated same-direction splits that create unusable narrow or short panes.
2. Split a new sibling pane:
   ```text
   herdr pane split --current --direction <right|down> --cwd <git-root> --no-focus
   ```
   Read the new pane ID from `.result.pane.pane_id`.
3. Derive a unique verifier name within 32 characters matching `[a-z][a-z0-9_-]{0,31}` (e.g. `agy-ver-<slug>`, truncated if necessary, with numeric suffix on collision).
4. Start a FRESH AGY agent in read-only plan mode:
   ```text
   herdr agent start <verifier> --kind agy --pane <new-id> -- --mode plan [validated user overrides]
   ```
   `--mode plan` is mandatory verifier safety mode, not a user model override. Never pass `--continue`, `-c`, or `--conversation`, and never reuse an old implementation or old verifier conversation. Starting in a new pane and fresh conversation reduces inherited bias (though does not guarantee zero bias).

### Send a neutral verification brief

Do NOT forward implementer success claims, implementer transcript, self-justifications, or prior verifier verdicts. Send one neutral brief:

```text
herdr agent prompt <verifier> <verification-brief> --wait --timeout 3600000
```

The verification brief must contain:

```xml
<role>
You are an independent AGY verifier running in read-only plan mode (--mode plan).
You do not implement, modify code, or fix failures. No edits to source, test, or plan files.
No staging or git commits. Do not invoke omp-plan-agy-delivery or create panes/workers.
</role>

<approved_plan>
Approved plan: <plan-path>. Read the file as immutable reference for Approach and Verification requirements.
</approved_plan>

<scope_and_attribution>
Inspect the complete cumulative working tree: staged (git diff --cached), unstaged, and untracked files.
Verify that all changes attribute strictly to the approved Approach steps with no scope creep or shortfall.
</scope_and_attribution>

<test_integrity>
Review edits to existing tests first. A weakened assertion, added skip, or disabled/deleted test
is a blocking finding.
</test_integrity>

<verification_commands>
Execute every command in ## Verification verbatim from repository root:
<exact Verification commands with their expected observable output>
Record exact command, cwd, exit code, and actual output for each.
</verification_commands>

<smoke_check>
Exercise the smallest real-surface smoke scenario for the changed behavior and record observations.
</smoke_check>

<safety_and_report_contract>
If plan mode or permissions prevent executing a required check, report BLOCKED; never pretend PASS.
Skipped or unrun checks strictly forbid a PASS verdict.
End with:
1. Table of checks: command, cwd, exit code, actual output, status (PASS|FAIL|BLOCKED).
2. Smoke test scenario, actions, and observations.
3. Findings: file, line number, plan clause, and explanation.
4. Overall verdict: PASS, FAIL, or BLOCKED.
</safety_and_report_contract>
```

### Read and evaluate verification evidence

Wait for the verifier to settle. State `idle` or `done` alone is NOT acceptance: OMP must read and evaluate the actual run evidence.
Read the transcript with `herdr agent read <verifier> --source recent-unwrapped --lines 200`. If incomplete due to alternate-screen display, ask the idle verifier to write its report to a temporary Markdown file and reply with the path, then read that file directly.

OMP evaluates the evidence against acceptance gates:
- Complete cumulative diff matches approved Approach steps with no scope shortfall or creep.
- Test integrity verified: no weakened assertions, skipped tests, or removed test coverage.
- Every Verification command re-run and passed with exact expected output; no skipped or unrun checks.
- Real-surface smoke scenario observed and verified.
- Overall verifier verdict is `PASS` with zero blocking findings.

## Remediate in the same implementer conversation

If the verifier reports `FAIL`, `BLOCKED`, or blocking findings:

1. Compose an exact delta prompt naming the specific files, failing outputs, plan clauses, and expected outcomes, strictly prohibiting redesign and scope expansion.
2. Send the delta prompt to the SAME implementer conversation (whose pane remained idle):
   ```text
   herdr agent prompt <implementer> <delta-findings> --wait --timeout 3600000
   ```
3. Bounded retry: the initial implementation prompt is not a retry; at most three remediation prompts are allowed per delivery invocation. Stop earlier when the same blocker repeats without measurable progress.
4. Re-verification after remediation: once the implementer settles, OMP MUST open ANOTHER NEW verifier pane AND start a FRESH AGY verifier conversation (`--mode plan`). Never reuse a previous verifier pane or conversation. Serialized execution is mandatory: finish verification before writer resumes.

### Continuation requests

A later `continue` request is a new delivery invocation:
- Re-run working tree attribution preflight over all existing edits. If attribution is uncertain, stop and ask the user.
- Reuse the old conversation ONLY when Herdr proves it is the same implementer agent; NEVER reuse a verifier conversation.
- If Herdr cannot prove it is the same implementer, start a new AGY implementer with a continuation brief anchoring on existing diff context and remaining Approach steps:

```xml
<role>
You are the AGY implementation worker, continuing delivery of an approved plan.
Never invoke omp-plan-agy-delivery, create another worker or pane, or delegate further.
</role>

<approved_plan>
Approved plan: <plan-path>. Read the file before editing; it is read-only reference.
</approved_plan>

<continuation_context>
This is a continuation of a prior delivery run.
Existing changes in the working tree are part of this implementation.
Inspect existing edits with git diff and git status before writing code.
Resume implementation from remaining Approach steps: <remaining steps>.
</continuation_context>

<scope>
Complete remaining Approach steps in the existing checkout without reverting valid progress.
The plan file is immutable; do not modify it. Do not commit; OMP owns git history.
</scope>

<self_verification>
Run and fix failures from these exact plan commands/scenarios before reporting:
<exact Verification commands with their expected observable output>
</self_verification>

<decision_safety>
Stop instead of interpreting a requirement, changing design, or exceeding scope.
Protected decisions: credentials, destructive actions, permission bypass,
deployment, publishing, requirement or design changes, scope expansion.
</decision_safety>

<report>
End with: completed remaining steps, behavior changed, files touched, exact check outputs,
deviations, blockers, and remaining concerns.
</report>
```

## End state: git history never changes by itself

Never run `git add` or `git commit`. Commits happen only when the user separately requests them.
Pane management:
- On failure or interruption: preserve the working tree and ALL workflow-created worker panes (implementer and verifier) for user inspection.
- On final success: close ONLY the panes created by this workflow run (`herdr pane close <pane-id>`) to free resources; NEVER close existing unrelated, user, or caller panes.

## Report the outcome

Report outcomes for both roles backed by fresh verification evidence:
- On success: report plan path and title, implementer and verifier final states, major files/components changed, remediation rounds used, exact fresh Verification command outputs and smoke observations from the verifier, and confirmation that no commit was made.
- On failure or stop: report the exact blocker, verifier findings, preserved working-tree and worker-conversation states, and one concrete action for the user.
