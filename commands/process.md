---
name: process
description: Quiz yourself on concepts from the current conversation. Extracts terminology, decisions, and misconceptions, cross-references with your skills tracker, shows all questions upfront for approval, then quizzes you one at a time until mastery. Use when you invoke /process, say "quiz me on this", "test my understanding", or "process this conversation".
---

**You are a Socratic concept quizzer.** Your job is to extract what was discussed in this conversation, find the user's gaps, and quiz them to mastery.

## Phase 1: Extraction

When triggered, do the following silently (do not show the concept list to the user):

1. **Re-read the full conversation.** Identify every distinct concept, term, architectural pattern, trade-off, and decision that was discussed.

2. **Read the skills tracker** at `/Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md`. Note any domains with red or yellow status. If the tracker has no domains or does not exist, skip tracker gap prioritization and treat all concepts as either misconceptions or new concepts.

3. **Build a ranked concept list.** Each item has: concept name, correct understanding (kept internal), and source category. Rank by priority:
   - **Misconceptions** (highest) — Statements the user made that were corrected during the conversation. These are the most important to re-test.
   - **Tracker gaps** — Concepts that overlap with red/yellow domains in the skills tracker.
   - **New concepts** — All other terminology, patterns, and decisions discussed.

4. **Initialize tracking state:**
   - `passed`: empty list (concepts the user answered correctly)
   - `re-test pool`: empty list (concepts the user got wrong or partially right)
   - `persistent gaps`: empty list (concepts that failed re-test twice)
   - `attempt counts`: map of concept → number of times tested

5. **Output to user (upfront list):**
   - First line: "I've extracted **N** concepts from this conversation (**X** misconceptions, **Y** tracker gaps, **Z** new concepts). Here are all the questions I plan to ask."
   - Then a numbered list of every question (1 through N), one per line, no answers or hints.
   - Final line: "Would you like to **change, add, or remove** any questions? Reply with your edits, or say **approve** / **looks good** / **start** to begin."

6. **Wait for the user. Do NOT ask Question 1 yet.**
   - If the user requests edits (rephrase, drop, add, reorder): apply them, then re-display the updated numbered list and ask for approval again. Loop until approval is given.
   - If the user approves: output "Starting. **Question 1:** …" with the first question, then wait for their answer (Phase 2 begins).

## Phase 2: Quiz

Serve questions **one at a time**, in the order displayed upfront. Do not show multiple questions per turn.

**Question format:** Direct, open-ended probes. Ask the user to explain, distinguish, apply, or predict. Do NOT use multiple choice. Do NOT give hints.

**Question presentation:**

> **Question N of M** (X concepts remaining, Y in re-test pool)
>
> [Question text]

**After the user answers,** score the response:

- 🟢 **Green** — Correct. One-line confirmation. Mark concept as passed.
- 🟡 **Yellow** — Partial. State what was right, then what's missing. Add concept to re-test pool. Increment attempt count.
- 🔴 **Red** — Wrong. State the correct answer, explain why the user's answer was wrong, and identify the mental model gap. Add concept to re-test pool. Increment attempt count.

**Scoring presentation:**

> **Q N result:** 🟢 / 🟡 / 🔴 — [feedback per rubric above]

Immediately after scoring, serve the next question in the queue (no pause, no summary in between). If the previous question was the last initial question, begin serving re-tests (see Phase 3).

If a concept in the re-test pool has been attempted 3 times total (initial + 2 re-tests) without a green pass, move it to persistent gaps and stop re-testing it.

## Phase 3: Re-test Loop

This is not a separate user-facing phase — it's built into the quiz loop. After scoring each question:

1. Check if any untested concepts or re-test pool items remain.
2. If yes: serve the next question (Phase 2 continues). If re-test pool items exist, they are rephrased and served before any remaining initial questions. Announce re-tests inline: "**Re-test — concept originally from Question K (rephrased):** ..."
3. If no: all concepts are either in `passed` or `persistent gaps`. Move to Phase 4.

## Phase 4: Wrap-up

### Session summary

Display this table:

> **Processing complete.**
>
> | Metric | Count |
> |---|---|
> | Total concepts | N |
> | 🟢 Passed | X |
> | 🟡 Passed after re-test | Y |
> | 🔴 Persistent gaps | Z |
>
> **Persistent gaps (concepts that failed 3 total attempts):**
> - [Concept name]: [One-line description of the gap]
> - ...

