# Pi OpenSpec AGY Delivery Specification

## Purpose

Defines a Pi-owned delivery contract for safely coordinating dependency-aware parallel AGY workers through an approved OpenSpec change while preserving independent acceptance, recoverability, and lifecycle gates.

## Requirements

### Requirement: Delivery requires a separate post-planning authorization

The workflow SHALL begin implementation only after planning has stopped and the user has issued a separate explicit request to deliver a named approved OpenSpec change through Pi and AGY.

#### Scenario: Planning artifacts become ready

- **WHEN** Pi completes an OpenSpec explore or proposal workflow
- **THEN** Pi stops without starting AGY, creating delivery branches, or modifying implementation files

#### Scenario: User authorizes delivery separately

- **WHEN** the user sends a new request to deliver the approved change through Pi and AGY
- **THEN** the workflow may proceed through its preflight, implementation, verification, synchronization, and archive gates

### Requirement: Delivery orchestration is owned by Pi

The workflow SHALL run only under a Pi orchestrator and SHALL prevent an AGY worker or another orchestrator role from recursively starting the delivery workflow.

#### Scenario: Pi receives the delivery request

- **WHEN** the current agent is confirmed as Pi and all required runtime conditions are available
- **THEN** Pi may resolve and orchestrate the delivery

#### Scenario: AGY discovers the orchestration skill

- **WHEN** an AGY worker can read the skill from a shared repository or installation
- **THEN** the skill stops before creating workers or mutating delivery state and directs AGY to its assigned atomic OpenSpec workflow

### Requirement: OpenSpec context is resolved dynamically

The workflow SHALL derive the selected change, schema, planning root, change root, action context, artifact paths, apply state, and context files from current OpenSpec CLI output.

#### Scenario: Change is repository-local

- **WHEN** the selected change belongs to the nearest repository OpenSpec root
- **THEN** every stage uses the paths returned for that root rather than assumed repository-relative locations

#### Scenario: Change belongs to a standalone store

- **WHEN** the user selects a registered standalone store
- **THEN** the selected store remains attached to every applicable OpenSpec command and AGY handoff through archive

#### Scenario: Apply is blocked

- **WHEN** OpenSpec reports missing or incomplete planning prerequisites
- **THEN** Pi stops before creating implementation workers and reports the blocking artifacts

### Requirement: Prerequisites and existing user work are protected

The workflow SHALL verify Pi, Herdr, AGY, OpenSpec, git, AGY authentication, the configured AGY model, repository identity, and attributable working-tree state before delegation.

#### Scenario: Unrelated work is already present

- **WHEN** tracked, staged, or untracked changes cannot be attributed to the selected OpenSpec change
- **THEN** delivery stops without stashing, cleaning, resetting, switching away from, or overwriting the user's work

#### Scenario: Required runtime capability is unavailable

- **WHEN** a mandatory CLI, authentication state, model, or Herdr runtime is unavailable
- **THEN** delivery stops before implementation and reports the exact missing prerequisite

### Requirement: Pi schedules tasks from explicit dependencies and repository evidence

Pi SHALL build a task dependency graph from the approved artifacts and relevant project evidence, and SHALL execute only tasks whose dependencies and shared contracts are ready.

#### Scenario: Tasks are independent

- **WHEN** tasks have no producer-consumer dependency, unsafe path overlap, shared mutable contract, ordered migration, or common generated output
- **THEN** Pi may place them in the same parallel execution wave

#### Scenario: A task depends on earlier work

- **WHEN** a task consumes an interface, schema, fixture, configuration, or output produced by another task
- **THEN** Pi schedules it only after the producing task has been accepted and integrated

#### Scenario: Dependency evidence is uncertain

- **WHEN** Pi cannot establish that two tasks are safe to run concurrently
- **THEN** Pi serializes them rather than guessing that they are independent

### Requirement: Concurrent writers are isolated

Every concurrently active AGY writer SHALL have its own branch, git worktree, Herdr pane, worker identity, assigned task set, and bounded edit scope.

#### Scenario: A parallel wave contains multiple ready lanes

- **WHEN** two or more safe independent lanes are ready
- **THEN** Pi creates separate worktrees and Herdr AGY workers from the latest accepted integration commit

#### Scenario: Only one task is ready

- **WHEN** the dependency graph exposes one ready lane
- **THEN** Pi runs one writer without creating unnecessary parallel workers

#### Scenario: Worker count is not overridden

- **WHEN** the delivery request does not specify a concurrency limit
- **THEN** Pi runs no more than three AGY implementation workers concurrently

#### Scenario: User requests another concurrency limit

