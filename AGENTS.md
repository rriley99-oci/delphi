# Delphi Agent Guide

This repository includes a project-local Codex playbook under `.codex/`.

When working in this repo:

1. Read `.codex/rules/` before making substantial changes.
2. Reuse `.codex/skills/` workflows when the task matches them.
3. Keep implementation aligned with [docs/product-spec.md](/Users/rriley/Documents/Data Quality/delphi/docs/product-spec.md) and [docs/architecture.md](/Users/rriley/Documents/Data Quality/delphi/docs/architecture.md).
4. Prefer small, vertical slices that keep docs, API, and UI behavior coherent.
5. Treat `.codex/` as an evolving project playbook and maintain it when repeated work reveals a real gap.

## Project Priorities

- Internal platform quality over demo theatrics
- Operational density over decorative UI
- PostgreSQL-first implementation
- FastAPI backend
- Versioned contracts, evaluation history, and violation lifecycle as first-class concepts
- Natural language answers grounded in Delphi metadata only

## Playbook Maintenance

The repository playbook under `.codex/` should evolve with the project.

Update `.codex/` when:

- the same instruction or correction is repeated across multiple tasks
- a bug or avoidable rework reveals missing guidance
- a new tool, framework, or workflow becomes part of the stack
- a recurring manual process should become a reusable skill
- an existing rule or skill is stale, unclear, or contradicted by how the project actually works

Safe default:

- Codex may make small, additive improvements to `.codex/` when they are clearly justified by the task at hand.

Use extra care:

- For broad rewrites, deletions, or policy changes with non-obvious consequences, pause and confirm with the user before changing the playbook.

When updating `.codex/`:

1. keep the change tightly scoped
2. update `.codex/playbook-log.md`
3. mention the playbook change and reason in the final summary

If a task reveals a likely improvement but the current turn is not the right moment to edit `.codex/`, note the suggested follow-up explicitly.
