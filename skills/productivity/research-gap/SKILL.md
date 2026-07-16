---
name: research-gap
description: Evaluate a research question against prior work, make an evidence-backed novelty assessment, and adapt a section-level reading plan to the user's understanding. Use when the user asks whether a research question is novel, what papers or paper sections to read, or how to prioritize literature for a question.
disable-model-invocation: true
---

# Research gap

Assess a research question against prior work, then direct the user to the smallest set of paper sections that can change the novelty judgment or their next research decision.

Reuse the discovery discipline in `literature-review` and the one-question diagnosis pattern in `learn`. Do not recreate either workflow or claim complete coverage.

## Phase 1: Resolve the question

Use the slash argument, then the latest substantive user message. If the question is still missing, ask only: "What research question should I assess?"

Ask at most one further question only when a domain, population, intervention/method, or outcome is essential to distinguish the question from prior work. Keep every question one at a time.

## Phase 2: Search prior work

Search best-effort across peer-reviewed papers, preprints, review articles, theses, and influential technical reports. Emphasize peer-reviewed papers in the assessment. Use scholarly indexes and primary sources where possible; use citation chaining from the closest work until results repeat.

Record:

- sources and query terms searched;
- date or coverage limits that may hide work;
- terms with ambiguous meanings; and
- material unavailable in full text.

Never say that all relevant literature was found. Never invent a citation, paper content, access status, page, or section heading.

## Phase 3: Assess novelty

Compare the research question with the closest work on population, setting, inputs, method, outcome, and claimed contribution. Give one evidence-backed assessment:

- **likely novel** — no close work answers the same question in the same setting;
- **partially anticipated** — prior work covers meaningful parts but leaves a stated difference; or
- **already addressed** — close prior work substantially answers it.

For every conclusion, cite the supporting paper and state the uncertainty or search limitation that could change it. This is an evidence-based assessment, not a guarantee of novelty.

## Phase 4: Build the reading queue

Rank papers by direct usefulness for answering the research question and changing the novelty assessment. Prefer a short queue. For each paper, include:

| Priority | Paper | Read | Extract | Why now |
|---|---|---|---|---|
| 1 | citation and link | exact sections/pages/headings | result, method, limitation, or definition to learn | effect on the novelty assessment |

Only give section-level guidance when the full text is accessible and supports it. For a paywalled or inaccessible but important paper, label it **important—full text unavailable** and omit section guidance. Include a **Skip for now** list for relevant papers or sections unlikely to change the judgment or next decision.

## Phase 5: Adaptive reading loop

After the user reads a recommended item, ask one concise open-ended question about the specified extraction goal. Do not quiz broadly and do not expose a long dependency stack.

Use the answer to revise the next item:

- if their reading resolves the key comparison, move to the next uncertainty;
- if they missed a prerequisite, recommend only the shortest relevant section that supplies it;
- if new evidence changes the assessment, say what changed and rerank the queue.

Continue whether the question appears novel or not. Stop when the user can explain the closest prior work, the remaining gap (if any), and the evidence supporting that view.

## Output format

Use this compact structure after research:

```markdown
# Research-gap review: [question]

## Novelty assessment
[likely novel | partially anticipated | already addressed] — [one evidence-backed sentence].

## Closest prior work
- [citation](url) — [specific overlap and difference]

## Read next
| Priority | Paper | Read | Extract | Why now |
|---|---|---|---|---|

## Skip for now
- [paper or section] — [why it is unlikely to change the decision]

## Search limits
- [sources, queries, dates, unavailable material, and blind spots]
```

End with one question only when a user response is needed to refine the queue.
