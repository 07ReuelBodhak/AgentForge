# Task Report Schema

Use this schema when writing `reports/tasks/TASK-XXX.md` after each task completes:

```markdown
# [TASK-ID] Report

## Task
[Task ID and title]

## Status
[VERIFIED | FAILED | BLOCKED | ESCALATED]

## What Was Implemented
- [Summary of functional components implemented]

## Files Changed
- [List of files created or modified]

## Architecture / Behavior Changes
- [Architectural components, routes, or behavior added or altered]

## Tests Performed
- [Specific test commands executed and results]

## Integration Verification
- [PASS | FAIL | NOT REQUIRED]

## Browser / UI Verification
- [PASS | FAIL | NOT REQUIRED]

## MCPs Used
- [List of MCPs used, or None]

## Evidence
- [File paths to evidence files under evidence/<task-id>/]

## Retry Information
- Iterations used: [Count]
- Final iteration: [Iteration number]
- Any failures encountered: [None or brief summary]

## Remaining Issues
- [None or remaining blockers]

## Change Request
- [CR-XXX or NONE]
```
