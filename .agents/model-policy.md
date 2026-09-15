# Model Routing Policy

This document defines the logical model routing policies for the multi-agent system and maps them to environment capabilities in Antigravity.

## Logical Policies

| Policy Name | Purpose & Characteristics | Typical Agent Scope | Antigravity Tier |
| :--- | :--- | :--- | :--- |
| **`HIGH_REASONING`** | Deep architectural analysis, topological dependency decomposition, Change Request impact analysis, complex refactors. | `planner` | `Model: "pro"` |
| **`FAST_CODING`** | Surgical code implementations, minimal-diff edits, targeted bug fixes within single services. | `coder` | `Model: "flash"` |
| **`FAST_TESTING`** | Fast, cleanroom automated test execution, dependency manifest audits, live server startup tests. | `strict_tester` | `Model: "flash"` |
| **`FAST_BROWSER`** | Live Chrome automation via CDP, DOM element interaction, browser console auditing, visual fidelity comparisons. | `browser_qa` | `Model: "flash"` |
| **`ORCHESTRATOR`** | State-machine loop progression, dependency gating, parsing machine-readable results, escalation dispatching. | `manager` | `Model: "inherit"` |

## Fallback & Environment Portability Rules
- If a high-tier model is unavailable or rate-limited, `HIGH_REASONING` tasks may fall back to `inherit`.
- Low-latency verification and coding tasks should remain on `flash` to preserve token efficiency and reduce run durations.
- Agents must never hardcode specific model string identifiers in workflow logic; references must use these logical policy aliases.
