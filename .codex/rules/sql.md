# SQL Rules

## Query design

- Write SQL to be readable first, then optimize with evidence.
- Prefer explicit column lists over `SELECT *` in application queries.
- Use clear aliases and stable naming.
- Keep business meaning visible in the query shape.

## Safety

- Parameterize values instead of interpolating user input into SQL.
- Treat custom SQL execution as a controlled boundary.
- Validate assumptions around table identity and accessible schemas before execution.

## Domain semantics

- Make pass/fail evaluation queries deterministic.
- Keep rule queries explainable enough that an operator can understand why they failed.
- Preserve enough observed data to support evidence in the UI and NL layer.

## Maintainability

- Use CTEs when they improve clarity, not as a reflex.
- Keep each query focused on one job.
- Prefer set-based logic over row-by-row procedural thinking.

## Performance

- Filter early when it reduces scan cost meaningfully.
- Use indexes and query plans to guide optimization, not guesswork.
- Avoid unnecessarily expensive queries in synchronous request paths.
