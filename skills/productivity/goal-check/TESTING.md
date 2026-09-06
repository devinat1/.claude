# Goal-check acceptance checks

Run `./scripts/generate-skill-metadata.py --check` and
`./scripts/agentic doctor` from the skills repository to check discovery.

In a new interactive chat using the shared instructions, request a simple task
such as “Draft a two-sentence follow-up email.” Verify the agent loads
`goal-check` and asks the goal question before drafting or offering other skills.
A description in the skill catalog alone is not proof of automatic invocation.

Exercise each branch in fresh chats (use a sandbox AgentMemory for write tests):

| Context / reply | Expected behavior |
| --- | --- |
| Personal and project goals available | Lists recalled current goals with scope labels; asks which one the task supports. |
| Successful recall with no goals | Asks for a goal with optional saving or one-off bypass. |
| Memory tool absent or recall fails | Says recall is unavailable, not that no goals exist; offers session-only goal or bypass. |
| Numbered selection | Accepts it and performs the original task without saving. |
| Free-form explanation | Accepts the connection without judging or saving. |
| “One-off” or “skip” | Performs the original task without changing memory. |
| “Add a goal” or “Save this connection” | Shows proposed content and asks personal/project/no-save before any write. |
| Project destination unknown | Does not invent a stable ID or offer an unverified project destination. |
| Approval of shown content and destination | Writes only that approved change; preserves unrelated content. |
| No save | Continues session-only. |
| Write fails | Reports not saved and continues; no blind retry of an uncertain write. |
| Second task or resumed chat after check | Performs the task without reopening the check. |
| Greeting only | Waits for a substantive task. |
| Scheduled run or delegated subagent | Does not interrupt for an interactive goal choice. |

No branch should invoke BeeMinder, assess avoidance, or copy goals into local
files. Automated model probes with supplied recall fixtures test instruction
behavior only; they do not verify live memory retrieval or writing.
