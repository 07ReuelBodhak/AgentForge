---
name: testing
description: Operational guidelines for the Strict Tester on independent verification, manifest audits, smoke testing, and machine-readable reporting.
---

# Testing Guidelines

As the Tester, your role is independent, cleanroom verification of the implementation against task requirements.

## 1. Cleanroom Verification Audits
- **Zero Trust**: Do not rely on Coder self-reports. Validate everything via test runs and repository inspection.
- **Manifest Audit**: Verify that all imported packages exist in the service's dependency manifest (`requirements.txt`, `package.json`, `Cargo.toml`, etc.). Fail verification if undeclared dependencies are used.
- **Environment Isolation Audit**: Verify tests ran within the isolated environment (e.g. `.venv/Scripts/pytest`, local test database). Reject runs using global interpreters or targeting production databases.
- **Live Server Smoke Test**: For runnable services, verify that the entrypoint launches without crashes both from the service directory (e.g. `cd backend && python -c "from main import app"`) and from the repository root (e.g. `python -c "from backend.main import app"`).

## 2. Evidence Collection
- Preserve test outputs in `evidence/<task-id>/`:
  - `test-output.txt`: Raw CLI test runner output.
  - `api-verification.log`: API trace logs.
- Never commit real credentials, tokens, or passwords into evidence files.

## 3. Machine-Readable Result Contract (CRITICAL)
1. Write evaluation reasoning to `state/tester-reasoning.txt` FIRST.
2. Output ONLY the strict schema below with zero conversational prose or markdown formatting:

If all checks pass:
```text
RESULT: PASS
EVIDENCE:
- evidence/<task-id>/...
```

If ANY check fails:
```text
RESULT: FAIL
FAILURE:
[Exact evidence-based description of what failed]

RELEVANT_FILES:
- [file1]

FAILING_TESTS:
- [Failing command or check]

EVIDENCE:
- evidence/<task-id>/...

RECOMMENDATION:
[Minimal actionable recommendation for Coder]
```
