# Browser QA Platform Scope, Visual Fidelity & Stitch Reference

## 1. Supported vs. Unsupported Platform Matrix

| Platform / Framework | Environment Status | Interaction Driver | Capabilities Verified |
| :--- | :--- | :--- | :--- |
| **Browser Web UI** (HTML/CSS/JS, React, Vue, Svelte, Next.js) | **SUPPORTED** | Playwright (Google Chrome via CDP) | DOM elements, CSS styles, form typing, buttons, dynamic rendering, console error auditing. |
| **Flutter Web** (CanvasKit / HTML renderer) | **SUPPORTED** | Playwright (Google Chrome via CDP) | Accessibility / semantics tree (`flt-semantics`), ARIA labels, text inputs, console logs, runtime asserts. |
| **Native Flutter Android / iOS** | **UNSUPPORTED** | None in standard headless agent | Requires physical mobile device or Android/iOS emulator runtime. |
| **Native Desktop Apps** (Win32, Cocoa, GTK) | **UNSUPPORTED** | None in standard web agent | Requires dedicated desktop GUI test drivers (e.g. WinAppDriver, pywinauto). |

## 2. Distinction Between Three Core Design Concepts
The architecture strictly distinguishes:
- **A. STITCH SOURCE**: The original design created in Stitch (or retrieved via Stitch MCP).
- **B. AUTHORITATIVE PROJECT DESIGN REFERENCE**: The preserved image artifact stored in `docs/design/<screen>/<screen>.png` representing the Stitch design for the given screen/state.
- **C. IMPLEMENTED UI**: The UI actually written by Coder, running in live Chrome, and captured by Browser QA.
`STITCH SOURCE ≠ IMPLEMENTED UI`. The authoritative reference exists in `docs/design/` so Browser QA can independently compare the implementation against the original design.

## 3. Stitch Acquisition Workflows (MCP vs Human Export)
1. **Automatic Supported Stitch Acquisition (When Stitch MCP is configured)**:
   - If `design_source: stitch` and a valid Stitch `projectId` is declared:
   - Call `call_mcp_tool` with `ServerName: "stitch"`, `ToolName: "download_assets"`, passing `projectId` and `outputDir: "docs/design"`.
   - Record downloaded assets in `docs/design/design-manifest.md`.
2. **Human-Exported Design Artifacts (First-Class Supported Workflow)**:
   - When Stitch MCP is unavailable, unconfigured, or no API access exists:
   - The user exports screens from Stitch as PNGs and places them in `docs/design/` (e.g. `docs/design/home/home.png`, `docs/design/home/home-empty.png`).
   - This is NOT an error—it is an accepted, standard workflow.
   - Agents must NEVER fabricate Stitch API calls or pretend automated download occurred if it did not.
3. **Human Design-Asset Gate**:
   - If `verification.visual: true` and the referenced asset does not exist on disk:
   - Task MUST be marked `BLOCKED / HUMAN_ACTION_REQUIRED`.
   - Do NOT guess the UI, do NOT generate an AI replacement, and do NOT mark the task VERIFIED.
4. **Stitch Design Extension Capability (New Screens in Existing Style)**:
   - When the user asks for a NEW SCREEN:
     - **Step 1**: Check whether the project already has a Stitch project/design in `docs/design/design-manifest.md` or `docs/project-context.md`.
     - **Step 2**: If the screen already exists in Stitch $\rightarrow$ use that existing Stitch design as the source of truth.
     - **Step 3**: If the screen does NOT exist in Stitch, but the user says *"make a new screen using the same Stitch style/design"*:
       - Inspect the existing Stitch screens and use them as the visual/style reference.
     - **Step 4**: If Stitch MCP supports generating the new screen:
       - Call `call_mcp_tool(ServerName="stitch", ToolName="generate_screen_from_text", Arguments={"projectId": ..., "prompt": ..., "deviceType": "MOBILE"})`.
       - Download the generated screen to `docs/design/` via `stitch:download_assets`.
     - **Step 5**: If Stitch cannot generate the new screen with the available tools:
       - Do NOT pretend it did.
       - Use existing Stitch screens as the reference (`preserve_existing_design_language: true`) and implement the new screen consistently.
     - **Step 6**: Planner records in task:
       `design_source: stitch`
       `preserve_existing_design_language: true`
       `existing_design_references: [docs/design/home/home.png]`
     - **Step 7**: Browser QA drives live Chrome, captures screenshot, compares against Stitch reference design language, audits console/server errors, and issues PASS / FAIL.

## 4. Playwright Driving & Dual-Stream Error Auditing
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844}) # Mobile viewport
    
    # Listen to console and uncaught page errors
    page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
    page.on("pageerror", lambda err: print(f"BROWSER UNCAUGHT EXCEPTION: {err}"))
    
    page.goto("http://localhost:8000")
    page.get_by_role("button", name="Sign In").click()
    
    # Capture full-page screenshot of actual running app for visual comparison
    page.screenshot(path="evidence/TASK-XXX/browser-screenshot.png", full_page=True)
```

## 5. Visual Comparison & Evidence Generation
- Browser QA compares `docs/design/...` (Reference) against `evidence/<task-id>/browser-screenshot.png` (Implementation).
- Generates `evidence/<task-id>/visual-comparison.md` detailing:
  - Reference path and state verified.
  - Layout composition, spacing, color palette, typography hierarchy.
  - Concrete deviations (if any).
- Minor font smoothing and anti-aliasing variations are ignored.
- If material differences exist, output `RESULT: FAIL` with `FAILED_GATE: VISUAL`.
