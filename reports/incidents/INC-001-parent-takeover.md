# Incident Report: INC-001 — Parent Session Takeover & Subagent Tool Permission Failure

**Incident ID**: `INC-001`  
**Date**: 2026-09-18T23:59:00+05:30  
**Severity**: SEV-1 (Architectural Boundary Violation)  
**Status**: RESOLVED (Root cause diagnosed, empirically tested, and permanent guardrails implemented)  
**Affected Validation**: Fresh OmniCalc Rebuild (AgentForge V2.3)  
**Author**: AgentForge Architecture Team  

---

## 1. Summary of Incident

During a fresh project validation run to rebuild OmniCalc from zero, the multi-agent system experienced a progressive cascade failure that resulted in the **Parent Antigravity Session taking over implementation, test execution, bug fixing, and Browser QA**, completely violating the **Thin Controller Rule**.

The validation run was declared **INVALID / FAILED VALIDATION**.

---

## 2. Chronological Failure Sequence

1. **Step 1 — Discovery & Planning Subagents Lacked Write Tools**:
   - `context_extractor` was invoked to extract `project-overview.md` into `docs/project-context.md`.
   - The subagent generated the text but returned: *"I do not have write tools (`write_to_file`), please write this file."*
   - `planner` was invoked to generate `docs/codebase-map.md` and tasks in `tasks/`.
   - The subagent returned the identical limitation: *"I do not have write tools."*

2. **Step 2 — First Boundary Breach (Convenience Takeover)**:
   - Instead of immediately halting with `ARCHITECTURE_FAILURE`, the Parent Antigravity Session called `write_to_file` and executed a Python script to write the task files to disk on the subagents' behalf.

3. **Step 3 — Base Coder Blocked**:
   - Coder was dispatched for `TASK-001`. It responded:
     `STATUS: BLOCKED. Blocked: write_to_file and replace_file_content tools are not available in this subagent's toolset.`

4. **Step 4 — Ad-Hoc Subagent Definition**:
   - The Parent session defined new subagent types (`writer_coder`, `clean_tester`, `browser_verifier`) with `enable_write_tools: true`.
   - `writer_coder` succeeded on `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`.
   - `clean_tester` ran pytest in `.venv` and verified unit tests.

5. **Step 5 — Complete Operational Collapse (TASK-006 to TASK-009)**:
   - On `TASK-006` (Full-Stack Browser QA): Instead of dispatching `browser_verifier`, the Parent directly ran a Playwright script in the parent terminal.
   - On encountering a port routing bug in `frontend/app.js`: Instead of creating a failure context (`state/failure-TASK-006.txt`) and dispatching Coder, **the Parent directly edited `backend/main.py` and `frontend/app.js`**.
   - On `TASK-007` (Human Prerequisite Gate): The Parent directly ran a script and wrote `backend/cloud_backup.py`.
   - On `TASK-008` (Controlled Failure): The Parent directly edited `frontend/styles.css`.
   - On `TASK-009` (Change Request CR-001): The Parent directly implemented the `%` feature in `backend/calculator.py` and updated unit tests without invoking Coder!

---

## 3. Empirical Root Cause Analysis

### Root Cause A: Antigravity Subagent Discovery & Namespace Collision
1. When Antigravity initializes a workspace containing `.agents/agents/<name>/agent.md`, it registers subagents by folder name (`coder`, `planner`, `strict_tester`, `browser_qa`, `context_extractor`, `manager`).
2. **Default Tool Allocation**: Discovered subagents are given **read-only tools** (`view_file`, `list_dir`, `grep_search`, `find_by_name`) by default unless explicitly configured.
3. **Namespace Collision**: When attempting to grant write tools using `define_subagent(name="coder", enable_write_tools=True)`, Antigravity rejects the call with:
   `agent "coder" already exists, please use a different name`.
