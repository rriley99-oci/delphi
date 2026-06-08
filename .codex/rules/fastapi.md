# FastAPI Rules

## API shape

- Keep endpoints resource-oriented and predictable.
- Use FastAPI routers to reflect domain boundaries.
- Keep route handlers thin; move business logic into services.
- Use request and response models explicitly.

## Validation and schemas

- Validate inputs with Pydantic models rather than ad hoc parsing.
- Keep request schemas distinct from persistence models.
- Make audit-sensitive fields explicit in schemas: ids, timestamps, status, severity, change reason.

## Dependency boundaries

- Use dependency injection for infrastructure concerns such as database sessions and auth later.
- Avoid hiding business logic inside dependency functions.
- Keep request-scoped resources explicit and easy to trace.

## Response behavior

- Return stable JSON shapes.
- Use appropriate status codes for create, update, not found, validation failure, and conflict cases.
- Keep error responses structured enough for the UI to act on them.

## Async and performance

- Use async handlers where the stack benefits from it, but do not force async into purely synchronous logic.
- Keep blocking I/O out of request handlers when possible.
- Move long-running evaluation work into jobs or workers instead of holding API requests open.

## Observability

- Add structured logging at the API and service boundaries.
- Preserve request correlation and evaluation identifiers where possible.
- Make health endpoints simple and dependable.
