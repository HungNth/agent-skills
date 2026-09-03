## ADDED Requirements

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
