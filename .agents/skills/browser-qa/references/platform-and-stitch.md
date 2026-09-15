# Browser QA Platform Scope & Reference

## 1. Supported vs. Unsupported Platform Matrix

| Platform / Framework | Environment Status | Interaction Driver | Capabilities Verified |
| :--- | :--- | :--- | :--- |
| **Browser Web UI** (HTML/CSS/JS, React, Vue, Svelte, Next.js) | **SUPPORTED** | Playwright (Google Chrome via CDP) | DOM elements, CSS styles, form typing, buttons, dynamic rendering, console error auditing. |
| **Flutter Web** (CanvasKit / HTML renderer) | **SUPPORTED** | Playwright (Google Chrome via CDP) | Accessibility / semantics tree (`flt-semantics`), ARIA labels, text inputs, console logs, runtime asserts. |
| **Native Flutter Android / iOS** | **UNSUPPORTED** | None in standard headless agent | Requires physical mobile device or Android/iOS emulator runtime. |
| **Native Desktop Apps** (Win32, Cocoa, GTK) | **UNSUPPORTED** | None in standard web agent | Requires dedicated desktop GUI test drivers (e.g. WinAppDriver, pywinauto). |

## 2. Playwright Driving & Dual-Stream Error Auditing
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page()
    
    # Listen to console and uncaught page errors
    page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
    page.on("pageerror", lambda err: print(f"BROWSER UNCAUGHT EXCEPTION: {err}"))
    
    page.goto("http://localhost:8000")
    # Interact via ARIA / role locators
    page.get_by_role("button", name="Sign In").click()
```

## 3. Stitch Screen Verification
When a task defines a Stitch `Design Reference` (e.g. `projects/13734835499614695629/screens/c220cd2801544f39bddf7afc53e93d55`), use `call_mcp_tool` with `stitch:get_screen` to retrieve design tokens, color palette, typography, and layout specifications to compare against the running UI.
