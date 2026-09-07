## Context

See `proposal.md` for motivation and `specs/pi-openspec-agy-delivery/spec.md` for the behavior contract. The repository already contains an OMP-owned `openspec-agy-delivery` skill, shared OpenSpec action skills, an AGY delegate relay, and root policy for OMP/AGY ownership. Pi 0.85.1 discovers project-specific skills under `.pi/skills/`; the current environment also provides Herdr, AGY, OpenSpec, git, and the `gemini-3.8-flash-high` model.

The existing delivery skill deliberately excludes parallel workers and assigns verification, synchronization, and archive to OMP. The new workflow must therefore remain a separate Pi-owned capability rather than revise that contract. Concurrent writers cannot safely share one checkout, and OpenSpec planning artifacts produced by proposal workflows are commonly uncommitted, so parallel delivery needs a stable committed planning baseline before lane worktrees can be created.

## Goals / Non-Goals

**Goals:**

- Give Pi one deterministic workflow for supervising an approved OpenSpec change through parallel AGY implementation and serial verification, synchronization, and archive.
- Preserve dependency ordering while reducing elapsed time for genuinely independent tasks.
- Keep one writer per worktree, one owner for authoritative task markers, and one integration branch for accepted work.
- Make every stage independently reviewable, recoverable after interruption, and blocked on protected decisions.
- Reuse installed Pi, Herdr, AGY, OpenSpec, and git capabilities without introducing a scheduler service or helper runtime.

**Non-Goals:**

- Share implementation ownership with the existing OMP delivery skill or alter its specification.
- Generalize into a provider-independent multi-agent scheduler.
- Support a non-Herdr fallback in the initial version.
- Optimize for unlimited concurrency or parallel lifecycle mutations.
- Automatically land the delivery on the default branch or remote repository.

## Decisions

### Create a separate Pi-owned skill and capability

The canonical package will be `skills/pi-openspec-agy-delivery/SKILL.md`, with an identical runtime copy at `.pi/skills/pi-openspec-agy-delivery/SKILL.md`. Root `AGENTS.md` will identify the Pi-owned workflow separately from the OMP-owned workflow. The orchestration skill will not be installed into `.agents/skills/` as part of this repository.

The skill begins with a fail-closed role preflight. Pi-specific installation is the primary isolation boundary, but the prompt guard remains necessary because a source skill may still be visible in an authoring repository. Role confirmation must use the active harness context and must not rely only on inherited environment variables, which an AGY child process may inherit.

Rejected alternatives:

- Rewriting `openspec-agy-delivery` would break its OMP ownership and archive contract.
- A broad `pi-agy-orchestrator` name would trigger outside OpenSpec delivery.
- Trigger wording alone would not prevent recursive orchestration if AGY reads the source skill.

### Preserve a hard planning-to-delivery approval boundary

Explore and proposal requests authorize planning only. The delivery skill starts only from a later explicit request naming an approved change. That request authorizes local planning and lane commits, dependency-safe worktrees, AGY implementation and remediation, recommended spec synchronization, archive after all gates, and safe cleanup of workflow-created resources. It does not authorize push, deployment, publishing, permission bypass, model escalation, destructive cleanup, or requirement changes.

Rejected alternative: automatically continuing from proposal would erase the user's artifact review boundary and conflict with the existing OpenSpec planning contract.

### Resolve all OpenSpec state before scheduling

Pi first resolves a named change and optional standalone store, then runs current status, apply instructions, and strict change validation. It reads every reported context file and discovers exact project gate commands from repository policy and manifests. Store selection remains sticky in Pi commands and every AGY brief.

CLI-returned schema, roots, paths, task state, context, and instructions remain authoritative. The scheduler never assumes `tasks.md` or repository-relative `openspec/changes/<name>` paths for custom schemas.

### Build a conservative dependency graph and execute topological waves

Pi derives task nodes and dependency edges from, in order: explicit task wording and ordering, design decisions, specs, code symbols and modules, produced interfaces or fixtures, verification commands, and overlapping edit surfaces. Each lane records task IDs, dependencies, owned paths, shared contracts, and targeted gates in its brief.

A task becomes ready only after every dependency is accepted on the integration branch and every shared contract it consumes is stable. Uncertain dependencies are serialized. Migrations, lockfiles, generated outputs, central registries, and tasks that modify the same module default to one lane unless the artifacts establish a safe split.

Execution proceeds in waves. Every wave branches from the latest accepted integration commit; later waves therefore see all accepted predecessors. Pi integrates accepted lane commits in topological order, not worker completion order.

Rejected alternatives:

