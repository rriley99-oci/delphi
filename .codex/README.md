# Delphi Codex Playbook

This directory is the project-local operating guide for Codex sessions in Delphi.

## Structure

- `rules/`: project conventions and guardrails
- `skills/`: reusable Delphi workflows expressed as Codex skills
- `plans/`: lightweight planning templates for larger work

## Rule Set

The rule library is split into two layers:

- product rules: backend, frontend, verification
- stack rules: python, fastapi, sql, postgres, typescript, react, docker, kubernetes, alembic, github-actions, testing

Use the product rules to stay aligned with Delphi's domain and UX shape. Use the stack rules for language and framework best practices while implementing.

## How to use this

- Start with the rules when opening a fresh task.
- Use the skills when the task matches a recurring workflow.
- Keep the docs in `docs/` as the product and architecture source of truth.

Current skills:

- `delphi-backend-slice`
- `delphi-ui-slice`
- `delphi-contract-rules`
- `delphi-github-workflow`
- `delphi-issue-runner-automation`
- `delphi-maintain-playbook`
- `delphi-work-issue`

## Current focus

Delphi is still early. The most important thing is keeping the emerging implementation aligned with the agreed product shape:

- Postgres as both the first source system and metadata backbone
- FastAPI backend
- UI-authored contracts
- SCD Type 6-style contract history
- rule-driven evaluations
- one open violation per failing rule until resolved
- grounded NL over metadata only
