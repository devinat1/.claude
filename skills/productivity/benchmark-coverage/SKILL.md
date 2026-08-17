---
name: benchmark-coverage
description: Match an arbitrary prompt to source-backed public LLM and agent benchmarks, then assess a named model using only model results returned by the benchmark catalog API. Use when someone asks whether a prompt is covered by benchmarks, which benchmark represents a task, or whether a particular model would likely pass relevant evaluations.
---

# Benchmark Coverage

Determine benchmark coverage task by task. Use only the API configured in
`BENCHMARK_API_URL`; never fill data gaps from memory or web search.

## Workflow

1. Ask for the exact model and version unless the user already supplied both.
2. Ask for the prompt to assess unless it is already present.
3. Split compound prompts into distinct tasks.
4. State a reasonable interpretation for each ambiguous task and continue.
5. Query `$BENCHMARK_API_URL/v1/benchmarks` without authentication:
   - Use `q` for short capability or task-form terms.
   - Make additional queries when one query cannot represent all task facets.
   - Pass `model` to return only results for the selected model.
6. Treat a benchmark as credible only when both its core capability and task form
   overlap the task. Domain overlap supports a match but is not required.
7. Return every credible match. Do not force weak matches.

If `BENCHMARK_API_URL` is unset, the API is unavailable, or required record
fields are missing, stop and report benchmark data unavailable. Do not use the
agent's internal knowledge as a fallback.

## Output

For each task, report:

- `covered` or `not covered`
- every credible benchmark name
- one brief explanation of the capability and task-form overlap per match
- one performance verdict per match
- one overall performance verdict

Do not report numerical confidence.

## Performance Rules

For each matched benchmark:

- Find the selected model in `modelResults`.
- With no matching result, return `insufficient evidence`.
- Otherwise apply `scoring.passRule` exactly:
  - `gte`: score at or above the threshold means `likely passes`.
  - `lte`: score at or below the threshold means `likely passes`.
  - The opposite result means `unlikely to pass`.
- Treat the score as aggregate evidence, not a guarantee for the specific prompt.
- If no benchmark covers the task, return `not applicable`.

Combine usable benchmark verdicts:

- all pass: `likely passes`
- all fail: `unlikely to pass`
- disagreement: `mixed`
- none usable: `insufficient evidence`

If usable results agree while other matches lack results, keep the corresponding
likely/unlikely verdict and explicitly note the evidence gaps.

## API Contract

- `GET /v1/benchmarks?q=&capability=&domain=&model=`
- `GET /v1/schema`
- `GET /v1/rules`

Use `scripts/api.ts` to run the bundled development endpoint:

```bash
node scripts/api.ts
```

The catalog is unauthenticated and read-only. Treat source URLs, evaluation
settings, and benchmark versions as part of each result; scores from different
settings are not automatically comparable.
