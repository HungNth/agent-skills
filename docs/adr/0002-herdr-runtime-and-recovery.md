# Herdr-only delivery runtime

Agent delivery runs only when Herdr Core can prove the current Codex parent identity and launch the versioned `agy-implementer` template; it does not fall back to direct AGY execution. Delivery recovery uses the named feature worktree, Git history, canonical local ticket references, current diff, and any live Herdr transcript rather than a separate orchestration state file, and stops when an unfinished candidate cannot be attributed to one ticket.
