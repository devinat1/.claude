---
name: dissenter
description: >
  Run two independent perspectives for a meaningful decision, proposal,
  recommendation, or plan: one analyzes the user's prompt as written and one
  supplies the strongest credible dissent. Use when competing courses of action
  or assumptions need stress-testing; skip routine execution, factual lookups,
  and status questions.
---

# Dissenter

Stress-test a material choice without manufacturing a debate.

## Dispatch

1. Confirm the request contains a meaningful choice, proposal, recommendation, or plan. If it does not, answer normally.
2. Launch exactly two independent subagents in parallel. Do not give either agent the other's response.
   - **Original:** Send the user's original prompt unchanged. Ask it to analyze and answer the prompt directly, stating key assumptions and tradeoffs.
   - **Dissent:** Send the user's original prompt and ask it to identify the strongest credible objection: challenge its core assumptions, surface material risks, and present a viable alternative. Do not use a literal inverse or a straw man.
3. Wait for both agents. Do not substitute the coordinator's own answer for either perspective.

## Return

Return only this concise structure:

```markdown
## Original view
[direct analysis]

## Credible dissent
[counter-analysis]

## Takeaways
- [meaningful agreement, if any]
- [decision-critical disagreement or assumption]
```

Do not force a winner or recommendation. Preserve uncertainty where the agents disagree.

## Partial results

If one agent fails or is unavailable, return the completed view under its heading and write `Unavailable: [brief reason]` under the missing heading. Still include only takeaways supported by the available result.
