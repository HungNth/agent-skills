# Agent Delivery

This context defines the language used to plan and deliver agent-executed changes.

## Language

**Lead Agent**:
The Codex agent that owns orchestration, review, acceptance, and reporting for a delivery.
_Avoid_: Implementer, worker

**Implementation Agent**:
An AGY agent assigned one approved ticket and responsible for changing product code within that ticket's scope.
_Avoid_: Lead agent, reviewer

**Delivery**:
The execution of an approved specification and its ticket dependency graph through accepted changes.
_Avoid_: Planning, feature design

**Delivery Worktree**:
The isolated Git worktree in which one delivery's tickets are implemented and accepted in dependency order.
_Avoid_: Worker worktree, ticket worktree

**Delivery Base**:
The recorded clean commit from which a delivery branch and its worktree are created.
_Avoid_: Latest main, current code

**Ticket Frontier**:
The ordered set of approved tickets whose blockers have all been completed.
_Avoid_: Backlog, queue

**Ticket Acceptance**:
The Lead Agent's evidence-backed decision that an Implementation Agent's candidate satisfies its approved ticket and may be committed.
_Avoid_: Agent completion, done message
