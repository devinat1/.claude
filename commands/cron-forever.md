---
name: cron-forever
description: Create a self-renewing cron job that never expires. Usage: /cron-forever <cron-expression> <prompt>
---

Create a **self-renewing cron job** from the following arguments:

$ARGUMENTS

## How to parse arguments

The arguments contain a **cron expression** and a **task prompt**. The cron expression is the standard 5-field format (minute hour day-of-month month day-of-week). Examples of valid input:

- `/cron-forever "0 9 * * *" Check my open PRs and summarize status`
- `/cron-forever */30 * * * * Monitor deploy status`
- `/cron-forever 0 9 * * 1-5 Review overnight alerts`

If the cron expression is quoted, use the quoted portion. Otherwise, take the first 5 space-separated tokens as the cron fields and everything after as the task prompt.

If the arguments are missing or unclear, ask the user for the cron schedule and prompt.

## How to create the job

### Step 1: Generate a job ID

Create a short, descriptive kebab-case ID from the task prompt (e.g., `check-open-prs`, `monitor-deploys`). Check that `~/.claude/cron-forever/<id>.md` does not already exist. If it does, append a number.

### Step 2: Write the job definition file

Write the following to `~/.claude/cron-forever/<id>.md`, substituting the real values:

```markdown
---
cron: <CRON_EXPRESSION>
created: <TODAY'S DATE>
---

## Step 1: Renew this job (DO THIS FIRST)

Before doing anything else, re-create this cron job so it does not expire.
Call CronCreate with:
- cron: "<CRON_EXPRESSION>"
- durable: true
- recurring: true
- prompt: "Read the file /Users/devinat1/.claude/cron-forever/<ID>.md and follow all instructions in it exactly."

If CronCreate fails, warn the user that this job will expire if not manually renewed.

## Step 2: Execute the task

<TASK_PROMPT>
```

### Step 3: Create the initial cron job

Call CronCreate with:
- cron: the parsed cron expression
- durable: true
- recurring: true
- prompt: `Read the file /Users/devinat1/.claude/cron-forever/<ID>.md and follow all instructions in it exactly.`

Avoid the :00 and :30 minute marks when the user's time is approximate (per CronCreate guidelines).

### Step 4: Confirm to the user

Tell the user:
- The job was created and will self-renew on every execution
- The job definition lives at `~/.claude/cron-forever/<id>.md`
- They can edit that file to change the task without recreating the job
- They can delete that file and the cron job to stop it permanently
- Show the cron schedule in human-readable form
