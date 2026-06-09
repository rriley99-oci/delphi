# Issue Automation Contract

This document defines the intended Phase 2 workflow for issue-driven execution in Delphi.

## Goal

Allow a GitHub issue to start a Codex working session only after a deliberate human signal, then move through a label-driven planning and execution flow without noisy repeated comments.

## Trigger

Do not trigger on issue creation.

Preferred trigger:

- the issue's organization GitHub Project status moves to `In Progress`

Fallback trigger if project automation is not available:

- a label such as `status:in-progress`

## Workflow

1. Issue is created and reviewed by a human.
2. Human moves the issue to `In Progress`.
3. Automation inspects `gh project item-list 17 --owner oci-ai-incubations --format json` as the source of truth.
4. Automation selects the first `In Progress` issue from `https://github.com/rriley99-oci/delphi` that has label `codex:ready` or `codex:approved`.
5. Codex fetches issue comments, labels, and checks for an existing open PR.
6. If the issue is `codex:ready`, Codex posts a plan comment with a `<!-- codex-plan-id: ... -->` marker and intended branch name, then changes the label to `codex:planned`.
7. A human reviews the plan and changes the label to `codex:approved`.
8. On a later run, Codex sees `codex:approved`, changes the label to `codex:running`, and executes the approved plan.
9. Codex creates the working branch from `development`, executes the work, and verifies honestly.
10. Codex pushes the branch, opens a PR against `development`, comments back with the PR URL plus the plan id, and changes the label to `codex:in-review`.

## Guardrails

- no auto-start on `opened`
- no implementation before `codex:approved`
- no new branch if existing branch state is ambiguous
- no branch creation during the planning-only phase
- no more than one Codex workflow label at a time
- no repeated error comments for the same unresolved condition
- no PR without explicit issue linkage
- no fake test claims

## Recommended branch naming

`codex/issue-<number>-<slug>`

## Recommended issue lifecycle

- `Todo`
- `In Progress`
- `PR Open`
- `Done`

The plan-review step lives in issue comments plus workflow labels instead of requiring its own project state.

## Codex responsibility

Codex should:

- understand the issue
- make a short plan with a stable plan id marker
- wait for the label to move to `codex:approved`
- execute cleanly
- report verification honestly
- open a PR linked to the issue and normally target `development`

## Automation responsibility

The automation layer should:

- detect the `In Progress` transition
- start or route the Codex session
- pass the issue identity cleanly
- avoid duplicate session creation
- prefer organization-project events over polling when the board supports them
- treat the project item list as the source of truth for active intake
- rely on a visible label state machine that humans can inspect and change deliberately
- avoid posting duplicate blocking comments by using stable hidden error markers

The automation layer should not decide implementation details.
