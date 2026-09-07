## Context

See proposal.md for motivation. AGENTS.md currently has an OMP-first title, multiple OMP-only sections, and an appended Pi policy. The existing skills at `skills/pi-openspec-agy-delivery/SKILL.md` and `skills/openspec-agy-delivery/SKILL.md` already document the detailed workflows. OpenSpec configuration references root AGENTS.md, so its shared rules must be valid for both orchestrators.

A design note is appropriate because careless consolidation could change authority, commit permission, or failure handling even though this change intends only editorial clarification.

## Goals / Non-Goals

**Goals:** Make shared rules appear once; make runtime-specific ownership unambiguous; retain concise reminders of critical differences while delegating procedural detail to the selected skill.

**Non-Goals:** Normalize the two workflows into one policy, introduce pi-subagents behavior, or alter either skill or existing OpenSpec specification.

## Decisions

### Use three sections and a neutral title

Use `OpenSpec Delivery: Pi + AGY and OMP + AGY` as a neutral heading, followed by Shared rules, Pi + AGY, and OMP + AGY. Keep English to match repository instructions. Target approximately 50–70 lines rather than copying the skills into AGENTS.md.

Shared rules cover OpenSpec as the planning source of truth, no duplicate plan, separate delivery approval, current context discovery, minimal scoped work, test integrity, evidence-based completion, protected decisions, and AGY non-recursion. The orchestrator retains architecture and acceptance responsibility; AGY follows only its assigned atomic workflow.

### Keep workflow differences scoped to their owning orchestrator

The following matrix is the review checklist, not a requirement to duplicate a full table and bullets in AGENTS.md:

| Concern | Pi + AGY | OMP + AGY |
| --- | --- | --- |
| Required skill | pi-openspec-agy-delivery | openspec-agy-delivery |
| Planning | Pi owns explore/propose | OMP owns planning and synthesis |
| Apply | Scoped AGY lanes; Pi does not write implementation | AGY implementation worker |
| Verify | Fresh read-only AGY conversation per cycle; Pi independently reruns gates | OMP runs openspec-verify-change and project gates |
| Sync/archive | AGY, separately authorized after Pi acceptance | OMP |
| Parallelism | Dependency-aware waves, default maximum three; isolated branch/worktree/pane per concurrent writer | One AGY worker by default in safely attributed existing checkout; alternate topology only as authorized |
| Task markers | AGY integration worker after Pi accepts integrated work; lanes report candidate completion | AGY apply worker updates markers |
| Commits | Pi creates local checkpoints and accepted commits; default-branch delivery uses delivery/<change>; no automatic push or default-branch merge | No commit without a separate user request |
| Retry | Continue with measured progress; stop after two consecutive no-progress rounds | At most three failed remediation rounds; stop earlier on repeated stagnation |
| Cleanup | Success-only non-force cleanup; preserve resources on failure and retain integration branch | Preserve failed work; optional worker-pane closure per OMP skill, including termination |

Require each orchestrator to read its named skill before delivery. Do not put either workflow's distinct commit, retry, marker, or cleanup rule into Shared rules. Keep CLI recipes, model arguments, path conventions, prompt templates, and detailed lifecycle steps in the skills rather than reprinting them.

### Preserve OMP support without exporting its worker conventions

Condense OMP-specific discovery and cost guidance: scout for repository exploration, librarian for external research, sonic for mechanical work, and main-agent ownership of architecture and acceptance. Retain the substantial-change reviewer guidance in the OMP section. Do not simply rename OMP to Pi: that would incorrectly impose OMP worker kinds and direct verification/sync/archive ownership on Pi.

### Preserve behavior rather than inventing new specifications

Use skip_specs: true because this change consolidates documentation without altering either delivery contract. Existing main specs and historical artifacts remain untouched. Any discovered conflict requiring a workflow change must be reported rather than silently resolved during this documentation edit.

Rejected alternatives: removing OMP support contradicts the confirmed scope; maintaining two full policy copies perpetuates duplication; replacing all content with two links loses always-visible safety and role boundaries.

## Risks / Trade-offs

- Over-compression can hide stage ownership -> Review the resulting text against every row of the matrix and retain direct skill references.
- Moving a Pi-only restriction into Shared rules can change OMP behavior -> Explicitly check marker, commit, retry, and cleanup wording for cross-workflow leakage.
- Repeated summaries can drift from the skills -> Keep only concise invariants in AGENTS.md and require reading the unchanged detailed skill.
- A hard line limit can encourage dense, unreadable paragraphs -> Treat length as a target; clarity and complete scope take precedence.
