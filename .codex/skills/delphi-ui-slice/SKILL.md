---
name: delphi-ui-slice
description: Implement or refine a Delphi frontend feature for the internal operational UI. Use when building overview dashboards, dataset detail tabs, contract editing, evaluation history, violation workbench flows, or natural-language evidence views and you want to preserve Delphi's dense, operator-focused product style.
---

# Delphi UI Slice

Use this workflow when building or revising a UI feature in Delphi.

## 1. Re-anchor in product intent

Read:

- `docs/product-spec.md`
- `.codex/rules/frontend.md`
- `.codex/rules/verification.md`

Remember the product posture:

- internal tool
- operational density
- evidence-driven health states

## 2. Start from the workflow

Identify the operator action first:

- scan overview health
- inspect a dataset
- trigger an evaluation
- compare contract versions
- acknowledge or resolve a violation
- ask Delphi a metadata question

Design around completing that action quickly.

## 3. Favor dense clarity

- Prefer tables, compact panels, tabbed detail views, and strong status hierarchy.
- Keep current state and historical context close together.
- Show evidence near statuses and NL answers.
- Avoid ornamental UI that burns space without improving decision-making.

## 4. Wire behavior, not just layout

When building UI, make sure the core interactions are represented:

- action buttons
- loading states
- empty states
- failure states
- evidence display

The interface should feel like a real operator tool even before it is fully polished.

## 5. Verify the flow

Check the main operator path end to end:

1. find the relevant dataset or issue
2. open the relevant panel or tab
3. take the action
4. verify the visible state change
5. confirm evidence remains available
