# Backend Rules

## Service posture

- Keep the first implementation as a modular monolith inside FastAPI.
- Preserve clear boundaries between datasets, contracts, evaluations, violations, and NL query logic.
- Prefer explicit schemas and typed models over ad hoc dictionaries once an endpoint becomes real.

## Domain fidelity

- Treat contract versioning as a core domain concern, not an afterthought.
- Create new contract versions only for SLA or rule-definition changes.
- Preserve full evaluation history.
- Keep one open violation per failing rule until resolved.
- Keep natural language features grounded to Delphi metadata only.

## Storage and interfaces

- Bias toward PostgreSQL-compatible design decisions.
- Keep repository and service layers clean enough that source adapters can grow later.
- Normalize rule execution results into a common pass/fail shape with evidence.
- Store enough metadata to explain every dashboard status and NL answer.

## API design

- Prefer resource-oriented endpoints.
- Make evaluation triggering API-first so UI buttons and future schedulers use the same path.
- Favor additive contracts in request and response schemas.
- Keep audit-relevant fields explicit: timestamps, version ids, change reasons, severity, status.

## Implementation rhythm

- Build vertical slices that include model, schema, service, and route wiring together.
- Add tests around domain behavior, especially versioning and violation lifecycle.
- Avoid building abstractions for future source systems until Postgres-backed behavior is working.
