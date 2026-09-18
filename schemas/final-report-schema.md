# Project Final Report Schema

Use this schema when creating or updating the canonical `reports/final-report.md`:

```markdown
# Project Final Report

## Project Overview
- **Name**: [Project Name]
- **Purpose**: [Core Problem & System Purpose]
- **Architecture**: [High-Level Architectural Pattern]
- **Technology Stack**: [Languages, Frameworks, Libraries, Tools]

## Final Architecture
[Detailed description of implemented system architecture and component boundaries]

## Features Implemented
- [Feature 1]
- [Feature 2]

## Frontend & UI Implementation
- **Design Source of Truth**: [Stitch Project ID, Human-Provided Design Artifacts in docs/design/, or None]
- **Design Manifest**: [docs/design/design-manifest.md]
- **Screens & States Implemented**: [List of screens and verified states: default, empty, loading]
- **Main User Flows**: [Key user interaction workflows]
- **UI/Design Implementation**: [Styling, layout, tokens, responsiveness]
- **Design System Extension**: [Summary of new screens implemented preserving existing Stitch style language]
- **Authoritative Visual References**: [List of reference PNG paths under docs/design/ verified]
- **Implementation Screenshots & Evidence**: [Paths to browser screenshots in evidence/]

## Backend
- **Services**: [Backend services and entrypoints]
- **APIs**: [List of endpoints, methods, and responsibilities]
- **Business Logic**: [Core business and validation rules]
- **Authentication**: [Authentication and authorization mechanism]

## Database
- **Main Entities**: [Key database entities and attributes]
- **Relationships**: [Entity relationships and foreign keys]
- **Migrations/Schema**: [Schema creation and migration approach]

## External Integrations
- [External APIs, Cloud services, OAuth providers, and prerequisite handling]

## Integration Architecture
[Summary of full end-to-end integration: Frontend → API → Backend → Database / External Services → Response → Frontend State]

## Testing & Verification Model
- **Test Scope Strategy**: [How targeted vs related vs regression tests were scoped]
- **Unit Tests**: [Unit test suite summary and counts]
- **Integration Tests**: [Integration test summary and live service results]
- **Browser QA Verification**: [Live Chrome CDP execution, console, and process stream auditing]
- **Visual Verification**: [Comparison against authoritative visual references]

## Parallel Execution & Concurrency
- [Summary of parallel-safe task lanes executed concurrently without file conflicts]

## Code-Quality & Engineering Standards
- [Reusability, DRY compliance, avoidance of unnecessary abstractions and dependencies]

## Environment Isolation
- [Project-local virtual environments used, dependency manifests maintained]

## Security
- [Security controls, password hashing, session tokens, zero-secrets policy]

## MCP Usage
- [List of MCPs used and purpose, e.g. Stitch, Execution Controller]

## Task Summary

| Task | Status | Type | Parallel Lane | Test Scope | Summary |
| :--- | :---: | :---: | :---: | :---: | :--- |
| [TASK-001] | VERIFIED | backend | LANE_BACKEND | targeted | [Brief summary] |

## Change History
- **[CR-ID or Baseline]**: [Summary of changes, new/reopened tasks, and date]

## Known Limitations
- [Only verified, actual known limitations]

## Evidence
- [File paths to evidence folders under evidence/]

## Unresolved Issues
- [None or explicit blockers requiring human intervention]
```
