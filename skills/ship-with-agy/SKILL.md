---
name: ship-with-agy
description: "Orchestrate an approved Matt Pocock to-tickets delivery from OMP through Herdr and AGY. Use after /to-tickets when the current agent is OMP and the user asks to implement, ship, execute, continue, or finish the approved ticket set with AGY. Compute the unblocked frontier, run one ticket at a time in a fresh AGY context, independently verify each candidate, commit accepted tickets, update tracker state, and repeat. Never use during grilling/spec/ticket authoring, inside AGY, without a resolvable approved ticket set, or when the user wants OMP to edit product code directly."
---

# Ship With AGY

Orchestrate Matt-style tracer-bullet tickets through Herdr. Keep OMP as conductor and acceptance authority; keep AGY as the only product-code writer. Serialize delivery in one checkout: one fresh implementer per ticket, one fresh verifier per verification round, one accepted commit per ticket.

This skill intentionally replaces the closeout portion of Matt's `implement` workflow. The AGY implementer follows the same ticket-first/TDD/self-verification discipline but does **not** self-review or commit. A fresh AGY verifier performs independent review, then OMP creates the accepted commit and advances the ticket graph.

Read these references when entering the corresponding phase:

- [references/gates.md](references/gates.md) — frontier resolution, worktree attribution, candidate immutability, acceptance, tracker completion, and failure classification.
- [references/prompts.md](references/prompts.md) — exact implementer, verifier, remediation, continuation, and final-closeout prompt contracts.

## Non-negotiable roles

**OMP may:**
- inspect repository guidance, tracker artifacts, diffs, Git state, and worker evidence;
- operate Herdr and AGY lifecycle commands;
- compute the ticket frontier and choose the next ticket;
- execute deterministic verification commands that are explicitly established by the ticket, parent spec, `AGENTS.md`, or repository manifests/docs, recording exact exit/output evidence;
- decide PASS/FAIL/BLOCKED from explicit evidence;
- stage only the accepted ticket candidate, create its local commit, and update/close that ticket in the configured tracker.

**OMP must not:**
- edit product/source/test files or write implementation fixes;
- perform substantive code review itself;
- invent requirements, testing seams, smoke scenarios, verification commands, or architecture;
- push, merge, rebase, deploy, publish, bypass permissions, change credentials, or expand scope without explicit user authorization.

**AGY implementer:**
- owns exactly one ticket and may edit code/tests for that ticket;
- uses TDD at the agreed seams where applicable;
- runs focused checks while working and the repository's required final checks before reporting;
- never commits, never changes ticket/spec artifacts, never delegates, and never starts another ticket.

**AGY verifier:**
- is fresh for every verification round;
- reviews the exact uncommitted candidate from the ticket base against Standards + Spec/Ticket requirements;
- may inspect and exercise declared smoke/demo behavior but never edits, stages, commits, or fixes;
- receives no implementer success claims or prior verifier verdicts.

Run no parallel writers. Even when the frontier contains multiple tickets, process one ticket at a time in v1.

## 1. Confirm the conductor preflight

Before any Herdr mutation:

1. Confirm `HERDR_ENV=1`.
2. Confirm the current recognized agent is OMP using Herdr runtime metadata, not self-assertion. Inspect the current pane and `herdr agent get <current-pane-or-agent>`; fail closed if kind/identity cannot be proven.
3. Confirm planning is complete. `grill-with-docs`/`grill-me`, `to-spec`, and `to-tickets` must already have finished and the ticket breakdown must be approved.
4. Confirm the request is to ship/implement/continue the ticket set, not author or revise planning artifacts.
5. Confirm `docs/agents/issue-tracker.md` exists. If Matt's tracker setup is missing, stop and direct the user to `setup-matt-pocock-skills` rather than guessing a tracker.

If any check fails, do not split panes or prompt AGY. State the failed gate.

## 2. Learn the installed interfaces

The installed CLIs are authoritative. Run relevant help before mutating anything; do not rely on remembered Herdr syntax or version-specific exit-code quirks.

At minimum inspect:

```text
herdr --version
herdr pane current --help
herdr pane layout --help
herdr pane split --help
herdr pane close --help
herdr agent list --help
herdr agent get --help
herdr agent start --help
herdr agent prompt --help
herdr agent read --help
herdr agent wait --help
agy help
```

