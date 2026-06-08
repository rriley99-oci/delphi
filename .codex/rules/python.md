# Python Rules

## Style and structure

- Prefer clear, typed Python over clever Python.
- Use small modules with explicit responsibilities.
- Favor dataclasses or Pydantic models for structured state over loose dictionaries.
- Keep side effects near the edges of the system.

## Typing

- Add type hints to public functions, service methods, and domain models.
- Use concrete types where they improve clarity.
- Avoid `Any` unless the boundary is genuinely dynamic.
- Model optionality explicitly.

## Error handling

- Raise domain-meaningful errors instead of generic exceptions where behavior matters.
- Do not swallow exceptions silently.
- Convert infrastructure errors into application-level responses at the service or API boundary.

## Data and time

- Use timezone-aware timestamps.
- Keep timestamp generation consistent and auditable.
- Prefer immutable inputs and return values when practical for domain logic.

## Maintainability

- Keep functions short enough that the main path is easy to scan.
- Extract helpers only when they remove real duplication or clarify domain meaning.
- Write comments sparingly and only where intent is not obvious from the code.

## Testing

- Test business behavior, not just object construction.
- Prefer focused unit and service tests for domain logic.
- Keep fixtures readable and close to the domain language of the product.
