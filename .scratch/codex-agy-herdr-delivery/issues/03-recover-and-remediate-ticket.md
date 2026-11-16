# 03: Recover and remediate an unfinished ticket

**Parent specification:** `../spec.md`

**What to build:** Allow Codex to continue a safely attributable unfinished ticket, return implementation defects to its worker within a bounded loop, and preserve evidence when recovery or remediation cannot proceed safely.

**Blocked by:** 02: Deliver one local ticket through Codex and Herdr.

**Status:** ready-for-agent

## Allowed scope

Same-ticket continuation, candidate provenance, failure classification, remediation, blocked-worker handling, and failure preservation. Do not add parallel workers or multi-ticket closeout behavior.

## Acceptance criteria

- [ ] An existing deterministic branch or Delivery Worktree enters recovery checks instead of being deleted, overwritten, or renamed automatically.
- [ ] Recovery reconstructs state from the worktree, Git history, canonical local ticket references, current diff, and available Herdr terminal evidence without a separate state file.
- [ ] A dirty candidate continues only when it can be attributed to exactly one unfinished ticket.
- [ ] Ambiguous provenance, a specification gap, an environmental blocker, or a protected decision stops with one concrete user action and preserves the worktree and terminals.
- [ ] A candidate changed during review invalidates the review result.
- [ ] An implementation defect is returned with exact evidence to the same Implementation Agent for that ticket.
- [ ] Remediation permits at most three correction prompts after the initial implementation prompt and stops earlier when the same blocker repeats without measurable progress.
- [ ] Codex never auto-answers permission or trust prompts and never forces input into a blocked worker.
- [ ] If a worker exits, a fresh same-ticket worker may continue only when the existing candidate's provenance is clear.
- [ ] Failure paths do not stash, reset, clean, discard, commit, push, or merge unaccepted changes.
- [ ] Repository verification confirms that review commands do not mutate tracked candidate files.

## Testing seam

Exercise recovery and remediation through observable Git and Herdr states: an attributable dirty candidate, an ambiguous dirty candidate, a changed candidate during review, a dead worker, and a repeated implementation blocker.

## Demo path

Interrupt an in-progress disposable delivery, demonstrate safe continuation for the attributable case, then demonstrate fail-closed preservation for an ambiguous candidate and a repeated blocker.

## Expected deliverables

Recovery gates, bounded remediation contracts, failure classification, and evidence-preserving stop reports integrated into the single-ticket workflow.
