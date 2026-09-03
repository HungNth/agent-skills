For this dry run, no commands would be executed, no panes would be created, and no files would be modified. The required decisions are:

## Prerequisite decisions

1. **Confirm the orchestrator role first**
   - Verify that the current agent is **OMP**, not an AGY worker.
   - Verify `HERDR_ENV=1`.
   - This must happen before any OpenSpec command or Herdr mutation.
   - Given the scenario explicitly identifies me as OMP inside Herdr, the role preflight is conceptually satisfied.

2. **Resolve one approved change**
   - Delivery requires the exact name of one approved OpenSpec change.
   - If a standalone store is named, resolve its registered store ID first and use that ID for all subsequent OpenSpec and worker handoffs.
   - Since this prompt does not name a change, a real run could not proceed beyond preflight without asking for the change name.

3. **Validate OpenSpec readiness**
   For the named change, OMP would separately obtain:
   - change status
   - apply instructions
   - strict validation result
   - schema name
   - planning root and absolute change root
   - action context and context files
   - task state and dynamic apply instruction

   The apply state determines the path:
   - `blocked`: stop before creating an AGY worker.
   - `all_done`: skip AGY implementation and independently verify.
   - `ready`: read every returned context file and delegate implementation.

4. **Confirm required tooling**
   OMP must verify that these are installed and operational:
   - Herdr
   - AGY
   - OpenSpec
   - Git
   - AGY authentication and available models

   Supplemental testing or debugging skills are optional and do not block delivery.

5. **Resolve repository and project checks**
   - Resolve the absolute Git repository root.
   - Discover the repository’s exact lint, typecheck, test, build, and behavioral-smoke commands from `AGENTS.md`, repository documentation, and manifests.
   - AGY must receive these exact commands rather than being asked to infer or guess them.

6. **Protect existing work**
   - Inspect tracked, staged, and untracked changes.
   - The scenario states that there are no unrelated working-tree changes, so the existing tree is safe for the single-worker delivery.
   - OMP must not stash, reset, clean, switch branches, or overwrite user work.

## Workspace decisions

1. **Use the existing repository working tree**
   - The default single-worker topology uses the current repository checkout.
   - No worktree, alternate workspace, tab, or separate checkout should be created.
   - This follows both the clean-attribution result and the fact that the user did not request a worktree.

2. **Create one dedicated Herdr pane**
   - Inspect the current pane geometry and layout.
   - Split a wide pane to the **right**; otherwise split **down**.
   - Set the new pane’s working directory to the resolved absolute repository root.
   - Use `--no-focus` so the user’s current focus is preserved.

3. **Start exactly one AGY worker**
   - Give it a valid, collision-free Herdr name such as `agy-<change>`.
   - Start it in the new pane as an AGY agent.
   - Unless the user selected another supported model, use `gemini-3.8-flash-high` with high reasoning effort.
   - The worker remains in the same repository working tree.

4. **Keep role ownership explicit**
   - The worker must use the workflow named exactly `openspec-apply-change`.
   - `openspec-agy-delivery` remains OMP-owned.
   - AGY implements the approved tasks and updates required completion markers.
   - AGY must not create another plan or worker, redesign the change, commit, synchronize specifications, or archive it.
   - OMP independently reviews the diff, runs `/opsx-verify`, reruns project checks and smoke tests, coordinates up to three remediation rounds in the same worker conversation, and performs synchronization and archive only after all gates pass.

5. **Do not create unnecessary isolation**
   - A separate worktree is not inherently safer here because attribution has already passed and only one worker is involved.
   - Creating one would violate the workflow’s default topology absent an explicit user request or an approved concurrent-worker need.

Thus, the required topology is: **OMP in the current Herdr environment, one no-focus split pane rooted at the existing absolute repository root, and one dedicated AGY worker operating in that same clean working tree**. A real delivery would still require the exact approved change name before proceeding.