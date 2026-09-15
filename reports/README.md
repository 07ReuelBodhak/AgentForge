# Project Reports Repository

This directory contains the authoritative reports produced during project execution.

## Structure
```text
reports/
├── tasks/
│   ├── TASK-001.md              # Per-task completion reports (generated after each task)
│   ├── TASK-002.md
│   └── ...
└── final-report.md              # Canonical project final report (updated in-place)
```

## Reporting Rules
1. **Per-Task Reports (`reports/tasks/TASK-XXX.md`)**:
   - Generated immediately after a task completes (`VERIFIED`, `FAILED`, `BLOCKED`, or `ESCALATED`).
   - Follows `schemas/task-report-schema.md`.
   - Strictly contains factual deliverables, files changed, test results, and evidence links (no conversation transcripts).
2. **Canonical Final Report (`reports/final-report.md`)**:
   - Follows `schemas/final-report-schema.md`.
   - Represents the current canonical state of the entire project.
   - When a Change Session (`CR-XXX`) completes, `reports/final-report.md` is **updated in-place**. Never create duplicate versions (`final-report-v2.md`).
   - Evolution history is preserved in `## Change History`, `changes/CR-XXX.md`, and `docs/project-context-history/`.
