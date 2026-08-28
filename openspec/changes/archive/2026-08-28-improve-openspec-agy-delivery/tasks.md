## 1. Baseline and Evaluations

- [x] 1.1 Copy the current `openspec-agy-delivery` skill into `skills/openspec-agy-delivery-workspace/skill-snapshot/` before editing and verify the snapshot contains the original `SKILL.md` and shell helper unchanged.
- [x] 1.2 Create `skills/openspec-agy-delivery/evals/evals.json` with native-Windows, standalone-store, and verification-failure cases plus objective expectations, and verify the file parses as valid JSON against `.agents/skills/skill-creator/references/schemas.md`.

## 2. Cross-platform Skill Rewrite

- [x] 2.1 Rewrite `skills/openspec-agy-delivery/SKILL.md` as a self-contained direct orchestration workflow covering approval, store-aware OpenSpec preflight, user-work protection, Herdr worker lifecycle, bounded AGY authority, `/opsx-verify`, fresh project gates, remediation, archive, and result reporting; verify `.agents/skills/skill-creator/scripts/quick_validate.py` reports `Skill is valid!` in a Python environment containing PyYAML.
- [x] 2.2 Remove `skills/openspec-agy-delivery/scripts/openspec-agy-delegate.sh` and its empty directory, then verify repository search finds no skill reference to the removed helper, `jq`, `/opsx:verify`, or hardcoded `openspec/changes/<change>` paths.

## 3. Skill Creator Evaluation

- [x] 3.1 Run every eval as old-skill and revised-skill pairs in one batch, save each run's outputs, metadata, and timing under `skills/openspec-agy-delivery-workspace/iteration-1/`, and verify all six run directories contain their required artifacts.
- [x] 3.2 Grade every run against its objective expectations, run `.agents/skills/skill-creator/scripts/aggregate_benchmark.py`, and verify `benchmark.json` and `benchmark.md` compare the revised skill with the snapshot baseline.
- [x] 3.3 Generate the standard human review surface with `.agents/skills/skill-creator/eval-viewer/generate_review.py` and verify it displays all eval outputs and benchmark results without custom viewer code.
- [x] 3.4 Apply material review findings to the skill, rerun affected old-versus-new evaluations in a new iteration, and verify the final revised skill passes every blocking expectation without regressing previously passing cases.

## 4. Final Verification

- [x] 4.1 Re-run skill validation, validate `evals/evals.json`, and inspect the final skill against every requirement in `specs/openspec-agy-delivery/spec.md`; verify no executable helper or unrequested runtime dependency remains.
- [x] 4.2 Run `openspec validate improve-openspec-agy-delivery --type change --strict --no-interactive` and verify the approved change artifacts remain valid and coherent after implementation.
