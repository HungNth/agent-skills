## 1. Evaluation Contract

- [x] 1.1 Add a narrow `.gitignore` exception and `skills/pi-openspec-agy-delivery/evals/evals.json` covering positive and negative triggers, Pi/AGY role isolation, sticky stores, dependency waves, uncertain-dependency serialization, concurrency override, worktree isolation, task-marker ownership, integration boundaries, fresh verification, remediation stagnation, lifecycle gates, interruption preservation, and success cleanup; verify the JSON parses against `.agents/skills/skill-creator/references/schemas.md`.
- [x] 1.2 Add a bounded fixture-repository evaluation scenario with independent and dependent tasks plus observable expected branches, worktrees, worker roles, gates, sync, archive, and cleanup outcomes; verify the fixture definition contains no credentials, remote push, deployment, permission bypass, or destructive cleanup step.

## 2. Canonical Pi Delivery Skill

- [x] 2.1 Create `skills/pi-openspec-agy-delivery/SKILL.md` with precise trigger metadata, Pi-only fail-closed role detection, separate post-planning approval, store-aware OpenSpec resolution, prerequisite and dirty-tree checks, default-branch integration handling, and scoped planning checkpoint authorization; verify `python .agents/skills/skill-creator/scripts/quick_validate.py skills/pi-openspec-agy-delivery` reports `Skill is valid!`.
- [x] 2.2 Extend the canonical skill with conservative dependency-graph construction, topological execution waves, default maximum concurrency of three, per-lane branches and worktrees, Herdr pane and AGY startup using `gemini-3.8-flash-high --effort high`, bounded lane briefs, and targeted lane checks; verify dry-run scheduling cases parallelize only independent tasks and serialize uncertain or dependent tasks.
- [x] 2.3 Extend the canonical skill with Pi-owned diff review and local commits, dependency-order integration, single-writer authoritative task markers, mechanical conflict handoff, full integrated project gates, and explicit prohibition on Pi implementation edits and AGY commits or nested delegation; verify dry-run integration cases never share a writer worktree or mark unintegrated tasks complete.
- [x] 2.4 Complete the canonical skill with fresh read-only AGY verification cycles, Pi acceptance gates, separately prompted AGY sync and archive stages, progress-aware remediation, crash and timeout recovery, protected-decision stops, success-only non-force cleanup, failure preservation, and auditable success and blocked reports; verify dry-run failure cases forbid sync or archive until every blocking gate passes.

## 3. Pi Installation and Shared Policy

- [x] 3.1 Install an exact copy of the canonical skill at `.pi/skills/pi-openspec-agy-delivery/SKILL.md` without adding it to `.agents/skills/` or changing `openspec-agy-delivery`; verify both files have identical hashes and `npx skills list -a pi --json` reports the Pi skill.
- [x] 3.2 Update root `AGENTS.md` with the Pi-owned planning/delivery boundary, one-writer-per-worktree parallel policy, Pi acceptance ownership, AGY atomic-workflow ownership, local-only integration commits, and failure-preservation rules while retaining the existing OMP-only contract; verify repository search clearly distinguishes both delivery skills and contains no instruction for AGY to invoke either orchestration skill.
- [x] 3.3 Update `README.md` with Pi-specific installation and the separate `/opsx-explore` or `/opsx-propose` followed by explicit `pi-openspec-agy-delivery` invocation, concurrency override examples, final integration-branch behavior, and no-push boundary; verify the documentation does not advertise automatic apply after planning or overwrite the OMP usage sequence.

## 4. Behavioral Evaluation

- [x] 4.1 Run every evaluation as with-skill and no-skill baseline pairs in the same batch, save outputs, metadata, and timing under `skills/pi-openspec-agy-delivery-workspace/iteration-1/`, and verify every run directory contains the expected artifacts.
- [x] 4.2 Grade each run against objective assertions, run `python -m scripts.aggregate_benchmark` from the skill-creator context, and verify `benchmark.json` and `benchmark.md` report per-case and aggregate pass rates for the exact skill revision.
- [x] 4.3 Generate the standard skill-creator review surface with `.agents/skills/skill-creator/eval-viewer/generate_review.py`, review trigger false positives and workflow omissions, and update the canonical and Pi-installed copies together if findings require correction; verify the final copies remain byte-identical after any revision.
- [ ] 4.4 Exercise the bounded fixture-repository scenario without remote operations: verify independent task lanes run concurrently in separate worktrees, dependent work waits for its predecessor, Pi integrates accepted local commits, a fresh read-only AGY performs verification, AGY performs separately gated sync and archive, and only workflow-created successful resources are cleaned.

## 5. Failure and Recovery Validation

- [ ] 5.1 Exercise a lane review failure and verify Pi sends exact delta findings to the same AGY conversation, reruns targeted checks, and refuses integration until the lane passes.
- [ ] 5.2 Exercise an integrated verification failure and verify the responsible AGY worker remediates it, every implementation change receives a new read-only verifier conversation, and sync remains blocked until both AGY verification and Pi project gates pass.
- [ ] 5.3 Exercise two consecutive no-progress rounds, a protected decision, and a worker timeout with partial edits; verify automatic retries stop at the specified boundaries and all panes, conversations, branches, worktrees, commits, untracked files, and failure evidence remain available.
- [ ] 5.4 Exercise sync divergence, archive failure, and cleanup refusal; verify archive is withheld after sync mismatch, final audit detects incomplete archive state, and cleanup never uses force or removes a dirty resource.

## 6. Final Verification

- [ ] 6.1 Run structural validation on both skill copies, validate the evaluation JSON, confirm `agy models` contains `gemini-3.8-flash-high`, and verify the documented Herdr AGY startup arguments without starting an unapproved delivery.
- [ ] 6.2 Review the complete change against every requirement in `specs/pi-openspec-agy-delivery/spec.md`, inspect for weakened tests, recursive orchestration, shared-writer paths, unsafe git commands, permission bypass, automatic push or model escalation, and resolve every blocking finding.
- [ ] 6.3 Verify the existing canonical and installed `openspec-agy-delivery` files remain unchanged, the new canonical and Pi copies are byte-identical, tracked evaluations are present despite the general eval ignore rule, and no scheduler helper or runtime dependency was added.
- [ ] 6.4 Run `openspec validate add-pi-openspec-agy-delivery --type change --strict --no-interactive` and verify the change is valid and all implementation tasks remain unchecked until the separately authorized delivery phase.
