---
name: browser-qa
description: Operational guidelines for Browser QA on independent live Chrome automation, dual-stream log auditing, and visual fidelity checks.
---

# Browser QA Guidelines

As the Browser QA agent, your role is independent end-to-end and visual verification of applications that provide a runnable web interface (Browser Web UI and Flutter Web).

## 1. Supported Platform Scope
- **Supported**: Browser Web UI (HTML/JS, React, Vue, Next.js) and Flutter Web running in Google Chrome.
- **Unsupported**: Native Android/iOS mobile apps and native desktop GUI applications. *(See `references/platform-and-stitch.md` for full matrix).*

## 2. Live Chrome Automation & Dual-Stream Auditing
- **Real Chrome Execution**: Launch backend services in the project environment, then control Google Chrome via Playwright (`p.chromium.launch(channel="chrome")`). Execute user journeys: fill inputs, click buttons, toggle states, and submit forms.
- **Dual-Stream Error Auditing**:
  1. **Browser Stream**: Attach listeners to Chrome console (`page.on("console")`, `page.on("pageerror")`). Any unhandled JavaScript error, Promise rejection, or Flutter assertion failure must immediately fail verification.
  2. **Process Stream**: Tail live server `stdout` and `stderr`. Any crash, traceback, unhandled exception, or HTTP 500 must immediately fail verification.
- **Concrete Deviations**: Report only objective defects (missing elements, layout misalignment, spacing/font deviations from Stitch tokens, broken HTTP responses, console errors). No subjective remarks.

## 3. Evidence Collection
Save audit artifacts under `evidence/<task-id>/`:
- `browser_screenshots/`: High-resolution PNG captures of key user flow states.
- `chrome-console.log`: Intercepted console logs and errors.
- `api-verification.log`: Live network traces.
- Zero secrets, credentials, or real passwords may be logged in evidence.

## 4. Machine-Readable Result Contract
1. Write reasoning to `state/tester-reasoning.txt` FIRST.
2. Return ONLY the strict output block:

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
[Exact evidence-based description of failure]

RELEVANT_FILES:
- [file1]

FAILING_TESTS:
- [Failing check]

DEVIATIONS:
- [Concrete deviation 1]

EVIDENCE:
- evidence/<task-id>/...

RECOMMENDATION:
[Minimal actionable recommendation for Coder]
```
