# Testing Rules

## Strategy

- Test the system at the level where the risk lives.
- Prefer a layered approach: domain tests, service tests, API tests, and UI tests where appropriate.
- Keep the suite fast enough for regular use and strong enough to catch trust-breaking regressions.

## Backend

- Write unit or service tests for core domain behavior.
- Add API tests for endpoint contracts, validation, and status handling.
- Use realistic fixtures for datasets, contracts, evaluations, and violations.

## Frontend

- Test operator workflows, not just component snapshots.
- Verify state transitions after real actions like triggering evaluations or resolving violations.
- Include empty, loading, and failure states in coverage where they affect decisions.

## Data and domain integrity

- Prioritize tests around contract versioning, rule evaluation, violation lifecycle, and evidence rendering.
- Test repeated-failure behavior and history preservation explicitly.
- Include negative cases where plausible misuse or malformed inputs could silently break trust.

## Maintainability

- Keep tests readable and specific about intent.
- Avoid brittle assertions tied to irrelevant implementation details.
- Prefer a few high-signal tests over a large number of shallow ones.

## CI expectations

- Tests should be runnable in local development and in CI with minimal surprises.
- Keep required test setup explicit.
- Treat flaky tests as bugs to fix, not noise to accept.