- Running the task checklist in textual order would miss available parallelism.
- Treating all sibling checklist items as independent would create unsafe races.
- A persistent scheduler database would duplicate state already present in OpenSpec, git, and Herdr.

### Cap concurrency at three workers by default

The default active implementation limit is `min(3, ready lanes)`. A user-supplied limit is an upper bound, not a requirement to create that many workers. Pi may reduce it for dependency safety, machine resources, heavy build contention, or unusable Herdr geometry.

Targeted lane checks run inside each worker. Repository-wide lint, typecheck, test, build, and smoke checks run once on the integrated tree rather than independently in every lane.

Rejected alternative: unlimited workers increase merge and verification cost faster than they reduce elapsed time for the expected repository sizes.

### Isolate every writer with git worktrees and Herdr panes

For each ready lane, Pi creates a unique `agy/<change>/<lane>` branch and git worktree from the current integration HEAD, splits or creates an appropriate background Herdr pane rooted at that worktree, and starts a uniquely named AGY worker using `gemini-3.8-flash-high --effort high`. No two active writers share a worktree.

The skill uses separate host-native CLI operations and parses their outputs. It does not add a POSIX-only shell wrapper or depend on pipelines, `jq`, or command substitution for workflow correctness.

The lane worker must not create another worker, commit, merge, push, sync, archive, broaden scope, or alter an unstable shared contract. AGY receives a compact self-contained brief because each worker starts with an isolated conversation.

### Use a stable local integration branch and planning checkpoint

If delivery begins on a safe non-default feature branch, that branch is the integration branch. If it begins on the repository's default branch, Pi creates `delivery/<change>` before committing. Pi stages only the selected complete planning artifacts and creates a local planning checkpoint commit; unrelated files are never staged.

AGY leaves lane edits uncommitted. After Pi reviews the complete worktree, checks test integrity, and reruns targeted gates, Pi creates a local lane commit and integrates it into the integration branch. Pi does not edit implementation code. Mechanical integration conflicts are assigned to one AGY integration worker; contract-changing conflicts return to planning.

After successful archive the result remains on the integration branch. The workflow never pushes, opens a pull request, rebases, force-pushes, or merges into the default branch.

Rejected alternatives:

- Copying uncommitted planning artifacts into every lane would create divergent planning state.
- Passing raw patches between worktrees would be more fragile for untracked files and recovery than local commits.
- Letting AGY commit would move acceptance before Pi's review.

### Keep authoritative task markers on the integration branch

Parallel lane workers report candidate completion but do not own authoritative completion markers. Pi excludes lane-local marker edits from accepted implementation commits. After accepted lane code is integrated, one AGY integration worker verifies the integrated behavior and updates only the corresponding task markers. This gives the task artifact one writer and ensures a checked task refers to code present on the integration branch.

This is a concurrency-specific adaptation of the apply contract: implementation remains AGY-owned, but task completion is recorded only after Pi acceptance and integrated verification.

Rejected alternative: allowing every lane to edit its copy of the task artifact would cause avoidable cherry-pick conflicts and could mark unintegrated work complete.

### Separate implementation, verification, and lifecycle roles

Implementation and remediation stay in the responsible lane's AGY conversation so local context is preserved. After the integrated project gates pass, Pi starts a fresh AGY verifier with `--mode plan`, the configured model, and high effort. The verifier performs `openspec-verify-change`, cannot write, and never transitions into the lifecycle writer role.

Any valid blocking finding returns to the responsible implementation lane or the integration worker. If implementation changes, the next verification uses another fresh read-only conversation to reduce anchoring and self-review bias.

After verification and Pi's independent gates pass, Pi starts or prompts one write-capable AGY lifecycle worker to perform `openspec-sync-specs`. Pi then compares every selected delta against the main specs and runs strict specs validation. Only after that passes does Pi send a separate archive prompt invoking `openspec-archive-change`.

Rejected alternatives:

- Letting implementers verify their own work weakens independent assessment.
- Reusing a read-only verifier as a writer blurs authority and permission boundaries.
- Giving AGY one combined apply-to-archive prompt allows premature irreversible stage transitions.

### Make Pi the acceptance authority without making it the implementer

AGY performs all four post-planning OpenSpec workflows. Pi owns scheduling, worktree and pane lifecycle, diff review, test-integrity review, local commits, dependency-order integration, rerunning project gates, OpenSpec validation/status checks, stage authorization, and final reporting.

An AGY success report is always a claim. Pi advances only when the relevant diff, targeted or full project gates, behavioral smoke checks, and current OpenSpec state support it. Pi never silently fixes implementation or task markers itself; it routes concrete findings back to AGY.

