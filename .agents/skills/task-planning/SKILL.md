---
name: task-planning
description: Operational guidelines for the Planner agent on atomic task decomposition, verification flags, and Change Request impact analysis.
---

# Task Planning Guidelines

As the Planner, your role is to decompose `docs/project-context.md` into atomic, topologically ordered tasks (`tasks/TASK-XXX.md`), and to perform impact analysis on Change Requests (`changes/CR-XXX.md`).

## 1. Initial Project Decomposition
- **Bootstrap First**: Schedule environment and dependency manifest setup (`requirements.txt`, `package.json`, etc.) before feature implementation.
- **Service Boundaries**: Tag tasks with explicit `Project Area`, `Service`, and `Execution Environment`.
- **Mandatory Verification Flags**:
  - `Requires Integration Verification`: Set `true` if the task involves multi-service or frontend-to-backend API integration; otherwise `false`.
  - `Requires UI/E2E Verification`: Set `true` if the task delivers user-facing UI; otherwise `false`. If `true`, provide Stitch or local path under `Design Reference`.
- **Topological Dependencies**: Ensure every task explicitly lists prerequisite task IDs in `Dependencies:`.
- **Atomic Scope**: Scope each task for single-iteration implementation and cleanroom verification.

## 2. Change Request Impact Analysis (CR-XXX)
When a Change Request is submitted:
1. **Never Bypass to Coder**: Verify formal proposal exists in `changes/CR-XXX.md`.
2. **Snapshot Canonical Context**: Before making changes, snapshot current `docs/project-context.md` into `docs/project-context-history/v{N}-{CR_ID}.md`.
3. **Analyze Impact on Verified Tasks**:
   - Do NOT rerun unaffected verified tasks.
   - If an existing verified component is directly altered, mark that task `Status: REOPENED` or `Status: SUPERSEDED` with explicit justification in `Status Notes`.
4. **Create Sequential Tasks**: Assign new sequential task IDs referencing `Change Request: CR-XXX`.
5. **Additive Context Update**: Add amendments under `# Change Log & Context History` in `docs/project-context.md`. Never delete historical requirements.
6. *(See `references/change-requests.md` for full lifecycle details).*

## 3. Output Contract
Return a concise summary:
```text
STATUS: PLANNED (or ANALYZED)

TASKS:
- TASK-XXX — [Goal] (NEW)
- TASK-YYY — [Goal] (REOPENED: reason)

NOTES:
- [Key notes or environment considerations]

NEXT_ACTION:
- Ask user execution mode: ALL (execute all sequentially) vs ONE_BY_ONE (review after each task).
```
