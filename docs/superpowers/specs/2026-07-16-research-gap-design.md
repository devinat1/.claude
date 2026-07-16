# Research-gap skill design

## Purpose

Help a researcher evaluate whether a research question is novel and spend reading time only on literature that can change that judgment or the next research decision.

## Approach

Add one `research-gap` productivity skill. It composes the existing `literature-review` workflow for discovery and the `learn` workflow's one-at-a-time gap diagnosis pattern. It does not replace, edit, or change either skill's behavior.

## Workflow

1. Accept one research question and any supplied constraints.
2. Search prior work best-effort across peer-reviewed papers, preprints, reviews, theses, and influential reports, with peer-reviewed work weighted most heavily.
3. Report search coverage, search terms, sources searched, and blind spots.
4. Compare the question with the closest work and give a cited, uncertainty-aware novelty assessment: likely novel, partially anticipated, or already answered.
5. Produce a minimal ordered reading queue ranked by direct relevance to the question and novelty decision.
6. For accessible full text, name exact sections/pages/headings, the fact or method to extract, and why it affects the assessment. For inaccessible text, list the paper and state that section guidance is unavailable.
7. Mark material that can be skipped because it is unlikely to change the decision.
8. After reading, ask one concise comprehension question at a time and revise the queue from the user's response. Continue this loop regardless of novelty result.

## Boundaries

- Do not claim exhaustive coverage.
- Do not invent citations, text access, section locations, or novelty evidence.
- Do not draft the user's paper or research project.
- Reuse existing workflows rather than adding a second discovery or teaching implementation.

## Repository changes

- Add `skills/productivity/research-gap/SKILL.md`.
- Register it in the root README, productivity README, and `.claude-plugin/plugin.json`.
- Add a small assertion-based catalog check verifying all registrations.

## Verification

Run the catalog check. Confirm every listed path exists and that the new skill appears exactly once in each required catalog.
