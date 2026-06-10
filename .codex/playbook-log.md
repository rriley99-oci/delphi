# Delphi Playbook Log

This log tracks meaningful changes to the project-local Codex playbook in `.codex/`.

## 2026-06-08

### Initial playbook

- added project-local rules for backend, frontend, verification, and stack-specific best practices
- added initial Delphi skills for backend slices, UI slices, contract/rule work, and GitHub workflow
- added plan templates for backend and UI slices

Reason:

- establish a stable repo-specific operating guide for Codex sessions in Delphi

### GitHub project integration

- updated the GitHub workflow skill to add new Delphi tickets to GitHub project `oci-ai-incubations/17`

Reason:

- keep issue creation aligned with the actual planning board for the project

### Playbook maintenance loop

- added repo guidance for evolving `.codex/` over time
- added this playbook log
- added a skill for maintaining rules and skills deliberately

Reason:

- let the playbook improve with the project without becoming unstructured or forgotten

### Setup guide

- added `.codex/setup.md` to document how to bootstrap a similar Codex playbook in a new repository

Reason:

- make the Delphi playbook pattern reusable and easier to recreate in future repos

### Issue workflow automation

- added `delphi-work-issue` to codify the issue to plan to PR workflow
- added an issue automation contract document for the planned Phase 2 `In Progress` trigger
- aligned the automation path with an organization project so the runner can use org-project events instead of a personal-project workaround
- updated the playbook so ordinary Codex-created PRs target `development` instead of `main`

Reason:

- establish a deliberate, non-chaotic path for issue-driven Codex execution and future automation

## 2026-06-09

### Deterministic issue runner automation

- added `delphi-issue-runner-automation` to encode the exact local-checkout runner contract
- updated the issue workflow skill so planning happens before branch creation in the automation flow
- updated the automation contract and technical design to use project item list reconciliation, plan id markers, and `rocket` reaction approval on the exact plan comment
- added a visible `codex:owned` soft-lock label convention for the hourly poller to reduce duplicate starts

Reason:

- align the local Codex playbook with the new deterministic GitHub-driven runner behavior before implementation begins

### Label-driven runner state machine

- replaced the reaction and soft-lock model with a strict label workflow: `codex:ready`, `codex:planned`, `codex:approved`, `codex:running`, `codex:in-review`
- updated the automation contract so planning and execution are driven by label transitions
- added idempotent error-comment guidance using stable hidden markers so the hourly poller does not spam unresolved issues

Reason:

- make the simple scheduled automation easier to operate and safer to run repeatedly

## 2026-06-10

### Runner verification gate

- updated `delphi-issue-runner-automation` to require relevant local checks for
  execution work
- added an explicit PR CI verification gate before the runner comments on the
  issue and moves it to `codex:in-review`
- added a stable `ci-unverified` blocking marker for cases where CI cannot be
  observed

Reason:

- keep automated issue execution from declaring review readiness until both
  local verification and GitHub CI status are known

### Project terminology hardening

- updated `AGENTS.md` and the GitHub workflow skill so "the project" defaults to GitHub org project `oci-ai-incubations/17`, not the Delphi repository
- added explicit preview guidance to restate whether "project" means the org project or the repo before side-effecting GitHub actions

Reason:

- prevent repeated confusion between the repository target and the organization project board during ticket workflows
