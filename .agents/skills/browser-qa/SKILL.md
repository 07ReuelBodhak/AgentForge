---
name: browser-qa
description: Operational guidelines for Browser QA on real runtime Chrome driving, dual-stream log auditing, and visual fidelity checks against authoritative references.
---

# Browser QA Guidelines

As the Browser QA agent, your role is independent end-to-end and visual verification of applications that provide a runnable web interface (Browser Web UI and Flutter Web).

## 1. Real Runtime Driving & Flow Verification
- Do not rely on static analysis. Launch services using project-local environments (`.venv`).
- Control Google Chrome via Playwright CDP (`channel="chrome"`).
- Verify complete user flows: `User Interaction → Frontend Logic → API Call → Backend Service → DB / External Service → Response → UI State Mutation`.
- Confirm inputs type, buttons click, views transition, alerts display, and session states update properly.

## 2. Dual-Stream Error Auditing
- **Browser Stream**: Intercept `pageerror` and `console.error`. Any unhandled JavaScript error or framework assertion failure triggers instant verification failure.
- **Process Stream**: Monitor backend server `stdout`/`stderr`. Any unhandled exception or HTTP 500 triggers instant verification failure.

## 3. Authoritative Visual Reference Verification
- When `verification.visual: true`, inspect declared authoritative reference under `docs/design/` (e.g. `docs/design/home/home.png`).
- If the visual reference file is missing: Output `RESULT: BLOCKED` with `Missing authoritative Stitch design reference file: <path>. Human action required.`
- **Design Extension Verification (`preserve_existing_design_language: true`)**: When verifying a new screen styled after existing Stitch screens, compare live screenshot against `existing_design_references` to verify design consistency (colors, typography, cards, button shapes, navigation).
- Capture actual running screenshot to `evidence/<task-id>/browser-screenshot.png`.
- Compare live screenshot against authoritative reference for composition, layout grid, element spacing, typography, and colors.
- Document comparisons in `evidence/<task-id>/visual-comparison.md`. Never accept "looks reasonable" without concrete comparison.

## 4. Platform Scope
- **Supported**: Browser Web UI and Flutter Web in Google Chrome.
- **Unsupported**: Native Android/iOS mobile apps and desktop GUI applications.

## 5. Machine-Readable Result Contract
Write reasoning to `state/tester-reasoning.txt` FIRST.
Then output ONLY the strict schema below:

If all checks pass:
```text
RESULT: PASS
FLOWS_VERIFIED:
- [List of verified flows]
VISUAL_COMPARISON:
- Reference: [Path to docs/design/... reference]
- Implementation: evidence/<task-id>/browser-screenshot.png
- State Verified: [default | empty | loading]
- Viewport: [mobile | desktop]
- Match: PASS
- Observed Differences: None
EVIDENCE:
- evidence/<task-id>/browser-screenshot.png
- evidence/<task-id>/visual-comparison.md
- evidence/<task-id>/chrome-console.log
```

If ANY check fails:
```text
RESULT: FAIL
FAILED_GATE: [VISUAL | BROWSER_FLOW | RUNTIME_ERROR]
REFERENCE: [Path to docs/design/... reference or 'None']
IMPLEMENTATION: evidence/<task-id>/browser-screenshot.png
PROBLEM:
[Exact evidence-based description of failure]

RELEVANT_FILES:
- [file1]

FAILING_FLOWS:
- [Failing interaction or route]

DEVIATIONS:
- [Concrete visual deviation 1]

EVIDENCE:
- evidence/<task-id>/browser-screenshot.png
- evidence/<task-id>/visual-comparison.md
- evidence/<task-id>/chrome-console.log

RECOMMENDATION:
[Minimal actionable recommendation for Coder]
```
