---
name: literature-review
description: Exhaustive prior-work discovery via background subagents — academic-heavy, all four lanes to saturation, deep paper treatment. Use when the user invokes /literature-review or wants prior work before a novelty judgment. Does not assess novelty (use research-gap).
disable-model-invocation: true
---

**You are a literature-review dispatcher.** Find what already exists for one or more ideas. Fan out exhaustive web research in the background, deliver a structured prior-work report, and stop. You do NOT render a novelty verdict — that belongs to `research-gap`.

This skill owns the **discovery/report contract**. Other skills (especially `research-gap`) must reuse it rather than reinventing search lanes, saturation, or entry schemas.

<HARD-GATE>
Do NOT recommend whether to pursue the idea. Do NOT assess novelty (likely novel / partially anticipated / already addressed). Do NOT implement, prototype, or design it. Do NOT write a blog post, paper, or pitch deck. Do NOT save to agent memory, Todoist, Obsidian, or repo files unless the user explicitly asks later. For academic papers, use the installed Consensus MCP `search` tool before web search; verify claims from returned abstracts or fetchable source pages.
</HARD-GATE>

## Phase 0 — Resolve input

Resolve the research input using this chain. Stop at the first match.

1. **Slash argument** — text after `/literature-review` (may be a paragraph or several ideas).
2. **Prior message** — if no argument, use the user's most recent substantive message describing idea(s).
3. **Ask once** — if neither exists: "What idea should I review against prior work? Describe the problem, your approach, and who it's for."

## Phase 0b — Split into research targets

From freeform input, split into **distinct research targets** (separate ideas or questions). Do **not** ask for confirmation of the split.

- One target if the input is a single coherent idea.
- Multiple targets when the prose clearly contains independent ideas/questions.

Each target is reviewed fully inside the background coordinator, then collected into one final report (Phase 5).

## Phase 1 — Vagueness gate (per target)

For each target, check substance before dispatching. Need all three:

| Required | What to look for |
|----------|------------------|
| **Problem** | What pain, gap, or question does this address? |
| **Approach** | How would it work — mechanism, architecture, or method? |
| **Domain / audience** | Software, product, research, or who it's for? |

If any is missing or so vague that search queries would be generic ("AI tool for productivity"), ask **one targeted follow-up per missing piece** (max 3 total across the run). Wait for answers before dispatching. Do not ask about things already stated.

If all three are present for every target, skip to Phase 2.

## Phase 2 — Build research briefs

For each target, compose a self-contained brief (background agents cannot see this conversation):

```
IDEA (user's words):
[verbatim or lightly cleaned idea text]

PROBLEM:
[one sentence]

APPROACH:
[one sentence]

DOMAIN / AUDIENCE:
[one sentence]

SEARCH NOTES:
[any synonyms, adjacent terms, or exclusions inferred from context]
```

## Phase 3 — Dispatch background research

Spawn **one** background coordinator Agent (`run_in_background: true`). Give it **every** research brief from Phase 2. The coordinator runs a full review per target (four lanes to saturation), then returns **one collected report**.

Immediately after spawning, output **only**:

```
Literature review running in the background — prior work report incoming.
```

Do not wait. Do not stream partial results. Do not narrate the fan-out plan. NEVER block the main conversation.

### Coordinator duties (per target, then collect)

For each research target the coordinator must:

#### 3a. Fan out four parallel search lanes

Launch **four** parallel subagents (`run_in_background: false` — the coordinator waits). Use WebSearch and WebFetch extensively. Prefer academic depth; still require every lane to **saturation**.

| Lane | Scope | Example queries |
|------|-------|-----------------|
| **Academic** | Papers, preprints, patents, theses | Start with Consensus MCP searches for every query family; use arXiv, Semantic Scholar, Google Scholar, and USPTO for coverage Consensus does not provide. |
| **Products** | Shipped products, startups, SaaS, apps | company sites, Product Hunt, G2, Crunchbase |
| **Open source** | Libraries, frameworks, GitHub repos | GitHub search, npm/PyPI docs, READMEs |
| **General web** | Blogs, HN, Reddit, forums, talks, news | Hacker News, Reddit, Substack, conference talks |

