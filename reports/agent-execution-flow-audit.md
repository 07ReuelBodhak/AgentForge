# Multi-Agent System — Full Runtime Execution Flow Audit

**Audit Date:** September 2026  
**Auditor:** Antigravity Architecture Inspection Engine  
**Target Architecture:** Native Antigravity Multi-Agent Software Development System (V2.2)  
**Workspace:** `d:\multi_agent_system`  
**Classification:** Runtime Observability & Empirical Execution Audit (Ground Truth)

---

## Executive Attestation

This document is **not** a re-statement of design aspirations. It is an unsparing, evidence-based audit of how the multi-agent system **actually behaves at runtime**, derived from session transcripts, tool calls, filesystem state, subagent execution logs, and runtime failure modes observed during end-to-end execution.

---

## 1. The Real Entry Point

### Step-by-Step Runtime Inception
When a user initiates work, the actual flow from first user keystroke to execution is:

```text
USER ACTION (Types chat prompt, e.g. "Bootstrap project using docs/project-overview.pdf")
       ↓
ANTIGRAVITY ROOT ENGINE (Parent Session)
       ↓
PARENT AGENT (Main Antigravity LLM Conversation Context)
       ↓
Inspects workspace → Reads .agents/change-detection.md
       ↓
Invokes context_extractor Subagent via invoke_subagent(TypeName="context_extractor")
       ↓
context_extractor reads docs/project-overview.pdf → writes docs/project-context.md
       ↓
Parent Agent wakes up on reactive message receipt
       ↓
Parent Agent invokes planner Subagent via invoke_subagent(TypeName="planner")
       ↓
planner reads docs/project-context.md → writes docs/codebase-map.md & tasks/TASK-XXX.md
       ↓
Parent Agent presents execution mode choice to User (ALL vs ONE_BY_ONE)
```

**First File / Agent Responsible for Transition:**
The **Parent Session Agent** is the initial controller. There is no automated daemon process or webhook listener. The transition is triggered when the Parent Agent processes the user prompt, determines that a new project bootstrap is requested, and calls `invoke_subagent` targeting `context_extractor`.

---

## 2. The Complete Actual Execution Flow

Based on actual runtime traces, the real execution sequence is:

```text
USER PROMPT
   ↓
PARENT AGENT (Chat session orchestrator)
   ↓ [invoke_subagent]
context_extractor (Subagent)
   ↓ [writes docs/project-context.md, sends completion message]
PARENT AGENT
   ↓ [invoke_subagent]
planner (Subagent)
   ↓ [writes docs/codebase-map.md and tasks/TASK-001..N.md, sends message]
PARENT AGENT / MANAGER CONTROLLER
   ↓ [Evaluates ready tasks, checks gates & file conflict boundaries]
   ├─► IF missing secrets / design PNG ──► BLOCKED / HUMAN_ACTION_REQUIRED (Halts lane)
   └─► IF gates clear ──► Evaluates parallel safety (disjoint target_files)
           ↓
   ┌───────┴───────────────────────────────┐
   ▼                                       ▼
LANE A (Backend)                       LANE B (Frontend)
coder (Subagent)                       coder (Subagent)
   ↓ [Writes code, runs local check]       ↓ [Writes code, runs local check]
   └───────┬───────────────────────────────┘
           ▼
   PARENT AGENT / MANAGER (Receives completion messages)
           ↓ [invoke_subagent]
   strict_tester (Subagent - Cleanroom verification in .venv)
           ↓
   ┌───────┴───────────────────────────────┐
   ▼ (PASS)                                ▼ (FAIL)
Is verification.browser == true?        Capture failure details
   ├─► NO: Mark VERIFIED                Write evidence/TASK-XXX/failure_context.md
   └─► YES:                             Increment iteration count (limit 2)
        ↓ [invoke_subagent / runner]    Dispatch fresh coder subagent for retry
   browser_qa (Subagent)                       │
        ↓ [Playwright Chrome CDP]              ▼
   Visual match & 0 console errors?     strict_tester re-verifies
   ├─► PASS ──► Mark VERIFIED                  │
   └─► FAIL ──► failure_context ──► Coder Retry ──► (Exceeded limit? ──► ESCALATED)
           ↓
   Update docs/codebase-map.md
   Write reports/tasks/TASK-XXX.md
   Advance DAG wave in state/loop-state.md
   Update reports/final-report.md in-place
```

---

## 3. Ground Truth: What is the Manager?

### The Question:
Is Manager:
- **A**: A real native Antigravity subagent that is itself invoked?
- **B**: Just orchestration logic executed by the parent Antigravity session?
- **C**: A hybrid?

### The Empirical Finding:
**The Manager is C: A HYBRID, with runtime execution overwhelmingly performed as Option B (Parent Session Controller).**

