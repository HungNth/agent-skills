## Why

The repository has an OMP-owned OpenSpec-to-AGY delivery workflow, but no equivalent workflow for Pi to supervise AGY across the complete post-planning lifecycle. A Pi-owned workflow is needed to parallelize independent implementation tasks safely while retaining independent review, bounded authority, resumable remediation, and gated synchronization and archive.

## What Changes

- Add a Pi-owned `pi-openspec-agy-delivery` skill that starts only after a separate explicit delivery request for an approved OpenSpec change.
- Have Pi derive a dependency graph from the approved artifacts and project evidence, execute ready tasks in dependency-preserving waves, and run up to three independent AGY workers in parallel by default.
- Isolate every concurrent AGY writer in its own git branch, worktree, and Herdr pane, with one assigned task lane and explicit path and interface boundaries.
- Let AGY perform every post-planning OpenSpec workflow: apply through scoped implementation workers, verify through a fresh read-only verifier, and sync/archive through a gated lifecycle worker.
- Keep acceptance authority with Pi: inspect and integrate lane diffs, rerun project gates and OpenSpec validation/status checks, route exact failures back to AGY, and prevent later stages until evidence passes.
- Create local planning and accepted-lane commits as orchestration checkpoints without pushing, merging into the default branch, deploying, or publishing.
- Retry actionable AGY failures while measurable progress continues; stop on protected decisions or when the same blocker makes no progress across two consecutive rounds.
- Preserve panes, conversations, worktrees, branches, partial changes, and evidence on failure; automatically clean up only workflow-created, fully integrated resources after successful verification, synchronization, archive, and final audit.
- Add repeatable evaluations covering trigger isolation, dependency scheduling, worktree isolation, parallel execution, verification independence, remediation, lifecycle gates, interruption recovery, and cleanup behavior.

Non-goals:

- Modify or replace the existing OMP-owned `openspec-agy-delivery` workflow.
- Start delivery automatically from the planning request or from the same turn that creates planning artifacts.
- Allow concurrent writers in one working tree, infer unsafe parallelism when dependencies are uncertain, or parallelize verify, sync, and archive.
- Let AGY create nested workers, commit, merge, push, deploy, publish, approve protected decisions, or broaden the approved change.
- Add a scheduler service, persistent database, POSIX-only helper, or non-Herdr execution fallback in the initial version.
- Automatically escalate beyond `gemini-3.8-flash-high` or bypass AGY permissions.

## Capabilities

### New Capabilities

- `pi-openspec-agy-delivery`: Pi-owned, Herdr-based orchestration of dependency-aware parallel AGY workers across apply, verification, spec synchronization, and archive.

### Modified Capabilities

- None.

## Impact

- New canonical skill under `skills/pi-openspec-agy-delivery/` and an identical Pi runtime copy under `.pi/skills/pi-openspec-agy-delivery/`.
- Shared workflow guidance in root `AGENTS.md` and installation/usage guidance in `README.md`.
- Tracked skill evaluations and any narrow `.gitignore` exception required to retain them.
- OpenSpec planning and validation artifacts for the new capability.
- Runtime prerequisites remain Pi, Herdr, AGY CLI, OpenSpec CLI, git, and AGY authentication; no new package or service dependency is introduced.
