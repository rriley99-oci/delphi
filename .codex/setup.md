# Codex Setup Guide

This guide describes how to set up a project-local Codex playbook like the one used in Delphi.

Use it when bootstrapping a new repository so Codex has:

- a repo-scoped `AGENTS.md`
- a local `.codex/` playbook
- project rules
- stack rules
- reusable skills
- lightweight planning templates
- a maintenance loop so the playbook can evolve over time

This document is written so Codex can follow it directly.

## Goal

Set up a new repo with a focused, maintainable Codex operating system that matches the real stack and workflows of the project.

## Setup principles

- Keep the playbook small, opinionated, and useful.
- Prefer a map over a giant manual.
- Split guidance into product rules, stack rules, skills, and plans.
- Make the playbook evolve with real work rather than speculative process.
- Ask the user only when the answer cannot be safely inferred.

## Step 1: Inspect the repo

Before creating any files:

1. inspect the repo layout
2. inspect existing docs
3. inspect current tech stack signals
4. inspect any existing `AGENTS.md`, `.codex/`, `.claude/`, or similar project guidance

Look for:

- backend language and framework
- frontend language and framework
- database choice
- deployment model
- CI system
- naming conventions
- domain docs
- existing contribution or workflow docs

## Step 2: Infer what you can

Infer the stack and repo posture from evidence when possible.

Examples:

- `pyproject.toml`, `requirements.txt`, or `app/` suggest Python
- `fastapi` imports suggest FastAPI
- `package.json`, `tsconfig.json`, or `src/` suggest TypeScript/React
- `Dockerfile` or `docker-compose.yml` suggest Docker usage
- `k8s/`, `helm/`, or manifest files suggest Kubernetes
- `.github/workflows/` suggests GitHub Actions
- schema or migration folders suggest SQL and migration tooling

Do not ask questions whose answers are already visible from the repo.

## Step 3: Ask only for missing or strategic inputs

If the repo does not make these clear, ask concise questions for:

- product posture: internal tool, external product, demo, library
- primary audiences or users
- preferred backend stack
- preferred frontend stack
- database choice
- deployment target
- CI system
- GitHub project or issue workflow preferences
- whether the playbook should be able to evolve itself

Keep questions short and practical.

## Step 4: Create the top-level repo guidance

Create `AGENTS.md` at repo root.

It should:

- point to `.codex/`
- state the most important repo priorities
- tell Codex to read rules before substantial changes
- tell Codex to reuse skills when appropriate
- link the playbook back to product and architecture docs when they exist
- define whether `.codex/` is static or evolving

Keep this file concise. It is the repo entry point, not the whole policy corpus.

## Step 5: Create the `.codex/` structure

Create:

```text
.codex/
  README.md
  rules/
  skills/
  plans/
```

If the user wants the playbook to evolve, also create:

```text
.codex/playbook-log.md
```

## Step 6: Write `.codex/README.md`

This file should:

- explain the purpose of the local playbook
- describe the structure
- distinguish product rules from stack rules
- list the current skills
- summarize the current project focus

Keep it readable enough that a fresh Codex session can orient itself in under a minute.

## Step 7: Create product rules

Create a minimal first set of project-specific rules based on the product and workflow.

Typical starting set:

- `backend.md`
- `frontend.md`
- `verification.md`

Adjust names if the repo is not an app.

These rules should capture:

- product posture
- domain semantics
- UX or API philosophy
- operational priorities
- verification expectations

Do not fill these with generic best practices that belong in stack rules.

## Step 8: Create stack rules

Create one rule per language, framework, or platform that is actually part of the stack.

Typical examples:

- `python.md`
- `fastapi.md`
- `sql.md`
- `postgres.md`
- `typescript.md`
- `react.md`
- `docker.md`
- `kubernetes.md`
- `alembic.md`
- `github-actions.md`
- `testing.md`

Only create rules for technologies the project is using or very likely to use soon.

Each stack rule should focus on:

- code quality and maintainability
- safety and correctness
- operational discipline
- project-appropriate tradeoffs

Keep rules short enough that they remain actionable.

## Step 9: Create initial skills

Create only the skills that match recurring workflows in the repo.

Good candidates:

- backend feature slice skill
- frontend feature slice skill
- domain-specific modeling skill
- GitHub workflow skill
- playbook maintenance skill

Each skill should:

- have a strong `description` trigger in frontmatter
- be specific about when to use it
- encode a repeatable workflow
- stay focused on one class of work

Do not create many narrow skills before the repo has earned them.

## Step 10: Create planning templates

Create lightweight templates in `.codex/plans/` for work that benefits from structure.

Good starter templates:

- backend slice template
- UI slice template
- infrastructure slice template

Templates should be short and execution-oriented.

## Step 11: Add the maintenance loop

If the user wants an evolving playbook:

1. add maintenance guidance to `AGENTS.md`
2. create `.codex/playbook-log.md`
3. create a maintenance skill such as `maintain-playbook`

The maintenance policy should say:

- when Codex may update `.codex/`
- when Codex should ask first
- that meaningful playbook updates should be logged
- that final summaries should mention playbook changes

## Step 12: Use safe defaults for ambiguity

If the answer is not obvious, use these defaults unless the user says otherwise:

- keep the playbook repo-local
- prefer concise rules
- prefer fewer skills with stronger workflows
- use additive changes instead of broad policy rewrites
- make confirmation mandatory for external side effects like issue or PR creation
- keep testing guidance honest about what was actually run

## Step 13: Ask questions only when necessary

Ask the user instead of guessing when:

- product posture is unclear
- the stack has multiple plausible paths with real consequences
- GitHub workflow or project-assignment conventions matter
- deployment targets are ambiguous
- the user may want to keep the playbook static rather than evolving
- a major existing guidance system should be merged or replaced

## Step 14: Verify the setup

After creating the setup:

1. list the created files
2. verify `AGENTS.md` points to `.codex/`
3. verify `.codex/README.md` reflects the actual rules and skills present
4. verify skills are named consistently
5. verify the playbook log exists if maintenance was enabled

## Step 15: Summarize the result

In the final handoff:

- explain what was created
- note any assumptions that were inferred
- note any unanswered questions or follow-ups
- suggest the next most useful skill or rule only if it clearly follows from the stack

## Reference setup pattern

The Delphi pattern uses:

- `AGENTS.md` as the repo entry point
- `.codex/rules/` for project and stack guardrails
- `.codex/skills/` for repeatable workflows
- `.codex/plans/` for lightweight planning templates
- `.codex/playbook-log.md` for maintenance history

That pattern is a strong default for most application repos.
