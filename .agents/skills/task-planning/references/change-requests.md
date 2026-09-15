# Change Request & Impact Analysis Reference

## 1. Change Request Lifecycle

```text
User Change Request
        ↓
Detect Category (Bug Fix / Modification / New Feature)
        ↓
changes/CR-XXX.md (Status: PROPOSED)
        ↓
Planner: IMPACT_ANALYSIS (HIGH_REASONING)
        ↓
Snapshot: docs/project-context-history/v{N}-{CR_ID}.md
        ↓
Additive Update: docs/project-context.md (# Change Log & Context History)
        ↓
Task Decisions:
  - Unaffected tasks: Remain VERIFIED (never rerun)
  - Invalidated tasks: Set Status: REOPENED or SUPERSEDED with reason
  - New tasks: Create sequential TASK-XXX.md linked to CR-XXX
        ↓
CR Status: APPROVED
        ↓
USER EXECUTION CHOICE:
  - ALL (execute all sequentially)
  - ONE_BY_ONE (review after each task)
        ↓
Manager Execution Loop
        ↓
For Each Task: Generate reports/tasks/TASK-XXX.md
        ↓
When All Tasks Complete: Update existing reports/final-report.md in-place
```

## 2. Reopening vs. Superseding Rules
- **REOPENED**: The existing component needs modifications or extensions to support the new requirement. The task's original acceptance criteria are expanded.
- **SUPERSEDED**: The existing component or architecture is entirely replaced or deprecated by the new requirement. The old task remains in historical state marked `SUPERSEDED`, and a new task implements the replacement.
- **NEVER**: Silently alter an old verified task file without recording the reason under `Status Notes`.
- **NEVER**: Renumber historical task IDs. New work receives new sequential IDs.

## 3. Canonical Final Report Preservation
- On session completion, the existing `reports/final-report.md` is updated in-place with the change history entry.
- **CRITICAL**: Never create duplicate final reports (such as `reports/final-report-v2.md`). History is preserved via `changes/CR-XXX.md` and `docs/project-context-history/`.
