#!/usr/bin/env python3
"""
AgentForge Mechanical Parent Boundary Hook
Receives tool call on stdin and mechanically blocks writes to application code
and functional test execution from the controller session.
"""

import sys
import json
import re

FORBIDDEN_FILE_PATTERNS = [
    r"[/\\]backend[/\\].*",
    r"[/\\]frontend[/\\].*",
    r"[/\\]src[/\\].*",
    r"[/\\]app[/\\].*",
    r"[/\\]lib[/\\].*",
    r"[/\\]tests[/\\].*",
]

FORBIDDEN_COMMAND_PATTERNS = [
    r"\bpytest\b",
    r"\bplaywright\b",
    r"\bnpm\s+test\b",
    r"\bvitest\b",
    r"\bjest\b",
    r"\bpython\s+-m\s+unittest\b",
]

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return 0

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})

        # Check target file for write tools
        if tool_name in ["write_to_file", "replace_file_content"]:
            target_file = args.get("TargetFile", "")
            target_norm = target_file.replace("\\", "/")

            is_forbidden = any(re.search(pat, target_norm) for pat in FORBIDDEN_FILE_PATTERNS)
            if is_forbidden:
                response = {
                    "decision": "deny",
                    "reason": (
                        f"PARENT_BOUNDARY_VIOLATION\n"
                        f"HARD_STOP: ARCHITECTURE_FAILURE\n"
                        f"Mechanical hook blocked attempt to modify application code at '{target_file}'. "
                        f"The Parent Orchestrator is strictly forbidden from modifying application source code. "
                        f"Delegate this work exclusively to a Coder subagent."
                    )
                }
                print(json.dumps(response))
                return 0

        # Check command line for test execution tools
        if tool_name == "run_command":
            cmd = args.get("CommandLine", "")
            is_forbidden_cmd = any(re.search(pat, cmd, re.IGNORECASE) for pat in FORBIDDEN_COMMAND_PATTERNS)
            if is_forbidden_cmd:
                response = {
                    "decision": "deny",
                    "reason": (
                        f"PARENT_BOUNDARY_VIOLATION\n"
                        f"HARD_STOP: ARCHITECTURE_FAILURE\n"
                        f"Mechanical hook blocked attempt to execute verification test command '{cmd}' from Parent session. "
                        f"Test execution belongs exclusively to strict_tester and browser_qa subagents."
                    )
                }
                print(json.dumps(response))
                return 0

        # Allow all other tool operations
        print(json.dumps({"decision": "allow"}))
        return 0

    except Exception as e:
        # Fail safe: output allow or log error
        print(json.dumps({"decision": "allow", "reason": f"Hook error: {str(e)}"}))
        return 0

if __name__ == "__main__":
    main()
