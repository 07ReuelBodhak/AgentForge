# Escalation Record Schema

Use this schema when creating `state/escalation.md`:

```markdown
# Escalation: [TASK-ID or SYSTEM]

- **Timestamp**: [ISO 8601 Timestamp]
- **Task ID**: [TASK-XXX or Global]
- **Reason**: [MAX_RETRIES_EXCEEDED | INVALID_TESTER_OUTPUT | MISSING_MCP | CONTRADICTORY_SPEC | ENVIRONMENT_BLOCK]
- **Current State**: [CODING | TESTING | INTEGRATION_TESTING | UI_TESTING | RETRYING]
- **Iteration**: [Current iteration number / MAX_ITERATIONS]

## Blocking Issues
- [Concrete description of why automation cannot proceed]

## Evidence & Context
- [Path to failing test output or error logs, e.g. state/failure-<task-id>.txt]

## Required Human Intervention
- [Specific decision or manual fix needed from the engineer]
```
