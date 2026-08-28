## Context

See `proposal.md` for motivation and `specs/openspec-agy-delivery/spec.md` for the behavior contract. The current skill is a short Markdown wrapper around a Bash helper. That helper duplicates OpenSpec path resolution and Herdr lifecycle handling, while the installed OpenSpec and Herdr skills already define those contracts. The OMP-specific `openspec-verify-change` skill is now available at `.omp/skills/openspec-verify-change/SKILL.md` and is invoked as `/opsx-verify`.

Herdr supports native Windows, macOS, and Linux. The portability failure comes from the bundled Bash and `jq` orchestration rather than the underlying agent runtime.

## Goals / Non-Goals

**Goals:**

- Keep the complete delivery policy in one readable `SKILL.md`.
- Compose existing OpenSpec, Herdr, AGY, and OMP verification behavior instead of reimplementing their CLIs.
- Make successful execution independent of POSIX shell syntax.
- Preserve a strict ownership boundary: AGY implements; OMP verifies, remediates, and archives.
- Leave objective evaluation coverage for the cross-platform and safety contracts.

**Non-Goals:**

- Provide a general Herdr or AGY tutorial.
- Add another runtime helper in Node, PowerShell, Python, or another language.
- Change installed OpenSpec workflows or make AGY responsible for archive.
- Eliminate the explicit user approval boundary after planning.

## Decisions

### Keep orchestration in `SKILL.md`

The revised workflow will use one `SKILL.md` under 500 lines and remove the executable helper. OMP can already run commands, inspect JSON responses, read files, and make state decisions; an additional program adds drift without adding a capability.

Rejected alternatives:

- A PowerShell companion script duplicates the existing helper and creates two implementations.
- A Node helper is cross-platform but still duplicates Herdr and OpenSpec behavior already available to the orchestrator.
- A reference-only workflow adds indirection without reducing the initial skill enough to justify progressive disclosure.

A worker-prompt reference may be introduced later only if evaluation shows that the main skill has become difficult to navigate.

### Compose installed skills at explicit boundaries

The delivery skill will direct OMP to use:

- `openspec-apply-change` semantics when preparing the AGY implementation brief.
- `herdr` for pane, cwd, worker identity, lifecycle, blocked-state handling, and output collection.
- `openspec-verify-change` through the OMP invocation `/opsx-verify` for artifact conformance.
- `openspec-archive-change` for store-aware spec synchronization and archive.
- The local `.agents/skills/skill-creator/` workflow to evaluate the revised skill against the old version.

The delivery skill remains the integration policy; it does not copy the full bodies of those component skills.

### Resolve OpenSpec state before delegation

OMP will resolve one approved change, keep a selected standalone store sticky, then read `status --json` and `instructions apply --json`. The reported `planningHome`, `changeRoot`, `contextFiles`, state, and dynamic instruction become the source of truth. Hardcoded `openspec/changes/<name>` and `tasks.md` paths are removed.

Strict validation remains a preflight check. A blocked apply state stops before AGY starts; an all-done state skips implementation and proceeds to verification.

### Protect pre-existing work with a narrow preflight

The workflow will inspect tracked, staged, and untracked changes before delegation. It may continue when pre-existing changes are confined to the selected OpenSpec change root because newly proposed artifacts are commonly uncommitted. Unrelated dirty paths stop automatic delivery because AGY edits could not be attributed safely without altering or isolating user work.

The workflow never cleans, resets, stashes, or switches branches automatically.

### Drive Herdr directly and preserve repository context

OMP will confirm `HERDR_ENV=1`, inspect the current pane layout, choose a right or down split according to available geometry, and pass the resolved repository cwd explicitly. The split remains unfocused.

The AGY worker name will be derived from the change name and made unique within Herdr's naming limits. An existing worker is reused only when its live metadata matches the same repository and delivery; otherwise a new name is chosen. Remediation keeps the same worker conversation.

`agent prompt --wait` is sufficient for the default settled states. OMP reads the returned JSON status instead of translating it through custom exit codes. If the terminal transcript is incomplete, OMP asks AGY to write the full report to a temporary Markdown file and reads that file.

### Give AGY a self-contained bounded brief

The initial prompt will identify the change and store selection, require AGY to load the OpenSpec apply instructions and every context file, name exact project gates discovered by OMP, and define a structured final report. It will prohibit a second plan, unrelated refactoring, commit, sync, and archive.

AGY may answer safe mechanical questions, but protected decisions are returned to OMP as blockers. Remediation prompts contain only the concrete delta findings because the existing worker conversation retains the original context.

### Layer verification instead of trusting one signal

Verification has three independent layers:

1. Inspect the complete working-tree change, including staged and untracked files, against the approved artifacts.
2. Run `openspec-verify-change` and treat every CRITICAL finding as blocking.
3. Run fresh project lint, typecheck, test, build, and behavioral checks selected from repository evidence.

The OpenSpec verification skill uses heuristic implementation mapping, so it complements rather than replaces executable project verification. Warnings and suggestions are reported; they block only when they reveal a required behavior or project gate failure.

### Bound remediation and keep archive ownership with OMP

OMP sends verification findings to the same AGY worker, then re-runs all blocking verification. The loop stops after three failed rounds or earlier when the same blocker repeats without progress.

Successful delivery invokes `openspec-archive-change`. The explicit delivery request authorizes the recommended spec synchronization and archive after all gates pass, but never authorizes credentials, destructive actions, permission escalation, deployment, publishing, or scope decisions.

### Evaluate with the local `skill-creator`

Before editing, copy the current skill into the sibling evaluation workspace as the baseline. Add three realistic evals covering native Windows portability, standalone-store resolution, and failed verification/remediation. Run old-skill and revised-skill cases together, grade objective expectations, aggregate the benchmark, and generate the standard review viewer.

Iteration stops when the revised skill satisfies the expectations and human review finds no material workflow defect. Description optimization is optional after behavioral evaluation passes.

## Risks / Trade-offs

- [Agent command runners still differ by host] -> Express operations as individual CLI invocations and state transitions, not shell programs or POSIX parsing snippets.
- [A heuristic OpenSpec report can miss runtime defects] -> Keep fresh executable project gates and behavioral checks mandatory.
- [Herdr transcript history can truncate a long AGY report] -> Use the documented temporary-file fallback after an insufficient read.
- [Unrelated dirty files prevent fully automatic execution] -> Stop before delegation rather than risk absorbing or overwriting user work.
- [Three remediation rounds may stop a fixable change] -> Preserve the working tree and report exact remaining findings so the user can choose the next action.

## Migration Plan

1. Snapshot the existing skill for `skill-creator` baseline evaluation.
2. Replace the shell-helper instructions with the direct orchestration workflow and correct the OMP verification invocation to `/opsx-verify`.
3. Remove the Bash helper and add the initial eval set.
4. Run skill validation, old-versus-new evaluations, grading, benchmark aggregation, and the review viewer.
5. Iterate on the skill until the required expectations pass; keep the old snapshot only in the evaluation workspace.

Rollback is restoring the baseline `SKILL.md` and shell helper from the evaluation snapshot or version control. No project runtime data migration is required.
