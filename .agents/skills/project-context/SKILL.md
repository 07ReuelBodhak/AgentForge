---
name: project-context
description: Guidelines on progressive disclosure of project context, codebase mapping, and immutable snapshot versioning.
---

# Consuming & Versioning Project Context and Codebase Map

## 1. Core Source of Truth Separation
The system maintains a strict separation of concerns across documentation:
* **Project Context (`docs/project-context.md`)**: *"What is the product supposed to do?"* Requirements, architecture constraints, environments, and domain rules.
* **Authoritative Design Reference (`docs/design/*`, `docs/design/design-manifest.md`)**: *"What should the UI look like?"* Preserved visual artifacts representing the Stitch design source of truth. Never replace with AI interpretations.
* **Codebase Map (`docs/codebase-map.md`)**: *"Where is the implementation located?"* Persistent compact index of files, key exports, and dependencies.
* **Task Contract (`tasks/TASK-XXX.md`)**: *"What exactly are we changing now?"* Bounded unit of work with file conflict boundaries, design source references, and verification gates.
* **Failure Context (`state/failure-<task-id>.txt`)**: *"What specifically failed?"* Minimal reproducible failure output for Coder retries.

## 2. Versioning Conceptual Model
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
- Update `docs/codebase-map.md` incrementally for files affected by the change.

## 3. Progressive Disclosure (Token Conservation)
- **Manager Agent**: NEVER loads `docs/project-context.md` or the entire codebase map. Operates strictly from task metadata and compact state files.
- **Coder Agent**: Consumes active task contract, relevant codebase map rows, and targeted files. Avoids scanning the whole repository. *(See `references/codebase-map-policy.md`).*
- **Tester & Browser QA Agents**: Consult context and map only to verify environment boundaries, security rules, and integration endpoints.
- **Planner Agent**: Reads full context and codebase map during initial decomposition and CR impact analysis.

## 4. Handling Unknown Information
- If fields are marked `UNKNOWN` (e.g. cloud provider, production domain, CI runner), do NOT fabricate assumptions.
- Confine execution strictly to local/test environment boundaries.
