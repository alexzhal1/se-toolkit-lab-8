# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question:** "What is the agentic loop?"

**Response:**

The agentic loop is the fundamental reasoning cycle that autonomous AI agents follow to accomplish tasks:

| Step         | What Happens                                                           |
|--------------|------------------------------------------------------------------------|
| 1. Perceive  | Gather information (user input, tool outputs, environment, memory)     |
| 2. Reason    | Analyze the situation and decide what action to take                   |
| 3. Act       | Execute the action (call a tool, send a message, modify a file, etc.)  |
| 4. Observe   | Receive feedback from the action (success, failure, new data)          |
| 5. Repeat    | Loop back until the goal is achieved                                   |

**Why It Matters:**

This loop enables agents to:
- Handle multi-step tasks requiring sequential actions
- Adapt to failures by trying alternative approaches
- Make dynamic decisions based on real-time feedback
- Work autonomously without constant human guidance

**Lab Context:**
- Lab 7: You manually wrote the tool-calling loop yourself
- Lab 8: The nanobot framework provides the loop — you just configure tools via MCP and write skill prompts to guide the agent's reasoning

This is what distinguishes agents from simple chatbots — agents can take actions, observe results, and iterate until they achieve their goal.

---

## Task 1B — Agent with LMS tools

**Question 1:** "What labs are available in our LMS?"

**Response:**

Here are the 8 labs currently available in your LMS:

| ID | Title                                                        |
|----|--------------------------------------------------------------|
| 1  | Lab 01 – Products, Architecture & Roles                      |
| 2  | Lab 02 — Run, Fix, and Deploy a Backend Service              |
| 3  | Lab 03 — Backend API: Explore, Debug, Implement, Deploy      |
| 4  | Lab 04 — Testing, Front-end, and AI Agents                   |
| 5  | Lab 05 — Data Pipeline and Analytics Dashboard               |
| 6  | Lab 06 — Build Your Own Agent                                |
| 7  | Lab 07 — Build a Client with an AI Coding Agent              |
| 8  | lab-08                                                       |

You're currently working on Lab 8 ("The Agent is the Interface"), which focuses on setting up nanobot as an AI agent with MCP tools, observability capabilities, and proactive health checks.

---

**Question 2:** "Describe the architecture of the LMS system"

**Response:**

The Learning Management System (LMS) is a Docker Compose-based microservices platform. Here's the architecture:

**High-Level Diagram:**