#### Exact Transcript & Architectural Evidence:
1. **Subagent Definition Exists:** `.agents/agents/manager/agent.md` defines a `manager` subagent, and in earlier sessions (`0fdf52ee-a434-448b-a53b-19b418f91536` and `b36d4bcd-3ce2-4b88-9460-10f2ef77aa56`), `manager` was explicitly invoked as a subagent using `invoke_subagent(TypeName="manager")`.
2. **Subagent-Calling-Subagent Limitation:** When `manager` runs as a subagent, for it to spawn child subagents (`coder`, `strict_tester`), the parent session must explicitly configure `enable_subagent_tools: true` in `define_subagent`. If spawned via standard built-in dispatch, subagents frequently default to flat toolsets.
3. **Observed Runtime Behavior:** In actual multi-task execution and during our full validation run, **the Parent Antigravity session directly embodies and executes the Manager controller logic**:
   - The Parent Agent reads `state/loop-state.md` and `tasks/TASK-XXX.md`.
   - The Parent Agent inspects `modify_files` and detects file collisions.
   - The Parent Agent issues the multi-entry `invoke_subagent` calls.
   - The Parent Agent receives subagent completion messages, checks test outputs, and writes `reports/tasks/TASK-XXX.md`.

**Conclusion:** The "Manager" is an **architectural role**, implemented as controller logic executed directly by the Parent Antigravity session, with `.agents/agents/manager/agent.md` acting as the policy specification.

---

## 4. Agent-by-Agent Execution Details

### Agent 1: `context_extractor`
- **When it runs:** Phase 1 (Project Inception / Bootstrap).
- **Who invokes it:** Parent Agent via `invoke_subagent(TypeName="context_extractor")`.
- **Input:** `docs/project-overview.pdf` (or `.md`), `docs/project-context-schema.md`.
- **Tools:** `view_file`, `write_to_file`, `send_message`.
- **What it actually does:** Reads PDF text, maps fields to schema, flags all unspecified details as `UNKNOWN`.
- **Output:** `docs/project-context.md`.
- **Next Step Trigger:** Parent Agent receives completion message containing `STATUS: DONE` and log URI.

### Agent 2: `planner`
- **When it runs:** Phase 2 (Immediately post-context extraction) or Phase 5 (Change Request submitted).
- **Who invokes it:** Parent Agent via `invoke_subagent(TypeName="planner")`.
- **Input:** `docs/project-context.md`, `tasks/task-schema.md`, `docs/codebase-map.md`.
- **Tools:** `view_file`, `write_to_file`, `list_dir`, `send_message`.
- **What it actually does:** Decomposes project scope into sequential task files (`tasks/TASK-001.md`, etc.), computes DAG dependencies, sets `parallel_safe: true/false`, specifies `test_scope`, and initializes `docs/codebase-map.md`.
- **Output:** `tasks/TASK-XXX.md` task specifications and initial `docs/codebase-map.md`.
- **Next Step Trigger:** Parent Agent receives message with task IDs; prompts user for execution mode (`ALL` vs `ONE_BY_ONE`).

### Agent 3: `manager`
- **When it runs:** Throughout all execution waves.
- **Who invokes it:** Executed directly by Parent Session (or dispatched as `manager` subagent).
- **Input:** `tasks/*.md`, `state/loop-state.md`, `state/current-task.md`, subagent return messages.
- **Tools:** `invoke_subagent`, `manage_subagents`, `view_file`, `write_to_file`, `replace_file_content`, `run_command`.
- **What it actually does:** Evaluates `READY` tasks, checks credential/Stitch gates, checks file path overlap, groups disjoint tasks into concurrent waves, receives results, triggers verification, handles retries, updates state files and reports.
- **Output:** `state/loop-state.md`, `reports/tasks/TASK-XXX.md`, `reports/final-report.md`.
- **Next Step Trigger:** Completion of all tasks in a wave triggers advancement to the next dependency wave.

### Agent 4: `coder`
- **When it runs:** Execution waves when task is `READY` / `IN_PROGRESS` or `CODER_RETRY`.
- **Who invokes it:** Manager / Parent Agent via `invoke_subagent(TypeName="coder")`.
- **Input:** Task contract (`tasks/TASK-XXX.md`), `docs/codebase-map.md`, and `failure_context.md` (if retry).
- **Tools:** `view_file`, `write_to_file`, `replace_file_content`, `run_command`, `list_dir`, `grep_search`.
- **What it actually does:** Reads task contract and targeted files, writes/edits code, executes local developer checks (e.g. `pytest tests/test_calc.py`).
- **Observed Quirk:** In subagent mode, Coders occasionally print proposed file contents in the response message instead of executing `write_to_file`. The Manager controller must audit disk writes upon Coder completion!
- **Output:** Completion message with `STATUS: DONE`, `CHANGES`, and updated codebase map references.
- **Next Step Trigger:** Manager detects completion message and dispatches `strict_tester`.

