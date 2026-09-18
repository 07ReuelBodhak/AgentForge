---
name: task-planning
description: Operational guidelines for the Planner agent on execution topology, parallel safety, file conflict boundaries, and Change Request impact analysis.
---

# Task Planning Guidelines

As the Planner, your role is to decompose `docs/project-context.md` and `docs/codebase-map.md` into an atomic execution topology (`tasks/TASK-XXX.md`), and to perform impact analysis on Change Requests (`changes/CR-XXX.md`).

## 1. Execution Topology & Parallel Safety
- **Bootstrap First**: Schedule environment setup and dependency manifests (`requirements.txt`, `package.json`) before feature implementation.
- **Identify Concurrency Lanes**:
  - Independent domains (e.g. Backend API vs Frontend UI) with no shared files or sequential dependency must be tagged `parallel_safe: true`.
  - Tasks sharing files or depending on unverified tasks must be tagged `parallel_safe: false`.
- **File Ownership Metadata**: Declare `read_files`, `modify_files`, and `create_files`. Two concurrent tasks must never have overlapping write targets.
- **Human Input Gate**: Identify external credentials (e.g. Cloudinary, OAuth) and declare them in `required_human_inputs`. If missing at runtime, the Manager will block execution.
- **Stitch Design Source of Truth**: When requirements state that UI must match Stitch, preserve this explicitly. Never reduce to generic text prompts. Set `design_source: stitch`, populate `authoritative_design_reference: docs/design/<screen>/<screen>.png`, register in `docs/design/design-manifest.md`, set `verification.browser: true`, and set `verification.visual: true`.
- **Stitch Design Extension**: When user requests a NEW SCREEN matching existing Stitch design:
  - Check if screen already exists in Stitch (`docs/design/design-manifest.md`).
  - If screen does NOT exist in Stitch, but user wants same Stitch style: inspect existing Stitch screens as style reference. If Stitch MCP supports generation, use `stitch:generate_screen_from_text` and download to `docs/design/`. If tool cannot generate: do NOT pretend; set `preserve_existing_design_language: true`, `existing_design_references: [docs/design/...]`, and implement consistently.
- **Authoritative Visual References**: Visual tasks must declare explicit reference image files under `docs/design/` in `visual_references`. If missing, the task cannot be verified and must be gated as BLOCKED.
- **Targeted Test Scoping**: Explicitly specify `test_scope` (`targeted | related | integration | browser | regression`) and `test_rationale`. Do not prescribe full regression for localized changes.

## 2. Change Request Impact Analysis (CR-XXX)
When a Change Request is submitted:
1. **Never Bypass to Coder**: Verify formal proposal exists in `changes/CR-XXX.md`.
2. **Snapshot Canonical Context**: Snapshot current `docs/project-context.md` into `docs/project-context-history/v{N}-{CR_ID}.md`.
3. **Analyze Impact on Verified Tasks**:
   - Unaffected verified tasks remain `Status: VERIFIED`.
   - If an existing verified component is directly altered, mark that task `Status: REOPENED` or `Status: SUPERSEDED` with explicit justification in `Status Notes`.
4. **Create Sequential Tasks**: Assign new sequential task IDs referencing `Change Request: CR-XXX`.
5. **Additive Context Update**: Add amendments under `# Change Log & Context History` in `docs/project-context.md`. Never delete historical requirements.
6. *(See `references/change-requests.md` for full lifecycle details).*

## 3. Output Contract
Return a concise summary:
```text
STATUS: PLANNED (or ANALYZED)

TASKS:
- TASK-XXX — [Goal] (Parallel Safe: true/false | Lane: Frontend/Backend)
- TASK-YYY — [Goal] (REOPENED: reason)

TOPOLOGY:
- Parallel Lanes: [e.g. Lane A (TASK-101) + Lane B (TASK-102) concurrently]
- Sequential Gates: [e.g. TASK-103 waits for TASK-101 and TASK-102]

NEXT_ACTION:
- Ask user execution mode: ALL (execute all sequentially/parallel) vs ONE_BY_ONE (review after each task).
```