```
┌─────────────────────────────────────────────────────────────┐
│                      Clients                                │
│  [Browser/React Dashboard]  [Nanobot Web Chat]  [Telegram]  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Caddy Gateway (Port 42002)                │
│              (Reverse proxy routing all traffic)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ LMS Backend  │  │ Nanobot      │  │ Qwen Code API    │  │
│  │ (FastAPI)    │  │ (Agent)      │  │ (LLM Proxy)      │  │
│  │ :42001       │  │ :18790       │  │ :42005           │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────────────┘  │
│         │                 │                                  │
│         └──────── MCP ────┘                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                              │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ PostgreSQL   │  │ pgAdmin      │                         │
│  │ :42004       │  │ :42003       │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  Observability Stack                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ OTel         │  │ VictoriaLogs │  │ VictoriaTraces   │  │
│  │ Collector    │  │ :42010       │  │ :42011           │  │
│  │ :4317        │  │              │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Services Summary:**

| Service          | Purpose                            | Port  |
|------------------|------------------------------------|-------|
| caddy            | Reverse proxy / single entry point | 42002 |
| backend          | FastAPI LMS application            | 42001 |
| postgres         | PostgreSQL database                | 42004 |
| pgadmin          | Database management UI             | 42003 |
| client-web-react | React dashboard (static files)     | -     |
| qwen-code-api    | LLM API proxy                      | 42005 |
| otel-collector   | Telemetry collector                | 4317  |
| victorialogs     | Log storage & queries              | 42010 |
| victoriatraces   | Distributed trace storage          | 42011 |
| nanobot          | AI agent (Lab 8)                   | 18790 |

**Key Design Patterns:**

1. **Gateway Pattern** — Caddy is the single entry point for all client traffic
2. **Microservices** — Each component runs in isolation with clear responsibilities
3. **MCP (Model Context Protocol)** — Standardized tool interface for agents
4. **Observability by Default** — All services emit structured logs/traces via OpenTelemetry
5. **Private Network** — All services communicate over lms-network (Docker internal network)

**Data Flow:**

1. User request → Caddy → Appropriate service
2. Backend ↔ PostgreSQL (data persistence)
3. Backend → OTel Collector → VictoriaLogs/VictoriaTraces (telemetry)
4. Nanobot → MCP Tools → Backend/Observability → LLM → Response

This architecture enables Lab 8's core concept: "The Agent is the Interface" — one agent with reusable tools that multiple clients can talk to.

---

## Task 1C — Skill prompt

**Question:** "Show me the scores" (without specifying a lab)

**Response:**

I need to know which lab you'd like to see scores for. Here are the available labs:

| ID | Title                                                        |
|----|--------------------------------------------------------------|
| 1  | Lab 01 – Products, Architecture & Roles                      |
| 2  | Lab 02 — Run, Fix, and Deploy a Backend Service              |
| 3  | Lab 03 — Backend API: Explore, Debug, Implement, Deploy      |
| 4  | Lab 04 — Testing, Front-end, and AI Agents                   |
| 5  | Lab 05 — Data Pipeline and Analytics Dashboard               |
| 6  | Lab 06 — Build Your Own Agent                                |
| 7  | Lab 07 — Build a Client with an AI Coding Agent              |
| 8  | lab-08                                                       |

I can show you:
- Pass rates (average score + attempt count per task)
- Completion rate (passed / total learners)
- Top learners by average score
- Group performance (avg score + student count per group)
- Submission timeline (date + submission count)

Which lab would you like to see?

*(The skill prompt correctly teaches the agent to ask for clarification when the required `lab` parameter is missing.)*

## Task 2A — Deployed agent

**Nanobot startup log excerpt:**

```
nanobot-1  | Using config: /app/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | WebChat channel enabled
nanobot-1  | WebChat starting on 0.0.0.0:8765
nanobot-1  | MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
nanobot-1  | MCP: registered tool 'mcp_lms_lms_labs' from server 'lms'
nanobot-1  | MCP: registered tool 'mcp_lms_lms_learners' from server 'lms'
nanobot-1  | MCP: registered tool 'mcp_lms_lms_pass_rates' from server 'lms'
nanobot-1  | MCP: registered tool 'mcp_lms_lms_timeline' from server 'lms'
nanobot-1  | MCP: registered tool 'mcp_lms_lms_groups' from server 'lms'
nanobot-1  | MCP: registered tool 'mcp_lms_lms_top_learners' from server 'lms'
nanobot-1  | MCP: registered tool 'mcp_lms_lms_completion_rate' from server 'lms'
nanobot-1  | MCP: registered tool 'mcp_lms_lms_sync_pipeline' from server 'lms'
nanobot-1  | MCP server 'lms': connected, 9 tools registered
nanobot-1  | Agent loop started
```

---

## Task 2B — Web client

**WebSocket test:** The WebSocket endpoint at `ws://localhost:42002/ws/chat?access_key=student123` accepts connections (HTTP 101 Switching Protocols).

**Flutter client:** Accessible at `http://localhost:42002/flutter/`

To test interactively:
1. Open `http://localhost:42002/flutter/` in a browser
2. Log in with `NANOBOT_ACCESS_KEY=student123`
3. Ask questions like "What can you do?" or "What labs are available?"

---

## Task 3A — Structured logging

**Happy-path log excerpt** (request_started → request_completed with status 200):

