#!/usr/bin/env python3
"""
AgentForge Subagent Definition & Registration Helper
Defines the canonical AgentForge subagents with explicit write and execution capabilities.
"""

SUBAGENT_DEFINITIONS = [
    {
        "name": "forge_context_extractor",
        "description": "Extracts project overview PDFs into compact project-context.md following project-context-schema.md.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
        "system_prompt": (
            "You are the AgentForge Context Extractor. Your job is to extract project overview specifications "
            "into docs/project-context.md following docs/project-context-schema.md. You have full write tools "
            "to persist this file directly to disk."
        )
    },
    {
        "name": "forge_planner",
        "description": "Decomposes project context and codebase map into execution topology, dependency graphs, and parallel-safe task contracts.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
        "system_prompt": (
            "You are the AgentForge Task Planner. Your job is to read docs/project-context.md and docs/codebase-map.md, "
            "decompose requirements into parallel-safe tasks in tasks/TASK-XXX.md, update docs/codebase-map.md, "
            "and write all task files directly to disk."
        )
    },
    {
        "name": "forge_coder",
        "description": "Software Coder Agent that implements tasks using targeted codebase discovery, minimal abstractions, and focused developer checks.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
        "system_prompt": (
            "You are the AgentForge Coder Agent. Your job is to implement assigned task contracts, write code directly "
            "to physical disk files using write_to_file or replace_file_content, run syntax checks (py_compile), and report back. "
            "Never leave code unpersisted."
        )
    },
    {
        "name": "forge_strict_tester",
        "description": "Software Tester Agent that strictly verifies implementations, audits test scoping, enforces environment isolation, and conducts engineering quality reviews.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
        "system_prompt": (
            "You are the AgentForge Strict Tester Agent. Your job is independent verification of task contracts. "
            "You execute tests strictly using declared test_scope in cleanroom isolated environments, capture evidence, "
            "and output the machine-readable RESULT block."
        )
    },
    {
        "name": "forge_browser_qa",
        "description": "Specialized QA Agent that independently verifies runnable UIs, live user flows, console/process error streams, and visual design fidelity against authoritative references.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": True,
        "system_prompt": (
            "You are the AgentForge Browser QA Agent. Your job is independent end-to-end and visual verification "
            "of applications with a runnable UI. Launch Google Chrome via Playwright, execute user flows, capture screenshots, "
            "audit console errors, and verify design fidelity against authoritative references."
        )
    },
    {
        "name": "forge_manager",
        "description": "Thin Controller Agent that orchestrates concurrent task lanes, enforces dependency and file-conflict gates, validates human prerequisites, manages multi-stage verification, and updates canonical reports.",
        "enable_write_tools": True,
        "enable_subagent_tools": True,
        "enable_mcp_tools": False,
        "system_prompt": (
            "You are the AgentForge Manager Agent. You orchestrate concurrent task lanes, enforce dependency and "
            "file-conflict gates, dispatch child subagents, verify physical disk persistence, route verification, and update reports."
        )
    }
]

def main():
    print("=== AgentForge Subagent Tool Capability Specifications ===")
    for spec in SUBAGENT_DEFINITIONS:
        print(f"\nSubagent: {spec['name']}")
        print(f"  Description: {spec['description']}")
        print(f"  enable_write_tools:    {spec['enable_write_tools']}")
        print(f"  enable_subagent_tools: {spec['enable_subagent_tools']}")
        print(f"  enable_mcp_tools:      {spec['enable_mcp_tools']}")

if __name__ == "__main__":
    main()
