# Continue and remediate

## Reconstruct before editing

1. Read the canonical local spec and ticket set again. Inspect git worktree list
   --porcelain and the deterministic branch/path. Require the worktree to belong
   to the expected repository and branch; a foreign path or mismatched ref stops
   recovery. Never create another branch/path to hide a conflict.
2. Recover Delivery Base from consistent Delivery-Base trailers in accepted
   ticket commits. Before the first accepted commit, inspect the branch-creation
   reflog for its original base, or the explicit base recorded in this delivery's
   preserved launch/report. Validate the base resolves and is an ancestor of HEAD.
   If sources conflict, or expired reflogs leave no provable base, stop for the
   missing base SHA. Do not guess from today's main or a cached merge-base.
3. Reconstruct accepted tickets from exact Ticket trailers after that base.
   Implements-Ticket and arbitrary mentions do not prove acceptance.
   Validate every intervening commit is attributable to this delivery; unknown
   commits require inspection and user direction before frontier advancement.
4. Inspect all staged, unstaged and untracked changes. Tie every changed path
   to exactly one unfinished ticket using its scope and live worker transcript,
   preserved report, or an unambiguous diff. A plausible guess is insufficient.
   If several tickets could own the diff, preserve everything and request
   attribution. A clean tree still requires validating any unrecorded commits.
5. Inspect hc get and hc read for the owning worker. If its conversation is
   live and matches this ticket, reuse it only for that ticket. If it exited,
   a fresh same-ticket worker may continue with the continuation brief, but
   only after the provenance checks above. Never resurrect by rerunning blindly.

Continue must also pass the normal parent/template/model preflight. There is
no state file, pending-work reset, automatic stash, clean or discarded candidate.

## Classify before sending a correction

| Condition | Action |
| --- | --- |
| IMPLEMENTATION_DEFECT: settled criteria fail due to candidate code | Send exact evidence to the same worker; review the next stable candidate again |
| SPEC_GAP: missing/contradictory requirement, architecture or blocker edge | Stop for a planning decision |
| ENVIRONMENT_BLOCKED: unavailable account/service/tool or required check | Stop with the narrow environment action |
| PROTECTED_DECISION: permission, credentials, destructive action, publishing or scope expansion | Request the user's decision |
| CANDIDATE_CHANGED: fingerprint differs during review | Invalidate review, identify the writer/source, freeze again, then repeat all affected checks |

Read a blocked worker's actual screen before reporting. Never send --force,
permission answers, trust keystrokes or a replacement model to bypass the block.
An unexpected writer or unexplained mutation is an attribution blocker; Codex
does not fix the files while reviewing.

## Bounded corrections

Keep the count and evidence in the active conversation/transcript. Allow at
most three remediation prompts after the initial implementation task. Stop
earlier when the same blocker repeats without measurable progress.
On recovery reconstruct the count from available transcript evidence; if it
cannot be proved, stop for the missing history rather than reset the budget.

Use the [same-ticket remediation brief](prompts.md). Every correction is followed
by a fresh fingerprint, independent Codex review and the required checks.
Only the accepted candidate is committed; failures preserve the worktree and
workflow-created terminals. Report gate, ticket, actual finding/check output,
retry count, preserved state and one concrete action needed from the user.
