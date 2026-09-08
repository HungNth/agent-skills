# Domain Docs

This repository uses a single-context layout:
`CONTEXT.md` at the root and architectural decisions under `docs/adr/`.

## Before exploration

Read the root `CONTEXT.md` and ADRs relevant to the area being explored.

If these files or directories do not exist, proceed silently.
`/domain-modeling` creates them lazily when terminology or decisions
are resolved; setup does not create placeholder domain documents.

## Vocabulary

Use domain terms as defined in `CONTEXT.md` when writing issues,
proposals, hypotheses, and tests.

If a needed concept is missing, reconsider whether it belongs to the
domain; flag genuine vocabulary gaps for `/domain-modeling`.

## ADR conflicts

Surface any conflict with an existing ADR explicitly. Cite the ADR
and explain why the decision may need reopening.
