---
name: delphi-work-issue
description: Work a Delphi GitHub issue after it has been deliberately moved to In Progress. Use when Codex needs to fetch an issue, create a working branch, draft an implementation plan for approval, execute the approved plan, run relevant checks, and open a pull request that closes the issue.
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

## 3. Create the working branch

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

## 4. Draft the plan before coding

Before implementation, produce a short plan grounded in the issue.

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
2. implement in small, coherent steps
3. keep changes aligned with `.codex/rules/`
4. use the most relevant Delphi skills as needed

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
4. create a PR with `Closes #<number>` or `Fixes #<number>`

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
5. only after approval does implementation continue

Do not auto-start on issue creation alone.

## 9. Safe defaults

- one issue, one working branch
- one plan before coding
- one PR linked back to the issue
- no execution without explicit plan approval
- no hidden side effects

## 10. Good final state

A successful run leaves:

- the issue understood
- a branch created
- a plan approved
- implementation completed
- verification summarized honestly
- a PR opened and linked to the issue
