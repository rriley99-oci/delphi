---
name: delphi-github-workflow
description: Work Delphi GitHub issues and pull requests with GitHub CLI. Use when Codex needs to create a ticket, inspect an existing issue, branch from an issue, implement work tied to a ticket, push a feature branch, open a pull request, or check PR status for the current Delphi repository.
---

# Delphi GitHub Workflow

Use this skill for GitHub issue and PR work in the Delphi repo.

This skill is grounded in the current GitHub CLI workflow documented by GitHub:

- `gh issue create`
- `gh issue view`
- `gh issue develop`
- `gh pr create`
- `gh pr view`
- `gh pr checks`

Reference:

- [GitHub CLI `gh issue create`](https://cli.github.com/manual/gh_issue_create)
- [GitHub CLI `gh issue view`](https://cli.github.com/manual/gh_issue_view)
- [GitHub CLI `gh issue develop`](https://cli.github.com/manual/gh_issue_develop)
- [GitHub CLI `gh pr create`](https://cli.github.com/manual/gh_pr_create)
- [GitHub CLI `gh pr view`](https://cli.github.com/manual/gh_pr_view)
- [GitHub CLI `gh pr checks`](https://cli.github.com/manual/gh_pr_checks)

## 1. Preflight

Before any GitHub action:

1. confirm the current repo root
2. run `gh auth status`
3. confirm the current branch when PR work is involved
4. inspect working tree state before pushing or creating a PR

If GitHub CLI auth is missing, stop and tell the user to run `gh auth login` or provide a valid token before continuing.

## 2. Choose the workflow

Use one of these paths.

### A. Cut a ticket

Use when the user asks to:

- create an issue
- file a bug
- write up a task
- open a feature request

### B. Work a ticket

Use when the user asks to:

- pick up an issue
- implement issue `#N`
- branch from an issue
- continue work tied to a GitHub ticket

### C. Push a PR

Use when the user asks to:

- open a PR
- draft a PR
- push a branch and create a PR
- check PR status

## 3. Ticket creation rules

Draft the issue before posting it.

Suggested issue structure:

```md
## Summary

## Problem

## Proposed Approach

## Acceptance Criteria

## Notes
```

Guidelines:

- Keep the title short and action-oriented.
- Use labels only when they are known to exist.
- Do not invent assignees, milestones, or project settings.
- Show the full draft to the user before posting.
- Require explicit confirmation before running `gh issue create`.
- After creating a Delphi ticket, add it to the Delphi GitHub project.

Preferred command pattern:

```bash
gh issue create \
  --title "<title>" \
  --body-file "<temp-file>"
```

Use `--repo <owner/repo>` if the cwd repo is not the intended target.

### Delphi project assignment

Delphi tickets belong on this GitHub project:

- `oci-ai-incubations` org project `17`
- URL: `https://github.com/orgs/oci-ai-incubations/projects/17`

After creating the issue, add it to the project with:

```bash
gh project item-add 17 \
  --owner oci-ai-incubations \
  --url "<issue-url>"
```

Project operations require the `project` scope. Check that with:

```bash
gh auth status
```

If the token is missing the scope, the official GitHub CLI guidance is to refresh auth with the `project` scope before retrying.

If project assignment fails but issue creation succeeded:

- report the created issue URL to the user
- show the project-add command needed to finish the job
- do not pretend the ticket landed on the board

## 4. Working a ticket

When the user asks to work an issue:

1. fetch the issue details first
2. understand the scope from the actual issue body and comments
3. create or switch to a feature branch
4. keep implementation tied to the issue's acceptance shape

Preferred inspection commands:

```bash
gh issue view <number> --comments
gh issue view <number> --json number,title,body,labels,assignees,state,url
```

Preferred branch workflow:

```bash
gh issue develop <number> --checkout
```

If a deterministic branch name is needed, prefer:

```bash
gh issue develop <number> --checkout --name codex/issue-<number>-<slug>
```

If `gh issue develop` is unavailable or unsuitable, create the branch manually with git using the same naming pattern.

## 5. PR workflow

Before opening a PR:

1. review `git status --short`
2. review the branch diff and recent commits
3. push the branch explicitly
4. resolve the target base branch deliberately

PR body should be grounded in the actual diff and commit history, not guessed.

Suggested PR structure:

```md
## Summary

## Changes

## Testing

## Notes
```

Rules:

- Include `Closes #N` or `Fixes #N` when the PR should close the related issue.
- Keep the PR title concise and specific.
- Show a full preview before posting.
- Require explicit confirmation before running `gh pr create`.

Preferred command pattern:

```bash
gh pr create \
  --base <base> \
  --head <branch> \
  --title "<title>" \
  --body-file "<temp-file>"
```

Useful follow-up commands:

```bash
gh pr view --json number,title,url,reviewDecision,statusCheckRollup
gh pr checks
```

## 6. Confirmation rules

For side-effecting actions, confirmation is mandatory.

Require explicit confirmation before:

- creating an issue
- pushing a branch when that visibility matters to the user
- creating a PR

A preview should include:

- target repo
- branch and base branch where relevant
- title
- labels or reviewers if any
- project assignment target when relevant
- full body text

## 7. Delphi-specific expectations

- Work inside the current Delphi repo unless the user explicitly names another target.
- Prefer branch names like `codex/issue-123-short-topic`.
- Keep issues and PRs aligned with Delphi's product language: datasets, contracts, evaluations, violations, NL query, dashboard.
- Reflect actual testing honestly. Do not claim checks passed unless they were run.
- When a ticket drives implementation, keep the final PR tightly linked back to that ticket.
- For issue creation, default to adding the issue to GitHub project `oci-ai-incubations/17`.

## 8. Safe defaults

- Prefer `gh` commands over hand-built GitHub URLs.
- Prefer `--body-file` over inline body strings for long issue or PR text.
- Prefer reading issue and PR data from `gh ... --json` when structured fields are needed.
- Stop and ask if repo, base branch, reviewers, or issue linkage is ambiguous.
