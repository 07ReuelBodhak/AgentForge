# [TASK ID]: [Title]

**Status**: [PLANNED | READY | CODING | TESTING | INTEGRATION_TESTING | UI_TESTING | RETRYING | VERIFIED | FAILED | BLOCKED | ESCALATED | REOPENED | SUPERSEDED]
**Type**: [backend | frontend | fullstack | database | integration | ui | visual | infra | docs]
**Project Area**: [Frontend | Backend | Fullstack | Infra | Docs | E2E]
**Service**: [Name of specific service, app, or component, or Root]
**Execution Environment**: [Development | Test | CI | Local]
**Parallel Safe**: [true | false]
**Change Request**: [CR-XXX | None]
**Goal**: [Concise goal description]

---

## 1. File Ownership & Conflict Boundaries
- **read_files**:
  - [file paths that may be inspected]
- **modify_files**:
  - [file paths that will be edited; concurrent tasks cannot overlap with these]
- **create_files**:
  - [new file paths to be created]

---

## 2. Prerequisites, Design Source & Human Inputs Gate
<!-- If any required credential, token, or visual asset is missing, task MUST be marked BLOCKED -->
- **design_source**: [stitch | human_provided | none]
- **preserve_existing_design_language**: [true | false]
- **design_project_id**: [Stitch project ID if available via MCP, or 'None']
- **authoritative_design_reference**: [e.g. docs/design/home/home.png or 'None']
- **existing_design_references**:
  - [e.g. docs/design/home/home.png (existing Stitch screens used as style reference for new screen)]
- **design_states**: [default | empty | loading | populated | 'None']
- **required_human_inputs**:
  - [e.g. CLOUDINARY_API_KEY, OAuth client secret, or 'None']
- **external_dependencies**:
  - [e.g. Cloudinary, Stripe, Firebase, or 'None']
- **required_mcp**:
  - [e.g. stitch, execution-controller, or 'None']

---

## 3. Dependencies
- [TASK-ID of prerequisite tasks that must be VERIFIED before this task can start, or 'None']

---

## 4. Requirements & Acceptance Criteria
### Requirements
- [Functional requirement 1]
- [Functional requirement 2]

### Acceptance Criteria
- [Specific verifiable outcome 1]
- [Specific verifiable outcome 2]

---

## 5. Verification Gates
<!-- Task is VERIFIED only when all gates marked true pass successfully -->
<!-- Prior to dispatching verification, Manager enforces the Hard Disk Persistence Gate: all modify_files and create_files must physically exist on disk, or task fails with FAILED_GATE: CODER_OUTPUT -->
<!-- For visual=true or browser=true, task CANNOT be verified by Coder/Tester alone; requires Browser QA -->
- **unit**: [true | false]
- **integration**: [true | false]
- **browser**: [true | false]
- **visual**: [true | false]

### Visual References & Authoritative Design Artifacts
<!-- Required when visual verification is true. Must point to real reference files in docs/design/ -->
<!-- If visual: true and reference file does not exist, task MUST be marked BLOCKED / HUMAN_ACTION_REQUIRED -->
- **reference_files**:
  - [e.g. docs/design/home/home.png]
- **design_extension_mode**: [existing_screen | stitch_generated_new_screen | existing_style_extension | none]
- **style_reference_files**:
  - [e.g. docs/design/home/home.png (existing Stitch screens used as visual reference when creating a new screen)]
- **viewport**: [mobile | desktop | tablet]
- **state**: [default | empty | loading | populated]
- **visual_acceptance_criteria**: [Faithful reproduction of composition, layout, hierarchy, spacing, colors, typography]

### Test Scope & Required Tests
- **test_scope**: [targeted | related | integration | browser | regression]
- **test_rationale**: [Why this scope is sufficient, e.g. "Only isolated balance function modified"]
- **test_commands**:
  - [e.g. .venv/Scripts/pytest tests/unit/test_balance.py]

### UI / E2E Verification Steps
<!-- Audited by browser_qa when browser verification is true -->
- [Observable user flow from UI interaction to backend state and visible result, or 'None']

---

## 6. Engineering Constraints & Quality Checklist
### Engineering Constraints
- **reuse_existing**: [true | false] (Must inspect codebase map for existing components/helpers before writing new ones)
- **avoid_unnecessary_dependencies**: [true | false] (Do not introduce external packages if standard library or existing code suffices)
- **prefer_simple_solution**: [true | false] (Choose simplest maintainable solution; avoid premature abstraction)
- **no_global_dependency_installation**: true (Always use project-local environments e.g. .venv, package.json)

### Quality Review Criteria (Audited by Strict Tester)
- **duplication**: Verify no duplicated logic or components introduced.
- **complexity**: Verify code has no unnecessary layers or over-engineering.
- **dependencies**: Verify all imports exist in dependency manifest and are justified.
- **reuse**: Verify existing helpers/services were utilized where appropriate.

---

## 7. Status Notes
<!-- Reason if REOPENED, SUPERSEDED, BLOCKED, or ESCALATED; otherwise 'None' -->
- None
