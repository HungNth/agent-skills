# Verification

## Deterministic checks

From the repository root:

    python <installed-skill-creator>/scripts/quick_validate.py skills/ship-with-agy
    python -m unittest discover -s skills/ship-with-agy/tests -v
    git diff --check

Tests require PowerShell and a POSIX shell. On Windows set TEST_SH to Git's
usr/bin/sh.exe; test isolation prepends that directory for its standard utilities.
On macOS/Linux install PowerShell if running both platform contracts. An absent
required shell is a blocked contract, not a silently skipped PASS.

## Disposable live smoke

Run only when the user authorizes real AGY execution and AGY is authenticated.
Create a temporary Git repo with a committed local spec/ticket requesting one
harmless text change and its verification command. Keep runtime evidence in
the review context or an external report, not in product/planning files.

Use the actual installed template with hc run --bg, include the brief at launch,
and confirm first_message.sent, model identity, STARTED and DONE. Inspect actual
diffs and run the declared check independently. Fingerprint before/after review.
Commit only the accepted change with the exact Ticket/Spec/Delivery-Base trailers.
Read back the marker and clean up the accepted worker with hc kill then hc rm.
Verify the spec/ticket did not change and the delivery worktree remains clean.

Record BLOCKED if the account/service cannot run the model. Never replace the
real smoke with mocked output or label a local Git replay as a live AGY PASS.

## Recovery observations

In a disposable committed Git fixture, follow the recovery reference for an
attributable dirty ticket; compare its diff and untracked contents before/after
read-only inspection. Add an ambiguously owned candidate and confirm the
decision stops without reset, stash, clean or commit.

Alter one file between two fingerprints and confirm the earlier review is
invalidated. For a dead worker require provenance before preparing a new
continuation brief. Exercise repeated-blocker decisions from a transcript with
three correction prompts; missing retry history must not reset the budget.
These Git/transcript exercises do not prove live Herdr/AGY behavior.