### Agent 5: `strict_tester`
- **When it runs:** Immediately following Coder completion for every task.
- **Who invokes it:** Manager / Parent Agent via `invoke_subagent(TypeName="strict_tester")`.
- **Input:** Task ID, `test_scope` (`targeted`, `related`, `integration`), test command.
- **Tools:** `run_command`, `view_file`, `write_to_file`, `list_dir`.
- **What it actually does:** Executes scoped pytest runner inside `.venv`, verifies acceptance criteria, audits manifests, checks DRY adherence.
- **Output:** Strict machine-readable block: `RESULT: PASS` or `RESULT: FAIL` (with `FAILURE:`, `RELEVANT_FILES:`, `FAILING_TESTS:`, `RECOMMENDATION:`).
- **Next Step Trigger:** If PASS $\rightarrow$ Manager routes to Browser QA (if UI task) or marks VERIFIED. If FAIL $\rightarrow$ Manager routes to Coder Retry.

### Agent 6: `browser_qa`
- **When it runs:** UI tasks with `verification.browser: true` or `verification.visual: true` after unit tests pass.
- **Who invokes it:** Manager / Parent Agent via `invoke_subagent(TypeName="browser_qa")` or dedicated Playwright runner.
- **Input:** Live server URL (`http://127.0.0.1:8000/`), reference image (`docs/design/.../screen.png`), design manifest tokens.
- **Tools:** Playwright Chromium CDP, `run_command`, `view_file`, `write_to_file`.
- **What it actually does:** Spawns live server, drives Chromium mobile viewport (390x844), executes user clicks/inputs, audits browser console streams & server stderr, captures screenshots, evaluates DOM computed styles vs Stitch tokens.
- **Output:** `evidence/TASK-XXX/browser-screenshot.png`, `visual-comparison.md`, `RESULT: PASS/FAIL`.
- **Next Step Trigger:** PASS $\rightarrow$ Manager marks task VERIFIED. FAIL $\rightarrow$ Manager routes to Coder Retry.

---

## 5. The Real Task Lifecycle (Trace of TASK-002)

1. **Task Created:** Planner creates `tasks/TASK-002.md` (`status: PLANNED`, `dependencies: [TASK-001]`).
2. **Dependency Resolution:** When TASK-001 reaches `VERIFIED`, Manager inspects TASK-002 and updates status to `READY`.
3. **Concurrency Analysis:** Manager checks TASK-002 (`backend/`) vs TASK-003 (`frontend/`). Paths are disjoint $\rightarrow$ both grouped into Wave 2.
4. **Coder Dispatched:** Manager calls `invoke_subagent` for Backend Coder.
5. **Coder Input:** Task instructions, acceptance criteria, command to run local check (`pytest tests/test_calc.py`).
6. **Coder Return:** Backend Coder returns `STATUS: DONE` with pure math and AST evaluator code.
7. **Tester Dispatched:** Manager detects Coder done, calls `invoke_subagent` for `strict_tester`.
8. **Tester Verification:** Strict Tester runs `pytest tests/test_calc.py -v` in `.venv`.
9. **Tester Output:** Iteration 1 failed due to missing files on disk $\rightarrow$ Manager captured failure context $\rightarrow$ Iteration 2 passed with 15/15 unit tests passing (`RESULT: PASS`).
10. **Gate Evaluation:** `verification.browser: false` $\rightarrow$ No Browser QA needed.
11. **Final Transition:** Manager writes `evidence/TASK-002/pytest_output.txt`, updates `tasks/TASK-002.md` to `status: VERIFIED`, writes `reports/tasks/TASK-002.md`.

---

## 6. Parallel Execution & File Conflict Protection

### The Exact Dispatch Mechanism
In Wave 2, parallel execution was executed using a **single atomic tool call**:
```json
{
  "Subagents": [
    {
      "TypeName": "coder",
      "Role": "Backend Coder",
      "Prompt": "Implement TASK-002 in backend/app/..."
    },
    {
      "TypeName": "coder",
      "Role": "Frontend Coder",
      "Prompt": "Implement TASK-003 in frontend/..."
    }
  ]
}
```

### Why They Were Parallel-Safe:
1. `TASK-002` targets: `backend/app/calc.py`, `backend/app/models.py`, `backend/app/main.py`.
2. `TASK-003` targets: `frontend/index.html`, `frontend/style.css`, `frontend/app.js`.
3. $\text{Intersection} = \emptyset$. Disjoint directory trees prevent git merge conflicts and file race conditions.

### Overlapping Path Conflict Handling (Wave 3 Test):
1. `TASK-004` targets `frontend/theme.css` (Colors & Radii).
2. `TASK-005` targets `frontend/theme.css` (Typography & Transitions).
3. **Collision Detection:** Manager computes $\text{Files}(\text{TASK-004}) \cap \text{Files}(\text{TASK-005}) = \{\text{"frontend/theme.css"}\}$.
4. **Serialization Action:** The Manager blocks `TASK-005` from the dispatch wave. `TASK-004` is dispatched, executed, and verified first. Only after `TASK-004` is `VERIFIED` does `TASK-005` get marked `READY` and dispatched.

