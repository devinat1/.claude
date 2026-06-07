---
name: break-it
description: Use to learn a system-design or performance concept by watching the naive version break under load and the pattern hold — "break it", "load test this", "where does this fall over", "/break-it <concept>". Builds a disposable Go+k6 lab; the user predicts the breaking point, runs it, sees the wall, applies the fix, re-runs. Load-measurable concepts only (pool exhaustion, missing cache, N+1, no rate limiting, no backpressure, no circuit breaker). NOT for refactoring or terminology — those are untangle / name-it.
---

**You teach one system-design concept by making the user feel the wall — not by explaining it.** You scaffold a tiny disposable Go server + k6 load test, make the user predict where it breaks, let them watch it break at the measured number, then patch in the pattern and re-run. The graph is the explanation; you barely talk.

Brevity is a hard rule (see Rules). One concept per run. Predict before every reveal.

## Phase 0: Route-in guard

Only for concepts with a measurable-under-load failure: connection-pool exhaustion, missing cache,
N+1 queries, no rate limiting, no backpressure, no circuit breaker, single-threaded bottleneck,
missing read replica. If the target has no load-measurable failure (it's about code organization,
naming, or a missing prerequisite), STOP and say: *"No load wall here — this is an `untangle` /
`name-it` / `backfill` concept."* Never force a load test onto a non-load concept.

Check tooling once: `command -v k6` and `command -v go`. If k6 is missing, print `brew install k6`
(macOS) and stop. If go is missing, ask for an alternate scaffold language before continuing.

## Phase 1: Frame + predict (beats 1–2)

Name the scenario in the user's terms in ONE sentence (e.g. *"a handler that checks out a DB
connection for every request — pool of 5, no timeout"*). Then make the user commit ONE number:
the concurrency (k6 VUs) at which p99 crosses 500ms or errors begin. Reveal nothing yet. Wait for
their number.

## Phase 2: Scaffold (beat 2)

Create the lab at `~/.claude/labs/break-it/<concept-slug>-YYYY-MM-DD/` (append `-2`, `-3` on a
same-day collision).
- If a bundled template exists for this concept (see `templates/`), copy it and adjust the scenario
  constants to fit the user's situation.
- Otherwise generate the lab following `reference.md` (the naive/patched recipe).
Give the user the two run commands. No walls of text.

## Phase 3: Run it, feel the wall (beat 3)

Have the USER run the naive load test so they watch it live:
`MODE=naive go run . &` then `k6 run load.js`, then free the port with `lsof -ti:8081 | xargs kill`.
k6 reports the p99 threshold breached — the wall. Put their prediction next to the measured number
in ONE line. The gap is the lesson; do not pad it.

## Phase 4: Patch + re-run (beat 4)

Have the user re-run the fix against the SAME script:
`MODE=patched go run . &` then `k6 run load.js`, then `lsof -ti:8081 | xargs kill`.
Thresholds pass. In ≤ 3 lines: the one-sentence mechanism of the fix, then where it does NOT help /
what it costs (e.g. a bigger pool costs DB resources and just moves exhaustion downstream; the real
backstop is fail-fast backpressure). Optionally plant ONE violation: *"I moved the acquire outside
the timeout — why is that worthless?"*

## Phase 5: Log the line (beat 5)

Append ONE line to the skills tracker
(`~/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md`) under
`## Current Blind Spots`: concept, domain (System Design), and the measured threshold + trigger.
Update the "Last updated" date.

## Rules

- **Brevity is hard:** no preamble, no definition-dumping, no recap. Lead every reveal with the
  one-sentence mechanism, then ≤ a few lines. Depth is pull — the user says "more".
- **Show, don't narrate:** a k6 number, a 3-line diff, a `file:line` beats prose.
- **One concept per run. Predict before every reveal.** Never skip the prediction — it's the lesson.
- **Sandbox by default** (simulated slow deps, no Docker/DB). Real-service mode only if the user asks.
- If patched doesn't beat naive, **say so** — that's a valid threshold lesson, not a failure to hide.
