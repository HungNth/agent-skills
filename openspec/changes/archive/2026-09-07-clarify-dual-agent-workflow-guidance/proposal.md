## Why

Root AGENTS.md retains a long OMP-first policy followed by a separate Pi delivery policy, repeating responsibilities and making workflow-specific rules harder to distinguish. A concise shared section and two clearly scoped orchestration sections will preserve both supported workflows without duplicating their skills.

## What Changes

- Reorganize AGENTS.md into Shared rules, Pi + AGY, and OMP + AGY under a neutral title.
- State common OpenSpec ownership, separate post-planning approval, evidence-based completion, scope protection, and AGY non-recursion rules once.
- Retain distinct ownership, concurrency, task-marker, commit, remediation, and cleanup policies for each workflow.
- Require the responsible orchestrator to read its exact delivery skill; leave CLI recipes, detailed stage mechanics, and worker prompts in those skills.
- Condense OMP-specific scout/librarian/sonic guidance without applying OMP worker conventions to Pi or AGY.
- Aim for approximately 50–70 lines, prioritizing clarity and complete boundaries over a rigid line limit.

Non-goals: change either delivery contract; remove OMP support; edit either skill, README.md, OpenSpec configuration, existing specs, or archived changes; introduce new subagent tooling or runtime behavior.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- None. This is a documentation consolidation preserving existing behavior; `.openspec.yaml` declares `skip_specs: true`.

## Impact

- Implementation scope: root AGENTS.md only.
- Both Pi and OMP retain their existing dedicated delivery skills as the detailed workflow references.
- No dependencies, executable code, runtime configuration, or public interfaces change.
