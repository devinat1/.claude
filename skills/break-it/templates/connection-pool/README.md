# break-it lab — connection-pool exhaustion

A handler checks out a DB connection (simulated: a semaphore + a 40ms query) for every request.
- **naive:** pool of 5, no acquire timeout — requests queue unboundedly under load
- **patched:** pool of 100 + a 250ms fail-fast acquire timeout

## 1. Predict first
At how many concurrent users (k6 VUs) do you think p99 crosses 500ms? Write the number down now.

## 2. Run naive — watch it break
    MODE=naive go run . &
    k6 run load.js
    lsof -ti:8081 | xargs kill   # stop the server (frees port 8081 even though `go run` spawns a child)
k6 reports the p99 threshold BREACHED. That gap between your number and the real one is the lesson.

## 3. Run patched — watch it hold
    MODE=patched go run . &
    k6 run load.js
    lsof -ti:8081 | xargs kill   # stop the server (frees port 8081 even though `go run` spawns a child)
Both thresholds pass.

## The line
A pool of 5 exhausts under load; p99 blows past 500ms. A right-sized pool + fail-fast timeout holds at 100 VUs.
But a bigger pool isn't free — it costs DB resources and just moves the exhaustion downstream. The real backstop
is the fail-fast timeout (backpressure), not the size.
