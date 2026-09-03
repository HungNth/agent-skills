## Why

The delivery policy is sound, but the current installation exposes `openspec-agy-delivery` to the AGY implementation worker while OMP cannot resolve it. This reverses the intended ownership boundary, creates recursive-delegation risk, and leaves shared agent guidance and workspace isolation behavior ambiguous.

## What Changes

- Make `openspec-agy-delivery` resolvable by OMP as the delivery orchestrator without allowing an AGY implementation worker to execute the orchestration workflow.
- Add an explicit worker-role guard so AGY uses the OpenSpec apply workflow and never invokes the delivery workflow recursively.
- Make project-wide instructions resolvable by both OMP and AGY from an unambiguous shared path.
- Define one compatible workspace-isolation policy for delivery instead of simultaneously requiring and forbidding worktrees.
- Treat unavailable Superpowers skills as optional guidance unless they are installed and resolvable.
- Revalidate the current model-specific launch command and retain repeatable evidence for skill behavior and trigger placement.

Non-goals:

- Parallelize a single change across multiple AGY workers.
- Add a new orchestration helper or runtime dependency.
- Change OpenSpec's proposal, specification, design, task, verification, synchronization, or archive semantics.
- Automatically commit, deploy, publish, elevate permissions, or approve protected decisions.
- Replace `gemini-3.8-flash-high` as the default AGY implementation model.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `openspec-agy-delivery`: Clarify orchestrator-only discovery, worker-role isolation, shared guidance resolution, workspace policy, and validation evidence requirements.

## Impact

- Affected skill: `skills/openspec-agy-delivery/SKILL.md` and its installation/discovery target for OMP.
- Affected project guidance: the shared agent instruction location and `openspec/config.yaml` references.
- Affected evaluations: delivery trigger-placement, recursive-delegation prevention, native Windows launch, and current default-model coverage.
- Existing OpenSpec planning and archive data formats remain unchanged.