### Retry while progress exists and stop on repeated stagnation

There is no fixed remediation count. After each failure Pi sends a delta brief containing the exact task or requirement, file, failing command and output, required result, and preserved boundaries. Progress means relevant code or evidence improves: fewer failures or blocking findings, newly completed behavior, or a more advanced valid gate state.

Pi stops automatic retries when the same blocker shows no relevant progress across two consecutive rounds. It also stops immediately for credentials, destructive actions, permission escalation, deployment, publishing, requirement or design decisions, scope expansion, model escalation, or irreconcilable planning conflicts.

Timeouts and crashes do not authorize cleanup. Pi first inspects partial tracked, staged, and untracked work, then resumes the same conversation when safe or starts a replacement worker on the preserved lane.

Rejected alternatives:

- A fixed three-round cap can stop a steadily improving delivery prematurely.
- An unbounded blind loop can consume resources without increasing completion likelihood.
- Automatic model escalation changes cost and behavior without user approval.

### Derive recoverable state from existing systems

The initial version adds no scheduler manifest or database. OpenSpec task state, integration and lane branches, commit ancestry, `git worktree list`, Herdr agent state, and worker transcripts are sufficient to inspect or reconstruct delivery state. Worker and branch names include the change and lane identity.

If a Pi session is replaced, the next session reruns status and gates rather than trusting an unpersisted acceptance decision. This costs verification time but avoids introducing a second mutable source of truth.

### Clean only workflow-created resources after complete success

Lane workers, worktrees, and branches remain available until implementation, fresh verification, synchronization, archive, and final audit all pass. On success Pi may close workflow-created idle panes, remove clean lane worktrees, and delete fully integrated lane branches with non-force operations. It retains the integration branch.

On failure, interruption, or a user stop, Pi preserves every pane, conversation, worktree, branch, local commit, partial change, and failure output. If normal cleanup refuses a resource, Pi reports and retains it rather than using force.

### Track evaluations with the canonical skill

The canonical package will retain `evals/evals.json`; `.gitignore` will receive only the narrow exception needed for that file. Evaluations will cover positive and negative triggers, Pi/AGY role isolation, sticky stores, DAG waves, uncertain dependency serialization, concurrency override, one-writer isolation, task-marker ownership, branch boundaries, fresh read-only verification, repeated remediation, protected decisions, sync/archive gates, interruption preservation, and success cleanup.

The canonical and `.pi/skills` copies must match byte-for-byte before validation. Structural skill validation, evaluation grading, and strict OpenSpec change validation are required evidence; unavailable tooling is reported as unverified.

## Risks / Trade-offs

- [Dependency inference can be conservative and leave speed on the table] -> Prefer correctness; users can improve future plans with explicit dependency wording, but uncertainty remains serial by contract.
- [Parallel lanes can still produce semantic conflicts despite disjoint files] -> Re-run integrated gates and fresh OpenSpec verification, then route cross-lane failures to one integration AGY worker.
- [Local planning and lane commits alter branch history] -> Create only scoped local commits, never push automatically, and leave results on a reviewable integration branch.
- [Three AGY workers can contend for CPU, memory, or build caches] -> Treat three as an upper bound and reduce active workers when project gates are resource-heavy.
- [A fresh verifier per remediation cycle costs additional model time] -> Use one verifier at a time and only after integrated gates pass; independence is worth the bounded cost.
- [Preserving resources on failure can leave worktrees and panes behind] -> Report exact cleanup candidates and remove them automatically only after complete success.
- [The orchestration skill may still be visible to AGY in the source repository] -> Install the runtime copy under `.pi/skills` and retain a fail-closed role guard in the canonical source.
- [No separate manifest means reconstruction reruns checks] -> Prefer existing authoritative state over a new mutable registry; report branch, worktree, worker, and commit identities on every stop.

## Migration Plan

1. Add the canonical skill, tracked evaluations, and the Pi runtime copy without changing the existing OMP skill.
2. Add the Pi/AGY ownership and concurrent-worktree policy to root guidance and document the separate planning and delivery invocation.
3. Validate skill structure and exact canonical/runtime-copy equality.
4. Run dry-run evaluations for trigger isolation, scheduling, failure handling, and lifecycle gates without starting a real implementation delivery.
5. Run one bounded fixture-repository delivery that contains both dependent and independent tasks, verifying parallel lane creation, integration, fresh verification, sync, archive, and cleanup.
6. If validation fails, remove only the newly added Pi skill and guidance; the existing OMP workflow remains unchanged and provides the rollback path.