- **WHEN** the user explicitly supplies a worker limit
- **THEN** Pi treats it as an upper bound and may use fewer workers when dependencies, safety, resources, or observable Herdr layout require it

### Requirement: Parallel lanes have enforceable task boundaries

Each AGY implementation lane SHALL receive a self-contained brief containing its assigned task identifiers, satisfied dependencies, approved contracts, allowed scope, exact targeted checks, prohibited actions, and report format.

#### Scenario: Lane work begins

- **WHEN** Pi prompts a newly created AGY implementation worker
- **THEN** the worker can identify exactly which tasks to implement, what it may change, what it must preserve, and how its candidate completion will be evaluated

#### Scenario: Lane discovers cross-lane or planning scope

- **WHEN** correct completion requires changing an unassigned task, unstable shared contract, requirement, design decision, or another lane's owned paths
- **THEN** the worker stops and reports the dependency or scope conflict instead of absorbing it

### Requirement: Authoritative task completion follows accepted integration

A task SHALL be considered complete only after its implementation is accepted into the integration branch and its stated verification passes there.

#### Scenario: Lane reports candidate completion

- **WHEN** AGY finishes its assigned worktree task and reports passing targeted checks
- **THEN** Pi treats the report as a candidate claim and does not accept the authoritative task marker yet

#### Scenario: Accepted lane is integrated

- **WHEN** Pi reviews the lane, reruns the required checks, and integrates its local commit
- **THEN** a single AGY integration worker may verify the integrated result and update the corresponding authoritative task marker

### Requirement: Pi owns local integration and acceptance

Pi SHALL inspect complete lane changes, rerun required targeted checks, create local commits for accepted work, and integrate accepted lanes in dependency order without writing implementation code itself.

#### Scenario: Lane passes review

- **WHEN** the diff is scoped, required behavior is present, tests are not weakened, and targeted checks pass
- **THEN** Pi creates a local lane commit and integrates it into the selected integration branch

#### Scenario: Lane fails review

- **WHEN** scope, behavior, tests, or checks do not satisfy the assigned task contract
- **THEN** Pi sends exact delta findings to the same AGY conversation and does not integrate the lane

#### Scenario: Integration conflict is mechanical

- **WHEN** accepted lane commits conflict without requiring a new requirement or design decision
- **THEN** Pi assigns the conflict to one AGY integration worker and independently reviews the resolution

#### Scenario: Integration conflict changes the approved contract

- **WHEN** resolving a conflict requires a requirement, design, or scope decision
- **THEN** delivery stops and requests planning clarification from the user

### Requirement: Delivery uses safe local branch and commit boundaries

The workflow SHALL create only local orchestration commits, SHALL avoid committing unrelated work, and SHALL leave delivery results on a non-default integration branch when delivery starts from the default branch.

#### Scenario: Delivery starts on a feature branch

- **WHEN** the current non-default branch is safe to use as the integration branch
- **THEN** Pi creates the planning checkpoint and accepted delivery commits on that branch

#### Scenario: Delivery starts on the default branch

- **WHEN** the selected repository is on its default branch
- **THEN** Pi creates a local `delivery/<change>` integration branch before committing the approved planning checkpoint

#### Scenario: Delivery reaches a final branch

- **WHEN** synchronization and archive complete successfully
- **THEN** Pi leaves the verified local integration branch without pushing, force-pushing, rebasing, opening a pull request, or merging it into the default branch

### Requirement: AGY performs all post-planning OpenSpec workflows

AGY SHALL perform apply, verification, spec synchronization, and archive, while Pi SHALL own stage authorization and independent acceptance evidence.

#### Scenario: Implementation stage is authorized

- **WHEN** planning and delivery preflight pass
- **THEN** scoped AGY workers follow the OpenSpec apply contract for their assigned tasks

#### Scenario: Integrated implementation is ready for verification

- **WHEN** all required implementation tasks are integrated and project gates pass
- **THEN** Pi starts a fresh read-only AGY verifier to perform the OpenSpec verification workflow

#### Scenario: Verification and sync gates pass

- **WHEN** verification has no blocking finding and Pi's independent gates pass
- **THEN** Pi separately authorizes an AGY lifecycle worker to perform spec synchronization

#### Scenario: Synchronized specs pass independent validation

- **WHEN** Pi confirms the main specs match the selected deltas and strict specs validation passes
- **THEN** Pi separately authorizes the AGY lifecycle worker to perform archive

### Requirement: Verification is fresh, read-only, and independently accepted

Every verification cycle SHALL use a fresh AGY conversation without write authority, and its report SHALL not replace Pi's independent project checks.

#### Scenario: Fresh verification starts

