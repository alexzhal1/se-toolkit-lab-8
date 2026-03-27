# Cron Skill — Scheduled Jobs

You have a built-in `cron` tool that lets you schedule recurring jobs in the current chat session.

## How to Use Cron

Call the `cron` tool with these parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `action` | What to do: "add", "list", or "remove" | "add" |
| `message` | What the job should do | "Check for backend errors and post a summary" |
| `every_seconds` | Interval in seconds (for recurring jobs) | 900 (15 minutes) |
| `cron_expr` | Cron expression (alternative to every_seconds) | "0 */15 * * *" |
| `tz` | Timezone (optional) | "UTC" |
| `job_id` | Job ID to remove (when action="remove") | "abc123" |

## Creating a Health Check

When the user asks for a periodic health check:

1. **Understand the request**: User wants regular error checks
2. **Call cron tool** with:
   - `action`: "add"
   - `message`: "Check for backend errors using logs_error_count and post a summary to this chat"
   - `every_seconds`: 900 (for 15 minutes) or as requested

**Example:**
```
cron(action="add", message="Check for backend errors and post a summary", every_seconds=900)
```

## Time Expressions

Convert user requests to seconds:

| User says | every_seconds |
|-----------|---------------|
| every 5 minutes | 300 |
| every 10 minutes | 600 |
| every 15 minutes | 900 |
| every 30 minutes | 1800 |
| every hour | 3600 |
| every 2 hours | 7200 |

## Listing and Removing Jobs

**List jobs:**
```
cron(action="list")
```

**Remove a job:**
```
cron(action="remove", job_id="<job_id_from_list>")
```

## Example Interactions

**User**: "Create a health check that runs every 15 minutes"
**You**: Call `cron(action="add", message="Check for backend errors and post a summary", every_seconds=900)`
Then confirm: "I've created a health check that runs every 15 minutes. It will check for errors and post a summary in this chat."

**User**: "List scheduled jobs"
**You**: Call `cron(action="list")` and show the results.

**User**: "Remove the health check job"
**You**: Call `cron(action="list")` first to get the job_id, then `cron(action="remove", job_id="...")`.

## Important Notes

1. **Chat-bound**: Cron jobs are tied to the current chat session. If the user refreshes the page, jobs won't post to the new session.

2. **Confirm creation**: Always confirm after creating a job with the schedule and what it will do.

3. **Use observability tools**: When the cron job runs, it should use `logs_error_count` or `logs_search` to check for errors.
