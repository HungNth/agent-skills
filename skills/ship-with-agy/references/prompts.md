# Worker briefs

Fill every field with actual values. The parent address is resolved by Codex,
not a shell variable passed verbatim. Read referenced artifacts in full.

## Implementation brief

Give the template this task as the launch message:

    Implement exactly one approved ticket.
    Worktree: <absolute working directory>
    Parent terminal for reporting: <explicit address>
    Ticket: <canonical ref>, <exact title>
    Parent spec: <canonical ref>
    Ticket base: <SHA>
    Read repository guidance, domain docs, spec and ticket in full.
    Allowed scope: <semantic scope and any explicit path restrictions>
    Acceptance: <all acceptance criteria>
    Verification: <exact commands with cwd and declared demo>
    Apply TDD at <approved seams> where applicable; run focused checks regularly.
    Planning artifacts are immutable. Stop for design gaps or human permissions.
    No subagents, other tickets, staging, commits, pushes or merges.
    Report STARTED, BLOCKED, DONE using hc send <parent-address>.
    DONE includes changed paths, criterion coverage, exact check evidence,
    deviations and concerns. Stay idle for Codex review; DONE is not acceptance.

## Same-ticket remediation

Send to the existing owning worker only after classifying an implementation defect:

    Continue SAME ticket <canonical ref>; correction <n> of maximum 3.
    Blocking findings: <file/line, failed criterion, exact check evidence>.
    Fix only these defects under the approved scope; report a requirement gap
    instead of changing requirements. No staging, commits, or other tickets.
    Re-run <affected checks and required ticket checks>.
    Report DONE with the delta, evidence and concerns to <explicit parent>.
    Remain idle for another complete Codex review.

## New worker continuing the same unfinished ticket

Include the normal implementation brief, plus:

    Existing candidate belongs to <canonical ticket> based on <provenance>.
    Read status, staged/unstaged diffs and every untracked file before editing.
    Preserve valid progress and finish only unmet acceptance clauses.
    Ticket base: <original fixed ticket base>; current HEAD: <SHA>.
    Prior remediation prompts used: <proven count>; remaining: <count>.
    Stop if the existing candidate contradicts the approved scope.