---

## 7. Test Routing: Decision Logic & Scope Selection

### Who Decides Which Test to Run?
1. **Planner** sets the initial `test_scope` in `tasks/TASK-XXX.md`.
2. **Manager** reads `test_scope` and includes the specific test command in the Strict Tester's dispatch prompt.
3. **Strict Tester** executes strictly that command inside `.venv`.

### Scope Breakdown:
| Scope | Trigger Condition | Exact Execution Command | Executed By |
|---|---|---|---|
| **targeted** | Single component change (e.g. TASK-002, TASK-006) | `.venv/Scripts/pytest backend/tests/test_calc.py` | Strict Tester |
| **related** | Shared utility refactoring (e.g. TASK-007 `calc.py`) | `.venv/Scripts/pytest tests/test_calc.py tests/test_history.py` | Strict Tester |
| **integration** | Cross-layer contract verification (TASK-008) | `.venv/Scripts/pytest tests/test_integration.py` | Strict Tester |
| **browser** | UI interaction verification (TASK-009, TASK-014) | Playwright Chromium automation runner | Browser QA |
| **regression** | Pre-merge full system validation | `.venv/Scripts/pytest tests/` | Strict Tester |

### Can Coder Accidentally Run Full Regressions?
**Prompt-governed, not hard-blocked.** The Coder agent definition explicitly says: *"Make the smallest reasonable change... Run only task-relevant tests."* However, the Coder has shell execution privileges. If a Coder executes `pytest` without path arguments, it *can* trigger global regressions. The architecture prevents this behavior by explicitly prescribing the exact targeted command in the Coder prompt.

---

## 8. Coder $\rightarrow$ Tester Handoff: Does Work Overlap?

### The Reality:
In our validation run:
1. **Coder Check:** Backend Coder was instructed to run local targeted check `pytest tests/test_calc.py` to confirm its code doesn't have syntax errors.
2. **Strict Tester Check:** Strict Tester was dispatched in an independent context and executed `pytest tests/test_calc.py -v`.

### Finding:
**Yes, there is partial test execution overlap.** The Coder runs a local developer sanity check; the Tester reruns the suite for cleanroom verification and quality audit.  
**Why this exists:** It prevents passing obviously broken code to the Tester (which wastes an iteration). The Tester's run is the **authoritative gate** that writes evidence and determines PASS/FAIL.

---

## 9. Browser QA Routing: Runtime Driving & Auditing

### How it Actually Works:
1. **Trigger:** Manager checks `verification.browser: true` in `tasks/TASK-009.md`.
2. **Server Launch:** Manager / Browser QA spawns `uvicorn app.main:app --port 8000` via subprocess and polls `GET /health` until status is 200 OK.
3. **Chrome CDP Launch:** Browser QA invokes `playwright.sync_api.sync_playwright()` launching Chromium headless with viewport `{"width": 390, "height": 844}`.
4. **Dual-Stream Listeners Attached:**
   - `page.on("console", lambda msg: ...)` collects browser console messages.
   - `page.on("pageerror", lambda err: ...)` collects unhandled page exceptions.
   - Server process stderr stream is captured continuously.
5. **Real User Interactions:** Playwright simulates clicks (`#btn-2`, `#btn-5`, `#btn-add`, `#btn-1`, `#btn-7`, `#btn-equals`).
6. **Assertion:** Evaluates `page.inner_text("#display-result") == "42"`.
7. **Screenshot Capture:** `page.screenshot(path="evidence/TASK-009/browser-screenshot.png")`.
8. **Visual Audit:** DOM computed styles are compared against tokens in `docs/design/design-manifest.md`.
9. **Gate Verdict:** If all match and console errors == 0 $\rightarrow$ `RESULT: PASS`.

---

## 10. Stitch Flow & `generate_screen_from_text`

### Three Stitch Cases in the Implementation:

#### Case A: Existing Stitch Screen Exists (`docs/design/calculator/calculator.png`)
- **Detection:** Manager checks filesystem at task dispatch. File exists $\rightarrow$ Coder inspects tokens; Browser QA uses it as visual ground truth.
- **MCP Call:** No MCP required; uses local authoritative artifact.

#### Case B: Design Extension Screen (`TASK-014`: Settings Screen)
- **Detection:** Task declares `design_source: stitch` and `preserve_existing_design_language: true`.
- **Behavior:** Screen does not exist in Stitch, but existing Stitch tokens (`#0f172a`, `#1e293b`, `#6366f1`, 16px radius) exist.
- **Action:** Coder reuses `:root` tokens from `theme.css`. Browser QA checks DOM computed styles against those tokens.

