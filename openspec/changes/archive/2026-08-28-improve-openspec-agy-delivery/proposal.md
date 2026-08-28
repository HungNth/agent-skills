## Why

The current delivery skill delegates through a Bash and `jq` helper, which prevents native Windows use and duplicates OpenSpec and Herdr behavior that the orchestrator can already perform directly. Reworking the skill now also lets it use the newly installed `openspec-verify-change` workflow as the authoritative artifact-conformance gate.

## What Changes

- Replace the executable shell-helper flow with cross-platform, tool-driven instructions in `SKILL.md`.
- Resolve the selected change, standalone store, schema, artifact paths, and apply context from OpenSpec CLI output instead of hardcoded repository paths.
- Start and coordinate the AGY worker through Herdr with an explicit repository cwd, layout-aware pane selection, and safe worker identity handling.
- Require OMP-owned verification through `openspec-verify-change`, fresh project gates, bounded remediation, and archive only after every blocking gate passes.
- Add objective skill evals and compare the revised skill against the current version using the local `skill-creator` workflow.
- **BREAKING**: Remove `scripts/openspec-agy-delegate.sh`; callers must invoke the skill workflow rather than the helper script directly.

## Capabilities

### New Capabilities

- `openspec-agy-delivery`: Deliver an explicitly approved OpenSpec change through OMP, Herdr, and AGY on supported host platforms, then independently verify, remediate, and archive it.

### Modified Capabilities

None.

## Non-goals

- Change Herdr, AGY CLI, OpenSpec CLI, or the installed OpenSpec workflow skills.
- Bypass the separate user approval required between planning and implementation.
- Auto-approve credentials, destructive operations, permission escalation, deployment, publishing, or requirement and scope decisions.

## Impact

- Rewrite `skills/openspec-agy-delivery/SKILL.md`.
- Remove `skills/openspec-agy-delivery/scripts/openspec-agy-delegate.sh` and the empty `scripts/` directory.
- Add `skills/openspec-agy-delivery/evals/evals.json` and temporary sibling workspace artifacts used by `skill-creator` evaluation.
- Require OMP, Herdr, AGY CLI, OpenSpec CLI, and git for delivery execution; no new runtime package dependency is introduced.
