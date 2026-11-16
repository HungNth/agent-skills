# 01: Install the AGY Implementation Agent template safely

**Parent specification:** `../spec.md`

**What to build:** Provide a versioned Herdr template and portable installation experience that lets a user prepare the approved AGY Implementation Agent on Windows, macOS, or Linux without silently overwriting an existing customization.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

## Allowed scope

The Herdr implementer template, its Windows and POSIX installers, and black-box installer contract checks. Do not change delivery orchestration behavior in this ticket.

## Acceptance criteria

- [ ] The installed template launches interactive AGY in edit-accepting mode with `gemini-4-hydrogen-high`.
- [ ] Stable template instructions restrict the Implementation Agent to one assigned ticket, forbid commits and subagents, and require reporting to the explicit parent terminal.
- [ ] PowerShell installation resolves the Windows Herdr template directory and POSIX installation resolves the XDG or default user configuration directory.
- [ ] Both installers create a missing destination and copy the versioned template successfully.
- [ ] Reinstalling identical content succeeds without changing it.
- [ ] Conflicting installed content fails without modification unless the platform's explicit force option is supplied.
- [ ] Forced installation replaces only the named template.
- [ ] Contract checks use temporary configuration directories and do not modify the user's active Herdr templates.
- [ ] The repository's skill validator passes.

## Testing seam

Exercise each installer as a black box against temporary configuration roots. Assert fresh install, idempotent reinstall, conflict refusal, and forced replacement from observable files and exit codes.

## Demo path

Run both installer contract checks, inspect the installed template in each temporary destination, and show that its command pins the approved model and interactive mode.

## Expected deliverables

A versioned `agy-implementer` template, one PowerShell installer, one POSIX shell installer, and executable contract checks or an equivalent repository-native self-check.
