# Task Report Schema

Use this schema when writing `reports/tasks/TASK-XXX.md` after each task completes:

```markdown
# [TASK-ID] Report

## Task & Objective
- **Task ID**: [TASK-XXX]
- **Title**: [Task Title]
- **Goal**: [Concise objective summary]
- **Change Request**: [CR-XXX or NONE]

## Status
- **Final Status**: [VERIFIED | FAILED | BLOCKED | ESCALATED]
- **Parallel Execution Status**: [Sequential | Ran concurrently in LANE_X]

## What Was Implemented
- [Summary of functional components implemented]

## Files Changed & Created
- **Files Modified**:
  - [file1]
- **Files Created**:
  - [file2]

## Prerequisites, Design Source & External Services
- **Design Source**: [Stitch | Human-Provided | None]
- **Authoritative Reference**: [docs/design/... or 'None']
- **Human Inputs / Credentials**: [Available | Missing / BLOCKED]
- **External Dependencies**: [e.g. Cloudinary, Stripe, or None]
- **MCPs Used**: [List of MCPs used, e.g. stitch, or None]

## Testing & Verification Summary
- **Test Scope**: [targeted | related | integration | browser | regression]
- **Test Scope Rationale**: [Why this scope was selected]
- **Tests Performed**:
  - [Command executed and pass/fail result]
- **Integration Verification**: [PASS | FAIL | NOT REQUIRED]
  - [Summary of live multi-service/API integration verified]
- **Browser / UI Verification**: [PASS | FAIL | NOT REQUIRED]
  - [Summary of live Chrome CDP user flow verified]
- **Visual Verification**:
  - **Design Source**: [Stitch | Human-Provided | NOT REQUIRED]
  - **Reference**: [docs/design/... or 'NOT REQUIRED']
  - **Design Language Preserved**: [YES: Adheres to existing Stitch style tokens | N/A]
  - **Browser Screenshot**: [evidence/<task-id>/browser-screenshot.png or 'None']
  - **Comparison Report**: [evidence/<task-id>/visual-comparison.md or 'None']
  - **Visual Result**: [PASS | FAIL | NOT REQUIRED]

## Code Quality & Engineering Review
- **Duplication & DRY**: [PASS: Reused existing helpers / No duplication]
- **Complexity & Simplicity**: [PASS: Simplest maintainable solution]
- **Dependencies Audit**: [PASS: All imports declared in local manifest]
- **Codebase Map Updated**: [YES: Updated affected rows in docs/codebase-map.md]

## Evidence
- [File paths to evidence files under evidence/<task-id>/]

## Retry & Iteration Information
- **Iterations Used**: [Count]
- **Failures Encountered**: [None or summary of failure context]

## Remaining Issues & Notes
- [None or remaining blockers]
```
