---
name: coding
description: High-signal operational guidelines for Coder agents on targeted discovery, design checks, environment isolation, manifests, and reporting.
---

# Coding Guidelines

As the Coder, your job is to implement EXACTLY ONE assigned task contract (`tasks/TASK-XXX.md`).

## 1. Targeted Codebase Discovery
- **No Broad Scans**: Never grep or scan the entire repository. Read `tasks/TASK-XXX.md` and consult `docs/codebase-map.md` to identify target files.
- **Service Boundaries**: Place code strictly in its declared service directory (`frontend/`, `backend/`). Never put service files at repository root in multi-service projects.

## 2. Lightweight Design Check & Code Quality
- **Reuse & DRY**: Always search the codebase map for existing helpers, utilities, and components before writing new logic.
- **Simplest Solution**: Do not create unnecessary files, interfaces, or abstraction layers. Choose the simplest maintainable solution that fulfills acceptance criteria.
- **No Unrelated Refactoring**: Do not reformat untouched files or reorganize directories outside the task boundary.

## 3. Environment & Manifest Mandates
- **Environment Isolation**: Always use project-local environments (e.g. Python `.venv`, Node `node_modules`). Global package installations are strictly prohibited.
- **Dependency Manifests**: Check if stdlib or existing dependencies suffice before adding new libraries. If adding a library, declare it in the service manifest (`requirements.txt`, `package.json`, `Cargo.toml`, `pubspec.yaml`).
- **Dual-Import Compatibility**: Services must run both from inside their service folder and from project root.

## 4. Authoritative Design Reference as Implementation Guide
- For visual/UI tasks (`design_source: stitch` or `verification.visual: true`), inspect the designated reference in `docs/design/` using `view_file` before writing code.
- Faithfully reproduce layout, spacing, composition, hierarchy, colors, typography, and interactive states.
- Never substitute generic textual descriptions or guess designs when an authoritative reference is declared.
- **Design Extension (`preserve_existing_design_language: true`)**: When creating a new screen matching existing Stitch style, inspect declared `existing_design_references`. Extract and apply the existing app's colors, typography scales, button shapes, and card padding. Never invent an inconsistent design.

## 5. Focused Syntax & Static Checks (NOT Functional Test Suite)
- Run fast syntax validation (`python -m py_compile <file>`, `python -m compileall <dir>`, `tsc --noEmit`, or linter/static syntax checks) or minimal sanity checks.
- **NEVER** execute the full or functional test suite (`pytest`, `npm test`, etc.) that `strict_tester` immediately reruns. Prevent test redundancy and token waste.
- Update affected entries in `docs/codebase-map.md` upon completing file changes.

## 6. Physical Disk Persistence Requirement
- You MUST write all code directly to physical files on disk using `write_to_file` or `replace_file_content` before reporting completion.
- Do NOT simply output code snippets or code blocks in markdown without persisting them to disk.
- If files declared in `modify_files` or `create_files` are not found on disk, the Manager's Hard Disk Persistence Gate will reject the task with `FAILED_GATE: CODER_OUTPUT` and trigger a retry.

## 7. Output Contract
Send response using this exact schema:
```text
STATUS: [DONE | FAILED | BLOCKED]

DESIGN_REFERENCE_USED:
- [Path to docs/design/... reference inspected, or 'None']

CHANGES:
- [List of modified/created files and summary of edits]

DISK_PERSISTENCE:
- [Confirmed written to disk via write_to_file / replace_file_content: list of paths]

DESIGN_CHECK:
- Reuse: [Helpers reused / None]
- Simplicity: [Simplest maintainable solution verified]
- Dependencies: [Manifest verified / New dependency reason]

TESTS:
- [Syntax / compilation / static checks run and results; NO functional test suite]

CODEBASE_MAP_UPDATED:
- [YES / NO]

REMAINING:
- [Any blockers or 'None']
```
