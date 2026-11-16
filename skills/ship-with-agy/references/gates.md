# Delivery gates

## Candidate and evidence

Freeze the worker before review. Capture these exact values in Codex context:

1. git rev-parse HEAD
2. git status --porcelain=v1 --untracked-files=all
3. git diff --no-ext-diff --binary
4. git diff --cached --no-ext-diff --binary
5. git ls-files --others --exclude-standard, then git hash-object -- <path>
   for every returned path individually.

Repeat after verification and before staging. Compare exact content, including
all untracked hashes. Any difference invalidates the round. Ignored build files
are not deliverables unless repository guidance explicitly says otherwise.

For each check record command, cwd, exit code, salient output and its source
(ticket, spec, guidance or manifest). A missing tool or skipped required
observation is BLOCKED. A worker's claim never substitutes for this evidence.

## Local ticket identity

Read the configured tracker and approved set. Each ticket has one canonical
repository-relative path, exact title, parent, approved order and explicit
blocker refs. Resolve numeric blockers only inside that feature's approved set.
Reject missing refs, cycles and ambiguous edges before delegating.

A ticket is accepted only when Git history on the delivery branch after Delivery
Base contains a commit with the exact standalone trailer Ticket: <canonical-ref>.
Use git log <base>..HEAD --format=%B to inspect exact lines, not substring matches,
working-tree checkboxes, status labels or commits on another branch.
Require every blocker to have such a marker. Use the recorded Delivery-Base
trailer to reconstruct the original base across sessions; see recovery for
validation and pre-first-commit fallback.

## Ticket Frontier

Before dispatch validate the entire graph: unique canonical refs, one approved
parent, every blocker inside the set, no cycles, and approved stable ordering.
The frontier contains pending tickets whose blockers all have exact accepted
markers. Choose the first by approved order (local number order when approved).
Recompute after each commit and worker cleanup; never trust a cached frontier.

An Implements-Ticket trailer records implementation only, not acceptance, so
it cannot unblock a ticket in normal delivery. An explicit user-authorized
bootstrap that defers live observations must be reported separately and must
not be reconstructed as a normally accepted delivery.

## Acceptance

All acceptance clauses, declared demo/smoke and deterministic checks must PASS.
Codex must find zero blocking Standards or Spec/Ticket findings, preserve test
integrity, and prove scope attribution and candidate stability. Never accept
by confidence or majority vote.
