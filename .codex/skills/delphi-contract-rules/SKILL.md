---
name: delphi-contract-rules
description: Work on Delphi's data-contract and rule-evaluation domain model. Use when designing or implementing contract versioning, SLA fields, rule definitions, severity handling, freshness logic, row-count rules, custom SQL checks, or violation semantics tied to contract evaluation.
---

# Delphi Contract Rules

Use this skill when the work touches Delphi's core trust model.

## 1. Refresh the domain constraints

Read:

- `docs/product-spec.md`
- `docs/architecture.md`
- `.codex/rules/backend.md`

Key constraints:

- datasets are identified as `database.schema.table`
- contracts are authored in the UI
- contract versions are created only for rule or SLA changes
- rules support severity
- custom SQL is raw SQL with pass/fail normalization
- repeated failures keep a single open violation until resolved

## 2. Model rules deliberately

Supported rule families today:

- freshness
- row count
- custom SQL

Preserve a common outcome shape across all of them:

- pass/fail status
- message
- evidence

Keep room for additional rule types later without forcing them now.

## 3. Be explicit about evidence

Every rule should leave enough evidence to answer:

- what was expected
- what was observed
- why the outcome passed or failed

This matters for both the UI and the NL layer.

## 4. Treat versioning and violations as coupled behavior

When rules change:

- version the contract
- preserve previous rule history
- make it clear which contract version an evaluation used

When rules fail:

- open a violation if one is not already open
- otherwise update the existing open violation
- never silently replace historical evidence

## 5. Keep the first implementation pragmatic

- Optimize first for Postgres-backed execution.
- Keep custom SQL contracts bounded and explainable.
- Avoid building a general-purpose policy engine yet.
