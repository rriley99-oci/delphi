# React Rules

## Product behavior

- Build for operator workflows, not presentation flourishes.
- Keep pages responsive to real data states: loading, empty, partial, failure, success.
- Make important actions visible and low-friction.

## Component design

- Keep components focused on one surface or concern.
- Push data fetching and orchestration up when that makes presentational components simpler.
- Avoid giant page components that mix layout, state, data access, and formatting logic.

## UX discipline

- Keep tables, tabs, filters, and status summaries stable as data changes.
- Make state transitions visible after actions like triggering evaluations or resolving violations.
- Show evidence near the decision surface instead of hiding it in a distant panel.

## Performance and correctness

- Use memoization only where it solves a measured or obvious rerender problem.
- Keep keys stable in lists and tabular views.
- Treat optimistic UI carefully for domain actions that affect trust signals.
