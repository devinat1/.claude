---
name: research-gap
description: Evidence-backed opposing novelty views from a literature-review report (runs literature-review first if none exists in chat). Use when the user invokes /research-gap or asks whether a research question or idea is novel.
disable-model-invocation: true
---

# Research gap

Surface opposing novelty views from prior work. **Do not recreate discovery** — reuse `literature-review` for search lanes, saturation, and entry depth. Own only the evidence packet and dissent.

<HARD-GATE>
Do NOT implement or design the idea. Do NOT build an adaptive reading loop or “read next” queue. Do NOT save to agent memory, Todoist, Obsidian, or repo files unless the user explicitly asks later. Do NOT claim complete coverage of the literature. Do NOT invent citations, paper content, or metadata.
</HARD-GATE>

## Phase 1 — Resolve the question(s)

Use the slash argument, then the latest substantive user message. If nothing usable exists, ask only: "What research question should I assess?"

Ask at most one further question only when a domain, population, intervention/method, or outcome is essential to distinguish the question from prior work. Keep questions one at a time.

## Phase 2 — Obtain a literature-review report

Discovery contract lives in `literature-review`. Follow that skill’s phases when you must run discovery (briefs, four lanes to saturation, deep academic entries, collected multi-idea reports). Prefer invoking/running that skill over copying its search instructions here.

### 2a. Report already in chat

If a `/literature-review` (or equivalent prior-work) report is already in this conversation:

1. Use it as the primary evidence base.
2. If academic deep-treated entries look **sparse relative to the question**, or lack Consensus-backed paper searches for the question, fully re-run discovery via `literature-review`, wait for that denser report, then continue — do not novelty-judge on a thin academic set.
3. Otherwise proceed to Phase 3 with the existing report (no extra discovery required).

### 2b. No report in chat

Run `literature-review` to completion for the resolved question/idea(s) (**in-flow**: do the discovery work now, including waiting for saturation and the collected report). Then continue to Phase 3 in the **same flow** without requiring the user to re-invoke `/research-gap`.

When research-gap is driving discovery, background-notify behavior from `literature-review` may be skipped so the opposing views can follow immediately after the report is ready.

## Phase 3 — Prepare the evidence packet

If the report is a **collected multi-idea** review, prepare a **separate** evidence packet for **every** idea section.

For each question/idea, compare the closest work on population, setting, inputs, method, outcome, and claimed contribution. Include supporting citations and the search limits that bear on both views.

Preserve uncertainty. Never claim complete literature coverage or a final novelty verdict.

## Phase 4 — Two novelty views

Invoke `dissenter` once per evidence packet, with the resolved question, the collected literature-review report, and the closest-work comparison. Return its **Original view** and **Opposing view** as two evidence-backed positions on whether the idea is novel. Preserve disagreement; do not choose a winner or combine the views into a verdict.

## Output format

```markdown
# Research-gap review

## [Idea / question label]

### Original view
[Evidence-backed position on whether the idea is novel.]

### Opposing view
[Evidence-backed counter-position on whether the idea is novel.]

### Closest prior work
- [citation](url) — [specific overlap and difference]
- …

### Search limits
- [sparsity judgment, re-run notes, coverage gaps from the literature-review, unavailable full text, blind spots]

### Takeaways
- [Meaningful agreement or decision-critical disagreement.]

---

## [Next idea / question label, if multi-idea]

…
```

For a single idea, one section is enough (keep the same headings).

No “Read next”, “Skip for now”, or adaptive quiz loop.