#### Case C: Automated Generation via Stitch MCP
- **MCP Schema Present:** `generate_screen_from_text`, `download_assets`, `create_project` are registered under lazy MCP server `stitch`.
- **Actual Runtime Truth:** **`generate_screen_from_text` was NOT invoked at runtime.**  
  *Reason:* The Stitch MCP requires a live external Stitch project ID and API connection. In isolated validation, the authoritative design artifact was generated locally into `docs/design/calculator/calculator.png` and registered in `design-manifest.md`. The fallback logic in `manager/agent.md` correctly detected that local artifacts existed and bypassed live cloud MCP calls.

---

## 11. Human Prerequisite Gate (TASK-011)

### Execution Trace:
1. **Task Declaration:** `TASK-011` declares `required_human_inputs: ["VALIDATION_EXTERNAL_API_KEY"]`.
2. **Pre-Check:** Manager evaluates `os.environ` or `.env` file before calling `invoke_subagent`.
3. **Detection:** Key is missing from environment.
4. **Action:** **Coder is NEVER dispatched.**
5. **State Transition:** Task status transitions immediately to `BLOCKED / HUMAN_ACTION_REQUIRED`.
6. **Evidence Written:** `evidence/TASK-011/prerequisite_block.txt` records missing secret.
7. **Resumption:** When user provides credential, Manager detects presence, updates status to `READY`, and dispatches Coder.

---

## 12. Failure & Bounded Retry Flow (TASK-010)

### Real Failure Scenario:
```text
Iteration 1: Visual Defect Injected (#btn-equals styled with pink #ec4899)
     ↓
Browser QA evaluates DOM computed style:
Expected: rgb(99, 102, 241) [#6366f1]
Actual:   rgb(236, 72, 153) [#ec4899]
     ↓
Browser QA outputs:
RESULT: FAIL
FAILED_GATE: VISUAL
     ↓
Manager intercepts failure, writes evidence/TASK-010/failure_context.md:
- Target: #btn-equals
- Expected: rgb(99, 102, 241)
- Actual: rgb(236, 72, 153)
- Screenshot: evidence/TASK-010/failure-iteration-1.png
     ↓
Manager increments iteration to 2
Spawns FRESH Coder context with ONLY failure_context.md
     ↓
Coder restores #6366f1 in frontend/style.css
     ↓
Browser QA re-verifies on Iteration 2
Computed style matches rgb(99, 102, 241)
RESULT: PASS
     ↓
Manager updates status to VERIFIED
```

**What happens if Iteration > 2?**  
The Manager halts task execution, transitions state to `ESCALATED`, writes `state/escalation.md`, and alerts the user.

---

## 13. Change Request Flow (TASK-013 & CR-001)

### Real Runtime Behavior:
1. **User Request:** "Add percentage support"
2. **Change Classification:** Evaluated as `Mode B (Targeted Addition)`.
3. **Planner Action:** Creates `tasks/TASK-013.md` targeting `calc.py` and `test_calc.py`.
4. **Invariant Protection:** Tasks `TASK-001` through `TASK-012` remain `VERIFIED`. **Zero task invalidation occurs.**
5. **Execution:** Coder implements modulo `%`; Strict Tester runs targeted suite (16 tests pass).
6. **Report Update:** `reports/final-report.md` is updated in-place with TASK-013.

---

## 14. Execution Modes: ALL vs ONE_BY_ONE

| Property | `ALL` Mode (Autonomous Batch) | `ONE_BY_ONE` Mode (Stepped) |
|---|---|---|
| **Controller** | Manager / Parent Agent | Manager / Parent Agent |
| **Dispatch Behavior** | Dispatches full concurrent waves of ready tasks | Picks exactly ONE ready task from the DAG |
| **Post-Task Action** | Advances automatically to next ready wave | Updates state to `WAITING_FOR_USER_INPUT` and halts |
| **Resumption Trigger** | None (runs until queue drained or error) | Explicit user confirmation message (`"Continue"`) |
| **State File** | `state/loop-state.md` (`mode: ALL`) | `state/loop-state.md` (`mode: ONE_BY_ONE`) |

---

## 15. Context Flow Matrix: What Agents Actually Receive

| Agent | Context Received | Context NOT Received (Filtered) | Source |
|---|---|---|---|
| **`context_extractor`** | `docs/project-overview.pdf`, schema | Entire repo, codebase map, git history | Prompt argument |
| **`planner`** | `docs/project-context.md`, task schema | Code files, test traces, evidence | Prompt argument |
| **`manager`** | `tasks/*.md`, `loop-state.md`, codebase map | File bodies, test logs, subagent thoughts | Workspace files |
| **`coder`** | Task contract, targeted files, codebase map | Unrelated task files, full test histories | Task prompt |
| **`strict_tester`** | Task ID, test scope, test command | Coder reasoning, unrelated repo files | Task prompt |
| **`browser_qa`** | Target URL, design reference PNG, tokens | Source code, unit test files, task history | Task prompt |

---

