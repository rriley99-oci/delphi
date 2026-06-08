---
name: delphi-maintain-playbook
description: Maintain Delphi's project-local Codex playbook in `.codex/`. Use when a task reveals missing guidance, stale instructions, a repeated workflow that should become a skill, or a stack/process change that should be captured in repo-local rules, skills, or planning templates.
---

# Delphi Maintain Playbook

Use this skill when the project's Codex playbook should evolve.

## 1. Start from evidence

Only update `.codex/` for a concrete reason.

Good triggers:

- the same advice has been repeated across multiple tasks
- a bug or detour exposed a missing rule
- a workflow keeps recurring and should be codified
- a framework or tool is now part of the stack
- a current rule or skill is stale or misleading

Avoid playbook edits that are only speculative or decorative.

## 2. Choose the smallest useful change

Prefer:

- a small rule clarification
- a new focused rule file
- a targeted skill update
- a lightweight new skill
- a small plan template adjustment

Do not respond to every rough edge with a giant rewrite.

## 3. Respect the maintenance boundary

Codex may directly make:

- additive guidance
- small clarifications
- new examples
- narrow new rules or skills

Pause and ask the user before:

- deleting major playbook content
- rewriting core workflow policy
- changing GitHub, release, or deployment conventions in ways that alter team process significantly

## 4. Keep the playbook coherent

Before editing, read the relevant existing files in:

- `AGENTS.md`
- `.codex/README.md`
- `.codex/rules/`
- `.codex/skills/`
- `.codex/plans/`
- `.codex/playbook-log.md`

Make sure the new guidance fits what is already there.

## 5. Log the change

Every meaningful `.codex/` update should also update:

- `.codex/playbook-log.md`

For each entry:

- say what changed
- say why it changed

Keep the log concise and readable.

## 6. Report the change clearly

In the final response for the user:

- mention that the playbook was updated
- name the files changed
- explain the reason in one or two sentences

If you decide not to edit `.codex/`, but a follow-up improvement is warranted, say so explicitly.