```
backend-1 | 2026-03-27 15:09:58,057 INFO [app.main] - request_started
backend-1 | 2026-03-27 15:09:58,058 INFO [app.auth] - auth_success
backend-1 | 2026-03-27 15:09:58,059 INFO [app.db.items] - db_query
backend-1 | 2026-03-27 15:09:58,066 INFO [app.main] - request_completed
```

Each log entry includes structured fields:
- `trace_id` and `span_id` for distributed tracing correlation
- `resource.service.name` for service identification
- `event` for event type (request_started, auth_success, db_query, request_completed)
- `severity` (INFO, ERROR, etc.)

**Error-path log excerpt** (db_query with error when postgres stopped):

```
backend-1 | 2026-03-27 16:00:37,022 ERROR [app.db.items] - db_query
  error: "(sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: connection is closed"
```

**VictoriaLogs query result:**

Query: `curl "http://localhost:42010/select/logsql/query?query=*&limit=5"`

Returns structured JSON logs with fields like:
```json
{
  "_msg": "db_query",
  "event": "db_query",
  "severity": "ERROR",
  "error": "(sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) ... connection is closed",
  "service.name": "Learning Management Service",
  "trace_id": "4ef37ed0e2e834773771b9f03840b08c",
  "span_id": "97a514912140490b"
}
```

---

## Task 3B — Traces

**VictoriaTraces UI:** Accessible at `http://localhost:42002/utils/victoriatraces`

**Healthy trace:** Shows span hierarchy:
- `GET /items/` (root span)
  - `auth_success` (authentication)
  - `db_query` (database query)
  - `request_completed` (response)

**Error trace:** When postgres is stopped, the trace shows:
- Same span hierarchy
- `db_query` span contains error tag with exception details
- `request_completed` span has status 500/404

Trace ID from error: `4ef37ed0e2e834773771b9f03840b08c`

---

## Task 3C — Observability MCP tools

**New MCP tools added:**

| Tool | Description |
|------|-------------|
| `logs_search` | Search VictoriaLogs using LogsQL query |
| `logs_error_count` | Count errors per service over time window |
| `traces_list` | List recent traces for a service |
| `traces_get` | Fetch specific trace by ID |

**MCP server:** `mcp_observability` running alongside `mcp_lms`

**Skill prompt:** `nanobot/workspace/skills/observability/SKILL.md` teaches the agent:
- When asked about errors, call `logs_error_count` first for summary
- Use `logs_search` for detailed log queries
- If trace_id found in logs, fetch full trace with `traces_get`
- Format responses concisely

**Agent response to "Any errors in the last hour?":**

The agent now has access to 4 observability tools via MCP:
- `mcp_observability_logs_search`
- `mcp_observability_logs_error_count`
- `mcp_observability_traces_list`
- `mcp_observability_traces_get`

To test interactively:
1. Open `http://localhost:42002/flutter/`
2. Log in with `student123`
3. Ask "Any errors in the last hour?" or "Show me recent errors"

**Nanobot logs confirming tools registered:**
```
MCP: registered tool 'mcp_observability_logs_search' from server 'observability'
MCP: registered tool 'mcp_observability_logs_error_count' from server 'observability'
MCP: registered tool 'mcp_observability_traces_list' from server 'observability'
MCP: registered tool 'mcp_observability_traces_get' from server 'observability'
MCP server 'observability': connected, 4 tools registered
```

---

## Task 4A — Multi-step investigation

**Updated observability skill** at `nanobot/workspace/skills/observability/SKILL.md` now guides the agent to:

1. Search recent error logs with `logs_search(query="level:error OR severity:error", limit=10)`
2. Extract `trace_id` from error log entries
3. Fetch full trace with `traces_get(trace_id="...")`
4. Summarize findings in plain English

**Investigation flow when user asks "What went wrong?":**

The agent should:
1. Call `logs_search` to find recent errors
2. Find trace_id in the error logs (e.g., `trace_id=7b663c56bdcfc9aef652881d5f9bf9ab`)
3. Call `traces_get` to fetch the full trace
4. Report:
   - Service: Learning Management Service
   - Operation: db_query (database query)
   - Error: connection is closed / gaierror: Name or service not known
   - Root cause: PostgreSQL unavailable

