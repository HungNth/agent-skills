# OpenSpec AGY Delivery Specification

## Purpose

Defines the observable contract for delivering an approved OpenSpec change through OMP, Herdr, and AGY with cross-platform orchestration, independent verification, bounded remediation, and safe archiving.

## Requirements

### Requirement: Delivery requires explicit post-planning approval
The delivery workflow SHALL start implementation only after the planning workflow has stopped and the user has issued a separate, explicit request to deliver an approved change.

#### Scenario: Planning completes without delivery
- **WHEN** an OpenSpec explore or proposal workflow finishes creating planning artifacts
- **THEN** the delivery workflow does not start AGY or modify implementation files

#### Scenario: User explicitly approves delivery
- **WHEN** the user issues a new request to deliver a named approved change
- **THEN** the workflow may proceed through implementation, bounded remediation, required spec synchronization, and archive subject to its safety gates

### Requirement: Delivery works without a POSIX-only helper
The delivery workflow SHALL operate on supported host platforms without requiring Bash, `jq`, or another POSIX-only executable wrapper.

#### Scenario: Native Windows host
- **WHEN** OMP, Herdr, AGY CLI, OpenSpec CLI, and git are available in a native Windows environment
- **THEN** the delivery workflow can perform the same delivery lifecycle available on macOS and Linux

#### Scenario: Missing required CLI
- **WHEN** a required delivery CLI is unavailable or unauthenticated
- **THEN** the workflow stops before implementation and reports the missing prerequisite

### Requirement: OpenSpec context is resolved dynamically
The delivery workflow SHALL derive the selected schema, planning root, change root, artifact paths, apply state, and context files from OpenSpec CLI output instead of assuming repository-relative artifact paths.

#### Scenario: Repository-local change
- **WHEN** the approved change belongs to the nearest repository OpenSpec root
- **THEN** the workflow uses the paths and context reported for that root

#### Scenario: Standalone store change
- **WHEN** the user selects a registered standalone store
- **THEN** the workflow keeps that store selection on every applicable OpenSpec command through verification and archive

#### Scenario: Custom schema
- **WHEN** the approved change uses a schema whose task artifact is not `tasks.md`
- **THEN** the workflow follows the apply instructions and context files reported by that schema

### Requirement: Existing user work is protected
The delivery workflow SHALL inspect the working tree before delegation and SHALL NOT overwrite, discard, or silently absorb unrelated pre-existing changes.

#### Scenario: Only selected change artifacts are uncommitted
- **WHEN** the only pre-existing changes are inside the selected OpenSpec change root
- **THEN** the workflow may continue while preserving those artifacts

#### Scenario: Unrelated files are already modified
- **WHEN** the working tree contains unrelated pre-existing changes that make implementation attribution unsafe
- **THEN** the workflow stops before delegation and reports the conflicting paths

### Requirement: Herdr launches AGY in the correct workspace
The delivery workflow SHALL run inside a Herdr-managed OMP pane and SHALL launch an AGY worker in a background pane rooted at the selected repository.

#### Scenario: New worker is required
- **WHEN** no safe worker exists for the selected repository and change
- **THEN** the workflow creates a layout-appropriate sibling pane without stealing focus and starts a uniquely named AGY worker in the repository cwd

#### Scenario: Existing worker does not match
- **WHEN** a worker name already belongs to another repository, workspace, or active delivery
- **THEN** the workflow does not reuse that worker

### Requirement: AGY follows the approved OpenSpec apply contract
The AGY worker SHALL implement the remaining tasks described by the selected change and SHALL treat the reported OpenSpec apply context as authoritative.

#### Scenario: Apply state is ready
- **WHEN** OpenSpec reports remaining implementation tasks
- **THEN** AGY reads every reported context file, implements the remaining tasks, updates required completion markers, runs implementation-time checks, and returns a structured report

#### Scenario: Apply state is blocked
- **WHEN** OpenSpec reports that required planning artifacts are missing or the apply workflow is blocked
- **THEN** the delivery workflow stops without asking AGY to invent missing plans or requirements

#### Scenario: Worker encounters a protected decision
- **WHEN** implementation requires a credential, destructive action, permission escalation, deployment, publishing, requirement decision, or scope expansion
- **THEN** AGY stops and OMP presents the blocker to the user instead of guessing or auto-approving it

### Requirement: OMP independently verifies implementation
OMP SHALL treat AGY output as a claim and SHALL independently verify artifact conformance and project behavior before archive.

#### Scenario: AGY reports success
- **WHEN** AGY settles in an idle or done state after implementation
- **THEN** OMP inspects the complete working-tree change, runs `openspec-verify-change`, and runs fresh project-specific verification and behavioral checks

#### Scenario: OpenSpec verification finds a critical issue
- **WHEN** `openspec-verify-change` reports one or more CRITICAL findings
- **THEN** the workflow treats delivery as failed and does not archive

#### Scenario: Fresh project verification fails
- **WHEN** any required lint, typecheck, test, build, or behavioral check fails
- **THEN** the workflow treats delivery as failed regardless of AGY's reported results

### Requirement: Verification failures use bounded remediation
The delivery workflow SHALL send concrete verification findings back to the same AGY conversation and SHALL re-run all blocking gates after each remediation attempt.

#### Scenario: Remediation succeeds
- **WHEN** AGY fixes the reported findings within the allowed remediation rounds
- **THEN** OMP re-runs OpenSpec verification and fresh project verification before continuing

#### Scenario: Remediation remains unsuccessful
- **WHEN** three remediation rounds fail or the same unresolved blocker repeats without progress
- **THEN** the workflow stops, preserves the working tree, and reports the remaining findings without archiving

