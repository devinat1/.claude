# break-it — lab authoring reference

Read this when no bundled template fits the target concept. It tells you how to build a
naive/patched Go+k6 lab that breaks cleanly under load.

## The recipe

1. **Find the bottleneck.** Every load-measurable concept has one finite resource that saturates:
   a connection pool, the DB itself, CPU, memory, a downstream rate limit. Model it with a
   buffered-channel semaphore of size N plus a `time.Sleep` for the work. No real dependency.
2. **Naive = the bottleneck unmanaged.** Under-provision it and remove the safety (no timeout,
   no cache, no limit) so it saturates and p99 explodes under load.
3. **Patched = the pattern, and only that pattern.** Apply exactly the one pattern being taught
   (right-sized pool + acquire timeout, a cache, a rate limiter, batched query for N+1, …).
   Toggle naive/patched with a `MODE` env var in a single `main.go` so the k6 script is identical
   for both runs — the pattern is the only variable.
4. **k6 thresholds are the assertion.** `http_req_duration: ['p(99)<500']` and
   `http_req_failed: ['rate<0.01']`. Naive breaches (k6 exits non-zero) = the wall.
   Patched passes = the fix.
5. **Ramp to where naive breaks but patched holds.** Pick peak VUs so the contrast is unmistakable.

## Concept catalog (naive → patched)

- **Connection-pool exhaustion** → bundled template `templates/connection-pool/`.
  Naive: pool 5, no acquire timeout. Patched: pool 100 + 250ms fail-fast timeout.
- **Missing cache** → Naive: every request hits the 40ms semaphore-bounded "DB". Patched: an
  in-memory `sync.Map` cache keyed by a request param; hits skip the DB. Break: p99 climbs as the
  DB semaphore saturates; fix: a high hit-rate flattens it.
- **N+1 queries** → Naive: a per-item loop, each iteration a 5ms "query". Patched: one batched
  query (a single sleep). Break: latency scales with N under load; fix: constant.
- **No rate limiting** → Naive: an unbounded handler calling a downstream that returns errors past
  X concurrent (semaphore that rejects when full). Patched: a token-bucket limiter that sheds
  excess fast. Break: downstream error rate spikes; fix: bounded, fast 429s.

Keep every lab to one `main.go` + `load.js` + `go.mod` + a short `README.md`.
