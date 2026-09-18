#!/usr/bin/env python3
"""
AgentForge Mechanical Parent Boundary Hook
Receives tool call on stdin and mechanically blocks writes to application code from the controller session.
"""

import sys
import json
import re

FORBIDDEN_PATTERNS = [
    r"[/\\]backend[/\\].*",
    r"[/\\]frontend[/\\].*",
    r"[/\\]src[/\\].*",
    r"[/\\]app[/\\].*",
    r"[/\\]lib[/\\].*",
    r"[/\\]tests[/\\].*",
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

            # Check if target is in application code directories
            is_forbidden = any(re.search(pat, target_norm) for pat in FORBIDDEN_PATTERNS)
            if is_forbidden:
                response = {
                    "decision": "deny",
                    "reason": (
                        f"PARENT_BOUNDARY_VIOLATION + HARD STOP: Mechanical hook blocked attempt to modify "
                        f"application code at '{target_file}'. The Parent Orchestrator is strictly forbidden "
                        f"from modifying application source code. Delegate this work to a Coder subagent."
                    )
                }
                print(json.dumps(response))
                return 0

        # Allow all other tool operations
        print(json.dumps({"decision": "allow"}))
        return 0

    except Exception as e:
        # Fail safe: if hook encounters an error, output allow or log
        print(json.dumps({"decision": "allow", "reason": f"Hook error: {str(e)}"}))
        return 0

if __name__ == "__main__":
    main()