- **WHEN** integrated implementation is ready to verify
- **THEN** the verifier reads every current context file and evaluates completeness, correctness, coherence, task state, scenario coverage, and test integrity without modifying the repository

#### Scenario: Verification finds a blocking issue

- **WHEN** the verifier reports a valid CRITICAL issue or Pi's lint, typecheck, test, build, smoke, or validation gate fails
- **THEN** Pi routes the exact finding to the responsible implementation or integration AGY worker and forbids synchronization

#### Scenario: Implementation changes after a failed verification

- **WHEN** remediation modifies the integrated implementation
- **THEN** the next OpenSpec verification uses another fresh read-only AGY conversation

### Requirement: Remediation continues while measurable progress exists

The workflow SHALL automatically retry actionable AGY failures without a fixed remediation count while requiring fresh evidence of progress after each round.

#### Scenario: Remediation improves the result

- **WHEN** a round reduces failing checks or blocking findings, completes missing behavior, or otherwise produces relevant measurable progress
- **THEN** Pi continues the remediation and verification loop

#### Scenario: The same blocker makes no progress

- **WHEN** the same blocker persists across two consecutive rounds without relevant implementation or evidence improvement
- **THEN** Pi stops the automatic loop, preserves the delivery state, and reports the blocker and required user action

#### Scenario: A protected decision is required

- **WHEN** completion requires credentials, destructive action, permission escalation, deployment, publishing, requirement interpretation, design change, scope expansion, or model escalation
- **THEN** Pi stops and asks the user rather than allowing AGY to decide or auto-approve it

#### Scenario: AGY crashes or times out

- **WHEN** a worker process terminates before a trustworthy completion report
- **THEN** Pi inspects and preserves the partial work before deciding whether to resume the same conversation or start a replacement worker

### Requirement: Synchronization and archive are separately gated

Spec synchronization and archive SHALL be serial stages, and archive SHALL never begin before synchronized specs and the integrated implementation independently pass their required gates.

#### Scenario: Spec synchronization fails or diverges

- **WHEN** the AGY lifecycle worker reports failure, main specs do not match the selected deltas, or strict specs validation fails
- **THEN** Pi withholds archive and sends the exact mismatch back to AGY

#### Scenario: Archive succeeds

- **WHEN** AGY archives the change after every gate passes
- **THEN** Pi confirms the active change is absent, the archive target and metadata exist, the main specs remain valid, and no unrelated file changed

### Requirement: Workflow-created resources are cleaned only after success

The workflow SHALL preserve all delivery resources on failure, interruption, or unresolved blockers, and SHALL automatically clean only resources it created after complete success.

#### Scenario: Delivery completes successfully

- **WHEN** implementation, verification, synchronization, archive, and final audit pass
- **THEN** Pi may close workflow-created idle workers and panes, remove clean lane worktrees, and delete fully integrated lane branches using non-force operations while retaining the integration branch

#### Scenario: Delivery fails or is interrupted

- **WHEN** any blocking gate remains or the user stops the workflow
- **THEN** Pi preserves worker conversations, panes, branches, worktrees, commits, partial changes, and failure evidence for resumption

#### Scenario: Safe cleanup is refused

- **WHEN** git or Herdr cannot remove a resource without force or potential data loss
- **THEN** Pi leaves the resource intact and reports it instead of forcing cleanup

### Requirement: Delivery outcome is recoverable and auditable

The workflow SHALL report enough state and evidence for the user or a later Pi session to understand, resume, or inspect the delivery.

#### Scenario: Delivery succeeds

- **WHEN** final audit passes
- **THEN** the report identifies the change, integration branch, execution waves, AGY workers, accepted commits, remediation history, fresh gate outcomes, synchronization result, archive location, and cleanup result

#### Scenario: Delivery stops before success

- **WHEN** a blocker, interruption, or repeated non-progress condition stops delivery
- **THEN** the report identifies completed and pending lanes, each preserved worker, branch and worktree location, failing evidence, and the single next decision or action required

### Requirement: The skill revision has repeatable evaluation evidence

The skill package SHALL include tracked evaluations for its trigger boundary, role isolation, dependency scheduling, concurrency limit, worktree isolation, integration ownership, fresh verification, remediation policy, lifecycle gates, recovery, and cleanup behavior.

#### Scenario: Skill behavior changes

- **WHEN** trigger metadata, scheduling rules, worker prompts, model arguments, stage gates, or cleanup behavior changes
- **THEN** structural validation and affected behavior evaluations are rerun for the exact canonical and Pi-installed revision

#### Scenario: Evaluation tooling is unavailable

- **WHEN** a required validation or evaluation dependency cannot run
- **THEN** the revision is reported as unverified rather than treated as passing
