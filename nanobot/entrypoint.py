#!/usr/bin/env python3
"""
Entrypoint for nanobot Docker deployment.

Resolves environment variables into config.json at runtime, then launches nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def resolve_config():
    """Read config.json, inject env var values, write config.resolved.json."""
    config_path = Path(__file__).parent / "config.json"
    resolved_path = Path(__file__).parent / "config.resolved.json"
    workspace_path = Path(__file__).parent / "workspace"

    with open(config_path) as f:
        config = json.load(f)

    # Resolve LLM provider API key and base URL from env vars
    if "custom" in config.get("providers", {}):
        api_key = os.environ.get("LLM_API_KEY", "")
        if api_key:
            config["providers"]["custom"]["apiKey"] = api_key

        api_base = os.environ.get("LLM_API_BASE_URL", "")
        if api_base:
            config["providers"]["custom"]["apiBase"] = api_base

    # Resolve MCP server env vars (backend URL and API key)
    if "tools" in config and "mcpServers" in config["tools"]:
        if "lms" in config["tools"]["mcpServers"]:
            backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
            if backend_url:
                config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url

            api_key = os.environ.get("NANOBOT_LMS_API_KEY", "")
            if api_key:
                config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = api_key

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    return str(resolved_path), str(workspace_path)


def main():
    resolved_config, workspace = resolve_config()

    # Get gateway port from env var
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790")

    # Launch nanobot gateway with resolved config
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_config, "--workspace", workspace, "--port", gateway_port])


if __name__ == "__main__":
    main()