### Requirement: Archive is owned and gated by OMP
OMP SHALL own spec synchronization and archive, and AGY SHALL NOT perform either operation.

#### Scenario: Every blocking gate passes
- **WHEN** implementation is complete, OpenSpec verification has no CRITICAL findings, fresh project verification passes, and no protected decision remains
- **THEN** OMP follows `openspec-archive-change`, applies the approved recommended spec synchronization when required, and archives the change

#### Scenario: A blocking gate remains
- **WHEN** any required gate or decision remains unresolved
- **THEN** the change remains active and the workflow reports why archive was skipped

### Requirement: Delivery reports verifiable outcomes
The workflow SHALL finish with a concise report that identifies the selected change, worker state, affected areas, independently executed verification, remediation outcome, and archive result.

#### Scenario: Successful delivery
- **WHEN** the change is archived successfully
- **THEN** the report names the fresh verification commands and outcomes rather than only repeating AGY's claims

#### Scenario: Blocked delivery
- **WHEN** delivery stops before archive
- **THEN** the report identifies the exact blocker and the single action required from the user

### Requirement: The skill is evaluated against realistic delivery cases
The skill package SHALL include repeatable evaluations that distinguish the revised behavior from the previous skill behavior.

#### Scenario: Cross-platform evaluation
- **WHEN** the evaluation represents a native Windows delivery request
- **THEN** success requires a workflow that does not invoke the removed Bash helper or depend on `jq`

#### Scenario: Store-aware evaluation
- **WHEN** the evaluation represents a change in a standalone store
- **THEN** success requires sticky store selection and dynamic artifact paths

#### Scenario: Verification failure evaluation
- **WHEN** AGY settles but independent verification reports blocking findings
- **THEN** success requires remediation or a gated stop and forbids archive

### Requirement: Delivery orchestration is owned exclusively by OMP
The delivery workflow SHALL be available to the OMP orchestrator in its intended installation and SHALL NOT allow an AGY implementation worker to start or recursively delegate another delivery workflow.

#### Scenario: OMP receives an approved delivery request
- **WHEN** OMP receives a separate explicit request to deliver a named approved OpenSpec change through AGY
- **THEN** OMP can resolve and execute the delivery workflow

#### Scenario: AGY receives the implementation brief
- **WHEN** the AGY worker is asked to implement the approved change
- **THEN** it uses the OpenSpec apply contract and does not invoke the delivery workflow

#### Scenario: Orchestration skill is visible in a shared authoring repository
- **WHEN** an AGY worker can discover the delivery skill despite agent-scoped installation controls
- **THEN** the delivery skill fails closed for the AGY role and directs the worker to the apply workflow without creating another worker

### Requirement: Shared project guidance is resolvable by every participating agent
The workflow SHALL reference project-wide instructions through a concrete repository path that both OMP and AGY can read before making planning, implementation, or verification decisions.

#### Scenario: OpenSpec supplies project context
- **WHEN** OpenSpec instructions tell an agent to follow the project guidance
- **THEN** the referenced file exists at the named path and is included or explicitly read by the responsible agent

#### Scenario: AGY starts with an isolated conversation
- **WHEN** OMP sends the self-contained implementation brief
- **THEN** the brief identifies the shared guidance path in addition to the OpenSpec context files

### Requirement: Delivery uses one deterministic workspace-isolation policy
The workflow SHALL use the existing repository working tree for the default single-worker delivery after its attribution preflight passes, and SHALL create a worktree only when the user explicitly requests isolation or the approved topology requires concurrent workers.

#### Scenario: Single-worker delivery has an attributable working tree
- **WHEN** unrelated pre-existing changes are absent and one AGY worker will implement the change
- **THEN** delivery proceeds in the existing repository without creating a second worktree

#### Scenario: Unrelated work makes attribution unsafe
- **WHEN** the repository contains unrelated pre-existing changes
- **THEN** delivery stops and reports the paths instead of automatically stashing, cleaning, moving, or isolating them

#### Scenario: User explicitly requests an isolated worktree
- **WHEN** the user authorizes an isolated worktree for the delivery
- **THEN** the workflow may create and use that topology while preserving all other delivery gates

### Requirement: Optional workflow aids are not undeclared runtime dependencies
The workflow SHALL distinguish mandatory delivery tools from optional skills and SHALL remain executable when an optional skill is not installed.

#### Scenario: Required delivery CLI is missing
- **WHEN** Herdr, AGY, OpenSpec, git, or AGY authentication is unavailable
- **THEN** delivery stops before implementation and reports the missing prerequisite

#### Scenario: Optional engineering skill is unavailable
- **WHEN** an optional review, debugging, TDD, verification, or worktree skill cannot be resolved
- **THEN** OMP follows the equivalent explicit delivery policy without treating the missing skill as a delivery failure

### Requirement: The installed delivery revision has repeatable validation evidence
The workflow SHALL retain checks that cover agent-role placement, recursive-delegation prevention, the configured AGY model launch, independent verification, and gated archive behavior for the exact delivery skill revision being used.

#### Scenario: Default AGY model is available
- **WHEN** the configured default model appears in `agy models` and the AGY CLI accepts its model and effort arguments
- **THEN** OMP starts the worker with that explicit model configuration

#### Scenario: Current skill revision changes
- **WHEN** delivery instructions, trigger metadata, installation placement, or model arguments change
- **THEN** skill validation and affected behavior evaluations are rerun before the revision is treated as verified

#### Scenario: Validation tooling is unavailable
- **WHEN** a validation command cannot run because its own dependency is missing
- **THEN** the result is reported as unverified rather than treated as a passing check
