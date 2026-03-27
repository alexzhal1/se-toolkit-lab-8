"""MCP server exposing VictoriaLogs and VictoriaTraces as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import quote

import httpx

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("observability")

# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _NoArgs(BaseModel):
    """Empty input model for tools that only need server-side configuration."""


class _LogsSearchQuery(BaseModel):
    query: str = Field(
        default="*",
        description="LogsQL query (e.g., 'level:error', '_stream:{service.name=\"backend\"}')",
    )
    limit: int = Field(default=10, ge=1, le=100, description="Max logs to return")


class _LogsErrorCountQuery(BaseModel):
    service: str = Field(
        default="*",
        description="Service name filter (use '*' for all services)",
    )
    minutes: int = Field(
        default=60, ge=1, description="Time window in minutes (default 60)"
    )


class _TracesListQuery(BaseModel):
    service: str = Field(
        default="Learning Management Service",
        description="Service name to list traces for",
    )
    limit: int = Field(default=10, ge=1, le=100, description="Max traces to return")


class _TraceIdQuery(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch (hex string)")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_victorialogs_url: str = ""
_victoriatraces_url: str = ""


def _victorialogs_client() -> httpx.AsyncClient:
    if not _victorialogs_url:
        raise RuntimeError("VictoriaLogs URL not configured")
    return httpx.AsyncClient(base_url=_victorialogs_url, timeout=30.0)


def _victoriatraces_client() -> httpx.AsyncClient:
    if not _victoriatraces_url:
        raise RuntimeError("VictoriaTraces URL not configured")
    return httpx.AsyncClient(base_url=_victoriatraces_url, timeout=30.0)


def _text(text: str) -> list[TextContent]:
    """Return text content."""
    return [TextContent(type="text", text=text)]


# ---------------------------------------------------------------------------
# Tool handlers - VictoriaLogs
# ---------------------------------------------------------------------------


async def _logs_search(args: _LogsSearchQuery) -> list[TextContent]:
    """Search logs using VictoriaLogs LogsQL query."""
    async with _victorialogs_client() as client:
        # URL encode the query
        encoded_query = quote(args.query, safe="")
        url = f"/select/logsql/query?query={encoded_query}&limit={args.limit}"
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            # VictoriaLogs returns newline-delimited JSON
            lines = resp.text.strip().split("\n")
            logs = [json.loads(line) for line in lines if line.strip()]
            return _text(json.dumps(logs, indent=2, ensure_ascii=False))
        except httpx.HTTPStatusError as e:
            return _text(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            return _text(f"Request error: {type(e).__name__}: {e}")


async def _logs_error_count(args: _LogsErrorCountQuery) -> list[TextContent]:
    """Count errors per service over a time window."""
    # Build LogsQL query for errors
    if args.service == "*":
        query = "level:ERROR OR severity:ERROR OR level:error OR severity:error"
    else:
        query = f'_stream:{{service.name="{args.service}"}} AND (level:ERROR OR severity:ERROR OR level:error OR severity:error)'

    async with _victorialogs_client() as client:
        encoded_query = quote(query, safe="")
        # Get more logs to count errors
        url = f"/select/logsql/query?query={encoded_query}&limit=1000"
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            lines = resp.text.strip().split("\n")
            logs = [json.loads(line) for line in lines if line.strip()]

            # Count by service
            error_count = len(logs)
            by_service: dict[str, int] = {}
            for log in logs:
                svc = log.get("service.name", log.get("service", "unknown"))
                by_service[svc] = by_service.get(svc, 0) + 1

            result = {
                "total_errors": error_count,
                "time_window_minutes": args.minutes,
                "by_service": by_service,
            }
            return _text(json.dumps(result, indent=2))
        except httpx.HTTPStatusError as e:
            return _text(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            return _text(f"Request error: {type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# Tool handlers - VictoriaTraces
# ---------------------------------------------------------------------------


async def _traces_list(args: _TracesListQuery) -> list[TextContent]:
    """List recent traces for a service."""
    async with _victoriatraces_client() as client:
        # VictoriaTraces uses Jaeger-compatible API
        url = f"/jaeger/api/traces?service={quote(args.service)}&limit={args.limit}"
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            # Jaeger API returns {"data": [...]}
            traces = data.get("data", [])
            result = []
            for trace in traces[: args.limit]:
                result.append(
                    {
                        "trace_id": trace.get("traceID"),
                        "span_count": len(trace.get("spans", [])),
                        "start_time": trace.get("startTime"),
                        "duration_ms": trace.get("duration"),
                    }
                )
            return _text(json.dumps(result, indent=2))
        except httpx.HTTPStatusError as e:
            return _text(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            return _text(f"Request error: {type(e).__name__}: {e}")


async def _traces_get(args: _TraceIdQuery) -> list[TextContent]:
    """Fetch a specific trace by ID."""
    async with _victoriatraces_client() as client:
        url = f"/jaeger/api/traces/{args.trace_id}"
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            traces = data.get("data", [])
            if not traces:
                return _text(f"Trace not found: {args.trace_id}")

            trace = traces[0]
            # Simplify the trace output
            spans = []
            for span in trace.get("spans", []):
                spans.append(
                    {
                        "span_id": span.get("spanID"),
                        "operation": span.get("operationName"),
                        "service": span.get("process", {}).get("serviceName", "unknown"),
                        "duration_ms": span.get("duration"),
                        "tags": [
                            t.get("key") + "=" + str(t.get("value", ""))
                            for t in span.get("tags", [])
                            if t.get("key") in ("error", "http.status_code", "db.statement")
                        ],
                    }
                )

            result = {
                "trace_id": trace.get("traceID"),
                "spans": spans,
            }
            return _text(json.dumps(result, indent=2))
        except httpx.HTTPStatusError as e:
            return _text(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            return _text(f"Request error: {type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (
        model,
        handler,
        Tool(name=name, description=description, inputSchema=schema),
    )


_register(
    "logs_search",
    "Search logs in VictoriaLogs using LogsQL query. Returns matching log entries as JSON.",
    _LogsSearchQuery,
    _logs_search,
)
_register(
    "logs_error_count",
    "Count error logs per service over a time window. Returns total count and breakdown by service.",
    _LogsErrorCountQuery,
    _logs_error_count,
)
_register(
    "traces_list",
    "List recent traces for a service from VictoriaTraces. Returns trace IDs and metadata.",
    _TracesListQuery,
    _traces_list,
)
_register(
    "traces_get",
    "Fetch a specific trace by ID from VictoriaTraces. Returns span hierarchy and details.",
    _TraceIdQuery,
    _traces_get,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main() -> None:
    global _victorialogs_url, _victoriatraces_url
    _victorialogs_url = os.environ.get("VICTORIALOGS_URL", "http://localhost:9428")
    _victoriatraces_url = os.environ.get("VICTORIATRACES_URL", "http://localhost:10428")

    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