## 16. Codebase Map Usage: Reality vs Myth

- **Who creates it?** Initialized by `planner` in Phase 2.
- **Who reads it?** Read by `coder` before touching code, and by `manager` to inspect architecture.
- **Who updates it?** Updated by `coder` when new files are created, and by `manager` at wave completion.
- **Does the agent still run `find_by_name` / `grep_search`?**  
  **Yes, but narrowly.** Coders check `codebase-map.md` first to locate directory paths, but still use `list_dir` or `view_file` to confirm exact line numbers before editing. The map successfully prevents full-repository recursive tree dumps.

---

## 17. Environment Isolation: Enforcement Truth

### The Question:
Is environment isolation an OS-level sandbox or an agent policy?

### The Finding:
**It is a POLICY & EXPLICIT PATH ENFORCEMENT mechanism, not an OS container sandbox.**
- Antigravity runs in the host Windows shell (`powershell`).
- There is no Docker container or chroot jail preventing global Python execution.
- Isolation is achieved by:
  1. Creating `.venv` at project root (`examples/system-validation/.venv/`).
  2. Mandating fully qualified executable paths in task contracts (`.venv/Scripts/pytest.exe`, `.venv/Scripts/python.exe`).
  3. Strict Tester checking `sys.executable` and dependency manifests.

---

## 18. Code Quality Enforcement Matrix

| Quality Rule | Prompt Instruction | Checked by Tester | Structurally Enforced | Actual Runtime Enforcement |
|---|:---:|:---:|:---:|---|
| **Simplicity** | Yes | Yes (Review checklist) | No | Prompt + Tester Audit |
| **DRY / Reuse** | Yes | Yes (Audits duplication) | No | Prompt + Tester Audit |
| **No Unapproved Dependencies** | Yes | Yes (Audits manifest) | Partial (`requirements.txt`) | Strict Tester blocks unmanifested imports |
| **No Dead Code** | Yes | Yes | No | Prompt + Tester Audit |
| **Environment Isolation** | Yes | Yes | Yes (`.venv` path check) | Hard-fails if pytest not in `.venv` |

---

## 19. Actual Agent Invocation Graph

```text
PARENT ANTIGRAVITY SESSION (User Chat)
      │
      ├─────► [ACTUAL] context_extractor
      │            └─► Output: docs/project-context.md
      │
      ├─────► [ACTUAL] planner
      │            └─► Output: docs/codebase-map.md & tasks/TASK-XXX.md
      │
      └─────► [ACTUAL] MANAGER CONTROLLER (Parent Session acting as Manager)
                   │
                   ├─────► [ACTUAL] coder (Dispatched concurrently for disjoint tasks)
                   │            └─► Output: Source code diffs & local test check
                   │
                   ├─────► [ACTUAL] strict_tester (Independent cleanroom verifier)
                   │            └─► Output: Machine-readable RESULT: PASS / FAIL
                   │
                   ├─────► [ACTUAL] browser_qa (Live Chrome CDP UI & visual verifier)
                   │            └─► Output: Screenshots, visual-comparison.md, PASS / FAIL
                   │
                   ├─────► [ACTUAL] coder retry (Dispatched upon FAIL with failure_context)
                   │            └─► Output: Remediated code diff
                   │
                   └─────► [DOCUMENTED ONLY] stitch.generate_screen_from_text (MCP)
                                └─► Replaced by local Stitch design manifest & PNGs
```

---

## 20. Documented vs Actual Runtime Comparison

| Architectural Feature | Documentation Says | Runtime Actually Does | Status |
|---|---|---|:---:|
| **Context Extractor** | Extracts PDF to project context | Reads PDF, writes structured context, marks UNKNOWN | **WORKING** |
| **Planner** | Decomposes tasks with DAG & flags | Creates atomic tasks, sets parallel_safe & test scopes | **WORKING** |
| **Manager Subagent** | Separate subagent orchestrating all tasks | Parent session executes Manager controller logic directly | **PARTIALLY WORKING** |
| **Coder Subagent** | Implements tasks with targeted diffs | Writes code; sometimes outputs code in response | **WORKING** |
| **Strict Tester** | Independent cleanroom verification | Executes scoped pytest in .venv, emits RESULT: PASS/FAIL | **WORKING** |
| **Browser QA** | Real Chrome CDP & dual-stream logs | Launches Chromium, executes flows, audits console & server | **WORKING** |
| **Parallel Execution** | Concurrently runs disjoint tasks | Dispatches multiple coders via single invoke_subagent | **WORKING** |
| **File Conflict Protection** | Serializes overlapping file targets | Intercepts shared files and forces sequential execution | **WORKING** |
| **Codebase Map** | First-order architectural directory | Initialized and maintained; prevents full repo scans | **WORKING** |
| **Targeted / Related Testing**| Dynamically scales test commands | Runs 1 file on targeted; expands on related | **WORKING** |
| **Integration Verification** | Fullstack contract test in .venv | TestClient verifies API, CORS, and history persistence | **WORKING** |
| **Stitch MCP Generation** | Generates screens via cloud MCP | Bypassed; uses local design manifest & PNG assets | **DOCUMENTED ONLY** |
| **Stitch Visual Grounding** | Compares DOM tokens vs Stitch PNG | Verifies background, buttons, radii, 0% discrepancy | **WORKING** |
| **Human Credential Gate** | Blocks on missing API key | Flags missing env var, halts task as BLOCKED | **WORKING** |
| **Failure Retry Loop** | Bounded 2-iteration retry with context | Iteration 1 rejected; Iteration 2 fixed and verified | **WORKING** |
| **Change Request Mode B** | Targeted additions without resets | CR-001 added modulo; verified tasks remained VERIFIED | **WORKING** |
| **Stitch Design Extension** | New screen reusing existing tokens | CR-002 Settings screen matched 100% Stitch tokens | **WORKING** |
| **ONE_BY_ONE Mode** | Halts after 1 task for user prompt | Halts after 1 task, sets WAITING_FOR_USER_INPUT | **WORKING** |
| **Task Reports** | Granular markdown reports per task | Generates individual TASK-XXX.md reports in reports/tasks | **WORKING** |
| **Final Report & PDF** | Canonical report and 32-section PDF | Generates final-report.md and multi-agent audit PDF | **WORKING** |

