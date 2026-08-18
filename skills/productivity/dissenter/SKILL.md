---
name: dissenter
description: >
  Run two independent perspectives for a meaningful decision, proposal,
  recommendation, or plan: one analyzes the user's prompt as written and one
  supplies the strongest credible dissent. Use when competing courses of action
  or assumptions need stress-testing, including immediately before a skill gives
  consequential user-facing advice; skip routine execution, factual lookups,
  and status questions.
---

# Dissenter

Stress-test a material choice without manufacturing a debate.

## Advice gate

This is the authoritative gate for every owned skill that gives
consequential user-facing advice.

Apply it **after gathering relevant context and before** recommending,
prioritizing, selecting, scheduling, or proposing a course of action for the
user. Do not apply it to factual reporting, a procedure the user already
chose, routine execution, or immediate safety instructions.

When the gate applies:

1. Invoke `dissenter` with the decision, the user's goal, and the relevant
   evidence gathered so far.
2. Present the two views below without selecting a winner or default.
3. End with one explicit question that asks the user to choose or supply a
   different option.
4. Wait for that answer before taking an action that depends on the choice.

This gate overrides any local instruction to make a consequential
recommendation, choose a priority, or advance automatically.

## Dispatch

1. Confirm the request contains a meaningful choice, proposal, recommendation, or plan. If it does not, answer normally.
2. Launch exactly two independent subagents in parallel. Do not give either agent the other's response.
   - **Original:** Send the user's request plus the gathered context. Ask it for one viable course of action, its assumptions, and tradeoffs. It must not claim to choose for the user.
   - **Dissent:** Send the same request and context. Ask it for the strongest credible alternative: challenge the core assumptions, surface material risks, and present a viable course. Do not use a literal inverse or a straw man.
3. Wait for both agents. Do not substitute the coordinator's own answer for either perspective.

## Return

Return only this concise structure:

```markdown
## Original view
[direct analysis]

## Opposing view
[counter-analysis]

## Takeaways
- [meaningful agreement, if any]
- [decision-critical disagreement or assumption]

## Your decision
[one question that lets the user choose a view or name another option]
```

Do not force a winner or recommendation. Preserve uncertainty where the agents disagree, and wait for the user's choice.

## Partial results

If one agent fails or is unavailable, return the completed view under its heading and write `Unavailable: [brief reason]` under the missing heading. Still include only takeaways supported by the available result.
