## Context

See `proposal.md` for motivation. The canonical delivery skill lives under `skills/openspec-agy-delivery/`. The installed `skills` CLI has no `omp` agent target, and fresh OMP sessions resolve project skills from the universal `.agents/skills/` location rather than `.omp/skills/`. The AGY process running in the same authoring repository can discover the canonical skill, so runtime role isolation is required. OpenSpec context names root `AGENTS.md`, while the original workflow guidance was under `.omp/AGENTS.md`. Apply guidance also required a worktree and several unavailable Superpowers skills, while the delivery skill intentionally uses the existing clean working tree and declares only Herdr, AGY, OpenSpec, and git as mandatory.

The existing delivery lifecycle, default `gemini-3.8-flash-high` worker, independent OMP verification, bounded remediation, spec synchronization, and archive gates remain valid.

## Goals / Non-Goals

**Goals:**

- Make OMP the only agent allowed to orchestrate delivery.
- Keep one canonical distributable skill while installing it into OMP's agent-specific skill location for execution.
- Make an accidentally exposed delivery skill fail closed inside AGY.
- Give OMP and AGY one shared, concrete source of project guidance.
- Remove contradictory or unavailable apply-time dependencies.
- Leave repeatable evidence for the exact installed skill revision.

**Non-Goals:**

- Introduce a general multi-worker scheduler.
- Add a helper program, package, or service.
- Automatically create worktrees for the normal single-worker path.
- Change OpenSpec artifact formats or make AGY responsible for verification or archive.
- Add automatic model escalation; OMP may still stop and ask after bounded remediation.

## Decisions

### Keep the distributable skill canonical and install it where OMP resolves project skills

`skills/openspec-agy-delivery/SKILL.md` remains the canonical package source. The repository installs an identical copy under `.agents/skills/openspec-agy-delivery/`, the project-level location fresh OMP sessions resolve. The skill is not installed into `.gemini/skills` or other AGY-specific locations.

The `skills` CLI does not support an `omp` agent target, so documentation must not advertise `--agent omp`. The universal `.agents/skills` placement is paired with a runtime role guard because the authoring repository can still expose the canonical `skills/` source to AGY.

Rejected alternatives:

- `.omp/skills` does not resolve through `skill://` in a fresh OMP session.
- Maintaining a separate OMP command that duplicates the workflow would create two delivery policies that can drift.
- Relying only on trigger wording would not fail safely when AGY receives an implementation prompt containing the same delivery terms.

### Fail closed when the current agent is not OMP

The delivery skill begins with an explicit role preflight. It proceeds only from an OMP orchestrator running inside Herdr. If AGY loads it, the skill stops before any pane or agent mutation and directs the worker to `openspec-apply-change` for the named change.

The AGY brief also states that the recipient is the implementation worker, explicitly requires the apply workflow, and explicitly forbids invoking `openspec-agy-delivery`. This provides both preventive prompting and an enforcement guard.

### Use a root `AGENTS.md` for shared workflow policy

The OMP/OpenSpec/AGY responsibility split moves to a root `AGENTS.md`, which is readable through normal repository discovery by every participating agent. `openspec/config.yaml` references that exact path. OMP-only runtime settings remain in `.omp/config.yml`; redundant policy in `.omp/AGENTS.md` is removed rather than maintained as a second source.

The AGY implementation brief names the root guidance file alongside the dynamic OpenSpec `contextFiles`, because the worker starts with a separate conversation and must not depend on OMP's previously loaded context.

### Keep the existing working tree as the single-worker default

The dirty-tree attribution preflight is already the smallest safe isolation mechanism for one OMP orchestrator and one AGY worker sharing a repository. Delivery does not create a worktree automatically. A worktree is allowed only after explicit user authorization or a future approved topology requiring concurrent workers.

The unconditional `using-git-worktrees` apply guidance is removed. This resolves the contradiction without weakening protection of unrelated user work.

### Encode required behavior directly instead of depending on absent Superpowers skills

Herdr, AGY, OpenSpec, git, and AGY authentication remain mandatory. TDD, debugging, code review, and verification behaviors remain explicit in project guidance and the delivery skill, but named Superpowers skills are invoked only when actually installed and resolvable. Missing optional skills do not block delivery.

This avoids adding packages for behavior OMP already enforces through the delivery contract.

### Extend evaluations around ownership and the exact launch revision

The existing native-Windows, store-aware, and failed-verification cases remain. Add cases proving:

- OMP can resolve the installed delivery skill;
- an AGY worker cannot recursively orchestrate delivery even when the source skill is discoverable;
- the implementation brief selects the apply workflow and forbids the delivery workflow;
- the current `gemini-3.8-flash-high --effort high` launch is preserved;
- missing optional Superpowers skills do not block the explicit verification path.

Run structural skill validation and affected evaluations after synchronizing the OMP-installed copy. Keep benchmark or grading outputs long enough to audit the revision being delivered; a completed checkbox alone is not validation evidence.

## Risks / Trade-offs

- The canonical root skill can remain visible to AGY while working inside this skill-authoring repository. The role guard and worker brief make that visibility non-operative; complete invisibility would require moving the distributable source or changing AGY discovery behavior.
- The installed `.agents/skills` copy can drift from the canonical skill. Installation and validation must compare them before delivery use.
- Using the existing working tree favors simplicity over isolation. The strict dirty-tree preflight remains mandatory, and explicit worktrees remain available when isolation is actually needed.
- Root `AGENTS.md` broadens policy visibility beyond OMP. Its content must remain genuinely cross-agent; OMP-specific runtime settings stay under `.omp/`.
- `gemini-3.8-flash-high` remains a speed-oriented implementation default. Correctness continues to depend on OMP's independent verification rather than the worker model's self-report.
