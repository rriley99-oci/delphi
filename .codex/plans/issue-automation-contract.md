# Issue Automation Contract

This document defines the intended Phase 2 workflow for issue-driven execution in Delphi.

## Goal

Allow a GitHub issue to start a Codex working session only after a deliberate human signal, then require plan approval before implementation proceeds.

## Trigger

Do not trigger on issue creation.

Preferred trigger:

- the issue's organization GitHub Project status moves to `In Progress`

Fallback trigger if project automation is not available:

- a label such as `status:in-progress`

## Workflow

1. Issue is created and reviewed by a human.
2. Human moves the issue to `In Progress`.
3. Automation detects the organization project state transition.
4. Automation starts a Codex session for that issue.
5. Codex fetches the issue and creates a working branch.
6. Codex drafts an implementation plan.
7. Codex pauses for approval.
8. Human approves the plan.
9. Codex executes the work.
10. Codex pushes the branch and opens a PR.

## Guardrails

- no auto-start on `opened`
- no implementation before plan approval
- no new branch if existing branch state is ambiguous
- no PR without explicit issue linkage
- no fake test claims

## Recommended branch naming

`codex/issue-<number>-<slug>`

## Recommended issue lifecycle

- `Todo`
- `In Progress`
- `PR Open`
- `Done`

The plan-review step can live in comments instead of requiring its own project state.

## Codex responsibility

Codex should:

- understand the issue
- make a short plan
- wait for approval
- execute cleanly
- report verification honestly
- open a PR linked to the issue

## Automation responsibility

The automation layer should:

- detect the `In Progress` transition
- start or route the Codex session
- pass the issue identity cleanly
- avoid duplicate session creation
- prefer organization-project events over polling when the board supports them

The automation layer should not decide implementation details.
