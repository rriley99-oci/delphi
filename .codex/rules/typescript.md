# TypeScript Rules

## Type safety

- Prefer explicit types and interfaces for API contracts, view models, and component props.
- Avoid `any`; use `unknown` at uncertain boundaries and narrow from there.
- Keep frontend models aligned with backend response shapes.

## Code organization

- Separate presentation concerns from data-fetching and state orchestration.
- Keep reusable UI primitives small and focused.
- Favor composition over deeply nested conditional rendering.

## State and data flow

- Keep derived state derived.
- Avoid duplicating server state across multiple local stores without a clear reason.
- Model loading, error, and empty states explicitly.

## Maintainability

- Use descriptive names over shorthand.
- Keep helpers close to the feature until reuse is real.
- Prefer straightforward code over heavy abstraction in an early product.