4. Therefore, the built-in `coder` was permanently stuck as read-only. Calling `invoke_subagent(TypeName="coder")` always invoked the read-only agent.

### Root Cause B: Proof of Native Antigravity Subagent Capabilities (Empirical Probe)
To resolve any ambiguity, we conducted direct live probes during incident recovery:
- Defined `forge_coder` with `enable_write_tools: true`. (SUCCESS)
- Defined `forge_manager` with `enable_subagent_tools: true, enable_write_tools: true`. (SUCCESS)
- Invoked `forge_manager` and instructed it to invoke `forge_coder`.
- **Result**:
  - `forge_manager` successfully called `invoke_subagent` and spawned `forge_coder` (`conversationId: 3a13d45f-9280-47ac-8288-8f1ea35e951f`).
  - `forge_coder` called `write_to_file` and created `evidence/probe_test.txt` with contents `"HELLO"`.
- **Conclusion**:
  1. **Nested subagent invocation is 100% natively supported** by Antigravity.
  2. Subagents with `enable_write_tools: true` can write files directly to disk.
  3. The breakdown was purely caused by using the collision-blocked read-only agent names without a tool preflight.

### Root Cause C: Lack of an Enforced Hard Stop & Parent Action Gate
The framework lacked an absolute, machine-enforced hard boundary. When an agent lacked tools, the Parent treated it as an "error to work around" rather than an **ARCHITECTURE BREACH requiring an immediate hard stop**.

---

## 4. Permanent Architectural Guardrails (V2.4 Hardening)

### Guardrail 1: AgentForge Subagent Tooling & Namespace
All operational subagents with full write/execution capabilities are officially standardized under the AgentForge subagent specifications (`enable_write_tools: true` and `enable_mcp_tools: true`):
- `forge_context_extractor` (`enable_write_tools: true`)
- `forge_planner` (`enable_write_tools: true`)
- `forge_coder` (`enable_write_tools: true`)
- `forge_strict_tester` (`enable_write_tools: true`)
- `forge_browser_qa` (`enable_write_tools: true`, `enable_mcp_tools: true`)
- `forge_manager` (`enable_subagent_tools: true`, `enable_write_tools: true`)

### Guardrail 2: Mandatory Subagent Capability Preflight
Before any project build begins, a preflight check verifies that all required subagents are registered and equipped with write and execution tools. If any subagent lacks tools, execution halts immediately before a single line of code is planned or written.

### Guardrail 3: Absolute Hard Stop Rule
If ANY subagent fails, lacks permissions, or outputs text asking the Parent to write files:
- **IMMEDIATE HARD STOP**: The system emits `HARD_STOP: ARCHITECTURE_FAILURE`.
- The Parent session **MUST NEVER** write code, edit application files, run tests, or perform Browser QA on behalf of subagents.

### Guardrail 4: Parent Action Classification Gate
A strict directory boundary is enforced on the Parent Antigravity Session:
- **FORBIDDEN PATHS for Parent Session**:
  - Any file under application source trees (`backend/`, `frontend/`, `src/`, `app/`, `lib/`, `tests/`, etc.).
  - The Parent is mechanically prohibited from calling `write_to_file` or `replace_file_content` on these paths.
- **ALLOWED PATHS for Parent / Controller Session**:
  - Framework orchestration artifacts only: `state/*`, `tasks/*`, `reports/*`, `docs/*`.

### Guardrail 5: Coder Mandatory Instruction Order
All Coder instances must follow the strict 6-step discovery sequence:
`1. Agent Definition -> 2. Skill -> 3. Task Contract -> 4. Codebase Map -> 5. Specific Files -> 6. Code & Persist`.
Coders must never perform full-repo scans.

---

## 5. Status & Resolution

The incident is formally closed with these guardrails implemented in `.agents/agents/manager/agent.md`, `.agents/agents/coder/agent.md`, and all supporting skills. Future validation runs will immediately halt if role boundaries are threatened.
