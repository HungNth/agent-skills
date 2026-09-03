## Dry-run workspace and prerequisite decisions

No commands will be executed and no files will be modified in this evaluation.

### 1. Change and planning-root resolution

Before creating an AGY worker, OMP must resolve exactly one approved OpenSpec change.

- If a standalone store is named, first resolve its registered store ID with `openspec store list --json`.
- That `--store <id>` must then be used consistently for status, instructions, validation, verification, remediation, synchronization, and archive.
- If no store is named, use the repository’s active planning root.
- Because this prompt does not name the change, a real delivery could not proceed until the exact change was identified. OMP would list available changes and ask the user to select one rather than guessing.

For the selected change, OMP would obtain:

- schema name
- planning home and absolute change root
- action context
- apply state
- context files
- approved task list
- dynamic apply instructions

Strict OpenSpec validation must pass. The apply-state decision is:

- **`blocked`**: stop before AGY starts and report the missing planning prerequisite.
- **`ready`**: read every returned context file and delegate remaining implementation.
- **`all_done`**: do not start AGY for implementation; proceed directly to independent verification.

A prior planning approval alone would not authorize delivery. The separate delivery request is the implementation authorization.

### 2. Runtime prerequisites

Before delegation, OMP must verify:

1. `HERDR_ENV` equals `1`, proving OMP is running inside Herdr.
2. The required tools are present and responsive:
   - `herdr --help`
   - `agy help`
   - `agy models`
   - `openspec --help`
   - `git --version`
3. AGY is authenticated.
4. Git resolves an absolute repository root.
5. The selected OpenSpec change is strictly valid and has state `ready` or `all_done`.
6. The working tree can be attributed safely.
7. Exact project lint, typecheck, test, build, and behavioral-smoke commands have been discovered from repository instructions, documentation, and manifests.

OMP must not ask AGY to infer or invent project verification commands.

### 3. Working-tree protection decision

The scenario states that the existing repository working tree contains no unrelated changes. Therefore, subject to normal inspection in a real run, the attribution gate passes.

Permitted pre-existing edits would be limited to:

- files under the selected change root on a fresh delivery, or
- implementation edits demonstrably associated with the same change when continuing a partial delivery.

If unrelated or uncertain edits were found, OMP would stop and list them. OMP would not clean, reset, stash, switch branches, overwrite files, or otherwise rearrange the user’s work.

### 4. Workspace topology decision

The worker must operate in the existing repository workspace.

Because the user did **not** request a worktree:

- Do not create a Git worktree.
- Do not create another repository clone.
- Do not create another Herdr workspace or tab.
- Do not switch branches as part of setup.
- Do not choose a different working directory.
- Use the absolute repository root as the worker pane’s `cwd`.

OMP would inspect the current Herdr pane and layout, then create one dedicated pane:

- Split **right** if the current pane is wide.
- Otherwise split **down**.
- Use `--no-focus` so the user’s current pane remains focused.
- Start exactly one AGY agent in that new pane.
- Name it from `agy-<change>`, truncating to Herdr’s limit and adding a short suffix only if needed to avoid a collision.

This produces one AGY worker sharing the repository’s existing working tree. Herdr owns the pane and agent lifecycle; it does not imply an isolated filesystem workspace.

### 5. Worker reuse decision

The preferred setup is one new AGY worker for this delivery.

- Initial implementation goes to that worker.
- Any remediation must continue in the **same AGY conversation**.
- OMP must not launch extra workers for retries or reviews.
- A worker may be reused only if it was created earlier in this same delivery.

### 6. Delegation boundary

The AGY brief must contain the exact change, selected store or “none,” authoritative context files, dynamic apply instructions, remaining tasks, and exact project verification commands.

AGY may:

- implement the approved scope
- update required task-completion markers
- run implementation-time checks
- report blockers and results

AGY may not:

- create another plan
- redesign or broaden the change
- perform unrelated cleanup
- commit
- synchronize specs
- archive
- create another workspace or worker
- decide protected matters

Credentials, destructive operations, permission escalation, deployment, publishing, unresolved requirements, design conflicts, and scope expansion must be escalated to the user.

### 7. Post-worker ownership

Even if AGY reports success, OMP must independently inspect the full working tree and rerun:

- OpenSpec verification for the exact change and store
- canonical lint
- typecheck
- tests
- build
- the smallest real behavioral smoke scenario

OMP also checks for incomplete tasks, weakened tests, skipped assertions, untracked files, and unintended edits. Up to three bounded remediation rounds may be sent to the same worker.

Only after every blocking gate passes may OMP perform recommended spec synchronization and archive the change. No commit is made unless the user separately requests one.