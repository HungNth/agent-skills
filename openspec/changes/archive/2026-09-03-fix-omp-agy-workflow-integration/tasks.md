## 1. Regression Coverage

- [x] 1.1 Add evaluation cases for OMP-only discovery, AGY recursive-delivery rejection, explicit AGY apply-workflow selection, missing optional skills, and the `gemini-3.8-flash-high --effort high` launch; verify `skills/openspec-agy-delivery/evals/evals.json` parses against the skill-creator schema.

## 2. Shared Workflow Guidance

- [x] 2.1 Move the cross-agent responsibility and delivery policy from `.omp/AGENTS.md` into a root `AGENTS.md`, remove the redundant OMP-specific copy, and verify every project/OpenSpec guidance reference resolves to an existing file.
- [x] 2.2 Update `openspec/config.yaml` to use the existing clean working tree as the default single-worker path, allow worktrees only when explicitly authorized, and express TDD/debugging/review/verification behavior without requiring unavailable Superpowers skills; verify repository search finds no unconditional missing-skill or automatic-worktree requirement.

## 3. Orchestrator and Worker Isolation

- [x] 3.1 Update the canonical `openspec-agy-delivery` skill with an OMP-and-Herdr role preflight that fails closed inside AGY before any pane or worker mutation; verify the AGY-role evaluation directs the worker to `openspec-apply-change` and creates no nested delivery command sequence.
- [x] 3.2 Update the AGY implementation brief to identify the recipient as the implementation worker, require the OpenSpec apply workflow and root `AGENTS.md`, and explicitly prohibit invoking `openspec-agy-delivery`; verify the worker-brief evaluation contains all four constraints.
- [x] 3.3 Keep required delivery prerequisites limited to Herdr, AGY, OpenSpec, git, and AGY authentication while marking other engineering skills optional; verify the missing-optional-skill evaluation still reaches independent OMP verification.

## 4. OMP-Scoped Installation

- [x] 4.1 Install the canonical delivery skill into `.agents/skills/openspec-agy-delivery/` without installing it into Gemini/AGY-specific locations, and verify the installed `SKILL.md` matches the canonical source byte-for-byte.
- [x] 4.2 Start or reload a fresh OMP session and verify `skill://openspec-agy-delivery` resolves there; inspect the AGY implementation environment and verify any discoverable authoring-repository copy fails the role guard rather than orchestrating delivery.
- [x] 4.3 Update the repository installation guidance to use the actual OMP-resolvable project skill location and the separate post-planning delivery invocation; verify the documented sequence contains no unsupported `--agent omp` command and does not instruct AGY to invoke the delivery skill.

## 5. Validation and Evidence

- [x] 5.1 Run skill structural validation in an isolated Python environment containing PyYAML, and verify both the canonical and OMP-installed copies report `Skill is valid!`.
- [x] 5.2 Run the affected delivery evaluations and grading for the exact synchronized skill revision, aggregate the benchmark, and retain the grading and benchmark outputs needed to audit every new expectation.
- [x] 5.3 Run `openspec validate fix-omp-agy-workflow-integration --type change --strict --no-interactive`, confirm `agy models` contains `gemini-3.8-flash-high`, and confirm the installed Herdr/AGY CLIs accept the documented model and effort arguments without starting an implementation delivery.
