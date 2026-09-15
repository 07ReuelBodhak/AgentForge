---
name: project-context
description: Guidelines on progressive disclosure of project context and immutable snapshot versioning.
---

# Consuming & Versioning Project Context

The canonical source of truth for the project's requirements, architecture, environments, and change history is:
`docs/project-context.md`

## 1. Versioning Conceptual Model
```text
docs/project-context.md
        =
CURRENT CANONICAL PROJECT STATE

docs/project-context-history/
        =
IMMUTABLE HISTORICAL SNAPSHOTS (v1-initial.md, v2-CR-001.md, etc.)

changes/CR-XXX.md
        =
REASON FOR CHANGE
```

- When a Change Request (CR) is approved, save an immutable snapshot of `docs/project-context.md` to `docs/project-context-history/v{N}-{CR_ID}.md` before making edits.
- Amend `docs/project-context.md` **additively** under `# Change Log & Context History`. Never erase original requirements.
- Active tasks reference only their current requirements; never duplicate full historical context into task prompts.

## 2. Progressive Disclosure (Token Conservation)
- **Manager Agent**: NEVER loads `docs/project-context.md`. The Manager operates strictly from task metadata and compact state files.
- **Coder Agent**: Consumes only the active task (`tasks/TASK-XXX.md`). Inspects `docs/project-context.md` only for unstated domain constraints.
- **Tester & Browser QA Agents**: Consult context only to verify environment boundaries, security rules, and testing strategies.
- **Planner Agent**: Reads the complete context during initial decomposition and CR impact analysis.

## 3. Handling Unknown Information
- If fields are marked `UNKNOWN` (e.g. cloud provider, production domain, CI runner), do NOT fabricate assumptions.
- Confine execution strictly to local/test environment boundaries.
