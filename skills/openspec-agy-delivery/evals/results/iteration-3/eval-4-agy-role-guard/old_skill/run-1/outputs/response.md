As the AGY implementation worker, I should **not run the OMP orchestration workflow myself**. OMP owns preflight, Herdr lifecycle, independent verification, remediation decisions, spec synchronization, and archive.

For approved change `add-search`, my next steps would be:

1. **Use OMP’s self-contained implementation brief**, including:
   - Selected OpenSpec store ID, or confirmation that no standalone store is used.
   - Exact repository root and scope.
   - Canonical lint, typecheck, test, build, and smoke commands discovered by OMP.

2. **Resolve the authoritative implementation context**:
   - Run OpenSpec status for exactly `add-search`.
   - Run OpenSpec apply instructions for exactly `add-search`.
   - Include the selected `--store` on both commands if OMP specified one.
   - Read every returned `contextFiles` path.
   - Follow the returned dynamic apply instruction, approved proposal, specs, design, tasks, and action context.

3. **Implement only the approved remaining tasks**:
   - Do not create another plan or redesign the change.
   - Do not broaden scope or perform unrelated cleanup.
   - Update only the task completion markers required by the apply workflow.
   - Preserve unrelated user work.

4. **Run the exact project checks supplied by OMP**:
   - Lint, typecheck, tests, build, and relevant behavioral checks.
   - Fix implementation-related failures within the approved scope.
   - Confirm that working-tree changes are limited to the intended delivery.

5. **Stop rather than guess** if implementation requires:
   - Credentials or permission escalation.
   - Destructive operations.
   - Deployment or publishing.
   - A new requirement or design decision.
   - Scope expansion or resolution of a design conflict.

6. **Return a complete report to OMP** containing:
   - Work completed.
   - Files touched.
   - OpenSpec task progress.
   - Exact commands and observed outcomes.
   - Deviations, blockers, and remaining concerns.

I must **not commit, synchronize specs, archive the change, invoke OMP’s independent `/opsx-verify`, or declare delivery complete**. Those remain OMP’s responsibilities. In this dry run, no commands have been executed and no files have been modified.