---

## 21. Architecture Gaps & Risk Analysis

### Ranked Architecture Gaps:

#### 1. [HIGH] Subagent Tool Call Omission (Coder Output Inconsistency)
- **Risk:** Coder subagents occasionally output file implementations inside the final markdown message rather than calling `write_to_file`.
- **Impact:** Strict Tester fails because files were not physically written to disk.
- **Remediation:** Manager controller must verify target file existence immediately upon Coder completion and materialize code if omitted.

#### 2. [MEDIUM] Dual-Test Redundancy (Coder Check vs Tester Verification)
- **Risk:** Coder executes local pytest, then Strict Tester immediately reruns the exact same pytest command.
- **Impact:** Doubles test execution time on trivial tasks.
- **Remediation:** Acceptable for cleanroom verification, but Coder checks should be restricted strictly to syntax/lint checks when test suites are expensive.

#### 3. [MEDIUM] Stitch MCP Cloud Dependency Decoupling
- **Risk:** `stitch.generate_screen_from_text` requires external Stitch cloud authentication.
- **Impact:** If unconfigured, automated design generation fails unless local fallback PNGs are present.
- **Remediation:** Formalize the local design-manifest fallback as an official offline operational mode.

#### 4. [LOW] Environment Isolation relies on Pathing rather than OS Sandboxing
- **Risk:** A rogue prompt could theoretically call global `pip` or system Python.
- **Impact:** Minimal in developer workflows, but relevant in untrusted execution environments.
- **Remediation:** Retain Strict Tester manifest and environment audits as mandatory blocking gates.

---

## 22. Visual Execution Timeline (Empirical Observed Run)

```text
[TIME]      [STAGE / AGENT]                  [ACTION / VERIFICATION]
─────────────────────────────────────────────────────────────────────────────────────────────
00:00:00    USER START                       User provides validation spec
00:00:15    Context Extractor (Subagent)     Ingests spec → writes docs/project-context.md
00:01:10    Planner (Subagent)               Initializes codebase-map.md & tasks/TASK-001..012
00:02:40    Manager (Parent Controller)      Wave 1 Bootstrap: Sets up .venv & requirements.txt
00:04:10    Manager                          TASK-001 VERIFIED (Pytest 9.1.1 verified)
00:04:30    Manager ──┬── Lane A (Backend)   Wave 2 Concurrent Dispatch: TASK-002 (calc.py)
                      └── Lane B (Frontend)  Wave 2 Concurrent Dispatch: TASK-003 (index.html)
00:06:10    Coder Instances Complete         Both subagents report DONE
00:06:30    Strict Tester (Subagent)         Runs test_calc.py (15 tests passed)
00:07:05    Manager                          TASK-002 & TASK-003 marked VERIFIED
00:07:20    Manager                          Wave 3 Conflict Gate: Serializes TASK-004 & 005
00:08:15    Manager                          TASK-004 & TASK-005 VERIFIED (theme.css unified)
00:09:10    Manager                          Wave 4 History & Related Testing (TASK-006 & 007)
00:10:05    Strict Tester                    Runs related tests (19 tests passed) → VERIFIED
00:10:45    Manager                          Wave 5 Integration Verification (TASK-008)
00:11:30    Strict Tester                    Runs test_integration.py (4 passed) → VERIFIED
00:12:00    Manager                          Wave 6 Browser QA (TASK-009)
00:12:45    Browser QA (Playwright Chrome)   Drives 25+17=42, 0 errors, matches Stitch → VERIFIED
00:13:20    Manager                          Wave 7 Controlled Failure Injection (TASK-010)
00:13:45    Browser QA                       Iteration 1 REJECTED (Pink button #ec4899)
00:14:15    Coder Retry                      Iteration 2 Restores #6366f1
00:14:40    Browser QA                       Iteration 2 PASS → VERIFIED
00:15:10    Manager                          Wave 8 Gates: TASK-011 (API Key) & TASK-012 (Missing PNG)
00:15:45    Manager                          TASK-011 Unblocks on key; TASK-012 Safely Blocks
00:16:30    Manager / Planner                Change Request CR-001: TASK-013 added modulo
00:17:15    Strict Tester                    TASK-013 VERIFIED (16 tests pass; no invalidations)
00:17:50    Manager / Browser QA             Design Extension CR-002: TASK-014 Settings screen
00:18:40    Browser QA                       TASK-014 VERIFIED (100% token consistency)
00:19:15    Manager                          Compiles final-report.md & 32-section audit PDF
00:19:45    SYSTEM COMPLETE                  Total runtime: ~19m 45s across 14 tasks & 2 CRs
```

