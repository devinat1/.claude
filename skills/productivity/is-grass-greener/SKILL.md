---
name: is-grass-greener
description: Expose the pros and cons of named past, possible, or current life paths without recommending a choice. Use when the user invokes /is-grass-greener, asks whether the grass would have been greener, or wants an even tradeoff view of career, education, relationship, location, or another major life path.
---

# Is Grass Greener?

Expose the tradeoffs in each path the user names. The result is a compact
pros-and-cons view, not a verdict.

## Resolve the paths

Analyze only paths the user explicitly names. Accept one or several paths; do
not add the user's actual or current path unless they named it. A path that is
still available is analyzed the same way as a closed counterfactual.

Use relevant context already available in the conversation. Ask one essential
missing question at a time only when the answer would materially change the
analysis. If the requested scope is unclear, ask whether the user wants
domain-specific effects or whole-life consequences. Do not repeat that
question when the prompt or context already answers it.

## Ground the tradeoffs

For a counterfactual, analyze the single most plausible version of the path.
Represent uncertainty inside the bullets rather than inventing a detailed
alternate life or branching into scenarios.

Use current web research only when a time-sensitive fact could materially
change a pro or con. Keep research proportional to the brief output, and put
any necessary citation in the affected bullet.

Treat every path fairly. Give the user's actual path no privileged treatment,
and never declare that one entire life would have been better or worse.

Detect idealization: look for attention concentrated on an attractive feature
while routine costs, opportunity costs, or constraints are discounted. When
present, place one direct `Idealization warning:` sentence beneath that path's
heading and make the overlooked costs concrete in the cons.

## Return only the tradeoffs

Use this shape for every named path:

```markdown
## [Path]

[Optional: Idealization warning: one brief sentence.]

### Pros

- [Brief, personalized benefit]

### Cons

- [Brief, personalized cost]
```

Include at most three one-sentence pros and three one-sentence cons per path.
Use fewer when additional bullets would be weak or repetitive. Keep the tone
direct and unsentimental.

The final analysis contains only path headings, an optional idealization
warning, and the pros and cons. It has no ranking, winner, recommendation,
verdict, score, conclusion, synthesis, next step, or closure exercise. Stop
immediately after the final con.
