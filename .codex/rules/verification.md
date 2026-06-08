# Verification Rules

## General

- Verify behavior, not just structure.
- When implementing interactive UI, exercise the key path rather than only checking that elements render.
- Keep tests focused on the real domain risks of the change.

## Backend

- Prefer unit and service-level tests for contract versioning, evaluation normalization, and violation lifecycle.
- Add API tests when route behavior or schema shape changes.
- Keep fixtures explicit and domain-relevant.

## Frontend

- Validate the operator workflow end to end for the feature being changed.
- For dashboards and detail views, verify status changes, tab content, and evidence rendering.
- If an interaction opens a modal or panel, close it before moving on to the next assertion.

## Natural language

- Verify both answer text and evidence payloads.
- Do not accept a result that sounds plausible but cannot be traced to concrete metadata records.
