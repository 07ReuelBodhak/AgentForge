# Design Manifest & Authoritative Visual References

This manifest documents all authoritative design references derived from Stitch or provided as project design assets. It serves as the single source of truth for visual UI fidelity, ensuring that AI agents never guess designs or treat generated UIs as references.

---

## 1. Project Design Configuration
- **Design Source**: [Stitch | Human-Provided Assets | None]
- **Stitch Project ID**: [Stitch Project ID if available via MCP, or None]
- **Stitch Project URL**: [Web link to Stitch project if available, or None]
- **Storage Directory**: `docs/design/`
- **Acquisition Method**: [Stitch MCP `download_assets` | Human Export to docs/design/ | N/A]

---

## 2. Authoritative Screen & State Registry

| Screen / Component | State | Viewport | Authoritative Reference Path | Source | Associated Tasks | Verified Date |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: |
| Home Screen | default | mobile (390x844) | `docs/design/home/home.png` | Stitch | TASK-001 | Pending |
| Home Screen | empty | mobile (390x844) | `docs/design/home/home-empty.png` | Stitch | TASK-001 | Pending |
| Home Screen | loading | mobile (390x844) | `docs/design/home/home-loading.png` | Stitch | TASK-001 | Pending |
| Add Expense | default | mobile (390x844) | `docs/design/expenses/add-expense.png` | Stitch | TASK-002 | Pending |

---

## 3. Screen State Definitions
- **default**: Standard view with populated sample data in idle state.
- **empty**: Zero-data state (e.g. no expenses logged, first-time user onboarding).
- **loading**: Skeleton screens, progress spinners, or shimmer placeholders.
- **error / validation**: Input error banners, inline field validations, and network error dialogs.

---

## 4. Versioning & Change History
When Stitch designs change during a project lifecycle:
- Never overwrite previous references in-place without traceability.
- Archive superseded references as `docs/design/<screen>/v1-<state>.png`.
- Record new references in `changes/CR-XXX.md` and update this manifest.

---

## 5. Design System Tokens & Style Extension
When creating a new screen using the existing Stitch design language (`preserve_existing_design_language: true`):
- **Design Tokens Extracted From**: `docs/design/home/home.png`
- **Primary Color**: [Hex e.g. #1E88E5]
- **Secondary / Accent Color**: [Hex e.g. #FFC107]
- **Background & Surface**: [Hex e.g. #F8F9FA / #FFFFFF]
- **Typography Scale**: [Heading 1, Heading 2, Body, Caption]
- **Card & Container Styling**: [Border radius, elevation/shadow, internal padding]
- **Button Styling**: [Border radius, padding, font weight, hover state]
- **Header & Navigation Placement**: [App bar title alignment, bottom nav icons]
