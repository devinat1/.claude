---
name: confounding-variables
description: Identify discussion themes and candidate confounding variables in pasted text. Use when evaluating a claim, correlation, observation, article, meeting note, or conversation for alternative causal explanations.
---

# Confounding Variables

Analyze only the supplied text. Do not research, verify, or rank candidates.

1. Split the text into distinct themes. Combine repeated points about the same question.
2. For each theme, state any causal or correlational claim as `exposure -> outcome`. If neither is present, say that confounding cannot be assessed for that theme.
3. List candidate confounders: factors that could affect both the exposure and outcome. Give each a short mechanism.
4. Exclude variables described as caused by the exposure (mediators) or caused by both the exposure and outcome (colliders). If the text makes the direction unclear, keep the variable and mark the direction as unclear.
5. End each assessable theme with a compact causal map using arrows. Include the claimed relationship and each candidate's two links.

## Output

Use this structure:

```markdown
## Theme: [short name]

Claim: [exposure] -> [outcome], or `No assessable causal claim.`

Candidate confounders:
- [variable] — [how it could influence both sides]

Causal map: [confounder] -> [exposure]; [confounder] -> [outcome]; [exposure] -> [outcome]
```

Call the items candidates, not findings. A causal map shows a possible explanation; it does not establish causation.
