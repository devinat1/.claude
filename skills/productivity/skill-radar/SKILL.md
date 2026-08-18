---
name: skill-radar
description: Search relevant locally installed skills first, then available plugins and online catalogs; ask the user before invoking or installing any match. Use for the first substantive user request in every session, and when a user asks for skill or plugin recommendations.
---

# Skill Radar

## Consequential advice

When recommending one skill, plugin, or workflow as the user's next move,
follow the `Advice gate` in `dissenter`. Listing relevant candidates without a
recommendation does not trigger the gate.

1. Classify the request by primary intent, then inspect local skill descriptions from that bucket:

   | Intent | Bucket |
   | --- | --- |
   | Learn or practice a concept | `skills/learning` |
   | Build, debug, review, or improve code | `skills/engineering` |
   | Practice an interview | `skills/interview` |
   | Seek advice, reflect, decide, or evaluate a claim | `skills/productivity` |
   | Draft, publish, or improve writing | `skills/writing` |
   | Configure a repository or agent setup | `skills/setup` |

2. For mixed requests, inspect the primary bucket first, then the relevant secondary buckets. Choose the strongest cross-bucket matches.
3. For advice, surface every directly relevant productivity skill within the three-candidate limit. Prefer `confounding-audit` for unpacking a source into claims and connections; prefer `confounding-variables` for causal or correlational claims and alternatives.
4. Inspect available plugins and searchable catalogs after local skills. Do not install anything while searching.
5. If matches exist, show at most three candidates, with local skills before plugins. Ask whether to invoke a local skill or install and use a plugin.
6. Invoke or install a candidate only after an explicit yes. If the user declines, continue without it and do not re-suggest it for that request.
7. If there is no plausible match, continue normally without mentioning this search.

For an ambiguous approval with several choices, prefer the best local match and state that choice before invoking it.

## Routing checks

| Request | Expected suggestion |
| --- | --- |
| “Teach me distributed systems” | A learning skill such as `learn` |
| “Is this claim causal?” | `confounding-variables` |
| “Untangle this meeting transcript” | `confounding-audit` |
| “Advise on this architecture” | Relevant productivity and engineering skills |