Verify Git is available. If the user explicitly requested AGY model/effort overrides, validate the model with `agy models` and the effort values against `agy help`. Pass no model/effort override when the user did not request one. Never silently fall back or escalate.

Use `--mode accept-edits` for ticket implementers and `--mode plan` for verifiers. These mode choices do not authorize shell permission bypasses. Never use `--dangerously-skip-permissions`.

## 3. Resolve the approved ticket set

Read repository guidance first: root `AGENTS.md`/`CLAUDE.md`, `docs/agents/issue-tracker.md`, relevant `docs/agents/domain.md`, package/build manifests, and the parent spec/tickets.

Resolve tickets from the strongest available source, in order:

1. explicit ticket/spec references supplied by the user;
2. ticket references produced by the immediately preceding approved `to-tickets` run in this OMP context;
3. the configured tracker's parent/child or spec references.

Do not fuzzy-match a bare issue number when multiple trackers/repos could satisfy it. Canonicalize every ticket reference and confirm its title before delegation.

Build the dependency graph from explicit `Blocked by` edges. Prefer native tracker relationships when reliably readable, but also inspect the ticket body fallback because tracker publishing may not expose native edges consistently. An ambiguous or missing edge that changes execution order is a planning gap: stop rather than guess.

For local Markdown tracker tickets, use the configured `.scratch/<feature>/issues/` ticket set and blockers-first ordering. Treat those ticket/spec files as immutable planning artifacts.

Follow [references/gates.md](references/gates.md) for frontier and completion rules.

## 4. Protect existing work

Resolve `git rev-parse --show-toplevel` once and use the absolute root for every cwd-sensitive operation.

For a fresh delivery, require a clean implementation tree. The only allowable pre-existing changes are immutable local tracker/spec artifacts that belong to this exact approved ticket set. If any other staged, unstaged, or untracked path exists, stop and list it. Never stash, reset, clean, checkout, or switch branches.

For `continue`, accept a dirty implementation tree only when it is confidently attributable to exactly one unfinished ticket. Prove attribution from the live Herdr agent/transcript, ticket scope, and diff. If attribution is ambiguous, stop.

Record the delivery base commit before the first ticket. Do not create a second plan, tasks file, progress file, or orchestration state file.

## 5. Select one frontier ticket

Recompute the frontier before every ticket. A ticket is runnable only when every blocker is accepted/completed.

If several tickets are runnable, choose deterministically: preserve the order approved by `to-tickets` (blockers-first); otherwise use the configured tracker's stable ordering. Do not parallelize.

Record the current `HEAD` as this ticket's fixed base. Confirm the implementation tree contains no changes from another ticket before starting a fresh implementer.

## 6. Start one fresh AGY implementer

Inspect the current Herdr layout. Split one sibling shell pane in the current tab using an available direction that preserves usable pane dimensions, with cwd set to the Git root and without stealing focus.

Derive a unique name such as `agy-i-<ticket>` that satisfies Herdr's live-agent naming constraints. Start a **fresh** AGY conversation in that pane:

```text
herdr agent start <implementer> --kind agy --pane <pane-id> -- --mode accept-edits [validated-user-overrides]
```

Never pass continuation flags for a new ticket. Never reuse an implementer from another ticket.

If startup is blocked or not ready, inspect `agent get` + `agent read`. Never auto-answer approvals/questions or send blind `y`/Enter. Ask the user when an approval decision is required.

Send the implementation brief from [references/prompts.md](references/prompts.md) once with `herdr agent prompt ... --wait`. If Herdr reports a stall/timeout/unknown state, do not resend blindly; inspect pane/agent state and transcript first.

## 7. Settle the implementation candidate

Require the implementer to reach a settled state and read its transcript/report. Treat its success claim as evidence to inspect, never as acceptance.

If it reports a requirement/design ambiguity, protected decision, or environment blocker, stop before verification and classify it using [references/gates.md](references/gates.md). Do not let the worker guess.

Before independent review, record the candidate fingerprint from [references/gates.md](references/gates.md). The implementer must remain idle while verification runs.

## 8. Run deterministic checks as evidence collection

Execute only deterministic commands already established by the approved ticket/spec or repository guidance/manifests. Run them from the exact documented cwd and record command, cwd, exit code, and salient output.

Do not invent a substitute command when the required check cannot run. Mark it BLOCKED. Never change requirements merely to make a check pass.

These commands are evidence collection, not OMP code review. OMP must not diagnose/fix failures itself.

