## 1. Consolidate Guidance

- [x] 1.1 Rewrite only root AGENTS.md with a neutral title and Shared rules, Pi + AGY, and OMP + AGY sections; verify shared rules are stated once, both exact delivery skill references resolve, and the file is substantially shorter with an approximate 50–70 line target.

## 2. Verify Workflow Compatibility

- [x] 2.1 Review the revised AGENTS.md against every row of the design ownership matrix and both unchanged delivery skills; verify Pi retains AGY-owned post-planning stages, independent acceptance, isolated dependency-aware parallelism, integrated task markers, local commits, progress-aware retries, and success-only cleanup, while OMP retains AGY apply/markers, OMP verify/sync/archive, single-worker default, separate commit approval, bounded remediation, and its own pane cleanup policy.
- [x] 2.2 Review example Pi delivery, OMP delivery, planning-only, and AGY-worker requests against the guidance; verify each selects the correct responsibility and skill, planning never starts delivery, AGY never orchestrates, and OMP worker conventions do not leak into Pi instructions.
- [x] 2.3 Run `git diff --check` and `openspec validate clarify-dual-agent-workflow-guidance --type change --strict --no-interactive`; inspect the delivery diff against its baseline to verify AGENTS.md is the only implementation file changed and both skills, README.md, OpenSpec configuration, existing specs, and prior archives remain untouched.
