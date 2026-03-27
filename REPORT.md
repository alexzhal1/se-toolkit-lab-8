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

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
