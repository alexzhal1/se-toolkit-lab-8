# Cron Skill — Scheduled Jobs

You have a built-in `cron` tool that lets you schedule recurring jobs in the current chat session.

## Available Cron Commands

Use these commands directly in conversation:

| Command | Description |
|---------|-------------|
| "Create a job that runs every X minutes/hours" | Schedule a recurring job |
| "List scheduled jobs" | Show all active cron jobs |
| "Remove job [name/ID]" | Cancel a scheduled job |
| "Remove all jobs" | Cancel all scheduled jobs |

## Creating a Health Check

When the user asks for a periodic health check, create a job that:
1. Runs at the specified interval (e.g., every 15 minutes)
2. Checks for recent errors using `logs_error_count` or `logs_search`
3. Posts a summary to the same chat

**Example:**
User: "Create a health check that runs every 15 minutes"
You: Use your cron tool to create a job with:
- Schedule: `*/15 * * * *` (every 15 minutes)
- Task: Check for backend errors and post a summary

## Job Schedule Format

Use standard cron syntax:
- `*/15 * * * *` — every 15 minutes
- `0 * * * *` — every hour
- `0 */2 * * *` — every 2 hours
- `0 9 * * *` — every day at 9 AM

## Important Notes

1. **Chat-bound**: Cron jobs are tied to the current chat session. If the user refreshes the page or starts a new chat, jobs from the previous session won't post there.

2. **Confirm creation**: After creating a job, confirm with the user: "I've created a health check job that runs every 15 minutes. It will check for backend errors and post a summary in this chat."

3. **List jobs**: When asked to list jobs, show:
   - Job name/ID
   - Schedule (cron expression or human-readable)
   - Next run time
   - Task description

4. **Remove jobs**: When asked to remove a job, confirm: "I've removed the health check job. It will no longer run."

## Example Interactions

**User**: "Create a health check for this chat that runs every 15 minutes."
**You**: [Creates cron job] "Done! I've scheduled a health check that runs every 15 minutes. Each run will check for backend errors and post a summary in this chat."

**User**: "List scheduled jobs."
**You**: "You have 1 scheduled job:
- Health Check (every 15 minutes)
  Next run: 2026-03-27 16:45:00
  Task: Check for errors and post summary"

**User**: "Remove the health check job."
**You**: "I've removed the health check job. It will no longer run."