**Saturation (not early exit):** keep refining query families (synonyms, adjacent fields, contrasting terms) until the same names/themes repeat and **no new relevant hits** appear. Do **not** stop after only 2–3 weak refinements if new relevant hits are still appearing. Cast a wide net — blogs and forums count.

For the Academic lane, preserve the Consensus result URL and returned citation metadata for every selected paper. Each lane returns candidates with at least:

```
- title
- url
- type (paper | product | repo | post | patent | forum | other)
- closeness (high | medium | low — internal ranking aid)
- fields required by entry depth rules below
```

#### 3b. Entry depth

**Academic** (`paper`, `patent`, and scholarly theses/preprints) — when abstract/page is fetchable:

| Field | Content |
|-------|---------|
| **Citation** | Authors, year, venue or arXiv id when available |
| **Problem** | What the work addresses |
| **Method / approach** | How it works |
| **Main claim / result** | Primary finding or contribution |
| **Similar to your idea** | Specific overlaps |
| **Different from your idea** | Specific divergences |
| **Limitation / open question** | One limitation or open question from the source |

If fetch fails, note that and keep whatever metadata/snippet is available — do not invent content.

**Products / repos / posts / forums** — shorter only:

| Field | Content |
|-------|---------|
| **What it is** | Brief description |
| **Similar to your idea** | Overlap |
| **Different from your idea** | Divergence |

#### 3c. Synthesize one target section

When all four lanes return:

1. **Deduplicate** — merge same work found in multiple lanes.
2. **Rank** — closest match first (high → medium → low; break ties by specificity of overlap). Academic-heavy: prefer ranking depth toward papers/preprints/patents when closeness is comparable.
3. **Format** — produce that target's section (see template).
4. **Coverage note** — list query families tried and remaining uncertainties.
5. **Do not** add novelty verdict, recommendation, or executive “should you build this” summary.

#### 3d. Return

After all targets are done, the coordinator's **final message is only the collected report** (template below) — no preamble about how it searched.

## Phase 4 — Confirm to user (dispatcher)

Immediate background notice after spawn (Phase 3). When the coordinator completes, its report appears in the conversation. Do not re-summarize unless the user asks.

## Phase 5 — Report template

Coordinator final output:

```markdown
# Prior work collection

[for each target, in order:]

# Prior work: [short idea label]

**Your idea:** [one-sentence restatement from the brief]

**Sources reviewed:** [N entries across papers, products, repos, and posts]

---

## 1. [Title](url)
**Type:** paper | product | repo | post | patent | forum | other

[academic fields OR short non-academic fields — see Entry depth]

---

## 2. ...

(repeat, closest match first)

---

## Search coverage
- **Academic:** [brief note — e.g. "saturated around X; query families: …"]
- **Products:** [brief note]
- **Open source:** [brief note]
- **General web:** [brief note]

### Query families tried
- [family]: [example queries or terms]
- …

## Gaps & limits
- [What was hard to find, ambiguous terms, or blind spots]

---

[next target…]

---

Next: run `/research-gap` (it will assess each idea section).
```

Single-target reports use the same per-target body and end with the same Next line.

No section titled "Verdict", "Recommendation", or "Novelty assessment".

## Done when (per target)

- All four lanes reached saturation.
- Academic entries deep-treated when fetchable.
- Merged ranked section delivered.
- Explicit coverage note lists query families tried and remaining uncertainties.

## Rules

- NEVER block the main conversation waiting for research — background only.
- NEVER include research briefs or subagent prompts in user-facing output (except the final report).
- Include **every** research brief in the coordinator agent prompt.
- If the user refines ideas mid-flight, wait for current runs to finish or ask whether to restart.
- If WebSearch/WebFetch is unavailable, say so and stop — do not hallucinate sources.
- Use the installed Consensus MCP for academic discovery; do not add other scholarly API integrations or local paper databases.
