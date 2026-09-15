# Project Final Report Schema

Use this schema when creating or updating `reports/final-report.md`:

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

## Frontend
- **Screens**: [List of screens/views implemented]
- **Main User Flows**: [Key user interaction workflows]
- **UI/Design Implementation**: [Styling, layout, tokens, responsiveness]
- **Stitch References**: [Stitch project/screen IDs used, or None]

## Backend
- **Services**: [Backend services and entrypoints]
- **APIs**: [List of endpoints, methods, and responsibilities]
- **Business Logic**: [Core business and validation rules]
- **Authentication**: [Authentication and authorization mechanism]

## Database
- **Main Entities**: [Key database entities and attributes]
- **Relationships**: [Entity relationships and foreign keys]
- **Migrations/Schema**: [Schema creation and migration approach]

## Integration
[Summary of full end-to-end integration: Frontend → API → Backend → Database → Response → Frontend State]

## Testing
- **Unit Tests**: [Unit test suite summary and counts]
- **Integration Tests**: [Integration test summary and counts]
- **E2E / Browser QA**: [Browser test execution and tool used]
- **Visual Verification**: [Screenshot audit and design comparisons]

## Security
- [Security controls, password hashing, session tokens, zero-secrets policy]

## MCP Usage
- [List of MCPs used and purpose, e.g. Stitch, Execution Controller]

## Task Summary

| Task | Status | Summary |
| :--- | :---: | :--- |
| [TASK-001] | VERIFIED | [Brief summary] |

## Change History
- **[CR-ID or Baseline]**: [Summary of changes, new/reopened tasks, and date]

## Known Limitations
- [Only verified, actual known limitations]

## Evidence
- [File paths to evidence folders under evidence/]
```