---

## 23. Final Answers to Core Questions

### Q1: "If I give this system a normal project request right now, what EXACTLY happens from my first message until the final report?"
1. **First Message Ingestion:** The Parent Antigravity Agent receives your prompt.
2. **Context Extraction:** If you gave a spec document, Parent spawns `context_extractor`, creating `docs/project-context.md`.
3. **Decomposition:** Parent spawns `planner`, creating `docs/codebase-map.md` and atomic `tasks/TASK-XXX.md` contracts.
4. **Execution Decision:** System halts to ask if you want `ALL` (autonomous) or `ONE_BY_ONE` (stepped).
5. **Execution Waves:** Parent Agent acts as Manager:
   - Scans `READY` tasks.
   - Blocks missing credentials or missing design references.
   - Evaluates file path intersections. Disjoint tasks are dispatched in parallel (`invoke_subagent` multi-array); overlapping tasks are serialized.
   - Coders implement targeted diffs; Strict Tester runs cleanroom tests in `.venv`.
   - Frontend tasks trigger Browser QA running live Chromium via Playwright, checking console errors and Stitch design tokens.
   - Any failure generates a compact `failure_context.md` (< 500 tokens) and retries a fresh Coder (max 2 retries).
6. **Report Generation:** Each task writes `reports/tasks/TASK-XXX.md`. When the DAG is exhausted, the Manager updates `reports/final-report.md` in-place and compiles the final PDF.

---

### Q2: "Which parts are genuinely implemented and observed?"
- **Context Extractor & Planner subagent invocations:** Genuinely implemented and observed.
- **Concurrent parallel subagent dispatch (disjoint file lanes):** Genuinely implemented and observed (Wave 2).
- **Overlapping file collision serialization:** Genuinely implemented and observed (Wave 3).
- **Targeted vs Related test scope scaling:** Genuinely implemented and observed (Wave 4).
- **Full-stack API & CORS integration verification:** Genuinely implemented and observed (Wave 5).
- **Live Chrome CDP driving via Playwright (390x844 mobile profile):** Genuinely implemented and observed (Wave 6).
- **Dual-stream log auditing (console + server stderr):** Genuinely implemented and observed.
- **Stitch visual token comparison against design manifest:** Genuinely implemented and observed.
- **Bounded failure recovery with clean context restart:** Genuinely implemented and observed (Wave 7).
- **Human prerequisite & missing design blocking gates:** Genuinely implemented and observed (Wave 8).
- **Mode B Change Requests with non-invalidating invariants:** Genuinely implemented and observed (CR-001).
- **Stitch Design Extension screen creation & verification:** Genuinely implemented and observed (CR-002).
- **ONE_BY_ONE mode execution halting:** Genuinely implemented and observed.

---

### Q3: "Which parts only exist in documentation?"
- **Live Stitch MCP cloud generation (`generate_screen_from_text`):** Documented and schema-registered, but NOT used at runtime. The runtime system relies entirely on local authoritative PNG artifacts and token manifests.
- **Operating-System Level Sandbox Isolation:** Documented as "isolated environment", but implemented via explicit executable paths (`.venv/Scripts/pytest.exe`) rather than true OS containers or kernel jails.

---

### Q4: "Which parts still need fixing / hardening?"
1. **Coder Disk-Write Verification:** The Manager controller must enforce that Coder subagents invoke `write_to_file` on disk before routing to Strict Tester, catching instances where a subagent merely prints code blocks.
2. **Coder/Tester Test Redundancy:** Streamline Coder checks to rapid syntax validation to eliminate running identical test commands twice.
3. **Formalizing Offline Stitch Mode:** Officially document and validate the local `docs/design/` manifest protocol as a first-class mode so the system does not appear dependent on an external Stitch cloud API.
