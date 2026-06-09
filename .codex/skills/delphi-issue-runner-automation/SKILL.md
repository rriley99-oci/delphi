---
name: delphi-issue-runner-automation
description: Run the Delphi issue automation from the local checkout at /Users/rriley/Repos/rriley/delphi-runner. Use when Codex is invoked by automation to inspect GitHub project 17, process In Progress Delphi issues with Codex workflow labels, publish a plan, execute approved work, and open a PR against development.
---

# Delphi Issue Runner Automation

Use this skill when Codex is acting as the deterministic Delphi automation runner rather than as an interactive teammate.

## 1. Fixed operating context

- Work from the local checkout at `/Users/rriley/Repos/rriley/delphi-runner`
- Treat GitHub organization project `oci-ai-incubations/17` as the source of truth for intake state
- Only act on issues from repository `https://github.com/rriley99-oci/delphi`
- Default PR base branch is `development`
- Use these workflow labels as a strict state machine:
- `codex:ready`
- `codex:planned`
- `codex:approved`
- `codex:running`
- `codex:in-review`

Use GitHub CLI and git directly. Prefer deterministic reads before any side effect.

## 2. Intake query

Start with:

```bash
gh project item-list 17 --owner oci-ai-incubations --format json
```

From that output, find the first issue where:

- `repository` is `https://github.com/rriley99-oci/delphi`
- `status` is `In Progress`
- the issue has label `codex:ready` or `codex:approved`

If no matching issue exists:

- remain silent
- do nothing else

## 3. Issue inspection

For the selected issue number:

1. inspect issue comments with:

```bash
gh api repos/rriley99-oci/delphi/issues/<number>/comments
```

2. inspect issue labels
3. inspect whether an open PR already exists for the issue

Treat the workflow labels as the primary source of runner state.

If the issue has more than one Codex workflow label:

- treat that as a blocking error
- post one error comment only if that exact error marker does not already exist
- do not continue

If the issue has no Codex workflow label:

- remain silent

If an open PR already exists and the issue is not yet `codex:in-review`:

- move the label state to `codex:in-review`
- do not start work again

This inspection should use exact comment ids and bodies rather than approximate summaries.

## 4. Planning path

If the issue is labeled `codex:ready`:

1. do not create a branch yet
2. generate a unique plan id using the issue number plus a timestamp-like or hash-like suffix
3. decide an intended branch name in this format:

```text
codex/issue-<number>-<slug>
```

4. draft a short implementation plan grounded in the issue acceptance criteria
5. post an issue comment that contains:

- the exact marker `<!-- codex-plan-id: PLAN_ID -->`
- the intended branch name
- a concise implementation plan
- intended verification
- approval instructions telling the user to change the label to `codex:approved` when ready

6. move the issue label state from `codex:ready` to `codex:planned`
7. stop

If a blocking condition prevents planning:

- record it with a stable hidden marker
- post that error comment only once per distinct condition

## 5. Approval and execution path

If the issue is labeled `codex:approved`:

1. confirm a Codex plan comment exists
2. identify the latest plan comment
3. re-fetch the issue state before mutating labels
4. move the issue label state from `codex:approved` to `codex:running`
5. execute only the latest approved plan

If `codex:approved` exists but no plan comment exists:

- treat that as a blocking error
- post one error comment only if that exact error marker does not already exist
- do not continue

## 6. Execution protocol

When the issue is in `codex:running`:

1. align the checkout to `origin/development`
2. create or switch to the issue branch from `development`
3. implement the approved work
4. run the most relevant checks honestly
5. commit the changes
6. push the branch
7. open a pull request against `development` with `Closes #<number>`
8. comment on the issue with the PR URL and the plan id
9. move the issue label state to `codex:in-review`

If an actionable error prevents execution:

- record the reason clearly
- use a stable hidden marker for the distinct blocking condition
- do not post the same error comment repeatedly

## 7. Error comment protocol

Use hidden markers for machine-detectable blocking comments, for example:

```html
<!-- codex-error: multiple-state-labels -->
<!-- codex-error: approved-without-plan -->
<!-- codex-error: planned-without-plan-comment -->
<!-- codex-error: running-state-conflict -->
```

Before posting an error comment:

- scan existing comments for the exact error marker
- if it already exists, remain silent

Only comment for actionable human intervention. Never comment repeatedly about:

- no matching work
- waiting for approval
- the same unresolved blocking error

## 8. Silence rules

Remain silent when:

- no matching `In Progress` Delphi issue exists on project `17`
- the issue has no actionable Codex workflow label
- the issue is `codex:planned` and waiting on a human
- the same known blocking error is already recorded

Silence means no extra comments, no branch work, and no PR activity.

## 9. Safety defaults

- Treat labels as the primary workflow contract
- Require exactly one Codex workflow label at a time
- Never create the working branch during the planning-only phase
- Never execute without `codex:approved` or `codex:running`
- If an open PR already exists, prefer moving to `codex:in-review` over restarting work
- Report checks honestly and do not claim success for commands that were not run
