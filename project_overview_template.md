# [PROJECT NAME] — Project Overview Specification

> **Note for AI Generator / Author:** Fill out all bracketed `[PLACEHOLDERS]` and replace prompt hints with project-specific details. Ensure sections with intentionally unspecified items explicitly mark them as `UNKNOWN` rather than leaving blanks or guessing.

---

# 1. Project Overview

- **Project Name:** [e.g., TaskFlow / PaySwift / HealthTrack]
- **Purpose:** [1-2 sentences explaining what the application does and why it exists]
- **Problem Statement:** [What specific user pain point, workflow bottleneck, or gap is being addressed?]
- **Target Users:** [Primary personas, e.g., Freelancers, Internal Ops, Enterprise Admin]
- **Core Goals / Value Proposition:**
  - [Goal 1: Key measurable outcome or functionality]
  - [Goal 2: User experience or workflow improvement]
  - [Goal 3: Technical or operational objective]

---

# 2. Functional Requirements

Outline the user-facing capabilities and system behaviors:

- **Authentication & User Management:**
  - [User registration, login methods, role management]
- **Core Feature 1 - [Domain Specific Feature]:**
  - [Detailed functional requirement / behavior]
  - [CRUD operations, transitions, validation rules]
- **Core Feature 2 - [Domain Specific Feature]:**
  - [Detailed functional requirement / behavior]
- **Dashboard / Central Views:**
  - [Key metrics, aggregated summaries, status breakdowns]
- **Search, Filtering & Pagination:**
  - [Supported filter criteria, search fields, sorting parameters]
- **Notifications & Alerts:**
  - [Trigger events, in-app notification types, delivery criteria]

---

# 3. Technology Stack

Define the exact languages, frameworks, and tools:

- **Frontend Framework:** [e.g., Next.js 14+ (App Router) / React / Vue]
- **Frontend Language:** [e.g., TypeScript (Strict mode)]
- **Styling / UI Library:** [e.g., Tailwind CSS / shadcn/ui]
- **Backend Framework:** [e.g., FastAPI / Node.js Express / NestJS]
- **Backend Language:** [e.g., Python 3.11+ / TypeScript]
- **Database Engine:** [e.g., PostgreSQL 15+ / MySQL / MongoDB]
- **Authentication Strategy:** [e.g., Google OAuth 2.0 / NextAuth / JWT / Session Cookies]
- **API Style:** [e.g., RESTful JSON / GraphQL / gRPC]
- **Testing Tools:**
  - Frontend Unit & Component: [e.g., Vitest + React Testing Library]
  - Backend Unit & Integration: [e.g., Pytest + HTTPX / Jest]
  - End-to-End (E2E): [e.g., Playwright / Cypress]

---

# 4. System Architecture & Data Flow

- **Frontend Responsibilities:**
  - [Client-side routing, UI rendering, local state management, form validation]
- **Backend Responsibilities:**
  - [Business logic execution, API authentication/authorization, data validation, database persistence]
- **Database Layer:**
  - [ACID guarantees, indexing strategies, relationship integrity]
- **Authentication Flow:**
  - [Step-by-step description: OAuth exchange -> session issue -> request validation]
- **High-Level Data Flow:**
  1. [User triggers action on UI]
  2. [Client issues REST API call with credentials]
  3. [Backend checks authorization and validates payload]
  4. [Database transaction is committed]
  5. [Structured JSON response returned and UI state updated]

---

# 5. Database Schema & Entities

List the primary domain models, key fields, and entity relationships (No raw SQL required):

### Entity 1: [e.g., User]
- **Fields:**
  - `id`: [UUID / Primary Key]
  - `email`: [String, Unique, Required]
  - `name`: [String, Required]
  - `created_at` / `updated_at`: [Timestamps]

### Entity 2: [e.g., Item / Task / Order]
- **Fields:**
  - `id`: [UUID / Primary Key]
  - `title`: [String, Required]
  - `status`: [Enum: e.g., DRAFT, IN_PROGRESS, COMPLETED]
  - `user_id`: [Foreign Key referencing User.id]
  - `created_at` / `updated_at`: [Timestamps]

### Relationships:
- [e.g., User has many Items (`1:N`)]
- [e.g., Item belongs to exactly one User (`N:1`)]

---

# 6. API Specifications (Conceptual Endpoints)

List the endpoints required to support the application workflows:

### Authentication
- `POST /api/auth/[login-provider]`: [Authenticates user and returns session credentials]
- `POST /api/auth/logout`: [Invalidates active session]
- `GET /api/auth/me`: [Returns authenticated user profile]

### [Domain Entity Endpoints]
- `GET /api/[entities]`: [List all entities with optional query filters]
- `POST /api/[entities]`: [Create a new entity with payload validation]
- `GET /api/[entities]/{id}`: [Retrieve entity details by identifier]
- `PUT /api/[entities]/{id}`: [Update entity attributes]
- `DELETE /api/[entities]/{id}`: [Remove or archive entity]

