#!/usr/bin/env python3
"""
AgentForge System Preflight & Invariant Checker
Validates agent specifications, directory boundaries, tool permissions, and path gates.
"""

import os
import sys
import re
from pathlib import Path

REQUIRED_AGENTS = {
    "context_extractor": {"enable_write_tools": True, "enable_mcp_tools": False},
    "planner": {"enable_write_tools": True, "enable_mcp_tools": False},
    "coder": {"enable_write_tools": True, "enable_mcp_tools": False},
    "strict_tester": {"enable_write_tools": True, "enable_mcp_tools": False},
    "browser_qa": {"enable_write_tools": True, "enable_mcp_tools": True},
    "manager": {"enable_write_tools": True, "enable_subagent_tools": True},
}

REQUIRED_DIRECTORIES = [
    "state",
    "docs",
    "tasks",
    "reports",
    "reports/incidents",
    "schemas",
    ".agents/agents",
    ".agents/skills",
]

FORBIDDEN_PARENT_PATH_PATTERNS = [
    r"^backend/.*",
    r"^frontend/.*",
    r"^src/.*",
    r"^app/.*",
    r"^lib/.*",
    r"^tests/.*",
]

def check_directories(root: Path) -> bool:
    print("[PREFLIGHT] Checking required framework directories...")
    all_ok = True
    for d in REQUIRED_DIRECTORIES:
        p = root / d
        if not p.is_dir():
            print(f"  [MISSING] Directory not found: {d}")
            all_ok = False
        else:
            print(f"  [OK] Found directory: {d}")
    return all_ok

def check_agent_specifications(root: Path) -> bool:
    print("\n[PREFLIGHT] Checking AgentForge agent definitions...")
    all_ok = True
    agents_dir = root / ".agents" / "agents"
    for agent_name, reqs in REQUIRED_AGENTS.items():
        spec_path = agents_dir / agent_name / "agent.md"
        if not spec_path.is_file():
            print(f"  [MISSING] Agent definition not found: {spec_path}")
            all_ok = False
            continue

        content = spec_path.read_text(encoding="utf-8")
        # Check YAML frontmatter tool declarations
        write_ok = True
        if reqs.get("enable_write_tools"):
            if "enable_write_tools: true" not in content:
                print(f"  [FAIL] {agent_name} missing 'enable_write_tools: true'")
                write_ok = False
        if reqs.get("enable_mcp_tools"):
            if "enable_mcp_tools: true" not in content:
                print(f"  [FAIL] {agent_name} missing 'enable_mcp_tools: true'")
                write_ok = False
        if reqs.get("enable_subagent_tools"):
            if "enable_subagent_tools: true" not in content:
                print(f"  [FAIL] {agent_name} missing 'enable_subagent_tools: true'")
                write_ok = False

        if write_ok:
            print(f"  [OK] Agent specification verified: {agent_name}")
        else:
            all_ok = False

    return all_ok

def test_parent_action_gate() -> bool:
    print("\n[PREFLIGHT] Testing Parent Action Classification Gate...")
    test_cases = [
        ("backend/main.py", False),
        ("frontend/app.js", False),
        ("src/components/button.tsx", False),
        ("app/api/route.ts", False),
        ("tests/unit/test_calc.py", False),
        ("state/loop-state.md", True),
        ("tasks/TASK-001.md", True),
        ("reports/tasks/TASK-001.md", True),
        ("docs/project-context.md", True),
        ("docs/codebase-map.md", True),
    ]

    all_ok = True
    for file_path, expected_allowed in test_cases:
        # Check against forbidden patterns
        is_forbidden = any(re.match(p, file_path.replace("\\", "/")) for p in FORBIDDEN_PARENT_PATH_PATTERNS)
        is_allowed = not is_forbidden

        if is_allowed != expected_allowed:
            print(f"  [FAIL] Gate violation on '{file_path}': expected allowed={expected_allowed}, got={is_allowed}")
            all_ok = False
        else:
            status = "ALLOWED (Controller)" if is_allowed else "FORBIDDEN (Delegated to Coder)"
            print(f"  [OK] Path '{file_path}' -> {status}")

    return all_ok

def main():
    root = Path(__file__).resolve().parent.parent
    print(f"=== AgentForge System Preflight & Invariant Audit ===")
    print(f"Workspace Root: {root}\n")

    dirs_ok = check_directories(root)
    agents_ok = check_agent_specifications(root)
    gate_ok = test_parent_action_gate()

    if dirs_ok and agents_ok and gate_ok:
        print("\n>>> ALL PREFLIGHT AUDITS PASSED. AgentForge framework is fully compliant.")
        return 0
    else:
        print("\n>>> CRITICAL: Preflight audit failed. Review missing components above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
