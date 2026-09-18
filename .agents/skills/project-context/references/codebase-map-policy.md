# Codebase Map Policy & Operating Procedures

## 1. Core Operating Rule: No Broad Scans by Default
Agents must NOT perform full repository scans (`grep_search` across root, `find_by_name` across root, or recursively listing all folders) for every task.
Instead, follow this order of discovery:
1. Read active task specification (`tasks/TASK-XXX.md`).
2. Read relevant sections of `docs/codebase-map.md`.
3. Target only the identified files via `view_file` or focused search.
4. Expand inspection beyond the map ONLY if the map is proven incomplete or missing for that component.

## 2. Progressive Disclosure & Role Consumption
- **Context Extractor**: Initializes `docs/codebase-map.md` headers after initial scaffolding is planned.
- **Planner**: Reads `docs/codebase-map.md` to determine existing file paths, shared symbols, and dependencies during decomposition and Change Request impact analysis.
- **Coder**: Reads target map sections to discover where functionality lives, checks for existing utilities to reuse (DRY), and updates affected entries after modifying/creating files.
- **Strict Tester**: Uses map to verify file placement and ensure test files map accurately to components.
- **Manager**: Passes ONLY the relevant map section to task-specific Coder instances (never dumps entire map into prompt).

## 3. Incremental Update Policy
- After a task implements or alters code:
  - Do NOT rebuild the entire map.
  - Add or edit only the rows corresponding to files modified, created, or deleted by the task.
  - Update `Last Updated: [Timestamp or Task ID]`.
- Required columns for each entry:
  - `Path`: Relative file path.
  - `Purpose`: 1-sentence description of responsibility.
  - `Key Symbols / Exports`: Main classes, functions, widgets, or endpoints.
  - `Depends On`: Main internal/external dependencies.
  - `Domain / Feature`: Feature area.

## 4. Stale Map Detection & Targeted Rescan
A map section is considered stale if:
- A listed file no longer exists or was moved.
- Exported symbols have fundamentally changed.
- A newly created file is missing from the table.
**Resolution**: Perform a TARGETED inspection of the affected directory only (e.g. `lib/screens/` or `app/api/`) and update those specific table rows. Never trigger a whole-repository rescan.
