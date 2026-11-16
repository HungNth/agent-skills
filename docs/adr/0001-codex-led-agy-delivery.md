# Codex-led AGY delivery

Approved specifications and their ticket dependency graphs live only as local Markdown tracker files. Codex leads delivery through Herdr Core, directly reviews and accepts changes, and delegates product-code edits to a fresh AGY implementation agent for each ticket using `gemini-4-hydrogen-high`; tickets run sequentially in one feature-level delivery worktree so dependencies accumulate without parallel branches or duplicate planning artifacts.

## Consequences

Codex commits each accepted ticket with its canonical local ticket reference, leaving the approved planning files immutable. Push, merge, worktree removal, and changes to an approved plan require separate user direction.
