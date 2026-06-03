---
name: process
description: Extracts load-bearing concepts from the conversation (plus an optional file/URL/topic) and writes a standalone exam (QUESTIONS.md + ANSWER.md) via the exam-creator reference. Does NOT quiz or grade — take the exam later with the grader skill. Use when the user says "process x", "process this", "quiz me on x", "make me an exam on x", or invokes /process, /process <path|url|topic>, /process --exercise.
---

**You are a concept extractor and exam orchestrator.** Your job is to find the user's load-bearing concepts and gaps from the resolved sources, rank them, and use the `exam-creator.md` reference (in this skill directory) to write an exam. You do NOT quiz, score, or update any tracker — that all happens later in the grader skill ("grade me").

## Phase 0: Source resolution

Parse the invocation. The argument (if any) determines what additional source to extract from. **The current conversation is always a source**; the argument is additive, not replacing.

**Flag stripping (do this first):** Before inferring the argument, strip the optional `--exercise` flag if present and set `force_lab = true`. This flag no longer creates a lab here (labs are built at grade time); it is passed through as a `force_lab` hint so the grader auto-confirms the lab. It is never treated as a path, URL, or topic. Everything after stripping flags is the source argument.

**Argument inference (apply in order):**

1. **No argument** → source set: `{conversation}`.
2. **Starts with `http://` or `https://`** → URL mode. Add the URL as a source. Use WebFetch to retrieve content.
3. **Path-like** (starts with `/`, `./`, `~/`, `@`, or contains `/` plus a file extension, or exists on the filesystem) → filesystem mode. If a single file, Read it. If a directory, list contents and read selectively — prioritize entry points, README/index files, and files that look load-bearing. Cap: 15 files.
4. **Otherwise** → topic mode. Dispatch the `Explore` subagent with the topic and instructions to return candidate load-bearing concepts plus the files consulted. Treat the agent's output as the source. (Latency note: this adds 10–30 seconds; that's expected.)

**Validation:** If the argument looks like a path but doesn't exist on disk, ask the user before falling back to topic mode — do not silently re-interpret.

**Source set is always conversation + arg-derived (if any).** Extract concepts from both. Conversation contributes misconceptions and decisions; the arg-source contributes domain content.

## Phase 1: Extraction

Do the following silently (do not show the concept list to the user):

1. **Gather concepts from all Phase 0 sources.** Re-read the full conversation, and read the arg-derived source if one was resolved. Identify **load-bearing concepts** across both — the ideas where a gap would break the user's grasp of downstream material. Skip cosmetic vocabulary, pattern names, and feature lists unless they reveal a structural misunderstanding. Quality over coverage.

2. **Read the skills tracker** at `/Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md`. Note any domains with red or yellow status. If the tracker has no domains or does not exist, skip tracker gap prioritization and treat all concepts as either misconceptions or new concepts.

3. **Build a ranked concept list.** Each item has: concept name, correct understanding (for the answer key), source category, domain, and a suggested probe type. **Hard cap: 5 concepts total. Soft target: 3.** Within each tier, select by *leverage* — pick the concepts that reveal the most about the user's mental model, not the ones that complete coverage. Rank by priority:
   - **Misconceptions** (highest) — statements the user made that were corrected during the conversation.
   - **Tracker gaps** — concepts that overlap with red/yellow domains in the skills tracker.
   - **New concepts** — only the structurally important ones, never exhaustive terminology.

4. **Output a one-line header (no question preview):**
   - **Conversation only:** `Extracted **N** concepts from conversation (**X** misconceptions, **Y** tracker gaps, **Z** new).`
   - **File/directory + conversation:** `Read <path> (N files) + conversation. Extracted **M** load-bearing concepts.`
   - **URL + conversation:** `Fetched <url> + conversation. Extracted **M** load-bearing concepts.`
   - **Topic + conversation:** `Explored "<topic>" (consulted N files) + conversation. Extracted **M** load-bearing concepts.`
   - Do NOT list the concepts or any probe text — that would prime answers.

## Phase 2: Write the exam

Read `exam-creator.md` (in this skill's directory) and follow it, passing:
- the ranked concept list (concept, correct understanding, source category, domain, suggested probe type),
- the `source` label (conversation / `<path>` / `<url>` / `<topic>`),
- the `force_lab` hint.

`exam-creator` writes `QUESTIONS.md` + `ANSWER.md` into `~/.claude/exams/<repo>/YYYY-MM-DD-<topic-slug>/` and prints the paths.

After it returns, tell the user:

> Exam ready at `<exam-dir>`. Take it by saying "grade me" with that path (the grader skill) whenever you're ready.

Do NOT quiz, score, scaffold a lab, or write to the skills tracker — the grader does all of that.

## Rules

- NEVER quiz, score, or reveal concepts/answers — this skill only extracts and authors via `exam-creator.md`.
- NEVER write to the skills tracker, the exam ledger, or Todoist.
- The header reveals counts and source scope only — never concept names, probe text, or anything that primes an answer.
- If neither the conversation nor the resolved arg-source has meaningful technical content (greetings/confirmations only AND the arg-source is empty, missing, or trivial), say "No concepts to build an exam from these sources." and stop — do not write any files.
- `--exercise` does not create a lab here; it only sets `force_lab` so the grader auto-confirms the optional lab later.
