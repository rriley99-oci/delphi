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

Reason:

- establish a deliberate, non-chaotic path for issue-driven Codex execution and future automation
