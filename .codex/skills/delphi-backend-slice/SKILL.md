---
name: delphi-backend-slice
description: Implement or extend a Delphi backend feature in FastAPI. Use when working on datasets, contracts, evaluations, violations, or natural-language query APIs and you need a repeatable workflow that keeps models, schemas, services, routes, and tests aligned with the Delphi product spec and architecture.
---

# Delphi Backend Slice

Use this workflow when building a meaningful backend increment.

## 1. Re-anchor in the product shape

Before editing code, read:

- `docs/product-spec.md`
- `docs/architecture.md`
- `.codex/rules/backend.md`
- `.codex/rules/verification.md`

Confirm which domain slice you are changing:

- datasets
- contracts
- evaluations
- violations
- NL query

## 2. Build vertically

Prefer a narrow vertical slice over broad scaffolding.

Typical order:

1. domain model or persistence model
2. request and response schemas
3. service logic
4. route wiring
5. targeted tests

Keep each layer small and readable.

## 3. Preserve Delphi semantics

Honor these domain rules:

- version contracts only when SLA or rule logic changes
- preserve evaluation history
- keep one open violation per failing rule until resolved
- normalize all rule outcomes into pass/fail plus evidence
- keep NL outputs grounded in operational metadata

## 4. Prefer explicit data shapes

- Use explicit schema fields for audit-sensitive state.
- Keep timestamps, reasons, severity, and status first-class.
- Avoid hiding business meaning inside unstructured blobs unless the field is truly flexible.

## 5. Verify the risky parts

Tests should center on behavior that can quietly drift:

- contract version creation conditions
- repeated failure updating an existing open violation
- rule result normalization
- evidence included in API responses

If the backend is still mostly scaffold, add the smallest test coverage that proves the domain behavior.
