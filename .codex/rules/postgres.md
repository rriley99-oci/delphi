# PostgreSQL Rules

## Data modeling

- Design tables and indexes around Delphi's core read paths: current contract lookup, evaluation history, open violations, and dataset health.
- Use primary keys, foreign keys, and constraints to protect invariants.
- Model uniqueness explicitly, especially where one open violation per rule must hold.

## Schema evolution

- Prefer additive schema changes when possible.
- Make nullability, defaults, and backfill expectations explicit in migrations.
- Preserve historical data; do not overwrite audit-relevant records for convenience.

## Query behavior

- Use transactions around multi-step writes that must remain consistent.
- Keep version creation and violation updates transactionally safe.
- Use `RETURNING` where it simplifies write-followed-by-read patterns.

## JSON usage

- Use JSON or JSONB only for genuinely flexible rule configuration or evidence payloads.
- Do not hide core relational fields inside JSON.
- Keep query-critical and audit-critical fields relational.

## Operational discipline

- Be deliberate with indexes on status, severity, dataset id, contract version id, and time-based history fields.
- Measure query plans before adding complexity.
- Keep the first design simple enough to understand under load.