## 9. Start a fresh independent AGY verifier

Create a **new sibling pane** and a **fresh** AGY conversation for every round:

```text
herdr agent start <verifier> --kind agy --pane <pane-id> -- --mode plan [validated-user-overrides]
```

Never reuse a verifier conversation or pane for a later round. Do not send implementer transcripts, self-justifications, or prior verifier verdicts.

Send the neutral verifier brief from [references/prompts.md](references/prompts.md). It must review staged, unstaged, and untracked candidate changes against the ticket base, inspect existing-test integrity, check scope, and evaluate both Standards and Spec/Ticket requirements. It may execute only the declared demo/smoke behavior that can be exercised without modifying tracked project files; otherwise report BLOCKED for that observation.

After the verifier settles, read its actual evidence and verdict. Recompute the candidate fingerprint. If the candidate changed while being reviewed, invalidate the entire round regardless of verdict.

## 10. Decide acceptance or remediation

Accept a ticket only when all gates in [references/gates.md](references/gates.md) pass, including:

- candidate unchanged during independent verification;
- complete ticket behavior with no scope creep;
- existing-test integrity preserved;
- every required deterministic check PASS;
- required demo/smoke observation PASS when one is specified;
- fresh verifier verdict PASS with zero blocking findings.

For implementation defects, send an exact delta prompt to the **same implementer** for this ticket. Allow at most three remediation prompts after the initial implementation prompt. Stop earlier when the same blocker repeats without measurable progress. Every remediation must be followed by a **new** verifier pane/conversation and a new candidate fingerprint.

For spec/ticket gaps, environmental blockers, or protected decisions, stop and return control to the user. Do not route them to the implementer as coding fixes.

## 11. Commit the accepted ticket

After PASS, OMP may perform the administrative commit. This is the fixed point that makes the next ticket a fresh-context unit.

1. Confirm the candidate fingerprint still matches the accepted candidate.
2. Stage only paths attributable to this ticket. Never stage local planning artifacts unless the ticket explicitly changes them as product work.
3. Inspect the staged diff and ensure it matches the accepted candidate exactly.
4. Commit once using repository commit conventions. Include the canonical ticket reference in the commit message/body so local-tracker completion can be reconstructed from Git history.
5. Record the commit SHA.

If the user explicitly prohibited commits, stop after the first accepted ticket rather than accumulating multiple ticket diffs. Explain that advancing without a fixed-point commit breaks per-ticket isolation.

Do not push, merge, rebase, tag, deploy, or publish.

## 12. Mark the ticket complete and advance

After the commit exists:

- For GitHub/GitLab or another real tracker, use `docs/agents/issue-tracker.md` and the installed tracker CLI/API to attach the accepted commit/evidence and mark only this ticket complete. Do not close the parent spec automatically.
- For local Markdown tracker, keep planning files immutable. Treat the canonical `Ticket: <ref>` commit marker as the durable completion ledger.

Close only the implementer/verifier panes created for the accepted ticket, then recompute the frontier and repeat from step 5.

On any failure or user-intervention stop, preserve the working tree and workflow-created panes for inspection.

## 13. Final feature closeout

When every ticket is accepted/completed:

1. Ensure the implementation tree is clean except immutable local tracker artifacts.
2. Run the repository's authoritative full verification commands once more from a clean committed state.
3. Start one fresh AGY verifier in `--mode plan` and use the final-closeout brief from [references/prompts.md](references/prompts.md) to review the complete `delivery-base..HEAD` change against the parent spec.
4. Require PASS with no blocking integration/spec findings.

If final closeout finds a narrow implementation defect attributable to one delivered ticket, reopen that ticket (real tracker) or identify it by canonical ref (local), start a **fresh** implementer for a follow-up remediation, independently verify, commit the follow-up against the same ticket, then re-run final closeout. Allow at most two final-closeout remediation cycles. Cross-ticket design gaps, scope changes, and requirement ambiguities stop for user decision.

Never merge/push/close the parent spec automatically unless the user separately requests it.

## 14. Report

On success report:

- parent spec/ticket set;
- accepted tickets in execution order;
- commit SHA per ticket;
- remediation counts;
- deterministic verification evidence summary;
- final independent closeout verdict;
- tracker completion state;
- confirmation that no push/merge/deploy occurred.

On stop/failure report the exact gate, ticket, verifier finding or command evidence, preserved pane/working-tree state, and one concrete user decision/action needed next.