---

# 7. UI / UX Design Specifications

- **Primary Screens:**
  - **Login / Onboarding:** [Minimalist layout, authentication triggers, error banners]
  - **Main Dashboard:** [Core feed, navigation drawer, status widgets]
  - **Detail View:** [Interactive inspection modal or page, action controls]
  - **Settings:** [User profile, security preferences, session status]
- **UX & Usability Standards:**
  - **Responsiveness:** [Mobile (<640px), Tablet (640-1024px), Desktop (>1024px)]
  - **Loading Feedback:** [Skeleton loaders or progress bars on network calls]
  - **Empty States:** [Friendly illustration or text when lists/tables contain 0 items]
  - **Error Handling:** [Inline field validation, non-blocking toast notifications]
  - **Accessibility (a11y):** [WCAG 2.1 AA compliant, full keyboard tab-navigation, ARIA roles]

---

# 8. Security & Data Protection

- **Authentication Enforcement:** [Private routes reject unauthenticated requests (HTTP 401)]
- **Authorization & Ownership:** [Users cannot read or modify entities owned by other users (HTTP 403)]
- **Input Validation:** [All incoming request bodies validated strictly via backend schema schemas]
- **Token Handling:** [Tokens stored in HTTP-only, Secure, SameSite cookies to protect against XSS]
- **Secrets Management:** [Zero secrets/credentials committed to VCS; runtime injection via environment variables]

---

# 9. Testing & Quality Assurance Strategy

- **Backend Unit Tests:** [Pytest/Jest coverage over domain logic, services, and utility functions]
- **API Integration Tests:** [TestClient tests verifying status codes, auth gates, and DB mutations]
- **Frontend Component Tests:** [Testing component rendering, user interactions, and prop edge-cases]
- **End-to-End (E2E) Journeys:**
  - [Journey 1: Full user signup/login to dashboard transition]
  - [Journey 2: Create, modify, and delete a primary domain entity]
- **Static Code Analysis:**
  - Typecheck: [Strict mode checks with zero compiler warnings]
  - Linting: [Enforced styling and import ordering rules]
  - Build Validation: [Production bundle compilation passes cleanly]

---

# 10. Model Context Protocol (MCP) Requirements

Specify any MCP integrations required by the multi-agent development team:

- **[MCP Server Name, e.g., GitHub MCP]:**
  - **Purpose:** [e.g., Pulling issue context, managing branches, or checking PR status]
  - **Target Agent:** [Planner / Manager]
- **[MCP Server Name, e.g., Stitch MCP / Browser MCP]:**
  - **Purpose:** [e.g., Generating UI components or inspecting live web views]
  - **Target Agent:** [Coder / Tester]

---

# 11. Codebase & Repository Conventions

- **Frontend Conventions:**
  - [File naming: kebab-case vs PascalCase]
  - [Component hierarchy: feature-based vs type-based directories]
- **Backend Conventions:**
  - [Router/controller decomposition]
  - [Service layer vs repository pattern]
- **General Rules:**
  - [Zero dead code or commented-out blocks]
  - [Explicit semantic commit messages: feat, fix, chore, test]

---

# 12. Deployment Architecture

- **Frontend Hosting:** [e.g., Serverless edge deployment / Container runtime]
- **Backend Hosting:** [e.g., Containerized Docker instance / Managed app service]
- **Database Service:** [e.g., Managed relational DB instance with automated backups]

---

# 13. Non-Functional Requirements (NFRs)

- **Performance:** [P95 API latency < [e.g., 200ms]; initial page load < [e.g., 1.5s]]
- **Availability:** [Designed for high uptime without single points of failure]
- **Maintainability:** [Modular code structure allowing independent feature extensions]

---

# 14. Out of Scope (Explicit Non-Goals)

List features that development agents MUST NOT implement:

- [e.g., Native iOS / Android applications]
- [e.g., AI/LLM integration features]
- [e.g., Real-time chat or WebSockets]
- [e.g., Third-party payments or billing integrations]

---

# 15. Architectural Constraints

- [Constraint 1: e.g., Single primary database; no caching layer like Redis for MVP]
- [Constraint 2: e.g., Backend must remain completely stateless]
- [Constraint 3: e.g., Strictly use specified CSS utility framework; no foreign component suites]

---

# 16. Intentionally Unspecified / UNKNOWN Items

The following parameters are deliberately omitted at this stage and must be tracked as `UNKNOWN` rather than assumed:

- Cloud Provider: `UNKNOWN`
- Production Domain / CDN URL: `UNKNOWN`
- CI/CD Platform & Runner Environment: `UNKNOWN`
- Database Hosting Provider: `UNKNOWN`
