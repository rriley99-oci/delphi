# Alembic Rules

## Migration philosophy

- Treat migrations as part of the product's domain integrity, not boilerplate.
- Every schema change should be intentional, reviewable, and reversible when practical.
- Keep migrations aligned with actual SQLAlchemy model changes.

## Change design

- Prefer small, focused migrations over sweeping catch-all changes.
- Make table creation, constraints, indexes, and backfills explicit.
- Preserve historical and audit-sensitive data during schema evolution.

## Safety

- Avoid destructive migrations unless they are clearly justified and planned.
- Be careful with nullable-to-non-nullable changes, type changes, and uniqueness constraints on live data.
- Consider data backfill strategy before enforcing new constraints.

## Delphi-specific guidance

- Protect contract history, evaluation history, and violation records from accidental overwrite or collapse.
- Model invariants like single active violation behavior with database support where feasible.
- Keep contract versioning fields explicit and migration-safe.

## Operational discipline

- Give migrations clear names tied to the business change.
- Review generated migrations before trusting them.
- Keep upgrade and downgrade paths understandable.
