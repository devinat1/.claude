# Capacity Planning Dimensions — Question Bank

Reference file for the Capacity Planning phase of the system design interview. Contains Socratic question banks for each scale dimension.

Do not use this file standalone. It is referenced by the `/system` command during the Capacity Planning phase.

---

## Traffic

### Opener Questions
- "Before we optimize anything — how many requests per second do you think this system needs to handle? Walk me through how you'd estimate that."
- "You've got your design on the table. What does the traffic profile look like? Is this read-heavy, write-heavy, or balanced?"
- "How many concurrent users do you expect at peak? What does 'peak' even mean for this system?"

### Probe Chains

**Users to QPS:**
1. "How many total users?" → "What's your DAU/MAU ratio?" → "How many actions per session?" → "So what's your QPS? Show me the math."
2. "You said X QPS — is that reads, writes, or both?" → "What's the read/write ratio?" → "How did you arrive at that ratio?"

**Burst patterns:**
1. "Is traffic uniform throughout the day or are there spikes?" → "How big are the spikes relative to baseline?" → "What's your peak-to-average ratio?"
2. "Are there predictable events that cause traffic surges?" → "How much lead time do you have before a surge?" → "What happens if a surge is 3x what you planned for?"

**Geographic distribution:**
1. "Where are your users?" → "Does latency matter differently by region?" → "How does that affect where you deploy?"

### Red Flags (trigger pressure escalation)
- "We'll just auto-scale" — without explaining what triggers scaling or how fast it responds
- "It should handle the load" — without any QPS estimate
- "We'll add more servers" — without identifying the bottleneck
- "Traffic will be evenly distributed" — almost never true in practice
- Any answer that gives a single number without distinguishing reads from writes

### Specificity Anchors (what "good enough" looks like)
- A QPS number with derivation from user count and behavior assumptions
- Explicit read/write split with reasoning
- Peak multiplier over baseline with justification
- Acknowledgment of whether traffic is bursty or steady and why

---

## Data

### Opener Questions
- "How much data does this system generate per day? Walk me through the calculation from a single user action."
- "A year from now, how big is your database? How did you get that number?"
- "What data in this system is hot — queried constantly — versus cold?"

### Probe Chains

**Storage estimation:**
1. "What's the average size of a single [core entity]?" → "How many of those are created per day?" → "Multiply that out — what's your daily storage growth?" → "Now project that over a year. Over three years."
2. "Are you accounting for indexes?" → "What about replication factor?" → "What's the actual disk footprint versus raw data size?"

**Retention and lifecycle:**
1. "Does data live forever or do you expire it?" → "What's your retention policy?" → "How do you enforce that — TTL, batch jobs, or archival?"
2. "What happens to old data — is it deleted, archived, or moved to cold storage?" → "How does that affect your storage growth curve?"

**Hot vs cold data:**
1. "What percentage of your data is accessed in any given day?" → "What's the working set size that needs to fit in memory or fast storage?" → "How does that change over time?"

**Index and query patterns:**
1. "What are your most frequent queries?" → "What indexes do those require?" → "How large do those indexes get relative to the data itself?"

### Red Flags
- "We'll store everything in one table" — without considering access patterns
- "Storage is cheap" — without estimating actual volume
- "A lot of data" — not a number
- "We'll worry about that later" — data modeling decisions are hard to change
- No mention of indexes, replication overhead, or retention

### Specificity Anchors
- Storage estimate derived from entity size × creation rate × time
- Explicit retention policy with enforcement mechanism
- Working set size estimate (hot data that must be fast)
- Awareness of index overhead and replication factor in total storage

---

## Compute

### Opener Questions
- "Which operation in your system is the most computationally expensive? How expensive?"
- "What's your latency budget for the critical path? Where does the time go?"
- "If I gave you one box to run this on, what would be the first resource you'd run out of — CPU, memory, or network?"

### Probe Chains

**Per-request cost:**
1. "What happens CPU-wise when a request comes in?" → "Are there any computationally expensive operations — ranking, encryption, image processing?" → "How long does that operation take per request?" → "At your estimated QPS, what's the total CPU demand?"
2. "How much memory does each request/connection consume?" → "At peak concurrent connections, what's the memory footprint?" → "Does that fit on a single machine?"

**Latency budgets:**
1. "What's the end-to-end latency the user expects?" → "Break that down — how much time for network, application logic, database?" → "Which leg has the least room to spare?"
2. "What's the difference between your P50 and P99?" → "What causes the tail latency?" → "Is that acceptable or do you need to address it?"

**Batch and background processing:**
1. "Are there operations that don't need to happen in real time?" → "How much compute do those background jobs need?" → "When do they run — and does that compete with foreground traffic for resources?"

### Red Flags
- "It's fast enough" — without measuring or estimating
- "We'll just add more CPU" — without identifying what's consuming it
- Ignoring memory entirely — especially for systems with connection state
- Assuming P99 is close to P50 — it rarely is
- No distinction between foreground latency and background processing

### Specificity Anchors
- Identification of the most expensive operation and its per-request cost
- Latency budget breakdown across the critical path
- Memory estimate per connection/request at peak concurrency
- Awareness of background processing resource needs

---

## Organizational

### Opener Questions
- "How many teams or services touch this system in production?"
- "If this system goes down at 3 AM, who gets paged and how many people need to coordinate?"
- "How often does this get deployed, and what's the blast radius of a bad deploy?"

### Probe Chains

**Service boundaries:**
1. "Which teams own which parts of this system?" → "Where are the handoff points between teams?" → "What happens when team A needs a change in team B's service?" → "How does that affect your deployment velocity?"

**Deployment and rollout:**
1. "How do you deploy changes to this system?" → "Can you deploy one service without deploying others?" → "What's your rollback strategy?" → "How long does a rollback take?"

**On-call and incident response:**
1. "What's the on-call structure for this system?" → "If a downstream dependency fails, who notices first?" → "How many people need to coordinate during an incident?" → "Does the architecture make that easier or harder?"

### Red Flags
- "One team owns everything" — for a system with 5+ services
- No mention of deployment strategy for a distributed system
- "We'll figure out on-call later" — operational concerns shape architecture
- Assuming all services can be deployed in lockstep

### Specificity Anchors
- Clear ownership model for each service/component
- Deployment strategy that accounts for independent service updates
- Incident response model that matches the system's failure modes
- Awareness of how team boundaries affect API design and data ownership