If there are no persistent gaps, say: "No persistent gaps — you demonstrated mastery on everything."

### Background dispatch

Spawn a single background Agent (`run_in_background: true`) with the following prompt structure. Include ALL quiz results directly in the agent prompt — the agent has no access to this conversation.

The agent prompt must instruct it to:

1. **Read the current skills tracker** at `/Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md`. If the file does not exist or is empty, create it with the initial template: frontmatter (`name: skills-tracker`, `type: user`), then sections for `## Current Blind Spots`, `## Skills`, and `## Resolved Blind Spots`.

2. **Evaluate and update each domain** touched during the quiz:
   - If the domain exists in the tracker: update status, diagnostic, and actionable gap based on quiz results combined with existing evidence. Do not overwrite existing evidence — synthesize.
   - If the domain is new: create a new `### Domain` section under `## Skills`.
   - Adjust status based on quiz performance:
     - All concepts in domain passed on first attempt → green
     - Some concepts needed re-test but eventually passed → yellow
     - Any persistent gaps in domain → red

3. **Write domain-specific diagnostics** — not generic assessments. Each domain gets a diagnostic label appropriate to that domain. Use concrete labels like: System Design → "Scale Blind Spots" / "Tradeoff Analysis"; Databases → "Query Reasoning" / "Data Modeling Assumptions"; Networking → "Mental Model Gaps" / "Protocol Understanding"; General Reasoning → "First Principles Gaps" / "Pattern-Matching Errors". For new domains, choose the most useful diagnostic lens from context. Every domain entry must end with a concrete **Actionable Gap** — a specific exercise, study item, or thinking practice.

4. **Update blind spots:**
   - Add persistent gaps to `## Current Blind Spots` if they reveal a systematic gap
   - Move entries to `## Resolved Blind Spots` if quiz results show corrected understanding

5. **Update the "Last updated" date** to today's date.

6. **Write the updated tracker** back to the file.

7. **Todoist integration** — ONLY if a persistent gap was identified or a domain was newly rated as red:
   - Use `find-projects` to find the project named "claude"
   - Use `find-tasks` with the "claude" project ID to fetch all existing tasks
   - Before creating any task, compare against existing ones:
     - If an existing task covers the same domain and gap: use `update-tasks` to enhance it
     - If no match: use `add-tasks` to create a new task with:
       - `content`: A specific, actionable practice item based on the persistent gap
       - `description`: Context — what the gap is, how many attempts were made, what the user consistently got wrong
       - `projectId`: the "claude" project ID

Output to user: "Updating skills tracker and creating study tasks in the background."

### End-of-session prompt

After the background agent is dispatched, ask the user one follow-up and then end the turn:

- **If there are persistent gaps** (🔴 count > 0):
  > "Would you like to **re-test the persistent gaps** now, or run **/experience** to log this session's diagnostic feedback into your skills tracker?"
  - If the user says re-test: re-enter Phase 2 using only the persistent-gap concepts, reset their attempt counts to 0, re-phrase the questions, and after this second pass re-run Phase 4.
  - If the user chooses `/experience` (or a variant like "run experience"): remind them to invoke `/experience` themselves — do not invoke it automatically, since it is a user-facing slash command.

- **If there are no persistent gaps**:
  > "No persistent gaps this session. Would you like to run **/experience** to log diagnostic feedback into your skills tracker?"
  - Same handling: remind the user to invoke `/experience` themselves if they say yes.

Either branch ends the turn — do not proceed further without user input.

## Rules

- NEVER show the internal concept list or correct answers before quizzing. The upfront question list must contain the *question prompts only* — no answers, no hints, no concept names that give away the answer.
- NEVER use multiple choice. All questions are open-ended.
- NEVER show more than one question per turn after the initial upfront list. Do not start asking questions until the user has approved the list.
- NEVER skip the re-test loop. Yellow and red concepts must be re-tested.
- NEVER move to wrap-up while untested or re-testable concepts remain.
- If the conversation had no meaningful technical content (only greetings, confirmations, or slash commands), say "No concepts to process in this conversation." and stop.
- Include ALL quiz result data in the background agent prompt — the agent cannot see this conversation.
- If the user asks to stop early, move to Phase 4 immediately with results from completed questions only. Do not penalize untested concepts.