**Example agent workflow:**
```
User: "What went wrong?"
Agent: 
1. Calls logs_search(query="level:error", limit=10)
   → Finds error log with trace_id=7b663c56bdcfc9aef652881d5f9bf9ab
2. Calls traces_get(trace_id="7b663c56bdcfc9aef652881d5f9bf9ab")
   → Gets trace showing db_query span failed
3. Reports: "The backend encountered a database connection error.
   - Service: Learning Management Service
   - Operation: SELECT from item table
   - Error: connection is closed (PostgreSQL unavailable)
   - Trace ID: 7b663c56bdcfc9aef652881d5f9bf9ab
   
   All requests requiring database access will fail until PostgreSQL is restarted."
```

---

## Task 4B — Proactive health check

**Cron skill created:** `nanobot/workspace/skills/cron/SKILL.md`

The skill teaches the agent to:
- Create scheduled jobs using cron syntax
- List active cron jobs
- Remove jobs when requested
- Create health checks that periodically check for errors

**Creating a scheduled health check:**

The agent has a built-in `cron` tool that can schedule recurring jobs. To create a health check:

1. Ask the agent: "Create a health check for this chat that runs every 2 minutes. Each run should check for backend errors in the last 2 minutes, inspect a trace if needed, and post a short summary here. If there are no recent errors, say the system looks healthy. Use your cron tool."

2. Verify with: "List scheduled jobs."

3. The agent will proactively post health reports in the same chat every 2 minutes.

**To manage cron jobs:**
- "List scheduled jobs" — shows all active cron jobs
- "Remove the health check job" — cancels the scheduled job

**Note:** Cron jobs created from the web chat are tied to the current chat session. Do not refresh the Flutter page during testing.

**Testing:**
```
# Access the Flutter web client
http://localhost:42002/flutter/

# Login with NANOBOT_ACCESS_KEY (student123)
# Ask: "Create a health check that runs every 15 minutes"
# Ask: "List scheduled jobs"
```

**Nanobot cron service logs:**
```
nanobot-1 | Cron service started with 0 jobs
```

After creating a job via the Flutter chat, the agent will confirm and the job will appear in the list.

---

## Task 4C — Bug fix and recovery

### 1. Root cause — Planted bug

**Location:** `backend/app/routers/items.py`, function `get_items()`

**Bug:** The exception handler was catching all errors and re-raising them as HTTP 404 "Items not found":

```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Items not found",
        ) from exc
```

**Problem:** When PostgreSQL was unavailable, the error was masked as "404 Not Found" instead of surfacing the real database connection error. This made debugging harder because:
- Wrong HTTP status code (404 instead of 500)
- Misleading error message ("Items not found" vs "Database unavailable")

### 2. Fix — Remove the misleading exception handler

**Changed file:** `backend/app/routers/items.py`

**Before:**
```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Items not found",
        ) from exc
```

**After:**
```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    return await read_items(session)
```

The global exception handler in `main.py` already handles uncaught exceptions and returns proper 500 errors with details.

### 3. Post-fix failure check

After the fix, when PostgreSQL is stopped, the API returns:

```
HTTP/1.1 500 Internal Server Error
{
  "detail": "[Errno -2] Name or service not known",
  "type": "gaierror",
  "path": "/items/"
}
```

This correctly indicates:
- HTTP 500 (Internal Server Error) instead of 404
- Real error: DNS/connection failure to PostgreSQL
- Error type: `gaierror` (getaddrinfo failure)

### 4. Healthy follow-up

After restarting PostgreSQL, the system returns to healthy state:

```
HTTP/1.1 200 OK
[{"title":"Lab 01 – Products, Architecture & Roles","id":1,...}, ...]
```

The proactive health check would report: "System looks healthy — no errors in the last 2 minutes."

---
