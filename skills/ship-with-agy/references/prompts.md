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
