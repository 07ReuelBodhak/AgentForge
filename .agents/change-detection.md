# Default Agent Change Detection & Session Routing Protocol

When the user interacts with the default Antigravity agent in a repository, the agent must inspect the repository state and classify the user's intent into one of five distinct categories before taking action:

```mermaid
flowchart TD
    User([User Prompt]) --> Detect{Classify Request}
    
    Detect -->|A. Informational| Info["Answer Query Directly (Read-Only)"]
    Detect -->|B. Bug Fix| Fix["Create changes/CR-XXX.md (Bug Fix)"]
    Detect -->|C. Feature Modification| Mod["Create changes/CR-XXX.md (Modification)"]
    Detect -->|D. New Feature| NewFeat["Create changes/CR-XXX.md (New Feature)"]
    Detect -->|E. New Project| NewProj["Initialize Mode A (PDF Extraction)"]
    
    Fix & Mod & NewFeat --> Planner["Invoke Planner: IMPACT_ANALYSIS"]
    Planner --> Decision["Ask User Decision: ALL vs ONE_BY_ONE"]
    Decision --> Manager["Manager Execution Loop"]
    Manager --> UpdateReport["Update reports/final-report.md in-place"]
```

---

## Intent Classification Matrix

| Category | Typical User Query Examples | System Action | Development Workflow Triggered? |
| :--- | :--- | :--- | :---: |
| **A. Informational** | *"What does the auth module do?"*, *"Where is database initialized?"*, *"Explain how password hashing works."* | Use read tools (`view_file`, `grep_search`). Answer user directly in chat. | **NO** (Zero state/task changes) |
| **B. Bug Fix** | *"Login crashes when password is incorrect"*, *"Fix 500 error on registration"*, *"Button is unresponsive on mobile"*. | 1. Identify next `CR-XXX` ID (e.g. `CR-001`).<br>2. Write `changes/CR-XXX.md` with `Risk: MEDIUM/HIGH`.<br>3. Invoke `planner` for Impact Analysis.<br>4. Reopen affected verified tasks or create fix task.<br>5. Request user execution mode (`ALL` vs `ONE_BY_ONE`). | **YES** (`CHANGE_SESSION`) |
| **C. Existing Feature Modification** | *"Change the authentication card layout"*, *"Increase session expiration to 7 days"*, *"Update button colors"*. | 1. Create `changes/CR-XXX.md`.<br>2. Invoke `planner` for Impact Analysis.<br>3. Mark invalidated tasks as `REOPENED` or `SUPERSEDED`.<br>4. Request user execution mode.<br>5. Execute via Manager. | **YES** (`CHANGE_SESSION`) |
| **D. New Feature** | *"Add recurring expenses"*, *"Add OAuth login with Google"*, *"Implement export to CSV"*. | 1. Create `changes/CR-XXX.md`.<br>2. Snapshot `project-context.md` to `docs/project-context-history/`.<br>3. Planner creates new sequential tasks (`TASK-005`, etc.).<br>4. Request user execution mode.<br>5. Execute via Manager.<br>6. Update `reports/final-report.md`. | **YES** (`CHANGE_SESSION`) |
| **E. New Project** | *"Here is the project overview PDF for an expense tracker"*, *"Initialize new project from spec"*. | 1. Verify fresh or uninitialized repository.<br>2. Trigger Mode A: Context Extractor $\rightarrow$ `project-context.md` $\rightarrow$ Planner $\rightarrow$ Initial Task Graph $\rightarrow$ User Choice $\rightarrow$ Manager. | **YES** (`INITIAL_BUILD`) |

---

## Critical Rules
1. **Never Rebuild Completed Projects**: An existing project with `reports/final-report.md` must NEVER be re-initialized from scratch. Existing verified tasks remain verified unless explicitly reopened by the Planner.
2. **Never Fabricate CR IDs**: Check `changes/` to find the highest existing index (`CR-001`, `CR-002`, etc.) and increment sequentially.
3. **Mandatory User Decision Gate**: The default agent must STOP and ask the user whether to execute `ALL` or `ONE_BY_ONE` before invoking the Manager to implement changes.
4. **Canonical Report Preservation**: On session completion, the existing `reports/final-report.md` is updated in-place with the change history entry. Never create duplicate reports (such as `final-report-v2.md`).
