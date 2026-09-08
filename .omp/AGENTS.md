## Agent Development Workflow

This project uses Matt Pocock Skills for planning and delivery.

### Roles

- **OMP** is the planner, architect, conductor, and acceptance authority.
- **AGY + Gemini** is the implementation worker.
- **Herdr** manages panes and agent lifecycle.
- **Git** stores accepted implementation checkpoints.
- **GitHub/GitLab issues or local tickets** store ticket scope and dependencies.

OMP must not implement product code while `ship-with-agy` is managing delivery.

### Planning Workflow

For non-trivial feature work:

```text
grill-with-docs
→ to-spec
→ to-tickets
→ user approval
→ ship-with-agy
```

Use `grill-me` instead of `grill-with-docs` only when persistent domain documentation is not desired.

Keep requirement discovery, specification, and ticket decomposition in the primary OMP context.

### Ticket Design

Tickets should be self-contained vertical slices and include, where applicable:

- required behavior;
- acceptance criteria;
- testing seam;
- demo path;
- dependencies/blockers;
- parent specification.

Do not turn tickets into implementation scripts with unnecessary file paths or line numbers.

### Delivery

After tickets are approved, OMP acts as conductor.

For each ticket:

1. Determine the current unblocked ticket frontier.
2. Select one ticket.
3. Start a **fresh AGY implementer** through Herdr.
4. Give AGY the ticket, parent spec, project guidance, and acceptance requirements.
5. AGY implements only that ticket and performs focused self-verification.
6. AGY must not commit, close tickets, change requirements, expand scope, or start another ticket.
7. Freeze the resulting working-tree candidate.
8. Run declared deterministic project verification.
9. Start a **fresh AGY verifier** in read-only/plan mode.
10. Accept the ticket only when verification passes and the candidate remained unchanged.
11. Commit the accepted candidate with the ticket reference.
12. Update/close the ticket.
13. Recompute the frontier and continue.

Use sequential execution by default. Never allow concurrent writers in the same checkout.

### Fresh Context Rule

Use one fresh AGY implementation context per ticket.

Reuse an implementer only for remediation of the **same ticket**.

Never reuse an implementation context for a different ticket.

### Verification

Never treat an implementer success report as completion evidence.

Verification consists of:

- deterministic tests/build/lint/typecheck commands defined by project guidance, ticket, or spec;
- independent review by a fresh AGY verifier;
- scope and spec compliance;
- test integrity;
- ticket demo path where applicable.

OMP may execute declared deterministic verification commands and collect evidence, but must not invent replacement checks or perform substantive code review itself.

### Failure Handling

Classify failures before remediation:

- **Implementation defect** → return exact findings to the same AGY implementer.
- **Spec or requirement gap** → stop and return to OMP/user.
- **Environment blocker** → stop for environment/user intervention.
- **Protected decision** → stop for user approval.
- **Candidate changed during verification** → invalidate the verdict and verify again.

Use bounded remediation. Do not loop indefinitely when the same blocker repeats without measurable progress.

### Git and Ticket State

Commit only after independent verification passes.

Every ticket commit must contain a durable ticket reference, for example:

```text
Ticket: #123
```

For local Markdown tickets, use Git history as the completion ledger rather than creating separate progress or state files.

Do not stash, reset, clean, or discard unrelated user work automatically.

### Final Closeout

After all tickets are complete:

1. Run full project verification.
2. Start a fresh final AGY verifier.
3. Review the complete feature against the parent specification.
4. Remediate mapped implementation defects through the appropriate ticket.
5. Treat requirement or design gaps as planning decisions, not implementation fixes.

### Core Rules

- OMP plans and orchestrates; AGY implements.
- One ticket equals one fresh AGY implementation context.
- Reuse workers only for remediation of the same ticket.
- Never trust worker completion claims without independent evidence.
- Never commit an unverified candidate.
- Never advance past a ticket without a durable accepted checkpoint.
- Never allow multiple writers in the same checkout.
- Do not create a second planning or workflow-state system around Matt Pocock tickets.
