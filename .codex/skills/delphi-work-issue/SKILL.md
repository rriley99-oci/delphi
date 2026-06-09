---
name: delphi-work-issue
description: Work a Delphi GitHub issue after it has been deliberately moved to In Progress. Use when Codex needs to fetch an issue, draft an implementation plan for approval, wait for the approval signal, then create the working branch, execute the approved plan, run relevant checks, and open a pull request that closes the issue.
---

# Delphi Work Issue

Use this skill for the issue-to-plan-to-PR workflow in Delphi.

This skill assumes the issue has already been intentionally selected for work. It should not be triggered merely because an issue exists.

## 1. Preconditions

Before starting work, confirm:

- the target issue number
- the repo is the Delphi repo unless the user says otherwise
- the issue is intentionally in an active working state, preferably `In Progress`
- GitHub CLI auth works

Preferred checks:

```bash
gh auth status
gh issue view <number> --comments --json number,title,body,labels,state,url
git status --short
git branch --show-current
```

If the issue is ambiguous, not ready, or the repo context is wrong, stop and clarify before branching.

## 2. Start from the issue

Read the actual issue carefully.

Extract:

- problem to solve
- acceptance criteria
- likely impacted areas
- unclear assumptions
- whether the work is backend, frontend, infra, or mixed

Do not start implementation from the title alone.

## 3. Draft the plan before branching

In the automation flow, planning happens before branch creation.

During the planning phase:

- choose the intended branch name `codex/issue-<number>-<slug>`
- include that branch name in the plan
- do not create the branch yet
- do not start implementation yet

If the plan is being published back to GitHub for approval, include a stable plan marker such as:

```html
<!-- codex-plan-id: PLAN_ID -->
```

and require the agreed approval signal on that exact plan comment before execution continues.

## 4. Create the working branch after approval

Prefer a deterministic branch name:

```bash
codex/issue-<number>-<slug>
```

Preferred workflow:

```bash
gh issue develop <number> --checkout --name codex/issue-<number>-<slug>
```

If that is not appropriate in context, create the branch with git manually.

If the branch already exists:

- determine whether the user wants to resume work or start fresh
- do not silently overwrite existing branch work

Before implementation, produce or confirm the short approved plan grounded in the issue.

The plan should include:

1. what will change
2. what files or layers are likely involved
3. what verification will prove it works
4. any open risk or ambiguity

The plan should be:

- short
- concrete
- reviewable

Do not execute until the user explicitly approves the plan.

## 5. Execute after approval

Once approved:

1. update the plan status
2. align with `origin/development`
3. implement in small, coherent steps
4. keep changes aligned with `.codex/rules/`
5. use the most relevant Delphi skills as needed

Common pairings:

- `delphi-backend-slice`
- `delphi-ui-slice`
- `delphi-contract-rules`
- `delphi-github-workflow`
- `delphi-maintain-playbook`

## 6. Verify honestly

Run the checks that fit the change.

Examples:

- backend tests
- frontend tests
- lint or type checks
- targeted manual verification

Never claim a check passed unless it actually ran and passed.

If a check could not run, say so plainly in the PR and final summary.

## 7. Open the PR

After implementation:

1. review `git status --short`
2. inspect the diff and commit state
3. push the working branch
4. create a PR against `development` with `Closes #<number>` or `Fixes #<number>` unless the user explicitly directs a different base branch
5. comment back on the issue with the PR URL and the approved plan id when the workflow is automation-driven

The PR should include:

- Summary
- Changes
- Testing
- Notes

Use the GitHub workflow skill conventions for preview and confirmation before posting the PR.

## 8. Phase 2 automation contract

This skill is designed to pair with a deliberate automation trigger.

Recommended trigger:

- GitHub project item status changes to `In Progress`

Recommended behavior:

1. automation detects the transition
2. automation starts or resumes a Codex session for the issue
3. Codex uses this skill
4. Codex drafts a plan and pauses for approval
5. the plan comment becomes the approval target
6. only after approval does implementation continue

Do not auto-start on issue creation alone.

## 9. Safe defaults

- one issue, one working branch
- one plan before coding
- one PR linked back to the issue, normally targeting `development`
- no execution without explicit plan approval
- no hidden side effects

## 10. Good final state

A successful run leaves:

- the issue understood
- an approved plan comment or equivalent approval record
- a branch created after approval
- a plan approved
- implementation completed
- verification summarized honestly
- a PR opened and linked to the issue
