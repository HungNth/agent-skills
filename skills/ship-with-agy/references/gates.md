# Orchestration Gates

Use these rules whenever `ship-with-agy` computes state or decides acceptance. Fail closed when evidence is ambiguous.

## 1. Canonical ticket graph

Represent every ticket internally as:

```text
ref: canonical tracker ref or absolute/local repo-relative ticket path
title: exact tracker/file title
parent: canonical parent spec ref
blocked_by: zero or more canonical ticket refs
state: pending | active | accepted
order: approved blockers-first order
```

### Completion source

Use exactly one durable completion source per tracker:

- **Real tracker:** ticket is completed only when the configured tracker reports it closed/done. A commit alone does not make a still-open real-tracker ticket completed.
- **Local Markdown:** do not mutate planning files for progress. A ticket is completed when Git history after the delivery base contains an accepted commit with exact body/footer `Ticket: <canonical-ref>`.

### Frontier

A pending ticket is on the frontier iff every ref in `blocked_by` is completed.

Recompute from durable state after every accepted commit/tracker update. Never carry a cached frontier across a ticket boundary.

If blockers are missing/ambiguous or refer outside the approved ticket set in a way that affects ordering, classify `SPEC_GAP` and stop.

## 2. Working-tree attribution

### Fresh delivery

Allow only:

- no implementation changes; and
- immutable planning artifacts belonging to the exact local tracker/spec set, when those artifacts are intentionally uncommitted.

Everything else is unattributed user work and blocks delivery.

### Continuation

A dirty implementation tree may continue only if all changed/staged/untracked implementation paths can be tied to one unfinished ticket by:

- a live Herdr implementer whose name/transcript names the canonical ticket; or
- a prior preserved transcript/report plus ticket scope; or
- an unambiguous diff that matches exactly one ticket's accepted scope.

If more than one ticket could plausibly own the changes, stop.

## 3. Candidate fingerprint

Record the candidate immediately after the implementer settles and before deterministic verification/review:

1. `git rev-parse HEAD`
2. exact `git status --porcelain=v1 --untracked-files=all`
3. exact `git diff --no-ext-diff --binary`
4. exact `git diff --cached --no-ext-diff --binary`
5. for every untracked non-ignored file, record `git hash-object -- <path>` individually

Keep this record in OMP context/evidence only; do not write a progress file.

After each verifier settles and immediately before commit, rerun the same fingerprint. Compare exactly. Any difference means `CANDIDATE_CHANGED`; discard that verifier verdict and investigate attribution before continuing.

Ignored build/test artifacts are outside the fingerprint unless repository guidance explicitly makes them deliverables.

## 4. Deterministic verification evidence

For every required command record:

```text
command: exact command
cwd: absolute or repo-relative cwd
exit_code: integer
result: PASS | FAIL | BLOCKED
salient_output: enough stdout/stderr to prove the result
source: ticket | parent spec | AGENTS.md | repository manifest/docs
```

Use only authoritative commands. Reading a package manifest to select an explicitly defined `test`, `lint`, `typecheck`, or `build` script is allowed. Guessing a command because it is common for the ecosystem is not.

A required command that cannot execute is BLOCKED, never PASS.

## 5. Independent verifier gates

The verifier must inspect the complete candidate from the ticket base, including staged, unstaged, and untracked files.

Require explicit evaluation of:

- **Scope:** no approved behavior omitted; no unrelated refactor/cleanup.
- **Spec/Ticket:** every acceptance clause is satisfied by the candidate/evidence.
- **Standards:** repository guidance and established local patterns are respected.
- **Test integrity:** existing assertions are not weakened; no test is disabled/skipped/deleted to force green unless the ticket explicitly requires that change.
- **Testing seam:** agreed test-first seam is represented where applicable.
- **Demo/smoke:** the ticket's declared demo path is observed when one exists. The verifier must not invent a new acceptance scenario.

Verdict must be exactly PASS, FAIL, or BLOCKED. Any skipped required check forbids PASS.

## 6. Failure classification

Classify every non-PASS before prompting the implementer.

### IMPLEMENTATION_DEFECT

Use only when the approved ticket/spec is decision-complete and the candidate fails to implement it correctly.

Examples:
- failing declared test caused by the candidate;
- missing accepted behavior;
- regression introduced by the candidate;
- scope creep/refactor outside the ticket;
- verifier identifies a concrete code defect under settled requirements.

Action: same ticket, same implementer conversation, exact remediation delta; then fresh verifier.

### SPEC_GAP

Use when implementation requires a product/design/architecture decision not settled by the approved ticket/spec or the blocker graph is ambiguous.

Action: stop. Return to OMP/user planning. Do not let AGY choose.

### ENVIRONMENT_BLOCKED

Use for missing service, credential, network dependency, required tool, unavailable test environment, quota, or permission that prevents required evidence.

Action: stop and request the narrowest user/environment action. Do not downgrade verification.

### PROTECTED_DECISION

Use for credentials, destructive operations, permission bypass, deployment/publishing, model escalation, branch/history rewriting, requirement/design changes, or scope expansion.

Action: stop for explicit user authorization.

### CANDIDATE_CHANGED

Use when the implementation tree changes between candidate fingerprint and verdict/commit.

Action: invalidate the verification round. Identify the writer/source before any further prompt. Never accept the stale verdict.

## 7. Acceptance gate

Accept only if all are true:

- current fingerprint equals independently reviewed fingerprint;
- verifier verdict is PASS;
- zero blocking findings;
- every required deterministic command is PASS;
- declared demo/smoke is PASS when specified;
- test integrity is PASS;
- diff is attributable only to the current ticket;
- no protected decision remains pending.

No majority vote, confidence score, or implementer claim can override a failed gate.

## 8. Commit gate

Before commit:

1. fingerprint still matches;
2. stage only ticket-attributed implementation paths;
3. inspect `git diff --cached` and compare it to accepted candidate content;
4. ensure no unrelated staged paths;
5. create one local commit.

Prefer repository commit conventions. Always include the exact canonical ticket reference in the body/footer:

```text
Ticket: <canonical-ref>
```

When useful include:

```text
Spec: <canonical-parent-spec-ref>
```

Never amend an unrelated user commit. Never push automatically.

## 9. Tracker completion gate

Update tracker only after commit succeeds.

For a real tracker:

1. attach/comment commit SHA and concise verification result when the configured workflow supports it;
2. mark/close exactly the delivered ticket;
3. re-read it and confirm completed state before treating blockers as cleared.

For local Markdown:

- do not edit ticket/spec files merely to mark progress;
- confirm Git history contains the exact `Ticket:` marker after the delivery base.

If tracker update fails after commit, do not implement another ticket until tracker state is repaired; otherwise frontier state is no longer trustworthy.

## 10. Retry bounds

Per ticket:

- initial implementation prompt: 1
- remediation prompts after independent FAIL: maximum 3
- verifier conversations: always fresh; one per candidate round

Final feature closeout:

- maximum 2 follow-up remediation cycles

Stop earlier if the same blocker repeats with no measurable progress.
