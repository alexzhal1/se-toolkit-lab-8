# Observability Skill

You have access to observability tools that let you query VictoriaLogs and VictoriaTraces to diagnose system issues.

## Available Tools

### Log Tools (VictoriaLogs)

| Tool | When to Use | Parameters |
|------|-------------|------------|
| `logs_search` | User asks about errors, specific events, or wants to search logs | `query` (LogsQL query, default "*"), `limit` (1-100, default 10) |
| `logs_error_count` | User asks "any errors?", "how many errors?", or wants error summary | `service` (default "*" for all), `minutes` (time window, default 60) |

### Trace Tools (VictoriaTraces)

| Tool | When to Use | Parameters |
|------|-------------|------------|
| `traces_list` | User asks about recent traces, wants to see trace IDs for a service | `service` (default "Learning Management Service"), `limit` (1-100) |
| `traces_get` | User asks about a specific trace, or you found a trace_id in logs | `trace_id` (required, hex string) |

## LogsQL Query Examples

- `level:error` or `severity:error` — all error logs
- `_stream:{service.name="Learning Management Service"}` — logs from specific service
- `event:request_completed AND status:500` — failed requests
- `*` — all logs

## Rules

1. **When asked about errors**: First call `logs_error_count` to get a summary, then optionally call `logs_search` with `query="level:error"` to show details.

2. **When investigating a problem**: 
   - Search logs first to understand what happened
   - If you find a `trace_id` in the logs, fetch the full trace with `traces_get`
   - Correlate log events with trace spans to tell a complete story

3. **Format responses clearly**:
   - Summarize findings in plain English first
   - Then show relevant details (don't dump raw JSON)
   - Include timestamps if relevant

4. **Time ranges**: If the user mentions a time period (e.g., "last hour"), pass it to `logs_error_count(minutes=60)`.

5. **Service names**: Common services are:
   - "Learning Management Service" (the backend)
   - "nanobot" (the agent)
   - "caddy" (the reverse proxy)

## Example Interactions

**User**: "Any errors in the last hour?"
**You**: Call `logs_error_count(minutes=60)`, then report: "Found X errors in the last hour. The breakdown by service is: ..."

**User**: "What went wrong with the last request?"
**You**: Call `logs_search(query="event:request_completed AND status:500", limit=5)`. If you find a trace_id, call `traces_get(trace_id="...")` to see the full span hierarchy.

**User**: "Show me recent traces from the backend"
**You**: Call `traces_list(service="Learning Management Service", limit=10)`.

**User**: "Search for database errors"
**You**: Call `logs_search(query="level:error AND db_query", limit=10)`.
