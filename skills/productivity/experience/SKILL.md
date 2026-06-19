---
name: experience
description: Update agent memory with diagnostic feedback from the current session. Use when the user invokes /experience.
disable-model-invocation: true
---

**You are a skills assessment dispatcher.** Your job is to summarize the session's skill signals and hand them to a background agent for agent memory updates.

## When triggered

If the user provided additional text with the command (e.g., `/experience focus on my system design thinking`), treat it as a focus directive. Prioritize that area in your signal extraction and include the directive verbatim in the background agent prompt so it shapes the agent memory update.

### Step 1: Summarize session signals

Re-read the full conversation. For each domain touched (e.g., React, System Design, SQL, General Reasoning), extract:

1. **Thinking Check scores** — the Specificity, Ownership, and Diagnostic scores from each evaluated prompt, grouped by domain
2. **Prompt precision** — for each domain, note whether the user was decisive and specific (green signal), mixed (yellow signal), or vague and delegating (red signal)
3. **Incorrect assumptions** — list anything the user stated as fact that was wrong. For each, note:
   - What they said
   - What is actually true
   - What underlying mental model gap this reveals
4. **Strengths demonstrated** — areas where the user showed clear mastery, made good decisions unprompted, or corrected their own mistakes

### Step 2: Dispatch background agent

Spawn a single background Agent (`run_in_background: true`) with the following prompt structure. Include ALL of the signal data from Step 1 directly in the agent prompt — the agent has no access to this conversation.

The agent prompt must instruct it to:

1. **Read** [`agent-memory-logging.md`](../../learning/agent-memory-logging.md) and follow its recall-then-save workflow.

2. **Recall** prior entries for each touched domain via `memory_recall` / `memory_smart_search`.

3. **Save** one `memory_save` per discrete update, synthesizing with prior evidence (append-only):
   - domain status changes → `skills-domain:` with domain-specific diagnostic label and concrete actionable gap (System Design → Scale Blind Spots / Tradeoff Analysis; React → Thinking Mistakes / Mental Model Gaps; General Reasoning → First Principles Gaps; Databases → Query Reasoning / Data Modeling Assumptions; choose appropriately for new domains)
   - new systematic gaps → `blind-spot:`
   - corrected understanding → `resolved-blind-spot:` with identified date, resolved date, and evidence
   - adjust status (green/yellow/red) based on accumulated evidence, not single interactions

4. **Do not** write to any markdown tracker file. On MCP failure, report failure — no file fallback.

5. **Todoist integration** — ONLY if a new blind spot was added or a domain was newly rated as red:
   - Use `find-projects` to find the project named "claude"
   - Use `find-tasks` with the "claude" project ID to fetch all existing tasks in the project
   - Before creating any task, compare the new task against existing ones:
     - If an existing task covers the same domain and blind spot: use `update-tasks` to enhance it with new evidence and sharpen the actionable item, rather than creating a duplicate
     - If no existing task matches: use `add-tasks` to create a new task with:
       - `content`: A specific, actionable practice item (e.g., "Design a connection pooling strategy for a 100K-user app — start with pgBouncer docs and calculate max connections per instance given 4 app server replicas")
       - `description`: Context from the session — what the blind spot is, why it matters, what evidence triggered it
       - `projectId`: the "claude" project ID
   - Do NOT create tasks for yellow items, existing entries, or resolved blind spots

### Step 3: Confirm to user

Output only: "Updating agent memory in the background."

Do not output any other information. Do not wait for the agent to complete. Do not show agent results.

## Rules

- NEVER block the main conversation. The agent runs in the background.
- NEVER show agent results or agent memory contents to the user unless they explicitly ask.
- NEVER update agent memory without the user invoking /experience.
- Include ALL signal data in the agent prompt — the agent cannot see this conversation.
- If the session had zero skill signals, say "No meaningful skill signals in this session — nothing to update." and do not spawn an agent. A skill signal is any prompt that received a Thinking Check evaluation, or any exchange where the user made a technical claim, architectural decision, or debugging hypothesis. Greetings, confirmations, and slash commands are not skill signals.
