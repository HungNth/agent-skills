# Issue tracker: Local Markdown

Specs and tickets for this repo live as Markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation tickets are one file each at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order
- Triage state is a `Status:` line near the top of each file, using `docs/agents/triage-labels.md`
- Comments append under a `## Comments` heading

“Publish to the issue tracker” means create the corresponding Markdown file. “Fetch the relevant ticket” means read its full file. Use repository-relative paths as canonical references.

## Delivery completion

An approved spec and its tickets are immutable during delivery. An accepted commit must include `Ticket: <repository-relative-path>` in its message or body; these commit markers are the durable completion ledger.

## Wayfinding operations

For `/wayfinder`, the map is `.scratch/<effort>/map.md` and each child is `.scratch/<effort>/issues/<NN>-<slug>.md`.

- Record `Type:` as `research`, `prototype`, `grilling`, or `task`.
- Record `Status:` as `claimed` or `resolved`.
- Record blockers as `Blocked by: NN, NN`.
- The frontier is the first open, unblocked, unclaimed child by number.
- Claim by setting `Status: claimed`; resolve by adding `## Answer`, setting `Status: resolved`, and linking the result from the map.
